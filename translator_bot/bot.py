#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import re
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from googletrans import Translator

# Initialize the translator
translator = Translator()

# Function to detect if message contains Chinese
def contains_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))

# Main translation handler
def translate_message(update: Update, context: CallbackContext):
    text = update.message.text.strip()

    if not text:
        return

    try:
        # Detect language direction
        if contains_chinese(text):
            source_lang = 'zh-cn'
            target_lang = 'en'
        elif re.search(r'[a-zA-Z]', text):
            source_lang = 'en'
            target_lang = 'zh-cn'
        else:
            update.message.reply_text(
                "⚠️ Please send text in English or Chinese.",
                reply_to_message_id=update.message.message_id
            )
            return

        # Perform translation
        translated = translator.translate(text, src=source_lang, dest=target_lang).text

        # Send the translated message as a reply
        update.message.reply_text(translated, reply_to_message_id=update.message.message_id)

    except Exception as e:
        update.message.reply_text("❌ Translation failed.", reply_to_message_id=update.message.message_id)
        print(f"Translation error: {e}")

def main():
    TOKEN = os.environ.get("TOKEN")  # Bot token should be set in Render/hosting as environment variable

    if not TOKEN:
        print("❌ TOKEN not found. Please set the environment variable.")
        return

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Handle text messages in both groups and private chats
    dispatcher.add_handler(
        MessageHandler(
            Filters.text & (Filters.chat_type.groups | Filters.chat_type.private),
            translate_message
        )
    )

    print("✅ Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

