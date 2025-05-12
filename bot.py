from telebot import TeleBot

TOKEN = "7978253432:AAG-8P2-K271yommJelACT1WEh_1suu44Tg"
class Global:
    base = True

bot = TeleBot(token=TOKEN, parse_mode="Markdown")

@bot.message_handler(commands=["change"])
def listen(message):
    if Global.base:
        Global.base = False
    else:
        Global.base = True
    
    bot.send_message(chat_id=message.chat.id, text="Режим изменен")

@bot.message_handler(content_types=['photo'])
def photo_id(message):
    fileID = message.photo[-1].file_id   
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    if Global.base:
        with open(f"static/base_photo/{message.chat.id}.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
    else:
        with open(f"static/learn_photo/{message.chat.id}.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)  
            
@bot.message_handler()
def listen(message):
    bot.send_message(chat_id=message.chat.id, text="Бот запущен в режиме обучение, отправьте фото, фото должно быть квадратным" if Global.base else "Бот запущен в режиме тестирования, отправьте фото, фото должно быть квадратным")
        
bot.infinity_polling()
