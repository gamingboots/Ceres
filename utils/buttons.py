import discord
from discord.ext import commands
from typing import List
import config

async def memberCheck(guild: discord.Guild) -> List[int]:
    """Returns the memberList which contains memberIDs of all members combined"""
    memberList = []
    for member in guild.members:
        memberList.append(member.id)
    return memberList

class Calculator(discord.ui.View):
    def __init__(self,msg,ctx):
        self.msg = msg
        self.ctx = ctx
        self.exp = ''
        super().__init__(timeout=60)

    @discord.ui.button(label='1',row=0)
    async def one(self,b:discord.ui.Button,i:discord.Interaction):
        self.exp += '1'
        await i.response.edit_message(embed=self.build_em(self.exp))

    @discord.ui.button(label='2',row=0)
    async def two(self,b:discord.ui.Button,i:discord.Interaction):
        self.exp += '2'
        await i.response.edit_message(embed=self.build_em(self.exp))

    @discord.ui.button(label='3',row=0)
    async def three(self,b:discord.ui.Button,i:discord.Interaction):
        self.exp += '3'
        await i.response.edit_message(embed=self.build_em(self.exp))

    @discord.ui.button(label='x',style=discord.ButtonStyle.blurple,row=0)
    async def into(self,b:discord.ui.Button,i:discord.Interaction):
        self.exp += 'x'
        await i.response.edit_message(embed=self.build_em(self.exp))

    @discord.ui.button(label='4',row=1)
    async def four(self,b:discord.ui.Button,i:discord.Interaction):
        self.exp += '4'
        await i.response.edit_message(embed=self.build_em(self.exp))

    @discord.ui.button(label='5',row=1)
    async def five(self,b:discord.ui.Button,i:discord.Interaction):
        self.exp += '5'
        await i.response.edit_message(embed=self.build_em(self.exp))

    @discord.ui.button(label='6',row=1)
    async def six(self,b:discord.ui.Button,i:discord.Interaction):
        self.exp += '6'
        await i.response.edit_message(embed=self.build_em(self.exp))

    @discord.ui.button(label='÷',row=1,style=discord.ButtonStyle.blurple)
    async def divide(self,b:discord.ui.Button,i:discord.Interaction):
        self.exp += '÷'
        await i.response.edit_message(embed=self.build_em(self.exp))

    @discord.ui.button(label='←',row=1,style=discord.ButtonStyle.red)
    async def back(self,b:discord.ui.Button,i:discord.Interaction):
        self.exp = self.exp[:-1]
        if len(self.exp) < 1:
            self.exp = ''
            sol = '0'
        else:
            sol = self.exp
        await i.response.edit_message(embed=self.build_em(sol))

    @discord.ui.button(label='7',row=2)
    async def seven(self,b:discord.ui.Button,i:discord.Interaction):
        self.exp += '7'
        await i.response.edit_message(embed=self.build_em(self.exp))

    @discord.ui.button(label='8',row=2)
    async def eight(self,b:discord.ui.Button,i:discord.Interaction):
        self.exp += '8'
        await i.response.edit_message(embed=self.build_em(self.exp))
    @discord.ui.button(label='9',row=2)
    async def nine(self,b:discord.ui.Button,i:discord.Interaction):
        self.exp += '9'
        await i.response.edit_message(embed=self.build_em(self.exp))

    @discord.ui.button(label='+',row=2,style=discord.ButtonStyle.blurple)
    async def plus(self,b:discord.ui.Button,i:discord.Interaction):
        self.exp += '+'
        await i.response.edit_message(embed=self.build_em(self.exp))

    @discord.ui.button(label='CE',row=2,style=discord.ButtonStyle.red)
    async def clear(self,b:discord.ui.Button,i:discord.Interaction):
        sol = '0'
        self.exp = ''
        await i.response.edit_message(embed=self.build_em(sol))

    @discord.ui.button(label='.',row=3)
    async def dot(self,b:discord.ui.Button,i:discord.Interaction):
        self.exp += '.'
        await i.response.edit_message(embed=self.build_em(self.exp))

    @discord.ui.button(label='0',row=3)
    async def zero(self,b:discord.ui.Button,i:discord.Interaction):
        self.exp += '0'
        await i.response.edit_message(embed=self.build_em(self.exp))

    @discord.ui.button(label='=',row=3,style=discord.ButtonStyle.green)
    async def ans(self,b:discord.ui.Button,i:discord.Interaction):
        sol = self.get_ans()
        if sol == '0':
            self.exp = ''
        else:
            self.exp = sol
        await i.response.edit_message(embed=self.build_em(sol))

    @discord.ui.button(label='-',row=3,style=discord.ButtonStyle.blurple)
    async def minus(self,b:discord.ui.Button,i:discord.Interaction):
        self.exp += '-'
        await i.response.edit_message(embed=self.build_em(self.exp))

    @discord.ui.button(label='Quit',row=3,style=discord.ButtonStyle.red)
    async def quit(self,b:discord.ui.Button,i:discord.Interaction):
        for each in self.children:
            each.disabled = True
        mbed = discord.Embed(
            title='Calculator [Closed]',
            description=f'Use the buttons below to write expressions and the calculator will calculate them for you!``` {self.exp}```',
            color=discord.Color.embed_background()
        ).set_thumbnail(url=config.icon)
        mbed.set_footer(icon_url=self.ctx.author.display_avatar.url,text=f'Requested by {self.ctx.author.name}')
        await i.response.edit_message(embed=mbed,view=self)
        self.stop()

    def get_ans(self):
        exp = self.exp
        o = exp.replace('x','*')
        o = o.replace('÷','/')
        try:
            result = str(eval(o))
        except:
            result = 'An error occured [Wrong Syntax]'
        return result
    async def on_timeout(self):
        for each in self.children:
            each.disabled=True
        mbed = discord.Embed(
            title='Calculator [Closed]',
            description=f'Use the buttons below to write expressions and the calculator will calculate them for you!``` {self.exp}```',
            color=discord.Color.embed_background()
        ).set_thumbnail(url=config.icon)
        mbed.set_footer(icon_url=self.ctx.author.display_avatar.url,text=f'Requested by {self.ctx.author.name}')
        await self.msg.edit(embed=mbed,view=self)
        return await super().on_timeout()

    def build_em(self,exp):
        mbed = discord.Embed(
            title='Calculator',
            description=f'Use the buttons below to write expressions and the calculator will calculate them for you!``` {exp}```',
            color=discord.Color.embed_background()
        ).set_thumbnail(url=config.icon)
        mbed.set_footer(icon_url=self.ctx.author.display_avatar.url,text=f'Requested by {self.ctx.author.name}')
        return mbed
    
    async def interaction_check(self, i):
        if i.user != self.ctx.author:
            await i.response.send_message(f'{config.emojis.error} You can\'t do that',ephemeral=True)
            return False
        else:
            return True


class NitroButton(discord.ui.View):
    def __init__(self, m):
        self.m = m
        super().__init__(timeout=30)

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.success, emoji="<:nitro:914110236707680286>")
    async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            embed = discord.Embed(description=f"<:ceres_failure:951863495559872613> You can't do that {interaction.user.mention}!", color=discord.Color.red())
            return await self.ctx.send(embed=embed, delete_after=5)
        button.label = "Claimed"
        button.style = discord.ButtonStyle.danger
        button.emoji = "<:nitro:948879462458589184>"
        button.disabled = True
        await interaction.response.send_message(content="https://imgur.com/NQinKJB", ephemeral=True)
        embed = discord.Embed(description=f"***<:nitro:914110236707680286> {self.ctx.author.mention} claimed the nitro!***", color=discord.Color.nitro_pink())
        embed.set_image(url="https://media.discordapp.net/attachments/886639021772648469/903535585992523796/unknown.png")
        await self.msg.edit(embed=embed, view=self)
    async def on_timeout(self):
        for child in self.children:
            if child.disabled:
                return
        for child in self.children:
            child.disabled = True
        embed = discord.Embed(description=f"*<:ceres_failure:951863495559872613> Looks like either {self.ctx.author.mention} didn't wanna have it or {self.ctx.author.mention} went AFK**", color=discord.Color.red())
        embed.set_image(url="https://media.discordapp.net/attachments/886639021772648469/903535585992523796/unknown.png")
        await self.msg.edit(embed=embed, view=self)

class SupportButton(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Invite Me!", url="https://discord.com/api/oauth2/authorize?client_id=917032103743471627&permissions=8&scope=bot%20applications.commands"))
        self.add_item(discord.ui.Button(label="Support", url="https://discord.gg/ATzc2XQNnM"))
    

class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if interaction.user != view.player1 and interaction.user != view.player2:
            return await interaction.response.send_message(embed=discord.Embed(description="**<:ceres_failure:951863495559872613> This isn't your game!**", color=discord.Color.red()), ephemeral=True)

        elif interaction.user == view.player1 and view.current_player == view.O:
            return await interaction.response.send_message(embed=discord.Embed(description="**<:ceres_failure:951863495559872613> It isn't your turn!**", color=discord.Color.red()), ephemeral=True)

        elif interaction.user == view.player2 and view.current_player == view.X:
            return await interaction.response.send_message(embed=discord.Embed(description="**<:ceres_failure:951863495559872613> It isn't your turn!**", color=discord.Color.red()), ephemeral=True)

        if view.current_player == view.X:
            self.emoji = "<:ttt_x:938666005427793971>"
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = f"It is now {view.player2.mention}'s turn (O)"
        else:
            self.emoji = "<:ttt_o:938666514914107413>"
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = f"It is now {view.player1.mention}'s turn (X)"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = f"{view.player1.mention} won!"
                view.ended = True
            elif winner == view.O:
                content = f"{view.player2.mention} won!"
                view.ended = True
            else:
                content = "It's a tie!"
                view.ended = True

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)



class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1

    def __init__(self, player1: discord.Member, player2: discord.Member, message: discord.Message):
        super().__init__(timeout=80)
        self.Tie = -2
        self.current_player = self.X
        self.player1 =  player1
        self.player2 = player2
        self.ended = False
        self.message = message
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

    async def on_timeout(self):
        if self.ended == True:
            return
        for child in self.children:
            child.disabled = True
        return await self.message.edit(content=None, embed=discord.Embed(description="**<:ceres_failure:951863495559872613> The game ended | Player(s) didn't respond within time!**", color=discord.Color.red()), view=self)


# The ticket views are not added in the repo for some reasons!