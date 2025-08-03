import os
import re
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from googletrans import Translator

translator = Translator()

def contains_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def contains_english(text):
    return bool(re.search(r'[a-zA-Z]', text))

def translate_message(update: Update, context: CallbackContext):
    text = update.message.text.strip()
    user = update.effective_user.first_name

    if not text:
        return

    try:
        if contains_chinese(text):
            source_lang = 'zh-cn'
            target_lang = 'en'
        elif contains_english(text):
            source_lang = 'en'
            target_lang = 'zh-cn'
        else:
            # Silent ignore (no reply)
            return

        translated = translator.translate(text, src=source_lang, dest=target_lang).text

        # If translation is the same as input (no real translation), skip
        if translated.strip().lower() == text.strip().lower():
            return

        # Logging
        print(f"[{user}] {text} → {translated}")

        # Reply under the original message
        update.message.reply_text(translated, reply_to_message_id=update.message.message_id)

    except Exception as e:
        print(f"❌ Translation error: {e}")
        return  # Silent fail

def main():
    TOKEN = os.environ.get("TOKEN")
    if not TOKEN:
        print("❌ TOKEN not found. Please set the environment variable.")
        return

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

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
