from data.quiz_data import quiz_data
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.db_utils import update_quiz_index, get_quiz_index, reset_user_state

async def new_quiz(message):
    # получаем id пользователя, отправившего сообщение
    user_id = message.from_user.id
    # сбрасываем значения индекса и счета в 0
    await reset_user_state(user_id)

    # запрашиваем новый вопрос для квиза
    await get_question(message, user_id)

def generate_options_keyboard(answer_options, right_answer) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for option in answer_options:
        builder.add(InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if option == right_answer else "wrong_answer"
        ))
    builder.adjust(1)
    return builder.as_markup()

async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    if current_question_index >= len(quiz_data):
        return

    question = quiz_data[current_question_index]
    correct_option = question['options'][question['correct_option']]
    kb = generate_options_keyboard(question['options'], correct_option)

    await message.answer(f"{question['question']}", reply_markup=kb)

