from .config import token
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from .rne_parser import Rus4
import time
import threading

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="started")

def new(update, context):
    try:
        parsers = {
            4: Rus4()
        }
        args = list(map(lambda x: (*map(int, x.split(':')), 0), context.args))
        
        if not args:
            context.bot.send_message(chat_id=update.effective_chat.id, text="empty quiz")
            return
        
        for i in args:
            if i[1] < 0 or i[1] > 25:
                update.message.reply_text('quantity must be in range 0-25')
            if i[2] > 600 or i[2] < 5 and i[2] != 0:
                update.message.reply_text('period must be in range 5-600')
                return
            if i[0] not in parsers.keys():
                update.message.reply_text('problem {} is not supported. list of supported problems: {}'.format(i[0], parsers.keys()))
                return

        def send_problems():
            context.bot.send_message(chat_id=update.effective_chat.id, text="please wait")
            problems = map(lambda x: (parsers[x[0]].parse(x[1]), x[2]), args)
            for problem, delay in problems:
                context.bot.send_poll(
                    chat_id=update.effective_chat.id,
                    question=problem.question,
                    options=problem.options,
                    is_anonymous=False,
                    type=telegram.Poll.QUIZ,
                    correct_option_id=problem.answer_id,
                    open_period=None if delay < 5 else delay
                )
                if delay >= 5:
                    time.sleep(delay)
            
    except (BaseException):
        update.message.reply_text('Usage: /new <number>:<quantity>:?<period> ...')
        

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="unknown command")

def run():
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('new', new))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling()
