import discord
import config
from discord.ext import commands
import discord.utils
import sqlite3
import traceback
from utils.buttons import TicketPanelView,TicketCloseTop
from utils.select import helpselect
from utils.helpers.help import main_em as em

bot=commands.Bot(command_prefix="!",intents=discord.Intents.all(),help_command=None)
bot.db = sqlite3.connect("utils/databases/main.db")
bot.dbcursor = bot.db.cursor()

@bot.event
async def on_member_join(self,member):
    if member.guild.id==939019819871772673:
        guild = bot.get_guild(939019819871772673)
        botrole = discord.utils.get(guild.roles, name="Bots")
        humanrole = discord.utils.get(guild.roles, name="Member")
        if member.bot == True:
            await member.add_roles(botrole)
        else:
            await member.add_roles(humanrole)
            em= discord.Embed(title=f"Welcome to `GamingBoots's git repo`!",description=f"**I will show you the way around**\n**● Read Rules at** <#939019820341534748>\n\n**● Annoucement chanel **<#939019820639354911>\n\n**● Chat here **<#939019820639354916>\n\n**● Chek our [Youtube <:youtube:945144727987175505>](https://www.youtube.com/channel/UC5exlQvXHangpDBOxmC2xow)**",color=discord.Color.embed_background())
            em.set_image(url=f"https://some-random-api.ml/welcome/img/1/stars2?key=PwNWJnOYXR0qT8uob4iEGse7oLBoEvjNWBLcJQETsF3mqKnQDXFU3Ik6cxkmtcGo&username={member.name}&discriminator={member.discriminator}&avatar={member.avatar.url}%3Fsize=512&type=join&guildName=Gamingboot's%20git%20repo&textcolor=white&memberCount={member.guild.member_count}")
            await bot.get_channel(939019820341534747).send(content=member.mention,embed=em)
@bot.event
async def on_ready():
    print("Logged in as Ceres!")
    activity=discord.Activity(type=discord.ActivityType.watching,name='/help')
    await bot.change_presence(activity=activity)
    bot.add_view(TicketPanelView(bot))
    bot.add_view(TicketCloseTop(bot))
    bot.persistent_views_added = True
    bot.dbcursor.execute('CREATE TABLE IF NOT EXISTS ticket (guild_id INTEGER , count INTEGER, category INTEGER)')
    bot.dbcursor.execute('CREATE TABLE IF NOT EXISTS tickets (guild_id INTEGER, channel_id INTEGER, opener INTEGER, switch TEXT)')
    bot.db.commit()

@bot.slash_command(name="help")
async def help_(ctx):
    """returns a list of commands in the bot"""
    await ctx.respond(embed=em,view=helpselect())

extensions=[
            'cogs.mod',
            'cogs.fun',
            'cogs.utility',
            'cogs.api_cmd',
            'cogs.ticket',
            'jishaku'
]
if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
            
        except Exception as e:
            traceback.print_exc()
bot.run(config.TOKEN)