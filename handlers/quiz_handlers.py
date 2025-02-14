from aiogram import Router, F, types
from aiogram.filters import Command
from utils.db_utils import update_quiz_index, get_quiz_index, save_quiz_result
from utils.quiz_utils import get_question
from data.quiz_data import quiz_data

router = Router()

async def handle_callback(callback: types.CallbackQuery, answer_type: str):
    user_id = callback.from_user.id
    current_question_index = await get_quiz_index(user_id)

    # Сохраняем результат ответа
    result = {"user_id": user_id, "correct": answer_type == "right_answer"}
    await save_quiz_result(result)

    if answer_type == "right_answer":
        message_text = "Верно!"
    else:
        correct_option = quiz_data[current_question_index]['correct_option']
        message_text = f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}"

    # Удаляем кнопки после ответа
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Отправляем сообщение с результатом
    await callback.message.answer(message_text)

    # Обновляем индекс вопроса
    current_question_index += 1
    await update_quiz_index(user_id, current_question_index)

    # Проверяем, достигнут ли конец квиза
    if current_question_index < len(quiz_data):
        await get_question(callback.message, user_id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")

@router.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    await handle_callback(callback, "right_answer")

@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await handle_callback(callback, "wrong_answer")

@router.message(Command(commands=["stats"]))
async def show_stats(message: types.Message):
    """
    Обработчик команды /stats.
    Показывает статистику результатов игроков.
    """
    from utils.db_utils import get_all_results  # Импорт функции для получения результатов

    results = await get_all_results()
    if not results:
        await message.answer("Статистика пуста.")
        return

    stats_text = "Статистика игроков:\n"
    for user_id, score in results:
        stats_text += f"User ID: {user_id}, Score: {score}\n"

    await message.answer(stats_text)