#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from watcher import Watcher
from telegram.ext import Updater, CommandHandler
import threading

watch_thread = None


def event_received(event, msg, update, context):
    print('Event: ' + msg)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def start(update, context):
    if user_id:
        global watch_thread
        if watch_thread is None:
            watch_thread = threading.Thread(target=watcher.listen_events,
                                            name="Container Watch",
                                            args=[event_received, update, context])
            watch_thread.start()
            msg = 'Listening to events'
        else:
            msg = 'Already listening to events'
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Your user id on TG is ' + update.effective_user.id)


if __name__ == '__main__':
    global user_id
    socket_path = os.environ.get('DOCKER_SOCKET_PATH', '/var/run/docker.sock')
    bot_token = os.environ.get('BOT_TOKEN')
    user_id = os.environ.get('TG_USER_ID')
    watcher = Watcher(socket_path=socket_path)

    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    print('Bot is starting to poll..')
    updater.start_polling()
