import discord
from discord.ext import commands
from discord.commands import slash_command,Option
from datetime import datetime
import humor_langs
import random
import os
import config
import qrcode
import asyncio
import utils.buttons
from utils.buttons import TicTacToe,NitroButton
import akinator as ak
from PIL import Image
from io import BytesIO
import aiohttp
import animec
from petpetgif import petpet as petpetgif
import json
import requests

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("fun cog loaded")

#sad commands

    @slash_command(name="sad",description="express your sadness")
    async def sad(self,ctx):
        sad_gifs=["https://cdn.discordapp.com/attachments/918722247026434048/922767301693046835/baa50bb8d7556f7ca2e68c0576584dd4.gif",
                "https://cdn.discordapp.com/attachments/918722247026434048/922767300422172682/sad-aesthetic.gif",
                "https://cdn.discordapp.com/attachments/918722247026434048/922767300816416818/73b13bcd2590cd93ca1ca9bbc7f917be.gif",
                "https://cdn.discordapp.com/attachments/918722247026434048/922767301118398505/anime-sad.gif",
                "https://cdn.discordapp.com/attachments/918722247026434048/922767300422172682/sad-aesthetic.gif",
                "https://cdn.discordapp.com/attachments/918722247026434048/922767300115955722/tumblr_og7o11BeE91vctqxpo1_500.gif",
                "https://cdn.discordapp.com/attachments/918722247026434048/922767293941956628/c3c088c1dbaf514d63f952ffcae35a90.gif",
                "https://cdn.discordapp.com/attachments/918722247026434048/922767293354762286/tumblr_oqmi7sP7q41scqbpuo1_500.gif",
                "https://cdn.discordapp.com/attachments/918722247026434048/922767292931145728/ken-kaneki-sad.gif",
                "https://cdn.discordapp.com/attachments/918722247026434048/922767292624957450/kaneki-ken-crying.gif",
                "https://cdn.discordapp.com/attachments/918722247026434048/922767292398456922/7FPG.gif",
                "https://cdn.discordapp.com/attachments/918722247026434048/922767291945459732/tokyo-ghoul-crying.gif",
                "https://cdn.discordapp.com/attachments/918722247026434048/922767291416969247/f2e760dd14984591af840fe3eaddb17c.gif",
                "https://cdn.discordapp.com/attachments/918722247026434048/922767291173728256/aniyuki-sad-anime-gif-71.gif",
                "https://cdn.discordapp.com/attachments/918722247026434048/922767290909462538/8UgL.gif"]
        embed = discord.Embed(title=":(",timestamp=datetime.utcnow(),color=ctx.author.color)
        embed.set_footer(text=f'Requested by - {ctx.author}',icon_url=ctx.author.avatar.url)
        embed.set_image(url=random.choice(sad_gifs))
        await ctx.respond(embed=embed)

#owo command

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def owofy(self,ctx,message:Option(str,"Write the message to owofy",required=True)):
        """Converts your message in UwUs. its not worth trying, trust me."""
        await ctx.respond(f"<a:uwuemoji:949941845188829235> {humor_langs.owofy(message)}")
        
#british command

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def britainify(self, ctx: commands.Context, *, message:Option(str,"Write the message to britainify",required=True)):
        """Can you pass me a bo'le o' wo'e'r"""
        await ctx.respond(humor_langs.strong_british_accent(message))

#animestatus command

    @slash_command(name="anime",description="search an anime")
    async def animestatus(self,ctx,*,query: Option(str,"Anime Name To get Information",required=True)):
        await ctx.defer()
        try:
            anime=animec.Anime(query)
        except:
            anime_error_embed=discord.Embed(description=f"**No corresponding Anime wa found with the name of {query} please try again!**",color=ctx.author.color,timestamp=datetime.utcnow())
            anime_error_embed.set_thumbnail(url=f"https://cdn.discordapp.com/attachments/917073456670076938/923829287876984832/giphy_3.gif")
            await ctx.respond(embed=anime_error_embed)
            return
        embed=discord.Embed(title=anime.title_english,url=anime.url,description=f"{anime.description[:200]}...",color=ctx.author.color)
        embed.add_field(name="**Episodes**",value= str(anime.episodes))
        embed.add_field(name="**Rating**",value=str(anime.rating))
        embed.add_field(name="**Brodcasting**",value=str(anime.broadcast))
        embed.add_field(name="**Status**",value=str(anime.status))
        embed.add_field(name="**Type**",value=str(anime.type))
        embed.add_field(name="**NSFW status**",value=str(anime.is_nsfw()))
        embed.set_thumbnail(url=anime.poster)
        await ctx.respond(embed=embed)

#anime character command

    @slash_command(name="character",description="search an anime character")
    async def animecharacter(self,ctx,*,query: Option(str,"characters name to get information",required=True)):
        await ctx.defer()
        try:
            char=animec.Charsearch(query)
        except:
            anime_error_embed=discord.Embed(description=f"**No corresponding Anime character was found with the name of {query} please try again!**",color=ctx.author.color,timestamp=datetime.utcnow())
            anime_error_embed.set_thumbnail(url=f"https://cdn.discordapp.com/attachments/917073456670076938/923829287876984832/giphy_3.gif")
            await ctx.respond(embed=anime_error_embed)
            return
        character_embed=discord.Embed(title=char.title,url=char.url,color=ctx.author.color)
        character_embed.set_image(url=char.image_url)
        character_embed.set_footer(text=", ".join(list(char.references.keys())[:2]))
        await ctx.respond(embed=character_embed)

#sus command

    @slash_command(name="sus",description="sus")
    async def sus(self,ctx):
        suss = ["https://tenor.com/view/sus-gif-22065664",
       "https://cdn.discordapp.com/attachments/918722247026434048/920167249912946698/giphy.gif",
       "https://cdn.discordapp.com/attachments/918722247026434048/920167242585505882/lol-sus.gif",
       "https://cdn.discordapp.com/attachments/918722247026434048/920167242585505882/lol-sus.gif",
       "https://cdn.discordapp.com/attachments/918722247026434048/920167220557008926/monophy.gif",
       "https://cdn.discordapp.com/attachments/918722247026434048/920167194007056484/giphy_1.gif",
       "https://cdn.discordapp.com/attachments/918722247026434048/920167183831666718/TotalInfiniteAmericangoldfinch-size_restricted.gif",
]
        embed=discord.Embed(title="suspecious",timestamp=datetime.utcnow(),color=ctx.author.color)
        sussy_boy=random.choice(suss)
        embed.set_image(url=sussy_boy)
        embed.set_footer(text=f'Requested by - {ctx.author}',icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)



#happy command

    @slash_command(name="happy",description="give it a smile bro")
    async def sus(self,ctx):
        anime_smiles = ["https://cdn.discordapp.com/attachments/918722247026434048/920188623071109140/anime-smile.gif",
    "https://cdn.discordapp.com/attachments/918722247026434048/920188622693625876/idolmaster-makoto.gif",
    "https://cdn.discordapp.com/attachments/918722247026434048/920188622345469973/anime.gif",
    "https://cdn.discordapp.com/attachments/918722247026434048/920188621825380352/kimetsu-no-yaiba-sabito.gif",
    "https://cdn.discordapp.com/attachments/918722247026434048/920188621485654056/4591cb6b3c55d6dc7e299112864e2b47.gif",
    "https://cdn.discordapp.com/attachments/918722247026434048/920188621129134120/426fe481c0681433012adcdfbe4172f8.gif",
    "https://cdn.discordapp.com/attachments/918722247026434048/920188620575494234/b87a2400d65385c071af5a5a9550389f.gif",
    "https://cdn.discordapp.com/attachments/918722247026434048/920188620030230568/tumblr_prw9o76n6G1wcxiqr_400.gif",
    "https://cdn.discordapp.com/attachments/918722247026434048/920188619673698345/kaneki-tokyo-ghoul.gif",
    "https://cdn.discordapp.com/attachments/918722247026434048/920188619468185650/fra-anime.gif",
    "https://cdn.discordapp.com/attachments/918722247026434048/921301478906421328/kyojuro-kyojuro-rengoku.gif"]
        embed=discord.Embed(title=":D",timestamp=datetime.utcnow(),color=ctx.author.color)
        smile=random.choice(anime_smiles)
        embed.set_image(url=smile)
        embed.set_footer(text=f'Requested by - {ctx.author}',icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)

#8ball command

    @slash_command(name="8ball",description="get a magical answer to your questions.")
    async def eightball(self,ctx,*,question : Option(str,"Write your question",required=True)):
        ball_answers=['It is certain.',
                        'It is decidedly so.',
                        'Without a doubt.',
                        'Yes – definitely.',
                        'You may rely on it.',
                        'As I see it, yes.',
                        'Hell no.',
                        'Prolly not.',
                        'Idk bro.',
                        'I think so.',
                        'Hell yeah my dude.',
                        'Most likely.',
                        'Outlook good.',
                        'Yes.',
                        'Signs point to yes.',
                        'Reply hazy, try again.',
                        'Ask again later.',
                        'Better not tell you now.',
                        'Cannot predict now.',
                        'Concentrate and ask again.',
                        "Don't count on it.",
                        'My reply is no.',
                        'My sources say no.',
                        'Outlook not so good.',
                        'Very doubtful.']
        ball_e = discord.Embed(title=f"MAGIC 8-BALL", color=0x9B59B6)
        ball_e.set_thumbnail(url=f'https://cdn.discordapp.com/attachments/916342230397091840/918855555878105148/crystal-ball-dribble.gif')
        ball_e.add_field(name=f"🔮Question by `{ctx.author}`: `{question}`", value=f"**My Magic ball tells that:\n `{random.choice(ball_answers)}`**",inline=False
        )
        await ctx.respond(embed=ball_e)

#coinflip command

    @slash_command(name="coinflip",description="Not able to make a decision? lets flips a coin")
    async def coinflip(self,ctx):
        value=[f"<:heads:918026458960625714>",f"<:tails:918026497363705907>"]
        await ctx.respond(f"**coin fliping <a:CoinFlipping:923809410973855774> **")
        await asyncio.sleep(5)
        flip = random.choice(value)
        if flip == f"<:tails:918026497363705907>":
            await ctx.edit(content=f"**The coin flipped and gave us a `Tails` <:tails:918026497363705907>**")
        if flip == f"<:heads:918026458960625714>":
            await ctx.edit(content=f"**The coin flipped and gave us a `Heads` <:heads:918026458960625714>**")


#random number generator

    @slash_command(name="randomnumgen",description="Generates a random number!")
    async def randomnumgen(self,ctx):
        e=discord.Embed(title="Random Numer generated!!",description=random.randint(1,1000),color=ctx.author.color)
        await ctx.respond(embed=e)

#PING

    @slash_command(name="ping",description="sends the speed to the bot")
    async def ping(self, ctx):
        await ctx.respond(f"**Latency: {round(self.bot.latency * 1000)} ms**")

#petpet meme

    @slash_command(description="makes the popular petpet meme of the mentioned users avatar!",guild_ids=[883180896038027336])
    async def pet(self,ctx, image:discord.Member):
        image = await image.avatar.with_format('png').read()
        source = BytesIO(image)
        dest = BytesIO()
        petpetgif.make(source, dest)
        dest.seek(0)
        await ctx.respond(file=discord.File(dest, filename=f"{image[0]}-petpet.gif"))


    @slash_command(name="nitro",description='Generates a Nitro link totally legit xd!',guild_ids=[883180896038027336])
    async def nitro(self, ctx):
        interaction: discord.Inteaction = ctx.interaction
        embed = discord.Embed(description=f"**{ctx.author.mention} generated a nitro link!**", color=discord.Color.nitro_pink())
        embed.set_image(url="https://media.discordapp.net/attachments/886639021772648469/903535585992523796/unknown.png")
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_message()
        await message.edit(embed=embed, view=NitroButton(message, ctx))


    @slash_command(guild_ids=[883180896038027336])
    async def covid(self, ctx, *, countryname: Option(str,"Mention the country to get stats.",required=True)):
        """sends the covid stats of the mentioned country"""
        try:
            if countryname is None:
                embed=discord.Embed(title="This command is used like this: ```+covid [country]```", colour=0xff0000, timestamp=datetime.utcnow())
                await ctx.send(embed=embed)


            else:
                cov_url = json.loads(requests.get(f"https://coronavirus-19-api.herokuapp.com/countries/{countryname}").text)
                country = cov_url["country"]
                totalCases = cov_url["cases"]
                todayCases = cov_url["todayCases"]
                totalDeaths = cov_url["deaths"]
                todayDeaths = cov_url["todayDeaths"]
                recovered = cov_url["recovered"]
                active = cov_url["active"]
                critical = cov_url["critical"]
                casesPerOneMillion = cov_url["casesPerOneMillion"]
                deathsPerOneMillion = cov_url["deathsPerOneMillion"]
                totalTests = cov_url["totalTests"]
                testsPerOneMillion = cov_url["testsPerOneMillion"]

                embed2 = discord.Embed(title=f"**COVID-19 Status Of {country}**!", description="This Information Isn't Live Always, Hence It May Not Be Accurate!", colour=random.choice(config.color_list), timestamp=datetime.utcnow())
                embed2.add_field(name="**Total Cases**", value=totalCases, inline=True)
                embed2.add_field(name="**Today Cases**", value=todayCases, inline=True)
                embed2.add_field(name="**Total Deaths**", value=totalDeaths, inline=True)
                embed2.add_field(name="**Today Deaths**", value=todayDeaths, inline=True)
                embed2.add_field(name="**Recovered**", value=recovered, inline=True)
                embed2.add_field(name="**Active**", value=active, inline=True)
                embed2.add_field(name="**Critical**", value=critical, inline=True)
                embed2.add_field(name="**Cases Per One Million**", value=casesPerOneMillion, inline=True)
                embed2.add_field(name="**Deaths Per One Million**", value=deathsPerOneMillion, inline=True)
                embed2.add_field(name="**Total Tests**", value=totalTests, inline=True)
                embed2.add_field(name="**Tests Per One Million**", value=testsPerOneMillion, inline=True)
                embed2.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/564520348821749766/701422183217365052/2Q.png")
                await ctx.respond(embed=embed2)

        except:
            embed3 = discord.Embed(title="**Invalid Country Name Or API Error! Try Again..!**", colour=random.choice(config.color_list), timestamp=datetime.utcnow())
            embed3.set_author(name="Error!")
            await ctx.send(embed=embed3)

    @slash_command(guild_ids=[883180896038027336])
    async def akinator(self, ctx: commands.Context):
        """Play a game of akinator"""
        await ctx.respond(embed=discord.Embed(description="**Akinator is here to guess!\n--------------------------------\nOptions: y: `yes\n`no: `n`\nidk: `Don't know`\np: `probably`\npn: `probably not`\nb: `previous question`\nq: `quit the game`**", color=discord.Color.green()).set_image(url="https://static.wikia.nocookie.net/video-game-character-database/images/9/9f/Akinator.png/revision/latest?cb=20200817020737"))
        def check(msg):
            return (
                msg.author == ctx.author
                and msg.channel == ctx.channel
                and msg.content.lower() in ["y", "n", "idk", "p", "pn", "b", "q"]
            )

        try:
            aki = ak.Akinator()
            q = aki.start_game()
            while aki.progression <= 80:
                await ctx.send(embed=discord.Embed(description=f"**{q}\n\n[`y` | `n` | `idk` | `p` | `pn` | `b` | `q`]**", color=discord.Color.embed_background(theme="dark")))
                try:
                    msg = await self.bot.wait_for("message", check=check, timeout=60)
                    if msg.content.lower() == "q":
                        await ctx.send(embed=discord.Embed(description="**You have quit the game!**", color=discord.Color.red()))
                        break
                    if msg.content.lower() == "b":
                        try:
                            q = aki.back()
                        except ak.CantGoBackAnyFurther:
                            await ctx.send(embed=discord.Embed(description=f"**<:redTick:923810237230768210> {e}**"))
                            continue
                    else:
                        try:
                            q = aki.answer(msg.content.lower())
                        except ak.InvalidAnswerError as e:
                            await ctx.send(embed=discord.Embed(description=f"**<:redTick:923810237230768210> {e}**"))
                            continue
                except asyncio.TimeoutError:
                    return await ctx.send(embed=discord.Embed(description=f"**<:redTick:923810237230768210> The game timed-out.. try plsying a new one**"))

                except Exception as e:
                    await ctx.send(embed=discord.Embed(description=f"**<:redTick:923810237230768210> An error occured\n`{str(e).capitalize()}`**"))
            aki.win()
            await ctx.send(
                embed=discord.Embed(description=f"**Is it {aki.first_guess['name']}\n({aki.first_guess['description']})!\nWas I correct?(y/n)\n\t**", color=discord.Color.orange()).set_image(url=aki.first_guess['absolute_picture_path'])
            )
            correct = await self.bot.wait_for("message", check=check)
            if correct.content.lower() == "y":
                await ctx.send(embed=discord.Embed(description="**Yay!**", color=discord.Color.green()))
            else:
                await ctx.send(embed=discord.Embed(description="**Oof!**", color=discord.Color.red()))
        except Exception as e:
            await ctx.send(e)


    @slash_command(description="Play a TicTacToe Game with Someone on discord!",guild_ids=[883180896038027336])
    async def tictactoe(self, ctx: discord.ApplicationContext, user: Option(discord.Member, "The user you want to play tic-tac-toe with", default=None, required=True)):
        if user is None:
            return await ctx.respond(embed=discord.Embed(description="**<:error:897382665781669908? You can't play tic-tac-toe alone!**", color=discord.Color.red()), ephemeral=True)

        if user.bot:
            return await ctx.respond(embed=discord.Embed(description="**<:ceres_failure:951863495559872613> You can't play with a bot!**", color=discord.Color.red()), ephemeral=True)

        players = {
            str(ctx.author.id): str(user.id),
            str(user.id): str(ctx.author.id)
        }

        player1 = random.choice(list(players.keys()))
        player2 = players[player1]

        await ctx.interaction.response.send_message(f"{ctx.guild.get_member(int(player1)).mention}\'s turn (X)")
        
        msg = await ctx.interaction.original_message()

        await msg.edit(view=TicTacToe(
            player1=ctx.guild.get_member(int(player1)),
            player2=ctx.guild.get_member(int(player2)),
            message=msg
        ))


    #Qrcode
    @slash_command(description="Generates a Qrcode!")
    async def qrcode(self, ctx, url: Option(str, "The link you want the qrcode of", required=True, default=None), hidden: Option(str, "Do you want the qrcode to be visible only to you?", choices=["Yes", "No"], required=False, default=None)):
        img = qrcode.make(url)
        img.save("qrcode.png")
        if hidden == "Yes":
            await ctx.respond(content="**Here is your QRCode**", file=discord.File("qrcode.png"), ephemeral=True)
        else:
            await ctx.respond(content="**Here is your QRCode**", file=discord.File("qrcode.png"))
        os.remove("qrcode.png")


    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def kill(self, ctx, user: discord.Member = None):
        """Generates a kill poster for a user."""
        user = ctx.author if not user else user
        amogusimage = Image.open(f"img/kill.jfif")
        asset1 = user.avatar.with_format("jpg")
        asset2 = ctx.author.avatar.with_format("jpg")
        data1 = BytesIO(await asset1.read())
        data2 = BytesIO(await asset2.read())
        pfp = Image.open(data1)
        author = Image.open(data2)

        pfp = pfp.resize((55, 55))
        author = author.resize((55, 55))
        amogusimage.paste(author, (54, 58))
        amogusimage.paste(pfp, (170, 40))
        amogusimage.save("kill.jpg")
        try:
            await ctx.respond(file=discord.File("kill.jpg"))
            os.remove("kill.jpg")
        except:
            await ctx.respond("Error!")

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def serverstats(self,ctx,serverip:Option(str,"The ip of the server to get stats",required=True)):
        """gets the stats of any java minecraft server on discord"""
        async with aiohttp.ClientSession() as pokemonSession:
            async with pokemonSession.get(f'https://api.mcsrvstat.us/2/{serverip}') as pop:
                info=await pop.json()
                imag=f"https://mcapi.us/server/image?ip={serverip}"
                em=discord.Embed(title="lol")
                em.set_image(url=imag)

def setup(bot):
    bot.add_cog(Fun(bot))