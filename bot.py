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
    try:
        prompt = f"Представь, что ты создаешь популярные посты для соцсети Threads. Тема: {topic}. Создай 5 идей для постов, которые могут стать популярными. Посты должны быть короткими, интересными, и подходить для широкой аудитории."

        # Используем новую модель gpt-3.5-turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Заменили модель
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,  # Увеличили максимальное количество токенов
            n=5,
            temperature=0.7
        )

        # Извлекаем текст постов
        posts = [choice['message']['content'].strip() for choice in response['choices']]
        return posts
    except Exception as e:
        print(f"Error generating posts: {e}")
        return ["Ошибка при генерации постов. Попробуйте снова."]

# Основная функция для работы бота
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привет! Напиши тему, по которой я должен сгенерировать посты для Threads.")

async def generate_posts(update: Update, context: CallbackContext) -> None:
    topic = update.message.text
    print(f"Received topic: {topic}")  # Логирование

    # Генерируем посты на основе темы
    posts = generate_threads_posts(topic)
    print(f"Generated posts: {posts}")  # Логирование

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
