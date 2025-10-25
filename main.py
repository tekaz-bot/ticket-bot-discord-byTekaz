import os
import json
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from cogs.ticket_system import TicketSystem
from cogs.ticket_commands import Ticket_Command
from keep_alive import keep_alive
import asyncio

# Charger .env
load_dotenv()
token_env = os.getenv('DISCORD_TOKEN')

# Charger config.json
with open("config.json", "r") as f:
    config = json.load(f)

BOT_TOKEN = config.get("token", token_env)
GUILD_ID = int(config["guild_id"])
CATEGORY_ID1 = int(config["category_id_1"])
CATEGORY_ID2 = int(config["category_id_2"])

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# === RICH PRESENCE ===
@tasks.loop(minutes=1)
async def richpresence():
    guild = bot.get_guild(GUILD_ID)
    if guild:
        category1 = discord.utils.get(guild.categories, id=CATEGORY_ID1)
        category2 = discord.utils.get(guild.categories, id=CATEGORY_ID2)
        total_tickets = len(category1.channels) + len(category2.channels)
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{total_tickets} tickets | Tekaz.fr"
            )
        )

# === on_ready ===
@bot.event
async def on_ready():
    print(f"✅ Bot prêt : {bot.user} ({bot.user.id})")

    # Synchronisation spécifique à la guild
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)
    print("✅ Slash commands synchronisées sur la guild.")

    richpresence.start()

# === Setup complet ===
async def setup_bot():
    await bot.add_cog(TicketSystem(bot))
    await bot.add_cog(Ticket_Command(bot))
    print("✅ Cogs chargés avec succès.")

# === Main ===
async def main():
    keep_alive()
    async with bot:
        await setup_bot()
        await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
