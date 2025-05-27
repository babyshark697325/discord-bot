import discord
from discord.ext import commands
import asyncio
import random
import os
from flask import Flask
from threading import Thread

# --- Discord Setup ---
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

# --- Tokens ---
TOKEN = os.getenv("TOKEN")
GIRLFRIEND_USER_ID = int(os.getenv("GIRLFRIEND_USER_ID"))

# --- Affirmations ---
categorized_affirmations = {
    "love": [
        "You are loved and cherished.",
        "I’m proud of you every single day.",
        "You are loved more than you know.",
        "You’re my favorite part of every day.",
        "I believe in you endlessly.",
        "Your laughter is my favorite sound.",
        "I love you more than words can express.",
        "You are the most perfect you there is."
    ],
    "confidence": [
        "You are amazing and capable of great things.",
        "You are strong, smart, and so loved.",
        "You are enough, just as you are.",
        "You deserve rest, peace, and joy."
    ],
    "appreciation": [
        "I appreciate you.",
        "You brighten my day just by being you.",
        "Your smile makes my whole day better.",
        "Every day, you inspire me more and more."
    ],
    "presence": [
        "You are a beautiful person inside and out.",
        "The world is better with you in it.",
        "You light up every room you walk into."
    ]
}

# --- Emotion Keyword Mapping ---
emotion_to_category = {
    "sad": "love",
    "lonely": "presence",
    "unseen": "appreciation",
    "insecure": "confidence",
    "lost": "presence",
    "tired": "confidence"
}

def get_affirmation_by_category(category):
    return random.choice(categorized_affirmations.get(category, ["Category not found."]))

# --- Daily Affirmation Task ---
async def send_random_affirmation_daily():
    await client.wait_until_ready()
    user = await client.fetch_user(GIRLFRIEND_USER_ID)

    while not client.is_closed():
        try:
            category = random.choice(list(categorized_affirmations.keys()))
            affirmation = get_affirmation_by_category(category)
            message = (
                f"{affirmation}\n\n"
                f"𝐈 𝐥𝐨𝐯𝐞 𝐲𝐨𝐮 💛\n\n"
                f"Want another one? Just reply with: love, confidence, appreciation, or presence."
            )
            await user.send(message)
            print("Sent random daily affirmation.")
        except Exception as e:
            print(f"Error sending message: {e}")

        await asyncio.sleep(6 * 60 * 60)  # 6 hours

# --- Respond to Keywords or Emotions ---
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.id == GIRLFRIEND_USER_ID:
        content = message.content.lower().strip()

        # Category keyword
        if content in categorized_affirmations:
            affirmation = get_affirmation_by_category(content)
            await message.channel.send(affirmation)

        # Emotion-to-category
        elif content in emotion_to_category:
            category = emotion_to_category[content]
            affirmation = get_affirmation_by_category(category)
            await message.channel.send(affirmation)

    # No need for client.process_commands(message) since no commands are used

# --- On Ready Event ---
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(type=discord.ActivityType.listening, name="Her heart 💛")
    )
    client.loop.create_task(send_random_affirmation_daily())

# --- Keep Alive (for Railway or Replit) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

# --- Run Bot ---
keep_alive()
client.run(TOKEN)
