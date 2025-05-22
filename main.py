import discord
from discord.ext import commands
from discord.ui import View, Button
import asyncio
import random
import os
from flask import Flask
from threading import Thread

# --- Discord Setup ---
intents = discord.Intents.default()
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

def get_affirmation_by_category(category):
    return random.choice(categorized_affirmations.get(category, ["Category not found."]))

# --- Buttons ---
class CategoryButton(Button):
    def __init__(self, category):
        super().__init__(label=category.capitalize(), style=discord.ButtonStyle.primary)
        self.category = category

    async def callback(self, interaction: discord.Interaction):
        affirmation = get_affirmation_by_category(self.category)
        await interaction.response.send_message(affirmation, ephemeral=True)

class CategoryView(View):
    def __init__(self):
        super().__init__(timeout=None)
        for category in categorized_affirmations:
            self.add_item(CategoryButton(category))

# --- Task: Send Message Every 6 Hours ---
async def send_love_and_buttons_every_6_hours():
    await client.wait_until_ready()
    user = await client.fetch_user(GIRLFRIEND_USER_ID)

    while not client.is_closed():
        try:
            await user.send("𝐈 𝐥𝐨𝐯𝐞 𝐲𝐨𝐮 💛\nPick a category for your affirmation today:", view=CategoryView())
            print("Sent 'I love you' with buttons.")
        except Exception as e:
            print(f"Error sending message: {e}")

        await asyncio.sleep(6 * 60 * 60)  # 6 hours

# --- Events ---
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(type=discord.ActivityType.listening, name="Her heart 💛")
    )
    client.loop.create_task(send_love_and_buttons_every_6_hours())

# --- Keep Alive for Replit ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

# --- Run ---
keep_alive()
client.run(TOKEN)
