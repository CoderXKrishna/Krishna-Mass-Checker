import requests
from telegram import Bot
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Add your Telegram bot token here
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Stylish logo for BINof
def binof_logo():
    return '''
    
    
    $$\   $$\           $$\           $$\                           
    $$ | $$  |          \__|          $$ |                          
    $$ |$$  /  $$$$$$\  $$\  $$$$$$$\ $$$$$$$\  $$$$$$$\   $$$$$$\  
    $$$$$  /  $$  $$\ $$ |$$  _____|$$  __$$\ $$  __$$\  \____$$\ 
    $$  $$<   $$ |  \|$$ |\$$$$$$\  $$ |  $$ |$$ |  $$ | $$$$$$$ |
    $$ |\$$\  $$ |      $$ | \____$$\ $$ |  $$ |$$ |  $$ |$$  $$ |
    $$ | \$$\ $$ |      $$ |$$$$$$$  |$$ |  $$ |$$ |  $$ |\$$$$$$$ |
    \|  \__|\__|      \__|\_______/ \__|  \__|\__|  \__| \_______|
    '''

def is_vbv(card_number):
    vbv_indicator = card_number[0:6]
    vbv_bins = [
        "400115", "400117", "400118", "400119", "400135", "400136", "400137", "400138",
        "400139", "400175", "400344", "400345", "400346", "400347", "400348", "400349",
        "400350", "400351", "400352", "400353", "400354", "400355", "400356", "400357",
        "400358", "400359", "400360", "400361", "400362", "400363", "400364", "400365",
        "400366", "400367", "400368", "400369", "400370", "400371", "400372", "400373",
        "400374", "400375", "400376", "400377", "400378", "400379", "400380", "400381",
        # Add more VBV BINs here
    ]
    
    return vbv_indicator in vbv_bins

def get_bin_info(bin_number, update):
    url = f"https://lookup.binlist.net/{bin_number}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            bin_info = response.json()
            if bin_info:
                bot.send_message(chat_id=update.effective_chat.id, text=f"+++++++++++++++++BIN: {bin_number}")
                bot.send_message(chat_id=update.effective_chat.id, text=f"+++++++++++++++++Length: {bin_info.get('number', {}).get('length', 'N/A')}")
                bot.send_message(chat_id=update.effective_chat.id, text=f"+++++++++++++++++Card Type: {bin_info.get('type', 'N/A')}")
                bot.send_message(chat_id=update.effective_chat.id, text=f"+++++++++++++++++Brand: {bin_info.get('brand', 'N/A')}")
                bot.send_message(chat_id=update.effective_chat.id, text=f"+++++++++++++++++Country: {bin_info.get('country', {}).get('name', 'N/A')} {bin_info.get('country', {}).get('emoji', 'N/A')}")
                bot.send_message(chat_id=update.effective_chat.id, text=f"+++++++++++++++++Bank Name: {bin_info.get('bank', {}).get('name', 'N/A')}")
                bot.send_message(chat_id=update.effective_chat.id, text=f"+++++++++++++++++Bank URL: {bin_info.get('bank', {}).get('url', 'N/A')}")
                bot.send_message(chat_id=update.effective_chat.id, text=f"+++++++++++++++++Bank Phone: {bin_info.get('bank', {}).get('phone', 'N/A')}")
                bot.send_message(chat_id=update.effective_chat.id, text=f"+++++++++++++++++Bank City: {bin_info.get('bank', {}).get('city', 'N/A')}")
                bot.send_message(chat_id=update.effective_chat.id, text="")
            else:
                bot.send_message(chat_id=update.effective_chat.id, text="Invalid BIN Input !!")
        else:
            bot.send_message(chat_id=update.effective_chat.id, text="Invalid BIN Input !!")
    except requests.exceptions.RequestException:
        bot.send_message(chat_id=update.effective_chat.id, text="Error: Unable to retrieve BIN information. Please check your internet connection.")
    except ValueError:
        bot.send_message(chat_id=update.effective_chat.id, text="Error: Invalid response from the BIN information service.")

def mass_bin_info(file_path, update):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                bin_number = line.strip()
                get_bin_info(bin_number, update)
                if is_vbv(bin_number):
                    bot.send_message(chat_id=update.effective_chat.id, text="+++++++++++++++++ This card is VBV.")
                else:
                    bot.send_message(chat_id=update.effective_chat.id, text="$$$$$$$$$$$$$$$--- This card is non-VBV.")
    except FileNotFoundError:
        bot.send_message(chat_id=update.effective_chat.id, text="Error: The specified file does not exist.")
    except IOError:
        bot.send_message(chat_id=update.effective_chat.id, text="Error: Unable to read the file. Please check the file path.")

def start(update: Update, context: CallbackContext):
    update.message.reply_text(binof_logo())
    update.message.reply_text("""
    1. Mass BIN Check Mode
    2. Single Bin Check Mode
    3. Exit
    """)

# ...

def handle_text(update: Update, context: CallbackContext):
    text = update.message.text
    if text == '1':
        update.message.reply_text("Enter the path to the BIN file:")
        context.user_data['mode'] = 'mass_bin'
    elif text == '2':
        update.message.reply_text("Enter the BIN to check:")
        context.user_data['mode'] = 'single_bin'
    elif text == '3':
        update.message.reply_text("Exiting ....")
        context.user_data['mode'] = 'exit'
    else:
        update.message.reply_text("Invalid choice. Please enter a valid option.")

def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    updater.start_polling()

    try:
        updater.idle()
    except KeyboardInterrupt:
        print("\nExiting ....")

if __name__ == '__main__':
    main()
    
