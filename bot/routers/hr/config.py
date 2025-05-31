import html

import yaml
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from bot import settings
from bot.filters.hr import HRFilter

# Disabled insecure prompt setting procedure

router = Router()
router.message.filter(HRFilter())

class PromptChange(StatesGroup):
    prompt = State()

@router.message(Command("prompt"))
async def start(message: Message, state: FSMContext):
    await state.set_state(PromptChange.prompt)
    await message.answer("Please send a new prompt.")

@router.message(PromptChange.prompt)
async def change_prompt(message: Message, state: FSMContext):
    await state.clear()
    with open(settings.Prompt.Config.yaml_file, "w") as f:
        yaml.dump({"text": message.text}, f, encoding="utf-8", allow_unicode=True)
    await message.answer("Prompt was successfully changed. The new prompt is:\n" + html.escape(message.text))

