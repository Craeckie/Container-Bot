#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from watcher import Watcher
from telegram.ext import Updater, CommandHandler


def event_received(event, msg, update, context):
    print('Event: ' + msg)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def start(update, context):
    watcher.listen_events(event_received, update, context)


if __name__ == '__main__':
    socket_path = os.environ.get('DOCKER_SOCKET_PATH', '/var/run/docker.sock')
    bot_token = os.environ.get('BOT_TOKEN')
    watcher = Watcher(socket_path=socket_path)

    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    print('Bot is starting to poll..')
    updater.start_polling()
