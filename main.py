import downloader #our module to download audio
import helpers
import os
import sys
import time


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

dwn_msg = "/d youtube_video_url to download audio."
srch_msg = "/s text to search for audio."

usage_msg = "Use: \n%s \n%s" % (dwn_msg, srch_msg)

start_msg = "Hi %s! %s"

dwn_msg = "Your song is downloading, please wait..."

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

@run_async
def download(bot, update):
	try:
		try:
			text = update.callback_query.data
			update = update.callback_query
		except:
			text = update.message.text

		if not helpers.check(text):
			bot_msg = bot.send_message(chat_id=update.message.chat_id, text=usage_msg)
			time.sleep(20)
			bot.delete_message(chat_id=update.message.chat_id, message_id=bot_msg.message_id)
		else:
			sent_msg = bot.send_message(chat_id=update.message.chat_id, text=dwn_msg)
			url = helpers.get_url(text)
			vId = helpers.get_vId(url)
			sys.stdout.write("New song request client username %s\n" % update.message.chat.username)
			audio_info = downloader.download_audio(vId, url)
			bot.delete_message(chat_id=update.message.chat_id, message_id=sent_msg.message_id)

			try:
				bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
			except:
				pass

			if not audio_info["status"]:
				msg = "Something went wrong: %s" % audio_info["error"]
				return bot.send_message(chat_id=update.message.chat_id, text=msg)

			audio = open(audio_info["path"], 'rb')
			bot.send_audio(chat_id=update.message.chat_id, audio=audio, duration=audio_info["duration"], title=audio_info["title"], timeout=999)
	except:
		pass


@run_async
def search(bot, update):
	try:
		text = update.message.text
		query = helpers.get_query(text)
		if not query:
			msg = "Use: %s" % srch_msg
			return bot.send_message(chat_id=update.callback_query.message.chat_id, text=msg)

		results = helpers.search_songs(query)
		text = ""
		for res in results:
			text += "%s - %s\n" % (res["title"], helpers.youtube_url % res["url"])

		button_list = list(map(lambda x: InlineKeyboardButton(x["title"], callback_data=x["url"]), results))
		reply_markup = InlineKeyboardMarkup(helpers.build_menu(button_list, n_cols=3))
		bot.send_message(chat_id=update.message.chat_id, text=text, reply_markup=reply_markup)
	except:
		pass


@run_async
def button(bot, update):
	try:
		data = update.callback_query.data
		update.callback_query.data = "/d %s" % (helpers.youtube_url % data)
		download(bot, update)
	except:
		pass


@run_async
def echo(bot, update):
	try:
		bot_msg = bot.send_message(chat_id=update.message.chat_id, text=usage_msg)
		time.sleep(20)
		bot.delete_message(chat_id=update.message.chat_id, message_id=bot_msg.message_id)
	except:
		pass

@run_async
def start(bot, update):
	try:
		msg = start_msg % (update.message.chat.first_name, usage_msg)
		bot.send_message(chat_id=update.message.chat_id, text=msg)
	except:
		pass


download_handler = CommandHandler("d", download)
search_handler = CommandHandler("s", search)
start_handler = CommandHandler("start", start)
message_handler = MessageHandler(Filters.text, echo)

dispatcher.add_handler(download_handler)
dispatcher.add_handler(search_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)
dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()
updater.idle()

print("Bot started")
