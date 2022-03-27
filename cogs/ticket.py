import discord
from discord.ext import commands
from discord.commands import Option,SlashCommandGroup
from utils.buttons import TicketPanelView,TicketResetView


async def cleanup(guild: discord.Guild):
    for channel in guild.channels:
        if channel.name.lower().startswith('ticket'):
            await channel.delete()

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("ticket cog loaded")

    ticket=SlashCommandGroup("ticket","All the ticket related commands",guild_ids=[883180896038027336])
    panel_=SlashCommandGroup("panel","All the panel related commands",guild_ids=[883180896038027336])
    
    @ticket.command()
    @commands.has_permissions(manage_channels=True)
    async def category(self, ctx: commands.Context, categoryid: Option(str,"Input the category id to set the ticket category",required=True)):
        """Sets a category for the ticket the tickets will only open in that category.Highly Recommended."""
        try:
            if categoryid is None:
                self.bot.dbcursor.execute(f'SELECT category FROM ticket WHERE guild_id=?', (ctx.guild.id,))
                dataCheck = self.bot.dbcursor.fetchone()
                if not dataCheck:
                    return await ctx.respond(embed=discord.Embed(description="**<:ceres_failure:951863495559872613> You have not assigned a category to tickets yet**", color=discord.Color.red()))
            
                self.bot.dbcursor.execute(f'SELECT * FROM ticket WHERE guild_id=?', (ctx.guild.id,))
                categoryFind = self.bot.dbcursor.fetchone()
                cat = categoryFind[2]
                return await ctx.respond(embed=discord.Embed(description=f"**The category_id set for this server is {cat}**", color=discord.Color.green()))

            self.bot.dbcursor.execute(f'SELECT category FROM ticket WHERE guild_id=?', (ctx.guild.id,))
            data = self.bot.dbcursor.fetchone()
            if not data:
                self.bot.dbcursor.execute(f'SELECT * FROM ticket WHERE guild_id=?', (ctx.guild.id,))
                dataCheck2 = self.bot.dbcursor.fetchone()
                if not dataCheck2[0]:
                    self.bot.dbcursor.execute(f'INSERT INTO ticket (guild_id, category) VALUES(?,?)', (ctx.guild.id, categoryid))
                else:
                    self.bot.dbcursor.execute(f'INSERT INTO ticket (category) VALUES(?) WHERE guild_id=?', (categoryid, ctx.guild.id))
            if data:
                self.bot.dbcursor.execute(f'UPDATE ticket SET category = ? WHERE guild_id=?', (categoryid, ctx.guild.id))
            self.bot.db.commit()
            category = discord.utils.get(ctx.guild.categories, id=categoryid)
            embed = discord.Embed(description=f"**<:ceres_succces:938669698621509652> Successfully set `{categoryid}` as the ticket category!\n\nIf you want to keep ticket view permissions, make sure to change the category permissions.**", color=discord.Color.green())
            await ctx.respond(embed=embed)
        except commands.MissingPermissions:
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Manage channels` permission to be able to use this command!**")

    @panel_.command()
    @commands.has_permissions(manage_channels=True)
    async def create(self, ctx: commands.Context, channel: Option(discord.TextChannel,"The channel to create the panel in.",required=True), name : Option(str,"Panel name.",required=True)):
        """Creates a panel in a channel through which users can interact and open tickets"""
        try:
            if channel == ctx.channel:
                panel = discord.Embed(
                    title=name,
                    description="To create a ticket react with 📩",
                    color=discord.Color.green(),
                )
                panel.set_footer(text=f"{self.bot.user.name} - Ticket Panel", icon_url=self.bot.user.avatar.url)

                message = await channel.send(embed=panel, view=TicketPanelView(self.bot))
                try:
                    await ctx.author.send(embed=discord.Embed(description=f"**Panel id** of the panel you just created in <#{channel.id}>: `{message.id}` with the name :`{name}`", color=discord.Color.green()))
                except discord.Forbidden:
                    print("Couldn't DM that user!")
                embed2 = discord.Embed(description=f"**<:ceres_succces:938669698621509652> Successfully posted the panel in {channel.mention}\n\nPanel ID: `{message.id}`**", color=discord.Color.green())
                await ctx.respond(embed=embed2)
            if channel != ctx.channel:
                panel1 = discord.Embed(
                    title=name,
                    description="To create a ticket react with 📩",
                    color=discord.Color.green(),
                )
                panel1.set_footer(text=f"{self.bot.user.name} - Ticket Panel", icon_url=self.bot.user.avatar.url)

                message = await channel.send(embed=panel1, view=TicketPanelView(self.bot))
                embed2 = discord.Embed(description=f"**<:ceres_succces:938669698621509652> Successfully posted the panel in {channel.mention}\n\nPanel ID: `{message.id}`**", color=discord.Color.green())
                await ctx.respond(embed=embed2)
        except commands.MissingPermissions:
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Manage channels` permission to be able to use this command!**")

    @ticket.command()
    async def cleanup(self, ctx: commands.Context):
        """Delets all the tickets"""
        if ctx.author.id==ctx.guild.owner.id:
            if ctx.me.guild_permissions.manage_channels == True:
                try:
                    em=discord.Embed(description="<a:loading:952075303608545290> Deleating all the tickets",color=discord.Color.embed_background())
                    await ctx.respond(embed=em)
                    await cleanup(ctx.guild)
                    await ctx.edit(content="<:ceres_succces:938669698621509652>** Cleaned up all tickets!**",embed=None)
                except discord.Forbidden:
                    await ctx.respond("**<:ceres_failure:951863495559872613> Something went wrong!**")
            else:
                await ctx.respond("**<:ceres_failure:951863495559872613> I am missing some permissions!**")
        else:
            await ctx.respond("**<:ceres_failure:951863495559872613> This command can only be used by the guild owner!**")

    @ticket.command()
    @commands.has_permissions(manage_channels=True)
    async def role(self, ctx: commands.Context, switch: Option(str,"adds or removes a role from the tickets",choices=["add","remove"],required=True), role: Option(discord.Role,"The role to add or remove",required=True)):
        """Adds a role or removes the role from a server"""
        try:    
            if not ctx.channel.name.lower().startswith('ticket'):
                await ctx.send(embed=discord.Embed(description="**<:ceres_failure:951863495559872613> This command can only be used in a ticket!**", color=discord.Color.red()))

            if switch.lower() == "add":
                channel: discord.Channel = ctx.channel
                perms = channel.overwrites_for(role)
                perms.view_channel = True
                perms.send_messages = True
                perms.read_message_history = True
                await channel.set_permissions(role, overwrite=perms)
                embed = discord.Embed(description=f"**<:ceres_succces:938669698621509652> Successfully added {role.mention} in the ticket!**", color=discord.Color.green())
                await ctx.respond(embed=embed)
            
            if switch.lower() == "remove":
                channel: discord.Channel = ctx.channel
                perms = channel.overwrites_for(role)
                perms.view_channel = False
                perms.send_messages = False
                perms.read_message_history = False
                await channel.set_permissions(role, overwrite=perms)
                embed = discord.Embed(description=f"**<:ceres_succces:938669698621509652> Successfully removed {role.mention} from the ticket!**", color=discord.Color.green())
                await ctx.respond(embed=embed)
        except discord.MissingPermissions:
            await ctx.respond("**<:ceres_failure:951863495559872613> You need `Managet channels` Permission to be able to use this command!**")

    @panel_.command()
    @commands.has_permissions(manage_channels=True)
    async def delete(self, ctx: commands.Context, channel: Option(discord.TextChannel,"The text channel in which the panel is present"), panel_id: Option(str,"The panel id of the panel to  delete",required=True)):
        """Deletes a previously built panel in the server using panel id."""
        await ctx.defer()
        try:
            message = await channel.fetch_message(panel_id)
            try:
                await message.delete()
                embed = discord.Embed(description="**<:ceres_succces:938669698621509652> Successfully deleted the panel!**", color=discord.Color.green())
                await ctx.respond(embed=embed)
            except discord.Forbidden:
                embed = discord.Embed(description="**<:ceres_failure:951863495559872613> I couldn't do that!**", color=discord.Color.green())
                await ctx.respond(embed=embed)
            except discord.NotFound:
                embed = discord.Embed(description=f"**<:ceres_failure:951863495559872613> I couldn't find a panel with id `{panel_id}`! Please try again after checking the id!**")
                await ctx.respond(embed=embed)
        except discord.MissingPermissions:
            await ctx.respond("**<:ceres_failure:951863495559872613> You need `Manage channles` permissions to be able to use this command!**")


    @ticket.command()
    @commands.has_permissions(manage_channels=True)
    async def reset(self, ctx: commands.Context):
        """Resets the ticket count set of the server"""
        try:
            embed = discord.Embed(description=f"Are you sure you want to reset the **Ticket Count**?\n------------------------------------------------\nRespond Within **15** seconds!", color=discord.Color.orange())
            await ctx.respond(embed=embed)
            message =await ctx.interaction.original_message()
            await message.edit(embed=embed, view=TicketResetView(ctx, message, self.bot))
        except discord.MissingPermissions:
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Manage channels` permission to be able to use this command!**") 

    @ticket.command()
    @commands.has_permissions(manage_channels=True)
    async def delete(self,ctx):
        """deletes the ticket. can only be used in a ticket!"""
        try:
            if ctx.channel.name.lower().startswith('ticket'):
                await ctx.channel.delete()
                try:
                    await ctx.author.send("**<:ceres_succces:938669698621509652> Successfully deleated the ticket!**")
                except:
                    pass
            else:
                await ctx.respond("**<:ceres_failure:951863495559872613> This command can only be used in a ticket!**")
        except discord.MissingPermissions:
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Manage channels` permission to be able to use this command!**")      
def setup(bot):
    bot.add_cog(Ticket(bot))