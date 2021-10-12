#!/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
import os
import random
import signal
from time import sleep

from watcher import Watcher
from telegram.ext import Updater, CommandHandler
import threading

events = []
last_event_num = 1
retries = 0
signal_set = False


def handler(signum, frame):
    global last_event_num, retries, signal_set
    cur_events = events.copy()
    if len(cur_events) > last_event_num:
        last_event_num = len(cur_events)
        retries += 1
        print('Retry ' + str(retries))
        if retries < 3:
            signal.alarm(5)
            return
    for i in range(0, len(cur_events)):
        events.pop(0)
    last_event_num = 0
    retries = 0
    signal_set = False
    print('Sending')
    msg = '\n'.join([e['msg'] for e in cur_events])
    last_event = cur_events[-1]
    context = last_event['context']
    update = last_event['update']
    print(msg)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def event_received(event, msg, update, context):
    global signal_set
    print('Event: ' + msg)
    events.append({
        'msg': msg,
        'context': context,
        'update': update,
        'event': event
    })
    if not signal_set:
        signal_set = True
        signal.alarm(2)


async def start(update, context):
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
    signal.signal(signal.SIGALRM, handler)

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
