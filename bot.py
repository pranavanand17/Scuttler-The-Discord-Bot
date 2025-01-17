import discord
from discord.ext import commands
import random
import time
import os

# Enable intents
intents = discord.Intents.default()
intents.message_content = True  # Allow the bot to read message content
intents.members = True          # Enable Server Members Intent
intents.presences = True        # Enable Presence Intent

# Function to play Rock, Paper, Scissors
async def play_rock_paper_scissors(channel, bot, check):
    await channel.send("Playing Rock, Paper, Scissors\nFirst to 3 wins!\nPlay at 'Shoot'")
    time.sleep(1)

    # Initialize scores
    player_score = 0
    bot_score = 0

    # Game loop
    while player_score < 3 and bot_score < 3:
        await channel.send("Choose:\n1: 🪨\n2: 📜\n3: ✂️")
        time.sleep(1)
        await channel.send("Ready? Type 'ready' to begin.")

        # Wait for player confirmation to start
        jsg = await bot.wait_for('message', check=check)
        if jsg.content.lower() == 'ready':
            random_number = random.randint(1, 3)  # Bot's move
            moves = {1: "🪨", 2: "📜", 3: "✂️"}  # Move mapping

            # Countdown
            await channel.send("Rock...")
            time.sleep(1)
            await channel.send("Paper...")
            time.sleep(1)
            await channel.send("Scissors...")
            time.sleep(1)
            await channel.send("Shoot!")

            # Bot's move
            await channel.send(f'||{moves[random_number]}||')

            # Wait for player's move
            move = await bot.wait_for('message', check=check)

            if move.content in ["1", "2", "3"]:
                player_choice = int(move.content)

                # Determine the winner
                if player_choice == random_number:
                    await channel.send("It's a tie!")
                elif (player_choice == 1 and random_number == 3) or \
                     (player_choice == 2 and random_number == 1) or \
                     (player_choice == 3 and random_number == 2):
                    player_score += 1
                    await channel.send("You win this round!")
                else:
                    bot_score += 1
                    await channel.send("I win this round!")

                # Display updated scores
                time.sleep(1)
                await channel.send(f"Your score: {player_score} | My score: {bot_score}")
            else:
                await channel.send("Invalid input! Please choose 1, 2, or 3.")

    # End of game
    if player_score == 3:
        await channel.send("Congratulations, you won the game! 🎉")
    else:
        await channel.send("I win! Better luck next time. 🤖")

# Create the bot with a command prefix (e.g., "!")
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: The bot has successfully connected and is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')  # This prints when the bot is successfully logged in

    # Set bot's status
    activity = discord.Game("Scuttler, online!")
    await bot.change_presence(status=discord.Status.online, activity=activity)

# Command: When someone types "!hello", the bot responds
@bot.command()
async def hello(ctx):
    await ctx.send("Hello, I'm Scuttler, nice to meet you! :)")

# Command: When someone types "!skrr", the bot responds
@bot.command()
async def skrr(ctx):
    await ctx.send("The ting goes skrrrrrrrrr! pa,ka,ka,ka,ka!")

@bot.event
async def on_message(message):
    if message.content.lower().startswith(('scut', 'scuttler', 'hi scut')):
        channel = message.channel
        await channel.send('Wassup, b?')
        name=message.author.global_name

        def check(m):
            return m.content and m.channel == channel and m.author.global_name==name

        while True:
            msg = await bot.wait_for('message', check=check)
            if msg.content.lower() == 'hello':
                await channel.send(f'Hello {msg.author.global_name}!')
            elif msg.content.lower() == 'play':
                await channel.send(f'Sure {msg.author.global_name}!')
                await play_rock_paper_scissors(message.channel, bot, check)
            elif msg.content.lower() == 'bye scut':
                await channel.send(f'Cya {msg.author.global_name}!')
                break

bot.run(os.getenv("DISCORD_BOT_TOKEN"))

