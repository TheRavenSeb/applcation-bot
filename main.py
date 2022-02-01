import nextcord 
from nextcord.ext import commands
from nextcord.utils import get
from nextcord.ext import menus

#bot start-up
intents = nextcord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=".",intents=intents)

#on-ready
@client.event
async def on_ready():
    for guild in client.guilds:
    	print(f'{client.user} is connected to the following guild:\n'
          f'{guild.name}(id: {guild.id})')