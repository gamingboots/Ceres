import discord
from discord.ext import commands
from discord.commands import slash_command,Option
from discord.ui import Button,View
from discord.ext import commands
from discord.errors import Forbidden
from datetime import datetime
import datetime
import humanfriendly


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print("mod cog loaded")


#timout cmd

    @slash_command(name="timeout",description="🔇 timeouts the specified member",guild_ids=[883180896038027336,903168731885240350])
    @commands.has_permissions(moderate_members=True)
    async def timeout(self,ctx,member: Option(discord.Member, "Select the user", required=True), time: Option(str, "Mention the mute duration(s: seconds, m: minutes, h: hours, d: days)", required=True), reason: Option(str, "Reason for mute", required=False, default="Reason Not Mentioned")):
        try:    
            try:
                timeConvert = humanfriendly.parse_timespan(time)
            except:
                await ctx.respond(f"**{time} is not a valid time Please try again!**")
            oreason = f"{ctx.author.name} timedout {member.name} for - {reason}"
            confirm_time = Button(label="Confirm",style=discord.ButtonStyle.danger)
            cancel_time=Button(label="Cancel",style=discord.ButtonStyle.green)
            async def confirm_button_callback(interaction):
                try:
                    if interaction.user.id == ctx.author.id:
                        await member.timeout(discord.utils.utcnow()+datetime.timedelta(seconds=timeConvert), reason=oreason)
                        cmute_embed = discord.Embed(description=f"**<:ceres_succces:938669698621509652>  `{member.name}` was succesfully timed-out  for `{time}`!**", color=0x2ECC71)
                        await ctx.edit(embed=cmute_embed,view=None)
                    else:
                        await interaction.send_message(f"This is not for you!",ephemeral=True)
                except:
                    await ctx.respond(f"**Something went wrong!**")
            async def cancel_time_call(interaction):
                if interaction.user.id == ctx.author.id:
                    ca=discord.Embed(title="Canceled the process",description=f"the timeout of `{member.name}` was canceled by `{ctx.author}`!", color=discord.Color.embed_background())
                    await ctx.edit(embed=ca,view=None)
                else:
                    await interaction.send_message(f"This is not for you!",ephemeral=True)
            confirm_time.callback=confirm_button_callback
            cancel_time.callback=cancel_time_call
            view=View()
            view.add_item(cancel_time)
            view.add_item(confirm_time)
            is_admin = member.guild_permissions.administrator
            if member.id == ctx.guild.owner_id:
                await ctx.respond("**<:ceres_failure:951863495559872613> Cannot timeout the guild owner sorry!**",ephemeral=True)
            
            elif is_admin==True:
                await ctx.respond("**That member is an admin/moderator you cannot timeout them!**",ephemeral=True)

            elif member == ctx.author:
                await ctx.respond("**<:ceres_failure:951863495559872613> You cannot timeout yourself!**",ephemeral=True)
            elif ctx.guild.me.top_role.position < member.top_role.position:
                await ctx.respond("**<:ceres_failure:951863495559872613> That member has a higher role than mine please drag my role above them!**",ephemeral=True)
            elif ctx.author.top_role.position < member.top_role.position:
                await ctx.respond(f"**<:ceres_failure:951863495559872613> Your Role position is lower than the role of `{member.name}` so you cannot do that!**",ephemeral=True)
            else:
                em=discord.Embed(title="Are you sure?",description=f"**Please confirm the timeout of `{member.name}` for reason - `{reason}`**",color=0x2ECC71)
                await ctx.respond(view=view,embed=em)
        except commands.MissingPermissions:
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Moderate members` permission to be able to use this command!**")

#unmute cmd

    @slash_command(name="unmute",description=" 😁 Unmutes a specified user.",guild_ids=[903168731885240350,883180896038027336])
    @commands.has_permissions(manage_messages=True)
    async def unmute(self,ctx, member: Option(discord.Member,"Select the user to unmute!",required=True),reason : Option(str,"Write the reason the kicking the user.")):
        try:
            try:
                await member.timeout(until=None,reason=reason)
                embed = discord.Embed(description=f"**<:ceres_succces:938669698621509652> succesfully unmuted-{member.mention}!**",color=ctx.author.color)
                await ctx.respond(embed=embed)
            except:
                await ctx.respond(f"**{member.name} is not muted**")
        except commands.MissingPermissions:
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Manage member` permission to be able to use this command!**")

#kick cmd

    @slash_command(name="kick",description="🦶 kicks a user from the server",guild_ids=[883180896038027336,903168731885240350])
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx, user : Option(discord.Member,"Select the user to kick!",required=True), *, reason : Option(str,"Write the reason the kicking the user.")):
        """Kicks a user from the server."""
        try:
            if reason==None:
                reason="No reason provided!"
            oreason=f"{user.name} banned by {ctx.author.name} for - {reason}"
            if ctx.guild.me.top_role.position < user.top_role.position:
                return await ctx.respond(f"<:ceres_failure:951863495559872613> {user.name} has a higher role than mine i cannot kick them!")
            elif user.id == ctx.guild.owner_id:
                return await ctx.respond(f"**<:ceres_failure:951863495559872613> kick the server owner?**")
            elif ctx.author == user:
                await ctx.respond("**<:ceres_failure:951863495559872613> You cannot kick yourself.**")
                return
            elif ctx.author.top_role <= user.top_role:
                await ctx.respond(f"**<:ceres_failure:951863495559872613> You are not cool enough to kick that person.**")
                return
            else:
                try:    
                    await ctx.guild.kick(user,reason= oreason)
                    kick_embed = discord.Embed(description=f'**<:ceres_succces:938669698621509652> `{user}` was successfully kicked!**', color=ctx.author.color)
                    await ctx.respond(embed=kick_embed)
                except Forbidden:
                    await ctx.respond(f"**I don't have enough permission to kick this member!**")
        except commands.MissingPermissions:
                    await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Kick members` permission to be able to use this command!**")
#ban cmd

    @slash_command(name="ban",description="🔨 Bans a user from the server",guild_ids=[883180896038027336,903168731885240350])
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx, user : Option(discord.Member,"Select the user to ban!",required=True), *, reason : Option(str,"Write the reason for banning the user.")):
        try:    
            if reason==None:
                reason="No reason provided!"
            oreason=f"{user.name} banned by {ctx.author.name} for - {reason}"
            guild = ctx.guild
            is_admin = user.guild_permissions.administrator
            if ctx.guild.me.top_role.position < user.top_role.position:
                return await ctx.respond(f"<:ceres_failure:951863495559872613> {user.name} has a higher role than mine i cannot ban them!")
            if ctx.author.top_role.position < user.top_role.position:
                await ctx.respond("Your role needs to be higher than the person you are trying to ban.")
            elif user == ctx.guild.owner:
                return await ctx.respond(f'**<:ceres_failure:951863495559872613> ban the server owner?**')
            elif ctx.author == user:
                await ctx.respond("**<:ceres_failure:951863495559872613> You cannot ban yourself xD.**")
                return
            elif is_admin==True:
                await ctx.respond(f"**<:ceres_failure:951863495559872613> That user is a moderator/admin I cannot ban them**")
                return
            else:
                try:    
                    await guild.ban(user,reason = oreason)
                    ban_embed = discord.Embed(description=f'**<:ceres_succces:938669698621509652> ``{user}`` was successfully banned!**', color=ctx.author.color)
                    await ctx.respond(embed=ban_embed)
                except Forbidden:
                    await ctx.respond(f"**<:ceres_failure:951863495559872613> I don't have enough permission to ban this member!**")
        except commands.MissingPermissions:
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Ban members` permission to be able to use this command!**")

#unban cmd

    @slash_command(name="unban",description="✈️ unbans a banned member",guild_ids=[883180896038027336,903168731885240350])
    @commands.has_permissions(ban_members=True)
    async def unban(self,ctx,member:Option(str,"Write the user name with discriminator to unban or the user's id",required=True)):
        try:
            try:
                banned_users=await ctx.guild.bans()
                member_name,member_discriminator=member.split('#')
                for ban_entry in banned_users:
                    user=ban_entry.user
                    if(user.name,user.discriminator) == (member_name,member_discriminator):
                        await ctx.guild.unban(user)
                        unban_embed = discord.Embed(description=f'**<:ceres_succces:938669698621509652> ``{user}`` was unbanned succesfully!**', color=ctx.author.color)
                await ctx.respond(embed=unban_embed)
                return
            except:
                await ctx.respond(f"**<:ceres_failure:951863495559872613> There was some issue in unbanning the member. Make sure to check that u gave correct id and Try Again. **")
        except commands.MissingPermissions:
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Ban members` permission to be able to use this command!**")

#add slowmode

    @slash_command(name="slowmode",description="🐢 applies the mentioned seconds as slowmode in current channel",guild_ids=[883180896038027336,903168731885240350])
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self,ctx,time:Option(int,"Seconds of the slowmode delay")):
        try:    
            if time == 0:
                await ctx.respond("**Please tell an integer above `0`**")
            elif time>21600:
                await ctx.respond("**You cannot set the slowmode more than 6hours**")
            else:
                await ctx.channel.edit(slowmode_delay = time)
                await ctx.respond(f'**Slowmode succsfully set to `{time}`**')
        except commands.MissingPermissions:
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Manage messages` permission to be able to use this command!**")


    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, member: Option(discord.Member, "Select the member to change role of", required=True), role: Option(discord.Role, "Select the role", required=True)):
        """Add or Remove a role from a User"""
        try:
            if ctx.user.id == ctx.guild.owner_id:
                if role not in member.roles:
                    await member.add_roles(role)
                    await ctx.respond(f"`{member}` was given role `{role.name}`.")
                else:
                    await member.remove_roles(role)
                    await ctx.respond(f"`{role.name}` was removd from - `{member}`.")
            elif ctx.user.top_role.position > role.position:
                if role not in member.roles:
                    await member.add_roles(role)
                    await ctx.respond(f"`{member}` was given role `{role.name}`.")
                else:
                    await member.remove_roles(role)
                    await ctx.respond(f"`{member}` was removed from the role `{role.name}`.")
            else:
                await ctx.respond(f"**<:ceres_failure:951863495559872613>  That role is higher than or same as your top-most role!**", ephemeral=True)
        except commands.MissingPermissions:
            await ctx.respond(f"**<:ceres_failure:951863495559872613>  You need `Manage Roles` permission to be able to use this command.**")
        except discord.Forbidden:
            await ctx.respond(f"**<:ceres_failure:951863495559872613>  I don\'t have enough permissions to manage that role.**")

#purge command

    @slash_command(name="purge",description="🗑️ delete the amount of messages mentioned",guild_ids=[883180896038027336,903168731885240350])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self,ctx, amount:int):
        try:
            if amount <= 200:
                await ctx.channel.purge(limit=amount+1)
                await ctx.respond(f'**<:ceres_succces:938669698621509652> Succesfully deleated {amount} messages!**',delete_after=10)
                
            else:
                await ctx.respond("<:ceres_failure:951863495559872613>  Please mention number smaller than 200")
        except commands.MissingPermissions:
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Mange messages` permission to be able to use this command!**")

#nuke command   

    @slash_command(name="nuke",description="☢️ Nukes the channel(makes a new one and deletes the curent)",guild_ids=[883180896038027336,903168731885240350])
    @commands.has_permissions(manage_channels=True)
    async def nuke(self,ctx):
        try:
            channel = ctx.channel
            positions = ctx.channel.position
            n = await channel.clone()
            await n.edit(position=positions)
            await channel.delete()
            await n.send(f'**Channel nuked by {ctx.author}**')
            await n.send("https://tenor.com/view/kozhi-nuclear-bomb-gif-18586883",delete_after=10)
        except commands.MissingPermissions:
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Manage channels` permission to be able to use this command!**")




def setup(bot):
    bot.add_cog(Mod(bot))