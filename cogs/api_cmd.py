import discord
from discord.ext import commands,tasks
from discord.commands import slash_command,Option
from giphy_client.rest import ApiException
import aiohttp
import io
import utils.select as select
import urllib
import config
from discord.ui import Button,View
import random
from datetime import datetime
import textwrap
import json
import requests

class Api_cmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("api cog loaded")

#lyrics command

    @slash_command(name="lyrics",description="gets the lyrics of the mentioned song",guild_ids=[883180896038027336,903168731885240350]) # adding aliases to the command so they they can be triggered with other names
    async def lyrics(self,ctx, *, search = None):
        await ctx.defer()
        if not search:
            embed = discord.Embed(
                title = "No search argument!",
                description = "You havent entered anything, so i couldnt find lyrics!"
            )
            return await ctx.respond(embed = embed)
            
        
        song = urllib.parse.quote(search) 
        
        async with aiohttp.ClientSession() as lyricsSession:
            async with lyricsSession.get(f'https://some-random-api.ml/lyrics?title={song}') as jsondata: 
                if not 300 > jsondata.status >= 200:
                    return await ctx.respond(f'Recieved poor status code of {jsondata.status}')

                lyricsData = await jsondata.json() 

        error = lyricsData.get('error')
        if error: 
            return await ctx.respond(f'Recieved unexpected error: {error}')

        songLyrics = lyricsData['lyrics'] 
        songArtist = lyricsData['author'] 
        songTitle = lyricsData['title'] 
        songThumbnail = lyricsData['thumbnail']['genius']

        for chunk in textwrap.wrap(songLyrics, 4096, replace_whitespace = False):
            embed = discord.Embed(
                title = songTitle,
                description = chunk,
                color = discord.Color.blurple(),
                timestamp = datetime.utcnow()
            )
            embed.set_footer(text=songArtist)
            embed.set_thumbnail(url = songThumbnail)
            await ctx.respond(embed = embed)

    
#meme cmd

    @slash_command(name="meme",description="gets a random meme",guild_ids=[883180896038027336,903168731885240350])
    async def meme(self,ctx):
        await ctx.defer()
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://meme-api.herokuapp.com/gimme") as s:
                memejson = await s.json()
                i = 0
                while memejson["nsfw"] == True:

                    async with aiohttp.ClientSession() as cs:
                        async with cs.get("https://meme-api.herokuapp.com/gimme") as s:
                            memejson = await s.json()
                            i += 1
                            if i == 10:
                                await ctx.send(
                                    "Clean memes were not found after 10 tries, please try again."
                                )
                                return
                upvote_count=memejson["ups"]
                embed=discord.Embed(
                        title=(memejson["title"]), url=memejson["postLink"],timestamp=datetime.utcnow()).set_image(url=memejson["url"]).set_footer(text=f"👍 {upvote_count}")
                next_button=Button(label="Next meme",style=discord.ButtonStyle.green)
                end_button=Button(label="End interaction",style=discord.ButtonStyle.danger)
                async def end_button_callback(interaction):
                    if interaction.user.id == ctx.author.id:
                        await ctx.edit(view=None)
                    else:
                        await interaction.response.send_message(f"This is not for you.",ephemeral=True)
                        end_button.disabled=True
                async def next_button_callback(interaction):
                    if interaction.user.id == ctx.author.id:
                        async with aiohttp.ClientSession() as cs:
                            async with cs.get("https://meme-api.herokuapp.com/gimme") as s:
                                memejson = await s.json()
                                i = 0
                                while memejson["nsfw"] == True:

                                    async with aiohttp.ClientSession() as cs:
                                        async with cs.get("https://meme-api.herokuapp.com/gimme") as s:
                                            memejson = await s.json()
                                            i += 1
                                            if i == 10:
                                                await ctx.send(
                                                "Clean memes were not found after 10 tries, please try again."
                                                )
                                                return
                                upvote_count=memejson["ups"]
                                nexembed=discord.Embed(
                                    title=(memejson["title"]), url=memejson["postLink"],timestamp=datetime.utcnow()).set_image(url=memejson["url"]).set_footer(text=f"👍 {upvote_count}")
                                await ctx.edit(embed=nexembed)
                    else:
                        await interaction.response.send_message(f"This is not for you.",ephemeral=True)
                        next_button.disabled=True
                next_button.callback=next_button_callback
                end_button.callback=end_button_callback
                view=View(next_button,end_button)
                
                await ctx.respond(embed=embed,view=view)
        

#duck cmd

    @slash_command(name="duck",description="sends a random duck",guild_ids=[883180896038027336,903168731885240350])
    async def duck(self,ctx):
        await ctx.defer()
        duck_json=json.loads(requests.get("https://random-d.uk/api/v1/random").text)
        mbed = discord.Embed(title="**Quack!!**", colour=random.choice(config.color_list),timestamp=datetime.utcnow())
        mbed.set_image(url=duck_json["url"])
        mbed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed = mbed)

#coffee cmd

    @slash_command(name="coffee",description="sends a random coffee",guild_ids=[883180896038027336,903168731885240350])
    async def coffee(self,ctx):
        await ctx.defer()
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://coffee.alexflipnote.dev/random.json") as r:
                pika_json=await r.json()
        coffe_json= json.loads((requests.get("https://coffee.alexflipnote.dev/random.json").text))
        cofembed=discord.Embed(title="**Sip!!!**",color=ctx.author.color,timestamp=datetime.utcnow())
        cofembed.set_image(url=coffe_json["file"])
        cofembed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed = cofembed)

#pikachu cmd

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def pikachu(self,ctx):
        await ctx.defer()
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/pikachu") as r:
                pika_json=await r.json()
                cofembed=discord.Embed(title="**Pika pikachu!!!**",color=ctx.author.color,timestamp=datetime.utcnow())
                cofembed.set_image(url=pika_json["link"])
                cofembed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                await ctx.respond(embed = cofembed)

#achievement cmd

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def achievement(self, ctx, text: Option(str,"Enter the text for achievement", required=True)):
        """Gets an achievement of your choice"""
        image = f"https://api.cool-img-api.ml/achievement?text={text}"
        await ctx.respond(image)

#wink cmd

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def wink(self,ctx,member: discord.Member):
        """wink at someone"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/wink") as r:
                wink_json=await r.json()
                wink_embed=discord.Embed(title=f"**{ctx.author.name} Winks at {member.name}!!!**",color=ctx.author.color,timestamp=datetime.utcnow())
                wink_embed.set_image(url=wink_json["link"])
                wink_embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                await ctx.respond(embed = wink_embed)

#pat cmd

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def pat(self,ctx,member: discord.Member):
        """give someone a headpat!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/pat") as r:
                pat_json=await r.json()
                pat_embed=discord.Embed(title=f"**{ctx.author.name} Pats {member.name}...!!!**",color=ctx.author.color,timestamp=datetime.utcnow())
                pat_embed.set_image(url=pat_json["link"])
                pat_embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                await ctx.respond(embed = pat_embed)

#hug cmd

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def hug(self,ctx,member: discord.Member):
        """hug someone digitally!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/hug") as r:
                hug_json=await r.json()
                hug_embed=discord.Embed(title=f"**{ctx.author.name} Digitally Hugs {member.name}...!!!**",color=ctx.author.color,timestamp=datetime.utcnow())
                hug_embed.set_image(url=hug_json["link"])
                hug_embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                await ctx.respond(embed = hug_embed)

#dog fact cmd

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def dogf(self,ctx):
        """sends a random dog fact"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/facts/dog") as r:
                dog_fact_json=await r.json()
                dog_fact_embed = discord.Embed(title="**Dog Fact**",description=dog_fact_json["fact"],color=ctx.author.color,timestamp=datetime.utcnow())
                dog_fact_embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                dog_fact_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/917073456670076938/931832996099653652/dog-cute.gif")
                await ctx.respond(embed= dog_fact_embed)

#cat fact cmd

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def catf(self,ctx):
        """sends a random cat fact"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/facts/cat") as r:
                cat_fact_json=await r.json()
                cat_fact_embed = discord.Embed(title="**Cats Fact...uwu!!**",description=cat_fact_json["fact"],color=ctx.author.color,timestamp=datetime.utcnow())
                cat_fact_embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                cat_fact_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/916342232993370182/932139633834360832/105812.jpg")
                await ctx.respond(embed= cat_fact_embed)
    
#panda fact cmd

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def pandaf(self, ctx):
        """sends a random panda fact"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/facts/panda") as r:
                panda_fact_json=await r.json()
                panda_fact_embed = discord.Embed(title="**Panda Fact!!!**",description=panda_fact_json["fact"],color=ctx.author.color,timestamp=datetime.utcnow())
                panda_fact_embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                panda_fact_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/930389219170459658/937958979307462707/165728.jpg")
                await ctx.respond(embed= panda_fact_embed)

#fox fact

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def foxf(self,ctx):
        """sends a random fox fact"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/facts/fox") as r:
                fox_js=await r.json()
                fox_em=discord.Embed(title="**Fox fact!**",description=fox_js["fact"])
                fox_em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                fox_em.set_thumbnail(url="https://cdn.discordapp.com/attachments/917073456670076938/945921922477223988/2565477.jpg")
                await ctx.respond(embed =fox_em)

#bird fact

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def birdf(self, ctx):
        """sends a random bird fact!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/facts/bird") as r:
                bir_js=await r.json()
                bir_em=discord.Embed(title="**Bird fact!!**",description=bir_js["fact"])
                bir_em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                bir_em.set_thumbnail(url="https://cdn.discordapp.com/attachments/917073456670076938/945922845488328714/original.jpg")
                await ctx.respond(embed= bir_em)

#koala fact

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def koalaf(self,ctx):
        """sends a random koala fact!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/facts/koala") as r:
                k_js=await r.json()
                k_em=discord.Embed(title="**Koala fact!!**",description=k_js["fact"])
                k_em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                k_em.set_thumbnail(url="https://cdn.discordapp.com/attachments/917073456670076938/945923768415567892/d191fc691d2a824422062b58e4b0056f.jpg")
                await ctx.respond(embed= k_em)

#cat command

    @slash_command(name="cat",description="get a random cute kitty catty picture",guild_ids=[883180896038027336,903168731885240350])     
    async def cat(self,ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("http://aws.random.cat/meow") as r:
                data = await r.json()
                embed = discord.Embed(title="**Meow.!.uwu**", colour=random.choice(config.color_list))
                embed.set_image(url=data['file'])
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                c=await ctx.respond(embed=embed)
                emoji='<:cutekittyawwww:926356749236191263>'
                c=await ctx.interaction.original_message()
                await c.add_reaction(emoji)

#dog command

    @slash_command(name="dog",description="get a random loyal cute dogo picture",guild_ids=[883180896038027336,903168731885240350])
    async def dog(self,ctx):
        await ctx.defer()
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://dog.ceo/api/breeds/image/random") as r:
                data = await r.json()
                embed = discord.Embed(title="**Woof..!!**", colour=random.choice(config.color_list))
                embed.set_image(url=data['message'])
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                
                a = await ctx.respond(embed=embed)
                emoji='<a:cutedog:926356463994146836>'
                a=await ctx.interaction.original_message()
                await a.add_reaction(emoji)

#simp card cmd

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def simp(self,ctx,member: Option(discord.Member, "select the simp lol",required=True)):
        await ctx.defer()
        avat_simp=member.display_avatar.with_static_format("png")
        simp_car_json = (f'https://some-random-api.ml/canvas/simpcard?avatar={avat_simp}')
        simp_em= discord.Embed(title="**Simp detected 🚨🚨🚨..!!!**")
        print(simp_car_json)
        simp_em.set_image(url=simp_car_json)
        await ctx.respond(embed = simp_em)


#token cmd

#api https://g.tenor.com/v1/random?key=$0R6U3QR9N8QX&q=anime&limit=50

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def token(self,ctx):
        """sends the bots token"""
        toke_json=json.loads((requests.get("https://some-random-api.ml/bottoken").text))
        toke_embed=discord.Embed(title="Token:",description=f'{toke_json["token"]}\n **token might be fake xD**',timestamp=datetime.utcnow(),color=ctx.author.color)
        toke_embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed =toke_embed)



#triggered command

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def triggered(self,ctx, member: discord.Member=None):
        """trigger some ppl"""
        await ctx.defer()
        if not member:
            member = ctx.author
        avat_simp=member.display_avatar.with_static_format("png")
        async with aiohttp.ClientSession() as trigSession:
            async with trigSession.get(f'https://some-random-api.ml/canvas/triggered?avatar={avat_simp}') as trigImg: # get users avatar as png with 1024 size
                imageData = io.BytesIO(await trigImg.read())
                
                await trigSession.close()
                
                await ctx.respond(file=discord.File(imageData, 'triggered.gif'))

#joke cmd

    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def joke(self,ctx):
        """sends a random joke"""
        jok_json = json.loads(requests.get("https://some-random-api.ml/joke").text)
        jok_em=discord.Embed(title="**Joke**",timestamp=datetime.utcnow(),color=ctx.author.color,description=jok_json["joke"])
        await ctx.respond(embed =jok_em)


    @slash_command(guild_ids=[883180896038027336,903168731885240350])
    async def clyde(self, ctx, text: Option(str, "Enter the message you want Clyde to say")):
        """Makes Clyde say something for You"""
        await ctx.defer()
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://nekobot.xyz/api/imagegen?type=clyde&text={text}") as r:
                res = await r.json()
                embed = discord.Embed(color=ctx.author.color)
                embed.set_image(url=res['message'])
                embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
                await ctx.edit(embed=embed)


def setup(bot):
    bot.add_cog(Api_cmds(bot))