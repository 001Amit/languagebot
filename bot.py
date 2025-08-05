import os
import re
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from googletrans import Translator

translator = Translator()

# ✨ Replace this with your actual ID
ALLOWED_USER_ID = 1769111837

def contains_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def contains_english(text):
    return bool(re.search(r'[a-zA-Z]', text))

def translate_message(update: Update, context: CallbackContext):
    text = update.message.text.strip()
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    # ❌ Reject anyone who is not you
    if user_id != ALLOWED_USER_ID:
        print(f"Blocked user: {user_name} ({user_id}) tried to use the bot.")
        return  # Silent ignore

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
            return

        translated = translator.translate(text, src=source_lang, dest=target_lang).text

        if translated.strip().lower() == text.strip().lower():
            return

        print(f"[{user_name}] {text} → {translated}")

        update.message.reply_text(translated, reply_to_message_id=update.message.message_id)

    except Exception as e:
        print(f"❌ Translation error: {e}")
        return

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
