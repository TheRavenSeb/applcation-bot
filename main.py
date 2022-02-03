import nextcord 
import json
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

@client.command(name = 'app', help = 'start a ticket')
async def ticket(ctx):
    content = ctx.message.content
    command = content.split(" ")
    if command[1].lower() == "start":
        user = ctx.message.author
        promts = json.load(open("promt.json", "r"))
  
        promt_1 = promts["1"].replace("__USER__", f"<@{ctx.message.author.id}>")
        embed=nextcord.Embed(title="Beepu bot tickets (1/6)", description = promt_1, color=0xFFFFFF)
    
        if user.dm_channel is None:
            await user.create_dm()

        # if creation of dm successful
        if user.dm_channel != None:
            await user.dm_channel.send(embed=embed)
   
    
    print(f"{ctx.message.author} has started a ticket")

    ticket_res = {
        "status": "open",
        "user": {
            "id": ctx.message.author.id,
            "avatar": ctx.message.author.display_avatar.url,
            "username": str(ctx.message.author)
        },
        "message_id": ctx.message.id,
        "device": None,   # 1/6
        "username": None,            # 2/6
        "age": None,        # 3/6
        "description": None,    # 4/6
        "link": []             # 5/6
    } 
    
    msg_type = await client.wait_for('message', timeout=300)  

    if msg_type.content == 'cancel':
      await user.dm_channel.send('ticket stoped if this was a mastake rerun the command ' )
      
      return None
    else:
      ticket_res["device"] = msg_type.content

      promt_2 = promts["2"].replace("DEVICE", str(ticket_res["device"]).lower())
      embed=nextcord.Embed(title="Beepu bot tickets (2/6)", description = promt_2, color=0xFF0000)
      await user.dm_channel.send(embed=embed)
  
      msg_app = await client.wait_for('message', timeout=300)
      if msg_app.content == 'cancel':
        await user.dm_channel.send('ticket stoped if this was a mastake rerun the command ' )
        
        return None
      
      if len(msg_app.content) > 32:
          await user.dm_channel.send("Your username is too long, please shorten it to 32 characters or less")
          return
      ticket_res["username"] = msg_app.content
  
      # Start of prompt 3
      promt_3 = promts["3"].replace("USERNAME", str(ticket_res["username"]))
      embed=nextcord.Embed(title="Beepu bot tickets (3/6)", description = promt_3, color=0xFF0000)
      await user.dm_channel.send(embed=embed)
      # Wait for the message
      msg_summary = await client.wait_for('message', timeout=300)

      if len(msg_summary.content) > 256:
          await user.dm_channel.send("Your summary is too long, please shorten it to 256 characters or less")
          return

      #cancel the ticket 
      if msg_summary.content == 'cancel':
        await user.dm_channel.send('ticket stoped if this was a mastake rerun the command ' )
        
        return   
      else:
        ticket_res["age"] = msg_summary.content
  
      #Start of prompt 4
      embed=nextcord.Embed(title="Beepu bot tickets (4/6)", description = promts["4"], color=0xFF0000)
      await user.dm_channel.send(embed=embed)
  
      # Wait for the message
      msg_description = await client.wait_for('message', timeout=1200)
      
    
      if msg_description.content == 'cancel':
        await user.dm_channel.send('ticket stoped if this was a mastake rerun the command ' )
        return None  

      
      ticket_res["age"] = msg_description.content
  
      # Start of prompt 5
      embed=nextcord.Embed(title="Beepu bot tickets (5/6)", description = promts["5"], color=0xFF0000)
      await user.dm_channel.send(embed=embed)
      # Wait for the message
      msg_files = await client.wait_for('message', timeout=1200)
      
        
      
      if len(msg_files.attachments) > 0:
       for file in msg_files.attachments:
         ticket_res["link"].append(file.url)
      
      embed=nextcord.Embed(title="Beepu bot tickets (6/6)", description = promts["6"], color=0xFF0000)
      await user.dm_channel.send(embed=embed)
  
      # save the ticket res to a file
      with open("ticket.json", "w") as f:
          json.dump(ticket_res, f, indent=4)

      with open(ticket.json) as f:
        output =f.read()    
        embed=nextcord.Embed(title="Beepu bot tickets ", description = output, color=0xFF0000)
        await user.dm_channel.send(embed=embed)  
        await user.dm_channel.send("Your ticket has been created!\n\nThank you for using the gaming commuity app bot!")




with open('token.txt') as f:
   TOKEN =  f.read()

client.run(TOKEN)