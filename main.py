#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from watcher import Watcher
from telegram.ext import Updater, CommandHandler


def event_received(event, msg, update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def start(update, context):
    watcher.listen_events(event_received, update, context)


if __name__ == '__main__':
    socket_path = os.environ.get('DOCKER_SOCKET_PATH', '/var/run/docker.sock')
    watcher = Watcher(socket_path=socket_path)

    updater = Updater(token='2085905036:AAEb_Oycehn6z4Igr2Q5eZtUjaPiPgLmLDc', use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    updater.start_polling()
