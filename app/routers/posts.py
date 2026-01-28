from fastapi import APIRouter, Depends, HTTPException,status
from psycopg2 import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models import Post, User
from app.schemas import PostCreate, PostOut

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=PostOut)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    # Check if user exists first
    user_check = await db.execute(
        select(User).where(User.id == post.user_id)
    )
    user = user_check.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found. Cannot create post."
        )

    new_post = Post(**post.model_dump())
    db.add(new_post)

    try:
        await db.commit()
        await db.refresh(new_post)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid foreign key reference."
        )

    return new_post



@router.get("/", response_model=list[PostOut],status_code=status.HTTP_201_CREATED)
async def get_posts(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.user_id == user_id))
    return result.scalars().all()


@router.get("/stats/")
async def post_stats(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Post.user_id, func.count(Post.id))
        .group_by(Post.user_id)
    )
    return [{"user_id": r[0], "post_count": r[1]} for r in result.all()]
