from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import User, Question, Answer, Questionnaire, UserAnswer


class Database:
    def __init__(self, session):
        self.session: AsyncSession = session

    async def add_user(self, user_id, username=None):
        try:
            user = User(id=user_id, username=username)
            self.session.add(user)
            await self.session.commit()
            return user
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_user(self, user_id):
        return await self.session.get(User, user_id)

    async def add_questions(self, questions, author_id, questionnaire_name):
        try:
            q_ids = []
            for question in questions:
                q = Question(q_author=author_id, q_text=question["question"])
                self.session.add(q)
                await self.session.commit()

                a_correct = Answer(a_text=question["correct"], q_id=q.q_id)
                a_wrong = Answer(a_text=question["incorrect"], q_id=q.q_id)
                self.session.add_all([a_correct, a_wrong])

                await self.session.commit()

                q.correct_answer_id = a_correct.a_id
                await self.session.commit()
                q_ids.append(q.q_id)

            questioner = Questionnaire(questions=q_ids, name=questionnaire_name)
            self.session.add(questioner)
            await self.session.commit()
            return questioner

        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_questioner(self, questioner_id):
        return await self.session.get(Questionnaire, questioner_id)

    async def get_question(self, question_id):
        return await self.session.get(Question, question_id)

    async def get_questions(self, question_ids):
        res = await self.session.execute(select(Question).where(Question.q_id.in_(question_ids)))
        return res.scalars().all()

    async def get_answers(self, question_id):
        res = await self.session.execute(select(Answer).where(Answer.q_id == question_id))
        return res.scalars().all()

    async def get_answer(self, answer_id):
        return await self.session.get(Answer, answer_id)

    async def record_answer(self, user_id, question_id, answer_id, attempt_id):
        try:
            user_answer = UserAnswer(user_id=user_id, question_id=question_id, answer_id=answer_id, attempt_id=attempt_id)
            self.session.add(user_answer)
            await self.session.commit()
            return user_answer
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_user_answers(self, user_id, attempt_id):
        res = await self.session.execute(select(UserAnswer).where(UserAnswer.user_id == user_id, UserAnswer.attempt_id == attempt_id))
        return res.scalars().all()
