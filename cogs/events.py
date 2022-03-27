import discord
from discord.ext import commands
import config

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("fun cog loaded")


    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        em= discord.Embed(title=f"**I was removed from {guild.name}!**",color=discord.Color.embed_background(),description=f"**Guild ID:**\n`{guild.id}`\n**Member Count:**\n`{guild.member_count}`\n**Owner:**\n**{guild.owner}(`{guild.owner.id}`)**")
        em.set_footer(text=f"Guild Created At {guild.created_at}")
        try:
            em.set_thumbnail(url=f"{guild.icon.url}")
        except:
            em.set_thumbnail(url=config.icon)
        
        await self.bot.get_channel(945141129458876436).send(embed=em)
    
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        em = discord.Embed(title=f"New Guild Joined", description=f"**Name**: **{guild.name}**\n",color=discord.Color.embed_background(),timestamp=guild.created_at)
        em.add_field(name=f"Guild ID:", value=f"`{guild.id}`", inline=False)
        em.add_field(name="Member Count:", value=f"`{guild.member_count}`", inline=False)
        em.add_field(name=f"Owner:", value=f"**{guild.owner}** (`{guild.owner_id}`)", inline=False)
        try:
            em.set_thumbnail(url=f"{guild.icon.url}")
            em.set_image(url=f"https://cdn.discordapp.com/attachments/922039870808002640/944973408960127056/200.gif")
        except:
            em.set_thumbnail(url=f"https://cdn.discordapp.com/attachments/922039870808002640/944973408960127056/200.gif")
        em.set_footer(text=f"Guild Created At")
        await self.bot.get_channel(942708073368256533).send(embed=em)

def setup(bot):
    bot.add_cog(Fun(bot))