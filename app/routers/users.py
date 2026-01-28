from fastapi import APIRouter, Depends, HTTPException, Query , status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta, timezone
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserUpdate, UserOut
from app.cache import get_cache, set_cache, invalidate_cache

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut,status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    await invalidate_cache("users*")
    return new_user


@router.get("/")
async def get_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    
    cache_key = f"users:{page}:{limit}"
    cached = await get_cache(cache_key)
    if cached:
        return cached
    
    # calculated offset 
    skip = (page - 1) * limit

    total_result = await db.execute(select(func.count(User.id))) 
    total = total_result.scalar()

    result = await db.execute(
        select(User).offset(skip).limit(limit)
    )
    users = result.scalars().all()

    users_out = [UserOut.model_validate(u) for u in users]

    response = {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
        "data": users_out
    }

    await set_cache(cache_key, response)
    return response



@router.get("/{id}", response_model=UserOut)
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.put("/{id}", response_model=UserOut)
async def update_user(id: int, data: UserUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    await invalidate_cache("users*")
    return user


@router.delete("/{id}")
async def delete_user(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")

    await db.delete(user)
    await db.commit()
    await invalidate_cache("users*")
    return {"message": "Deleted"}


@router.get("/search/")
async def search_users(name: str | None = None,
                       created_after: datetime | None = None,
                       db: AsyncSession = Depends(get_db)):

    query = select(User)

    if name:
        query = query.where(User.name.ilike(f"%{name}%"))
    if created_after:
        query = query.where(User.created_at >= created_after)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/stats/")
async def user_stats(db: AsyncSession = Depends(get_db)):
    total = await db.scalar(select(func.count(User.id)))
    last_week = await db.scalar(
        select(func.count(User.id))
        .where(User.created_at >= datetime.now(timezone.utc) - timedelta(days=7))
    )

    return {
        "total_users": total,
        "users_last_7_days": last_week
    }
