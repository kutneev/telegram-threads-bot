import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

# Получаем ключи из переменных окружения
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Функция для генерации постов на основе заданной темы
def generate_threads_posts(topic):
    prompt = f"Представь, что ты создаешь популярные посты для соцсети Threads. Тема: {topic}. Создай 5 идей для постов, которые могут стать популярными. Посты должны быть короткими, интересными, и подходить для широкой аудитории."

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=5,
        temperature=0.7
    )

    posts = [choice.text.strip() for choice in response.choices]
    return posts

# Основная функция для работы бота
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привет! Напиши тему, по которой я должен сгенерировать посты для Threads.")

async def generate_posts(update: Update, context: CallbackContext) -> None:
    # Получаем тему от пользователя
    topic = update.message.text

    # Генерируем посты на основе темы
    posts = generate_threads_posts(topic)

    # Отправляем 5 постов пользователю
    await update.message.reply_text("\n\n".join(posts))

# Основной код для запуска бота
def main():
    # Создаём объект приложения для запуска бота
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_posts))

    # Запуск бота
    application.run_polling(allowed_updates=["message"])

if __name__ == '__main__':
    main()
