import nextcord
import json
import typing 
import nextcord.ext.commands
from datetime import datetime
from nextcord import SlashOption
from nextcord.ext import commands
from typing import Optional
BOT_TOKEN = "BOT_TOKEN"
DATA_USER = "lordfalcon787" 
DATA_PASS = "PASSWORD"
RETRIEVE_DB = "mongodb+srv://lordfalcon787:y6H1dURJT7Dj2Svp@robberbot787.3vaos.mongodb.net/"
RETRIEVE_MONGO = "mongodb+srv://lordfalcon787:y6H1dURJT7Dj2Svp@robberbot787.3vaos.mongodb.net/?retryWrites=true&w=majority&appName=RobberBot787"
TESTING_GUILD_ID = 1234605482937684059
RC_AUCTION_QUEUE = 1267530934723281009
RC_EVENT_QUEUE = 1267527896218468412
EVENT_QUEUE = 1266257466677792768
AUCTION_QUEUE = 1267355852856229918
RC_ICON = "https://i.imgur.com/K5L7kxl.png"
RC_BANNER = "https://i.imgur.com/kL6BSmK.jpeg"
GREEN_CHECK = "<:green_check2:1291173532432203816>"
RED_X = "<:red_x2:1292657124832448584>"


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = RETRIEVE_MONGO
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["Main"]
donocollection = db["Donations"]
usercollection = db["Users"]


class UnfilteredBot(commands.Bot):

    async def process_commands(self, message):
        ctx = await self.get_context(message)
        await self.invoke(ctx)


intents = nextcord.Intents.all()
intents.message_content = True
bot = UnfilteredBot(command_prefix=["!",""], intents=intents, activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="Over Robbing Central"), status=nextcord.Status.online)
BOT_ICON = "https://i.imgur.com/O6sjeKw.jpeg"


@bot.event
async def on_ready():
    member = await bot.fetch_user(1166134423146729563)
    current_time = int(datetime.now().timestamp())
    embed = nextcord.Embed(title="┊ ✅ ┊ Bot Startup", description=f"The bot has started up! \n Current Time: <t:{current_time}:F> \n Current Guilds: {len(bot.guilds)}", color=65280)
    embed.set_image(url=RC_BANNER)
    embed.set_thumbnail(url=BOT_ICON)
    embed.set_footer(text=f"Made by _lordfalcon_", icon_url=BOT_ICON)
    channel = await member.create_dm()
    await channel.send(embed=embed)
    print(f'Logged in as {bot.user}')
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"An error occurred: {e}")


@bot.slash_command(guild_ids=[TESTING_GUILD_ID])
async def event(interaction: nextcord.Interaction, 
                event: str = SlashOption(description="The name of the event."),
                prize: str = SlashOption(description="The prize of the event."),
                donate: int = SlashOption(name= "donated", choices={"Yes": 1, "No": 2}, description="Have you donated to the event?"),
                message: Optional[str] = SlashOption(required=False, description="Additional message for the event."),
                other: Optional[str] = SlashOption(required=False, description="Any other information for the event. (Reqs, modifiers, etc.)")):
    """Create an event for the server."""

    if donate == 2:
        await interaction.response.send_message(content=f"You must donate before running this command! Try again after you have donated.", ephemeral=True)
        return
    else:
        pass

    if message is None:
        message = "No message provided."
    if other is None:
        other = "No other provided."
    EVENT = event
    PRIZE = prize
    MESSAGE = message
    OTHER = other
    DONOR = interaction.user.id
    CONTENT = (f"<@&1246219564300238868> - <@{DONOR}> would like to donate for an {EVENT}")

    if (EVENT.lower() == "auction"):
        CHANNEL_TO_SEND = AUCTION_QUEUE
    else:
        CHANNEL_TO_SEND = EVENT_QUEUE

    embed = nextcord.Embed(title="┊ ✅ ┊ Successfully Donated", description=f"┊ 🎪 ┊ **Event:** {EVENT}\n ┊ 🏆 ┊ **Prize:** {PRIZE}\n ┊ 📝 ┊ **Message:** {MESSAGE}\n ┊ 🔗 ┊ **Other:** {OTHER}", color=65280)
    await interaction.response.send_message(embed=embed, ephemeral=False)
    response = await interaction.original_message()
    response_id = response.id
    embed = nextcord.Embed(title="┊ 📅 ┊ Event Pending", description=f"┊ 🎪 ┊ **Event:** {EVENT}\n ┊ 🏆 ┊ **Prize:** {PRIZE}\n ┊ 📝 ┊ **Message:** {MESSAGE}\n ┊ 🔗 ┊ **Other:** {OTHER} \n ┊ 💰 ┊ **Donor:** <@{DONOR}>", color=16036916)
    embed.set_footer(text=f"{response_id}", icon_url=RC_ICON)
    sent_message = await bot.get_channel(CHANNEL_TO_SEND).send(content=f"{CONTENT}", embed=embed)
    message_id = sent_message.id
    await sent_message.add_reaction(GREEN_CHECK)
    await sent_message.add_reaction(RED_X)


@bot.command(name="role_info")
@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)
    await role_info(ctx)

async def role_info(ctx):
    role_name = ctx.message.content.strip()
    if not ctx.message.content.startswith('-role info'):
        return

    if role_name is None:
        await ctx.send("Please provide a role name. Usage: `-role info [role name]`")
        return

    # Remove '-role info' from the beginning of the message content
    role_name = ctx.message.content[11:].strip()

    if not role_name:
        await ctx.send("Please provide a role name. Usage: `-role info [role name]`")
        return

    role = nextcord.utils.get(ctx.guild.roles, name=role_name)
    if role is None:
        await ctx.send(f"Role '{role_name}' not found.")
        return

    members_with_role = len(role.members)
    created_at = role.created_at.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    embed = nextcord.Embed(title=f"Role Information", color=role.color)
    description = f"""
    Name: {role.name}
    Members: {members_with_role}
    Color: #{role.color.value:06x}
    Created On: <t:{int(role.created_at.timestamp())}:F>
    Displayed Separately: {role.hoist}
    Permissions: {', '.join(perm.capitalize() for perm, value in role.permissions if value)}
    """
    if role.icon:
        embed.set_thumbnail(url=role.icon.url)
    embed.description = description
    embed.set_footer(text=f"ID: {role.id}")

    await ctx.send(embed=embed)




async def db(ctx):
    if not ctx.message.content.startswith('!db'):
        return
    """Run a command."""
    NAME = ctx.author.name
    USERID = ctx.author.id
    print(f"Added {NAME} to the database as {USERID}!")
    post = {"_id": USERID, "name": NAME, "user_id": USERID}
    if not usercollection.find_one({"_id": USERID}):
        usercollection.insert_one(post)
        await ctx.reply(f"Added {NAME} to the database as {USERID}!")
    else:
        print(f"User {USERID} already exists in the database.")

@bot.command()
async def dono(ctx):
    "Set donations."
    if not ctx.message.content.lower().startswith('dono'):
        return
    await ctx.send("Donation command received. Please confirm your donation.")





bot.run(BOT_TOKEN)