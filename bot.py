import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
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
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Напиши тему, по которой я должен сгенерировать посты для Threads.")

def generate_posts(update: Update, context: CallbackContext) -> None:
    # Получаем тему от пользователя
    topic = update.message.text

    # Генерируем посты на основе темы
    posts = generate_threads_posts(topic)

    # Отправляем 5 постов пользователю
    update.message.reply_text("\n\n".join(posts))

# Основной код для запуска бота
def main():
    # Получаем ключ API Telegram из переменной окружения
    updater = Updater(TELEGRAM_API_KEY)
    dispatcher = updater.dispatcher

    # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, generate_posts))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
