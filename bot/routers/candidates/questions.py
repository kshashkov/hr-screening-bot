import time
from hashlib import md5
import logging

from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database.helper import Database

from random import shuffle

router = Router()


class QuestionStates(StatesGroup):
    question = State()


async def generate_question(question_id, session) -> tuple[str, InlineKeyboardMarkup]:
    #logging.info("question generated")
    q = await session.get_question(question_id)
    answers = await session.get_answers(question_id)
    shuffle(answers)
    keyboard = InlineKeyboardBuilder()
    for a in answers:
        keyboard.add(InlineKeyboardButton(text=a.a_text, callback_data=f"answer_{question_id}_{a.a_id}"))
    return q.q_text, keyboard.adjust(1).as_markup()


@router.message(CommandStart(deep_link=True))
async def start(message: Message, command: CommandObject, state: FSMContext, session: Database):
    logging.info("Starting questionnaire for user id=" + str(message.from_user.id))
    await message.answer("Welcome")
    if (await session.get_user(message.from_user.id)) is None:
        await session.add_user(message.from_user.id, message.from_user.username)
    questions = await session.get_questioner(command.args.split("_")[1])
    if not questions:
        await message.answer("This questionnaire does not exist")
        return
    await state.update_data(questions=questions.questions[1:], attempt_id=md5(str(time.time()).encode()).hexdigest()[
                                                                         0:6],
                            questioner_id=questions.id)
    await state.set_state(QuestionStates.question)
    q, kb = await generate_question(questions.questions[0], session)
    await message.answer(q, reply_markup=kb)


@router.callback_query(QuestionStates.question)
async def answer_question(query, state: FSMContext, session: Database):
    data = await state.get_data()
    questions = data["questions"]
    question_id = query.data.split("_")[1]
    await session.record_answer(query.from_user.id, question_id, query.data.split("_")[2],
                                data["attempt_id"])
    if not questions:
        await query.message.answer("Thank you for your answers")
        await state.clear()
        creator_id = (await session.get_question(question_id)).q_author
        await query.bot.send_message(creator_id, f"User {query.from_user.username} has attempted a questionnaire")
        user_answers = await session.get_user_answers(query.from_user.id, data["attempt_id"])
        questioner = await session.get_questioner(data["questioner_id"])
        questions = await session.get_questions(questioner.questions)
        text = ""
        questions = {q.q_id: q for q in questions}
        answers = {}
        for q in questions.values():
            answers.update({a.a_id: a for a in await session.get_answers(q.q_id)})
        for a in user_answers:
            text += f"Question: {questions[a.question_id].q_text}\nAnswer: {answers[a.answer_id].a_text}" \
                    f" {'✅' if a.answer_id == questions[a.question_id].correct_answer_id else '❌'}\n\n"
        text += (f"Result: {len([a for a in user_answers if a.answer_id == questions[a.question_id].correct_answer_id])}"
                 f"/{len(user_answers)}")
        await query.bot.send_message(creator_id, text)
        return
    question_id = questions.pop(0)
    await state.update_data(questions=questions)
    q, kb = await generate_question(question_id, session)
    await query.message.answer(q, reply_markup=kb)
    await query.answer()
