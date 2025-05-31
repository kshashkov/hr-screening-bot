import logging

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.helper import Database
from bot.filters.hr import HRFilter
from bot.utils.chatgpt import generate_questions, InvalidJSONError

router = Router()
router.message.filter(HRFilter())


class GenerateQuestions(StatesGroup):
    file = State()


@router.message(Command("generate"))
async def start(message: Message, state: FSMContext):
    await state.set_state(GenerateQuestions.file)
    await message.answer("Please send a job description in PDF.")


@router.message(GenerateQuestions.file)
async def generate_questions_handler(message: Message, state: FSMContext, bot: Bot, session: Database):
    await bot.send_chat_action(message.chat.id, "upload_document")
    file = await bot.download(message.document.file_id)
    try:
        result = generate_questions(file)
    except InvalidJSONError as e:
        await message.answer("An error occurred when processing the file. The prompt may be incorrect.")
        logging.error("OpenAI response is not a valid JSON.", exc_info=e)
        return


    if list(result.keys())[0].lower() != "questions":
        await message.answer("An error occurred when processing the file. The prompt may be incorrect.")
        logging.error("OpenAI response is not a valid JSON.", result)
        return

    questions_raw = result.get("questions", [])
    questions = []
    for q in questions_raw:
        keys = list(q.keys())
        questions.append({
            "question":  q["question"],
            "correct":   q["correct"],
            "incorrect": q["incorrect"]
        })

    #     we assume that order of keys is always the same

    try:
        for q in questions:
            assert isinstance(q["question"], str)
            assert isinstance(q["correct"], str)
            assert isinstance(q["incorrect"], str)
    except AssertionError:
        await message.answer("An error occurred when processing the file. The prompt may be incorrect.")
        logging.error("OpenAI response is not formatted properly.", result)
        return



    logging.info(f"Generated questions: {questions}")


    q = await session.add_questions(questions, author_id=message.from_user.id)

    share_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Share the questionnaire", url="https://t.me/share/url?url=http://t.me/" + (await
                                                                                                            bot.get_me(

                                                                                                            )).username + "?start=questions_" + str(
                q.id))]])
    await message.answer("Your questionnaire has been generated.", reply_markup=share_button)

    await state.clear()
