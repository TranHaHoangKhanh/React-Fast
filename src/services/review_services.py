import logging

from fastapi import status
from fastapi import HTTPException
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.services.user_services import UserService
from src.services.book_services import BookService
from src.models.models import Review

from src.schemas.review_schemas import ReviewCreateModel
from src.utils.error_handling import (
    ReviewNotFound,
    BookNotFound,
    UserNotFound,
    ReviewError,
    ReviewNotDeleted
)


book_service = BookService()
user_service = UserService()


class ReviewService:

    async def get_all_reviews(self, session: AsyncSession):
        statement = select(Review).order_by(desc(Review.created_at))

        result = await session.exec(statement)

        return result.all()

    async def get_review(self, review_uid: str, session: AsyncSession):

        statement = select(Review).where(Review.uid == review_uid)

        result = await session.exec(statement)
        review = result.first()

        if not review:
            raise ReviewNotFound()

        return review

    async def add_review_to_book(self, user_email: str, book_uid: str, review_data: ReviewCreateModel, session: AsyncSession):
        try:
            book = await book_service.get_book(book_uid=book_uid, session=session)
            if not book:
                raise BookNotFound()

            user = await user_service.get_user_by_email(email=user_email, session=session)
            if not user:
                raise UserNotFound()

            review_data_dict = review_data.model_dump()

            new_review = Review(**review_data_dict, book=book, user=user)

            session.add(new_review)

            await session.commit()

            return new_review
        except Exception as e:

            logging.error(e)

            raise ReviewError()

    async def delete_review_to_from_book(self, review_uid: str, user_email: str, session: AsyncSession):
        user = await user_service.get_user_by_email(user_email, session)

        review = await self.get_review(review_uid, session)

        if not review or (review.user != user):
            raise ReviewNotDeleted()

        await session.delete(review)

        await session.commit()
