import sqlite3
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters


TOKEN = "8624724980:AAE7zRA0mARveAVlmE60GIX960gX9QUEfgQ"

OPEN_DATE = datetime(2031, 6, 27)

conn = sqlite3.connect("videos.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS videos(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
file_id TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
user_id INTEGER PRIMARY KEY
)
""")

conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cursor.execute(
        "INSERT OR IGNORE INTO users(user_id) VALUES(?)",
        (user_id,)
    )

    conn.commit()

    await update.message.reply_text(
        "🎓 Ласкаво просимо до капсули часу 11-Б!\n\nНадішліть відео, яке відкриється 27.06.2031 ❤️"
    )

async def receive_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    file_id = update.message.video.file_id

    cursor.execute(
        "INSERT INTO videos(user_id, file_id) VALUES(?, ?)",
        (user_id, file_id)
    )

    conn.commit()

    await update.message.reply_text(
        "✅ Відео збережено!"
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VIDEO, receive_video))

app.run_polling()
print("Bot started...")

app.run_polling()
