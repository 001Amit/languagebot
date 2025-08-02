#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install python-telegram-bot==13.15 googletrans==4.0.0-rc1


# In[ ]:


from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from googletrans import Translator
import re

translator = Translator()

def contains_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def translate_message(update: Update, context: CallbackContext):
    text = update.message.text.strip()

    if not text:
        return

    try:
        # Detect language
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

        # Translate
        translated = translator.translate(text, src=source_lang, dest=target_lang).text
        reply = f"{translated}"

        # Send reply directly under original message
        update.message.reply_text(reply, reply_to_message_id=update.message.message_id)

    except Exception as e:
        update.message.reply_text("❌ Translation failed.", reply_to_message_id=update.message.message_id)
        print(f"Translation error: {e}")

def main():
    TOKEN = "8222992423:AAEtiafm4aSMfGGGXayfiX3iIpEJwQ2K8p8"

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Enable bot to work in both group and private chats
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


# In[ ]:




