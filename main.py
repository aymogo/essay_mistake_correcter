import os
import logging
from telegram import Update, ForceReply
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackContext,
)
from functions import get_word_count, get_corrections, get_candidates

TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


HOME, REPLY_ESSAY = range(2)

async def start(update: Update, context: CallbackContext):
    # await context.bot.send_message(
    #     chat_id=update.effective_chat.id, text=rf"Hi {update.effective_user.mention_html()} !",
    # )
    await update.message.reply_html(rf"Hi {update.effective_user.mention_html()} !")

    return HOME


async def check_word(update: Update, context: CallbackContext) -> int:
    text = update.message.text

    candidates = get_candidates(text)

    await update.message.reply_text(", ".join(candidates))

    return HOME


async def check_essay(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Send me your essay which you want to check mistakes.")

    return REPLY_ESSAY


async def reply_essay(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    if data := get_corrections(message):
        text = "You\'ve some mistakes: \n"
        for d in data:
            text += f"\'{d[0]}\' -> \'{d[1]}\' \n"
    else:
        text = "Congrats, you\'re doing well, zero mistakes"
    
    await update.message.reply_text(text)

    return HOME


def main():
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            HOME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, check_word
                ),
                CommandHandler(
                    "check_essay", check_essay
                ),
            ],
            REPLY_ESSAY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, reply_essay
                ),
                CommandHandler(
                    "check_essay", check_essay
                ),
            ],
        },
        fallbacks=[MessageHandler(filters.TEXT, check_word)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()