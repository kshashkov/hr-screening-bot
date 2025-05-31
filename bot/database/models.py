from sqlalchemy import ForeignKey, BigInteger, String, ARRAY, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)


class Question(Base):
    __tablename__ = "questions"
    q_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    q_author: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    q_text: Mapped[str] = mapped_column(String, nullable=False)
    # q_context: Mapped[str] = mapped_column(String, nullable=True)
    correct_answer_id: Mapped[str] = mapped_column(Integer, ForeignKey("answers.a_id"), nullable=True)


class Answer(Base):
    __tablename__ = "answers"
    a_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    a_text: Mapped[str] = mapped_column(String, nullable=False)
    q_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.q_id"), nullable=False)

class UserAnswer(Base):
    __tablename__ = "user_answers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.q_id"), nullable=False)
    answer_id: Mapped[int] = mapped_column(Integer, ForeignKey("answers.a_id"), nullable=False)
    attempt_id: Mapped[str] = mapped_column(String, nullable=False)

class Questioner(Base):
    __tablename__ = "questioners"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    questions: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)



