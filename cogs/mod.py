import discord                                     #-
from discord.ext import commands                   #|
from discord.commands import slash_command,Option  #|
from discord.ui import Button,View                 #|
from discord.ext import commands                   #| IMPORTS
from discord.errors import Forbidden               #|
from datetime import datetime                      #|
import datetime                                    #|
import humanfriendly                               #-


class Mod(commands.Cog):#making the class
    def __init__(self, bot):#setup
        self.bot = bot
    

#timout cmd

    @slash_command(name="timeout",description="🔇 timeouts the specified member")#command decorator
    @commands.has_permissions(moderate_members=True)#the person must have `Moderate members` permission to use this command so just making that sure
    async def timeout(self,ctx,member: Option(discord.Member, "Select the user", required=True), time: Option(str, "Mention the mute duration(s: seconds, m: minutes, h: hours, d: days)", required=True), reason: Option(str, "Reason for mute", required=False, default="Reason Not Mentioned")):
        try:    
            try:
                timeConvert = humanfriendly.parse_timespan(time) #converting time intputed by the user.
            except:#responding when the time inputted is not valid
                await ctx.respond(f"**{time} is not a valid time Please try again!**")
            oreason = f"{ctx.author.name} timedout {member.name} for - {reason}"#i have this so that people can check who has muted the person even in the audit logs
            confirm_time = Button(label="Confirm",style=discord.ButtonStyle.danger)#defining confirm button
            cancel_time=Button(label="Cancel",style=discord.ButtonStyle.green)#defining cancel button
            async def confirm_button_callback(interaction):#making an interaction callback function for confirm button
                try:
                    if interaction.user.id == ctx.author.id:#making sure that the person who clicked is the author only
                        await member.timeout(discord.utils.utcnow()+datetime.timedelta(seconds=timeConvert), reason=oreason)#finally timeouting the member
                        cmute_embed = discord.Embed(description=f"**<:ceres_succces:938669698621509652>  `{member.name}` was succesfully timed-out  for `{time}`!**", color=0x2ECC71)
                        await ctx.edit(embed=cmute_embed,view=None)#responding as a confirmation message
                    else:#triggered when the user who clicked is not the author
                        await interaction.send_message(f"This is not for you!",ephemeral=True)
                except:#responding when something goes wrong
                    await ctx.edit(f"**Something went wrong!**",view=None)
            async def cancel_time_call(interaction):#making the interaction callback for cancel button
                if interaction.user.id == ctx.author.id:#this verifies that the person cicking is the author only
                    ca=discord.Embed(title="Canceled the process",description=f"the timeout of `{member.name}` was canceled by `{ctx.author}`!", color=discord.Color.embed_background())
                    await ctx.edit(embed=ca,view=None)#responding as a confirmation
                else:#responding when the person to click is not the author
                    await interaction.send_message(f"This is not for you!",ephemeral=True)
            confirm_time.callback=confirm_button_callback#telling that the functions are the callbacks for the oflling buttons
            cancel_time.callback=cancel_time_call#same as above
            view=View()#defining the view variable
            view.add_item(cancel_time)#adding cancel button
            view.add_item(confirm_time)#adding confirm button
            is_admin = member.guild_permissions.administrator#checking whether the member is an admin
            if member.id == ctx.guild.owner_id:#checking whether the member is the guild owner
                await ctx.respond("**<:ceres_failure:951863495559872613> Cannot timeout the guild owner sorry!**",ephemeral=True)
            
            elif is_admin==True:#making sure that the member is not an admin
                await ctx.respond("**That member is an admin/moderator you cannot timeout them!**",ephemeral=True)
                return

            elif member == ctx.author:#checking if the member is the author himself so that they cannot mute themselves
                await ctx.respond("**<:ceres_failure:951863495559872613> You cannot timeout yourself!**",ephemeral=True)
                return
            elif ctx.guild.me.top_role.position < member.top_role.position:#checking if the member's role is higher than the bots role if yes then to prevent errors we will return
                await ctx.respond("**<:ceres_failure:951863495559872613> That member has a higher role than mine please drag my role above them!**",ephemeral=True)
                return
            elif ctx.author.top_role.position < member.top_role.position:#checking if the author's role position is lower than the member's role position if yes then no mute will be given
                await ctx.respond(f"**<:ceres_failure:951863495559872613> Your Role position is lower than the role of `{member.name}` so you cannot do that!**",ephemeral=True)
            else:#finally after all the checks we are responding with the confirmation embed
                em=discord.Embed(title="Are you sure?",description=f"**Please confirm the timeout of `{member.name}` for reason - `{reason}`**",color=0x2ECC71)
                await ctx.respond(view=view,embed=em)#sending the embed
        except commands.MissingPermissions:#responding when the author lacks permissions.
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Moderate members` permission to be able to use this command!**")

#unmute cmd

    @slash_command(name="unmute",description=" 😁 Unmutes a specified user.",guild_ids=[903168731885240350,883180896038027336])
    @commands.has_permissions(manage_messages=True)
    async def unmute(self,ctx, member: Option(discord.Member,"Select the user to unmute!",required=True),reason : Option(str,"Write the reason the kicking the user.")):
        try:
            try:
                await member.timeout(until=None,reason=reason)#removing the timeout from the member
                embed = discord.Embed(description=f"**<:ceres_succces:938669698621509652> succesfully unmuted-{member.mention}!**",color=ctx.author.color)
                await ctx.respond(embed=embed)#responding
            except:#responding when the person mentioned is not muted
                await ctx.respond(f"**{member.name} is not muted**")
        except commands.MissingPermissions:#responding when the author is missing permissions to use this command
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Manage member` permission to be able to use this command!**")

#kick cmd

    @slash_command(name="kick",description="🦶 kicks a user from the server")
    @commands.has_permissions(kick_members=True)#mentioning the required permissions to use this command
    async def kick(self,ctx, user : Option(discord.Member,"Select the user to kick!",required=True), *, reason : Option(str,"Write the reason the kicking the user.")):#making the function
        """Kicks a user from the server."""#small description
        try:
            if reason==None:
                reason="No reason provided!"#we will have this as the reason when the user doesnt want to give a reason
            oreason=f"{user.name} banned by {ctx.author.name} for - {reason}"#this reason will apper in the audit log
            if ctx.guild.me.top_role.position < user.top_role.position:#checking if the member has a higher role than the bot if yes then the bot cannot kick the member
                return await ctx.respond(f"<:ceres_failure:951863495559872613> {user.name} has a higher role than mine i cannot kick them!")
            elif user.id == ctx.guild.owner_id:#checking if the user is the guild owner
                return await ctx.respond(f"**<:ceres_failure:951863495559872613> kick the server owner?**")
            elif ctx.author == user:#making sure that the author cannot kick themselves
                await ctx.respond("**<:ceres_failure:951863495559872613> You cannot kick yourself.**")
                return
            elif ctx.author.top_role <= user.top_role:#the author must have a higher role than the member to kick them.
                await ctx.respond(f"**<:ceres_failure:951863495559872613> You are not cool enough to kick that person.**")
                return
            else:
                try:    
                    await ctx.guild.kick(user,reason= oreason)#finally after the checks we will be kicking the member
                    kick_embed = discord.Embed(description=f'**<:ceres_succces:938669698621509652> `{user}` was successfully kicked!**', color=ctx.author.color)
                    await ctx.respond(embed=kick_embed)#responding as a cofirmation message
                except Forbidden:#responding when the bot doesnt have permissions to kick the user
                    await ctx.respond(f"**I don't have enough permission to kick this member!**")
        except commands.MissingPermissions:#responding when the bot doesn't have permissions to use this command
                    await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Kick members` permission to be able to use this command!**")
#ban cmd

    @slash_command(name="ban",description="🔨 Bans a user from the server")
    @commands.has_permissions(ban_members=True)#mentioning the required permissions to use this command
    async def ban(self,ctx, user : Option(discord.Member,"Select the user to ban!",required=True), *, reason : Option(str,"Write the reason for banning the user.")):#making the function
        try:    
            if reason==None:
                reason="No reason provided!"#this wll be a reason when the author doesnt want to provide a reason
            oreason=f"{user.name} banned by {ctx.author.name} for - {reason}"#this reason will appear in the audit log to tell who has banned the user
            guild = ctx.guild#just making the code shorter by defining guild
            is_admin = user.guild_permissions.administrator#this variable will be used in the `user is admin check`
            if ctx.guild.me.top_role.position < user.top_role.position:#checking if the member's role position is higher than the bot if yes then we cannot ban them(just to prevent errors)
                return await ctx.respond(f"<:ceres_failure:951863495559872613> {user.name} has a higher role than mine i cannot ban them!")
            if ctx.author.top_role.position < user.top_role.position:#checking if the author's role position is higher than the member so that people can be ban proved by having a certain role
                await ctx.respond("Your role needs to be higher than the person you are trying to ban.")
            elif user == ctx.guild.owner:#checking if the member is server owner
                return await ctx.respond(f'**<:ceres_failure:951863495559872613> ban the server owner?**')
            elif ctx.author == user:#making sure that the author doesnt ban themselves
                await ctx.respond("**<:ceres_failure:951863495559872613> You cannot ban yourself xD.**")
                return
            elif is_admin==True:#making sure the member is not an admin
                await ctx.respond(f"**<:ceres_failure:951863495559872613> That user is a moderator/admin I cannot ban them**")
                return
            else:
                try:    
                    await guild.ban(user,reason = oreason)#finally after the checks banning the user
                    ban_embed = discord.Embed(description=f'**<:ceres_succces:938669698621509652> ``{user}`` was successfully banned!**', color=ctx.author.color)
                    await ctx.respond(embed=ban_embed)#responding as a cofirmation
                except Forbidden:#responding when the bot is not allowed to ban the person(to hanle errors)
                    await ctx.respond(f"**<:ceres_failure:951863495559872613> I don't have enough permission to ban this member!**")
        except commands.MissingPermissions:#responding when the author lacks permissions to use this command.
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Ban members` permission to be able to use this command!**")

#unban cmd

    @slash_command(name="unban",description="✈️ unbans a banned member")
    @commands.has_permissions(ban_members=True)
    async def unban(self,ctx,member:Option(str,"Write the user name with discriminator to unban or the user's id",required=True)):#making the function
        try:
            try:
                banned_users=await ctx.guild.bans() #getting the user from the guild ban list
                member_name,member_discriminator=member.split('#') #spilling the name with the discriminator
                for ban_entry in banned_users: #looping through the ban entry. 
                    user=ban_entry.user #getting the user.
                    if(user.name,user.discriminator) == (member_name,member_discriminator):
                        await ctx.guild.unban(user) #unbanning the user.
                        unban_embed = discord.Embed(description=f'**<:ceres_succces:938669698621509652> ``{user}`` was unbanned succesfully!**', color=ctx.author.color)
                await ctx.respond(embed=unban_embed) #telling the author that the user is unbanned.
                return
            except: #error handling
                await ctx.respond(f"**<:ceres_failure:951863495559872613> There was some issue in unbanning the member. Make sure to check that u gave correct id and Try Again. **")
        except commands.MissingPermissions: #responding when a user doesnt have permission to use this command
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Ban members` permission to be able to use this command!**")

#slowmode

    @slash_command(name="slowmode",description="🐢 applies the mentioned seconds as slowmode in current channel")
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self,ctx,time:Option(int,"Seconds of the slowmode delay")):#making the function
        try:    
            if time == 0: #checking if the time is 0
                await ctx.respond("**Please tell an integer above `0`**")
            elif time>21600: #checking if the time is greater than 6 hours
                await ctx.respond("**You cannot set the slowmode more than 6hours**")
            else:
                await ctx.channel.edit(slowmode_delay = time) #finally editing the channel
                await ctx.respond(f'**Slowmode succsfully set to `{time}`**') #responding with the succes message
        except commands.MissingPermissions: #responding when the user doesnt have permissions to use this command.
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Manage messages` permission to be able to use this command!**")

#role command

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, member: Option(discord.Member, "Select the member to change role of", required=True), role: Option(discord.Role, "Select the role", required=True)):#making the function
        """Add or Remove a role from a User"""#small description
        try:
            if ctx.user.id == ctx.guild.owner_id: #cheacking if the user is the guild owner.(random check i dont think i needed this) 
                if role not in member.roles: #cheacking if the role is alredy there
                    await member.add_roles(role) #adding when the above statement^ is true
                    await ctx.respond(f"`{member}` was given role `{role.name}`.")
                else:
                    await member.remove_roles(role) #removing the role is the above if statement^ is false
                    await ctx.respond(f"`{role.name}` was removd from - `{member}`.")
            elif ctx.user.top_role.position > role.position: #cheacking if the role position is higher than that o the author to prevent misuse.
                if role not in member.roles:
                    await member.add_roles(role)
                    await ctx.respond(f"`{member}` was given role `{role.name}`.")
                else:
                    await member.remove_roles(role)
                    await ctx.respond(f"`{member}` was removed from the role `{role.name}`.")
            else: #responding when the role is higher than the author
                await ctx.respond(f"**<:ceres_failure:951863495559872613>  That role is higher than or same as your top-most role!**", ephemeral=True)
        except commands.MissingPermissions: #responding when the author lacks permissions.
            await ctx.respond(f"**<:ceres_failure:951863495559872613>  You need `Manage Roles` permission to be able to use this command.**")
        except discord.Forbidden: #responding when the bot lacks permissions.
            await ctx.respond(f"**<:ceres_failure:951863495559872613>  I don\'t have enough permissions to manage that role.**")

#purge command

    @slash_command(name="purge",description="🗑️ delete the amount of messages mentioned")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)#mentioning the required permissions to use this command
    async def purge(self,ctx, amount:int): #the function
        try:
            if amount <= 200: #I have a limit of 200 its up to you for the limit
                await ctx.channel.purge(limit=amount+1) #finally deleting the messages
                await ctx.respond(f'**<:ceres_succces:938669698621509652> Succesfully deleated {amount} messages!**',delete_after=10)#responding
                
            else:#this will be triggered when the limit is greater than 200
                await ctx.respond("<:ceres_failure:951863495559872613>  Please mention number smaller than 200")
        except commands.MissingPermissions:# responding when user does not have permissions to use the command.
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Mange messages` permission to be able to use this command!**")

#nuke command   

    @slash_command(name="nuke",description="☢️ Nukes the channel(makes a new one and deletes the curent)")
    @commands.has_permissions(manage_channels=True)#mentioning the required permissions to use this command
    async def nuke(self,ctx):#making the function
        try:
            channel = ctx.channel#defining the channel
            positions = ctx.channel.position#getting the position of the channel
            n = await channel.clone()#cloning the channel 
            await n.edit(position=positions)#shifting the channel as the previous position
            await channel.delete()#deleting the previous channel
            await n.send(f'**Channel nuked by {ctx.author}**')#responding
            await n.send("https://tenor.com/view/kozhi-nuclear-bomb-gif-18586883",delete_after=10)#just a fancy gif to send after responding
        except commands.MissingPermissions:#responding when user does not have permissions to use this command
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Manage channels` permission to be able to use this command!**")




def setup(bot):#cog setup
    bot.add_cog(Mod(bot))#adding the cog
    print("Mod cog is Loaded\n------")#printing when the cog gets loaded.