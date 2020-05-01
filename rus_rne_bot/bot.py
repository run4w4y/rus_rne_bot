from .config import token
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from .rne_parser import parse
import time

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="started")

def new(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="please wait")
    problems = parse()
    for problem in problems:
        context.bot.send_poll(
            chat_id=update.effective_chat.id,
            question=problem.question,
            options=problem.options,
            is_anonymous=False,
            type=telegram.Poll.QUIZ,
            correct_option_id=problem.answer_id
        )
        time.sleep(60)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="unknown command")

def run():
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('new', new))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling()
