import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from deep_translator import GoogleTranslator

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Default target language. Users can change with /setlang <code>
DEFAULT_TARGET_LANG = "en"

# In-memory store of each chat's preferred target language.
# Note: this resets on restart. For persistence, swap in a database later.
user_lang_prefs = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I'm Easy200Translate Bot.\n\n"
        "Just send me any text and I'll translate it to English by default.\n\n"
        "Commands:\n"
        "/setlang <code> - set target language (e.g. /setlang fr for French)\n"
        "/help - show help and language code examples"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌍 Language codes examples:\n"
        "en - English\n"
        "fr - French\n"
        "es - Spanish\n"
        "de - German\n"
        "ar - Arabic\n"
        "zh-CN - Chinese (Simplified)\n"
        "ha - Hausa\n"
        "yo - Yoruba\n"
        "ig - Igbo\n\n"
        "Usage:\n"
        "/setlang fr\n"
        "Then just send text to translate it to French."
    )


async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not context.args:
        await update.message.reply_text(
            "Please provide a language code. Example: /setlang fr"
        )
        return

    lang_code = context.args[0].lower()
    user_lang_prefs[chat_id] = lang_code
    await update.message.reply_text(f"✅ Target language set to: {lang_code}")


async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text
    target_lang = user_lang_prefs.get(chat_id, DEFAULT_TARGET_LANG)

    try:
        translated = GoogleTranslator(source="auto", target=target_lang).translate(text)
        await update.message.reply_text(translated)
    except Exception as e:
        logger.error(f"Translation error: {e}")
        await update.message.reply_text(
            "⚠️ Sorry, I couldn't translate that. Please check the language code "
            "with /help and try again."
        )


def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable is not set. "
            "Set it in Railway's Variables tab."
        )

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("setlang", set_lang))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text))

    logger.info("Bot is starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
