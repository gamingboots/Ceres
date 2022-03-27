import re
import discord
from discord.ext import commands
from discord.commands import Option,SlashCommandGroup,slash_command
from datetime import datetime
import collections
from io import BytesIO
import asyncio
import utils.buttons as buttons
import random
import config
import aiohttp
class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print("utility cog loaded")

#avatar cmd

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def avatar(self, ctx, user: Option(discord.Member, "Choose a Member", required=False)):
        """Gets the avatar of a User"""
        if not user:
            user = ctx.author
        embed = discord.Embed(
            title=f"`{user.name}`'s avatar", color=ctx.author.color)
        embed.description = f'[PNG]({user.display_avatar.with_format("png")}) | [JPEG]({user.display_avatar.with_format("jpeg")}) | [WEBP]({user.display_avatar.with_format("webp")})'
        embed.set_image(url=str(user.display_avatar.with_static_format("png")))
        embed.set_footer(
            text=f"Requested by {ctx.author}",  icon_url=ctx.author.avatar.url)
        if user.avatar.is_animated():
            embed.description += f' | [GIF]({user.display_avatar.with_static_format("gif")})'
            embed.set_image(url=str(user.display_avatar.with_static_format("gif")))

        await ctx.respond(embed=embed)

#nick command
        
    @slash_command(name="nick",description="Change the nick of the mentioned user",guild_ids=[883180896038027336,903168731885240350])
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self,ctx, member: Option(discord.Member,"Select the member",required=True), *, nick:Option(str,"The name",required=True)):
        try:
            if ctx.guild.me.top_role < member.top_role:
                return await ctx.respond(f"**<:ceres_failure:951863495559872613> This member has a greater role than me so i cant change their name!**")
            if ctx.author.top_role <= member.top_role:
                return await ctx.respond(f"**<:ceres_failure:951863495559872613> You can't change nick of that person**")
            else:
                await member.edit(nick=nick)
                await ctx.respond(f'**<:ceres_succces:938669698621509652> Succesfully changed the nick of``{member}`` to ``{nick}``**')
        
        except commands.MissingPermissions:
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Manage Nicknames` permission to be able to use this command!**")

#lock channel

    @slash_command(name="lock",description="locks the current channel",guild_ids=[883180896038027336,903168731885240350])
    @commands.has_permissions(manage_channels=True)
    async def lock(self,ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        try:
            await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.respond("**<:ceres_succces:938669698621509652> Channel locked down for the server members.**")
        except commands.MissingPermissions:
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Manage Channels` permission to be able to use this command.**")
        except discord.Forbidden:
            await ctx.respond(f"**<:ceres_failure:951863495559872613> I don\'t have enough permissions to edit this channel\'s settings.**")
        
#unlock channel

    @slash_command(name="unlock",description="unlocks the current channel",guild_ids=[883180896038027336,903168731885240350])
    @commands.has_permissions(manage_channels=True)
    async def unlock(self,ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        try:
            await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.respond("**🔓 Channel unlocked.**")
        except commands.MissingPermissions:
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Manage Channels` permission to be able to use this command.**")
        except discord.Forbidden:
            await ctx.respond(f"**<:ceres_failure:951863495559872613> I don\'t have enough permissions to edit this channel\'s settings.**")

#userinfo cmd

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def userinfo(self, ctx, member: Option(discord.Member, "Choose The Member", required=False)):
        """Gets Information about a User"""
        await ctx.defer()
        badge_emojis = {
            "bug_hunter": str(self.bot.get_emoji(947043753196150804)),
            "bug_hunter_level_2": str(self.bot.get_emoji(947043752936099860)),
            "discord_certified_moderator": str(self.bot.get_emoji(947043753078706197)),
            "early_supporter": str(self.bot.get_emoji(947042439649189948)),
            "verified_bot_developer": str(self.bot.get_emoji(947043753292615690)),
            "hypesquad": str(self.bot.get_emoji(947044204343865394)),
            "hypesquad_balance": str(self.bot.get_emoji(947043753175167006)),
            "hypesquad_bravery": str(self.bot.get_emoji(947044641163853824)),
            "hypesquad_brilliance": str(self.bot.get_emoji(947044669576069151)),
            "partner": str(self.bot.get_emoji(947043753422651422)),
            "staff": str(self.bot.get_emoji(947043752717983775))
        }

        def get_badges(member: discord.Member):
            badges = []
            for badge, value in iter(member.public_flags):
                if value and badge in badge_emojis.keys():
                    badges.append(badge_emojis[badge])
            return badges
        if member == None:
            member = ctx.author
        uroles = []

        for role in member.roles[1:]:
            if role.is_default():
                continue
            uroles.append(role.mention)
            uroles.reverse()
        if member.status == discord.Status.online:
            status = '<:online:946666678480142378>'
        elif member.status == discord.Status.idle:
            status = '<:idle:946666678601805854>'
        elif member.status == discord.Status.do_not_disturb:
            status = '<:dnd:946666678463389697>'
        elif member.status == discord.Status.offline:
            status = '<:offline:946666678727639050>'
        if member.activity == None:
            activity = "None"
        else:
            if member.activities[-1].type == discord.ActivityType.custom:
                activity = "None"
            elif member.activities[-1].type == discord.ActivityType.watching:
                activity = f"Watching {member.activities[-1].name}"
            elif member.activities[-1].type == discord.ActivityType.listening:
                activity = f"Listening to {member.activities[-1].name}"
            elif member.activities[-1].type == discord.ActivityType.playing:
                activity = f"Playing {member.activities[-1].name}"
            elif member.activities[-1].type == discord.ActivityType.streaming:
                activity = f"Streaming {member.activities[-1].name} on {member.activities[-1].platform}"
            else:
                try:
                    activity = member.activities[-1].name
                except:
                    activity = member.activities[-1]
        embed = discord.Embed(color=ctx.author.color, type="rich",description=
        f"**Name :** {member}\n**ID :** {member.id}\n**Avatar :** [PNG]({member.display_avatar.with_format('png')}) [JPEG]({member.display_avatar.with_format('jpeg')})\n**Created At :** **{discord.utils.format_dt(member.created_at)}**\n**Server Joined :** **{discord.utils.format_dt(member.joined_at)}**\n**Highest Role : **{member.top_role.mention}\n**Status : ** {status}\n**Badges : **{'  '.join(get_badges(member))if len(get_badges(member)) > 0 else '`-`'}\n**Activity : ** ```{activity}```"
        )
        if member.premium_since == None:
            pass
        else:
            embed.add_field(name="__Extra__",value=f"**Boosting since :** {discord.utils.format_dt(member.premium_since)}\n**Voice channel :** {member.voice.channel.mention}",inline=False)
        try:
            embed.set_thumbnail(url=f"{member.avatar.url}")
        except:
            pass
        try:
            embed.set_image(url=member.banner.url)
        except:
            pass
        embed.set_author(name=f"{member}",
                        icon_url=f'{member.avatar.url}')
        embed.set_footer(
            text=f"Requested by {ctx.author.name}",  icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)


        
#serverinfo cmd

    @slash_command(name="serverinfo",description="tells the information about the server",guild_ids=[883180896038027336,903168731885240350,939019819871772673])
    async def serverinfo(self,ctx):
        statuses = collections.Counter(
            [member.status for member in ctx.guild.members])

        online = statuses[discord.Status.online]
        idle = statuses[discord.Status.idle]
        dnd = statuses[discord.Status.dnd]
        offline = statuses[discord.Status.offline]
        info_embed= discord.Embed(color=ctx.author.color,description=
        f"**Owner :** {ctx.guild.owner.mention}\n**Server ID :** {ctx.guild.id}\n**Members :** {ctx.guild.member_count}\n**Created At : ** **{discord.utils.format_dt(ctx.guild.created_at)}**\n**Channels : **<:Textchannel:947499643401543751> {len(ctx.guild.text_channels)} <:Voicechannel:947499643342827621> {len(ctx.guild.voice_channels)}\n**Verification Level :** {str(ctx.guild.verification_level)}\n**Emojis :** {len(ctx.guild.emojis)}\n**Boost status :** <:Boost:947508528891965452> {ctx.guild.premium_tier} ({ctx.guild.premium_subscription_count})\n**Roles :** {len(ctx.guild.roles)}\n**Activity :** <:online:946666678480142378> {online} <:idle:946666678601805854> {idle} <:dnd:946666678463389697> {dnd} <:offline:946666678727639050> {offline}")
        info_embed.set_author(name=ctx.guild.name,icon_url=ctx.guild.icon.url)
        info_embed.set_footer(icon_url=f"{ctx.author.avatar.url}",text=f"Requested by - {ctx.author.name}")
        try:
            info_embed.set_thumbnail(url=ctx.guild.icon.url)
        except:
            pass
        try:
            info_embed.set_image(url=ctx.guild.banner.url)
        except:
            pass
        await ctx.respond(embed=info_embed)

#member count cmd

    @slash_command(name="membercount",description="displays the number of cool people in the server",guild_ids=[883180896038027336,903168731885240350])
    async def membercount(self,ctx):
        embed=discord.Embed(title="Number of cool people in this world" ,description=f"{ctx.guild.member_count}",color=ctx.author.color,timestamp=datetime.utcnow())
        await ctx.respond(embed=embed)

#msgcount cmd

    @slash_command(name="msgcount",description="counts the number of messages in the specified channel",guil_ids=[883180896038027336,903168731885240350])
    async def msgcount(self,ctx, channel: Option(discord.TextChannel,"Choose the channel to count messages from",required=True)):
        await ctx.defer()
        if not channel:
            channel=ctx.channel
        messages = await channel.history(limit=None).flatten()
        count = len(messages)
        embed = discord.Embed(title="Total Messages",colour=random.choice(config.color_list),description=f"There were {count} messages in {channel.mention}")
        await ctx.respond(embed=embed)

#embed cmd

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def embed(self,ctx,*,msg=Option(str,"Type the message for the embed",required=True)):
        if not msg:
            await ctx.send('Enter message withing 30s')

            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel

            try:
                mes=await self.bot.wait_for('message',check=check,timeout=30.0)
            except asyncio.TimeoutError:
                await ctx.send('Timeout! Please be quicker next time.')
            else:
                msg=mes.content

        em=discord.Embed(
            description=f'{msg}',
            timestamp=datetime.utcnow(),
            color=discord.Color.random()).set_author(
            name=f'{ctx.author.name}#{ctx.author.discriminator}',
            icon_url=f'{ctx.author.avatar.url}')

        await ctx.respond(embed=em)

#support command

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def support(self,ctx):
        """sends the invite to my support serve"""
        em=discord.Embed(title="Support server",description="**you can get any support related me on the server join**\n **it by clicking on the button below!**",color=discord.Colour.random())
        em.set_thumbnail(url=config.icon)
        await ctx.respond(embed=em,view=buttons.SupportButton())

#emoji commnds group(all the emoji commands will be under this group so it makes it better to look at!)

    emoji_=SlashCommandGroup("emoji","All the emoji related commands",guild_ids=[883180896038027336])

#and the emoji commands were planned to be in the utility group only but later it was decided to
#that they should also have a different group because of the count of commands!

#emoji rename

    @emoji_.command(guild_ids=[883180896038027336,903168731885240350])
    @commands.has_permissions(manage_emojis_and_stickers=True)
    async def rename(self,ctx,emoji:Option(discord.Emoji,"Select the emoji to edit",required=True),name:Option(str,"The new name of the emoji",required=True)):
        """rename an emoji"""
        try:
            try:
                old_name = emoji.name
                await emoji.edit(name=name)
                embed = discord.Embed(
                    color=discord.Colour.embed_background(),
                    description=f"__Successfully Updated Emoji:__\n**{old_name}** -> **{emoji.name}**",
                )
                await ctx.respond(embed=embed)
            except:
                await ctx.respond("**<:ceres_failure:951863495559872613> Something went wrong while completing this request please check the emoji you provided!**")
        except discord.MissingPermissions:
            await ctx.respond("**<:ceres_failure:951863495559872613> You need `Manage emoji and stickers` permissions to be able to use this command**")          

#emoji enlarge

    @emoji_.command(guild_ids=[883180896038027336,903168731885240350])
    async def enlarge(self,ctx,emoji:Option(discord.Emoji,"The emoji to enlarge",required=True)):
        """enlarges and sends the emoji"""
        try:
            embed = discord.Embed(
                color=discord.Color.embed_background(), description=f"[Open In Browser]({emoji.url})"
            )
            embed.set_image(url=emoji.url)
            await ctx.respond(embed=embed)
        except:
            await ctx.respond("**<:ceres_failure:951863495559872613> Something went wrong please check the emoji or report in the support sever!**",view=buttons.SupportButton())

#emoji remove

    @emoji_.command()
    @commands.has_permissions(manage_emojis_and_stickers=True)
    async def remove(self,ctx,emojis: Option(discord.Emoji,"The emojis to delete",required=True)):
        """deleats the mentioned emojis"""
        try:
            try:
                for emoji in emojis:
                    await emoji.delete()
                embed = discord.Embed(
                    color=discord.Color.embed_background(), description="Removed Selected Emojis."
                )
                await ctx.send(embed=embed)
            except:
                await ctx.respond(embed=discord.Embed(description="**<:ceres_failure:951863495559872613> It looks like there was something wrong while deleting the selected emojis**\n**You can check if the emojis were valid or if you think it is an error in the bot you can inform in our support server**",color=discord.Color.embed_background()),view=buttons.SupportButton())
        except discord.MissingPermissions:
            await ctx.respond("**<:ceres_failure:951863495559872613> You need `Manage emoji and stickers` permission to be able to use this command!**")
#emojify cmd

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def emojify(self,ctx,*,text: Option(str,"The text to turn into emojis")):
        await ctx.defer()
        emojis=[]
        for s in text.lower():
            if s.isdecimal():
                num2emo={'0':'zero'
                        ,'1':'one',
                         '2':'two',
                         '3':'three',
                         '4':'four',
                         '5':'five',
                         '6':'six',
                         '7':'seven',
                         '8':'eight',
                         '9':'nine'
                        }
                emojis.append(num2emo.get(s))
            elif s.isalpha():
                emojis.append(f':regional_indicator_{s}:')
            else:
                emojis.append(s)
        await ctx.respond(''.join(emojis))

    @emoji_.command()
    async def stats(self,ctx):
        """returns the stats of the guild emojis"""
        emote_limit = ctx.guild.emoji_limit
        static_emotes = animated_emotes = total_emotes = 0
        for emote in ctx.guild.emojis:
            if emote.animated:
                animated_emotes += 1
            else:
                static_emotes += 1
            total_emotes += 1
        percent_static = round((static_emotes / emote_limit) * 100, 2)
        percent_animated = round((animated_emotes / emote_limit) * 100, 2)
        static_left = emote_limit - static_emotes
        animated_left = emote_limit - animated_emotes
        await ctx.respond(
			f'Static emotes: **{static_emotes} / {emote_limit}** ({static_left} left, {percent_static}% full)\n'
			f'Animated emotes: **{animated_emotes} / {emote_limit}** ({animated_left} left, {percent_animated}% full)\n'
			f'Total: **{total_emotes} / {emote_limit * 2}**')

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def github(self,ctx,user: Option(str,"the user to search on github",required=True)):
        """search a user on github!"""
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://api.github.com/users/{user}") as r:
                    data = await r.json()
                    em=discord.Embed(description=f"**Type :** {data['type']}\n**Bio :** {data['bio']}\n**Site admin? :** {data['site_admin']}\n**company :** {data['company']}\n**location :** {data['location']}\n**email :** {data['email']}\n**Created at :** {data['created_at']}\n**Public repos :** {data['public_repos']}\n**Followers :** {data['followers']}",color=discord.Color.embed_background())
                    em.url=data['html_url']
                    em.title=f"**{user} on github**"
                    em.set_thumbnail(url=data["avatar_url"])
                    await ctx.respond(embed=em)
        except:
            em2=discord.Embed(description="**<:ceres_failure:951863495559872613> Something went wrong or the user doesnt exists!**",color=discord.Color.embed_background(),ephemeral=True)
            await ctx.respond(embed=em2)

    @emoji_.command()
    @commands.has_permissions(manage_emojis_and_stickers=True)
    async def steal(self, ctx: commands.Context, emoji: Option(discord.PartialEmoji,"The emoji you want to steal from other server only",required=True), name: Option(str,"The name of the emoji you are adding",required=True)):
        """Steal an emoji for another server"""
        try:
            try:
                emoji = await emoji.read()
                emoji_created = await ctx.guild.create_custom_emoji(image=emoji, name=name)
                await ctx.respond(embed=discord.Embed(description=f"**<:ceres_succces:938669698621509652> Successfully created the emoji - {emoji_created} with name: `{name}`**", color=discord.Color.green()))
                
            except:
                return await ctx.respond(embed=discord.Embed(description="**<:ceres_failure:951863495559872613> It looks like there was something wrong while deleting the selected emojis**\n**You can check if the emojis were valid or if it is an error in the bot you can inform in our support server**",color=discord.Color.embed_background()),view=buttons.SupportButton())
        except discord.MissingPermissions:
            await ctx.respond("**<:ceres_failure:951863495559872613> You need `Manage emoji and stickers` permissions to be able to use this command**",ephemeral=True)

    @emoji_.command(guild_ids=[883180896038027336])
    @commands.has_permissions(manage_emojis_and_stickers=True)
    async def emojiadd(self, ctx, emoji: Option(str,"Please give the url of the emoji you want to add to the server",required=True), name: Option(str,"The name of the emoji you are adding to the server",required=True)):
        """Creates an emoji in the server using an url"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(emoji) as r:
                    try:
                        imgOrGIF = BytesIO(await r.read())
                        bValue = imgOrGIF.getvalue()
                        if r.status in range(200, 299):
                            emojiCreate = await ctx.guild.create_custom_emoji(image=bValue, name=name)
                            await ctx.respond(embed=discord.Embed(description=f"**<:ceres_succces:938669698621509652> Successfully created emoji - {emojiCreate} with name: `{name}`**", color=discord.Color.green()))
                        else:
                            await ctx.respond(embed=discord.Embed(description=f"<:ceres_failure:951863495559872613> An error occured while creating the emoji | {r.status}", color=discord.Color.red()))
                    except discord.HTTPException:
                        await ctx.respond(embed=discord.Embed(description=f"<:ceres_failure:951863495559872613> The file size is too big!", color=discord.Color.red()))
                    except Exception as e:
                        print(e)
        except commands.MissingPermissions:
            await ctx.respond(f"**<:ceres_failure:951863495559872613> You need `Manage emojis` permission to be able to use this command!**")

def setup(bot):
    bot.add_cog(Utility(bot))