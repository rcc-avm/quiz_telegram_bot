from aiogram import Router, types
from aiogram.filters import Command
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from utils.db_utils import create_tables
from utils.quiz_utils import new_quiz

router = Router()

@router.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    """
    Обработчик команды /start.
    Приветствует пользователя и предлагает начать квиз.
    """
    # Создаем сборщик клавиатуры типа Reply
    builder = ReplyKeyboardBuilder()
    # Добавляем кнопку "Начать игру"
    builder.add(types.KeyboardButton(text="Начать игру"))
    # Прикрепляем кнопки к сообщению
    await message.answer(
        "Добро пожаловать в квиз! Нажмите 'Начать игру', чтобы стартовать.",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

# Хэндлер на команды /quiz
@router.message(F.text=="Начать игру")
@router.message(Command(commands=["quiz"]))
async def cmd_quiz(message: types.Message):
    # Отправляем новое сообщение без кнопок
    await message.answer(f"Давайте начнем квиз!")
    # Запускаем новый квиз
    await new_quiz(message)