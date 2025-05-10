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
        # Новый промпт, ограничиваем длину постов
        prompt = f"Представь, что ты создаешь вирусные посты для соцсети Threads по заданной теме. Тема: {topic}. Схема такая - придумываешь вопрос или тему для обсуждения и накидываешь свои 2 комментария для начала обсуждения."

        # Используем новую модель gpt-4o
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Заменили модель
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,  # Увеличили максимальное количество токенов
            n=1,
            temperature=0.7
        )

        # Извлекаем текст постов
        posts = [choice['message']['content'].strip() for choice in response['choices']]
        return posts
    except Exception as e:
        print(f"Error generating posts: {e}")
        return ["Ошибка при генерации постов. Попробуйте снова."]

# Функция для отправки сообщений с проверкой на длину
async def send_message_in_parts(update, text):
    max_length = 4096
    # Если текст слишком длинный, разбиваем его на части
    while len(text) > max_length:
        await update.message.reply_text(text[:max_length])
        text = text[max_length:]
    if text:
        await update.message.reply_text(text)

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
    post_text = "\n\n".join(posts)
    await send_message_in_parts(update, post_text)

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
