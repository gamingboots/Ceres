import discord                      #IMPORTS
from typing import List             #^


async def memberCheck(guild: discord.Guild) -> List[int]:#making a function to check a member from a guild
    """Returns the memberList which contains memberIDs of all members combined"""
    memberList = []#member list
    for member in guild.members:#looping through the guild members
        memberList.append(member.id)#adding member id to the list
    return memberList#returning




class NitroButton(discord.ui.View):#nitro button class
    def __init__(self, m):
        self.m = m
        super().__init__(timeout=30)

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.success, emoji="<:nitro:914110236707680286>")#button decorator
    async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):#making the interaction
        if interaction.user != self.ctx.author:#making sure the person to interact is the user only
            embed = discord.Embed(description=f"<:ceres_failure:951863495559872613> You can't do that {interaction.user.mention}!", color=discord.Color.red())
            return await self.ctx.send(embed=embed, delete_after=5)
        button.label = "Claimed"#this will become the label of the button after its clicked(having this will give a good impression)
        button.style = discord.ButtonStyle.danger#this would be the button colour after the click an  ^
        button.emoji = "<:nitro:948879462458589184>"#button emoji after the click and                 ^
        button.disabled = True#we will make it disabled to make it work properly and                  ^
        await interaction.response.send_message(content="https://imgur.com/NQinKJB", ephemeral=True)#responding with a rickroll gif on the click only visible the the person who clicked the button so that other people try the command 😂
        embed = discord.Embed(description=f"***<:nitro:914110236707680286> {self.ctx.author.mention} claimed the nitro!***", color=discord.Color.nitro_pink())#making the embed which will be displayed after the click
        embed.set_image(url="https://media.discordapp.net/attachments/886639021772648469/903535585992523796/unknown.png")
        await self.msg.edit(embed=embed, view=self)#editing the message
    async def on_timeout(self):#timeout when the user goes afk(to save our resources and prevent weird errors)
        for child in self.children:#looping through the buttons
            if child.disabled:#checking if the button is already disabled
                return#if its true then returning
        for child in self.children:#if the above check is false then again looping through the buttons
            child.disabled = True#now finally disabling them
        embed = discord.Embed(description=f"*<:ceres_failure:951863495559872613> Looks like either {self.ctx.author.mention} didn't wanna have it or {self.ctx.author.mention} went AFK**", color=discord.Color.red())
        embed.set_image(url="https://media.discordapp.net/attachments/886639021772648469/903535585992523796/unknown.png")
        await self.msg.edit(embed=embed, view=self)#editing the message after timeout

class SupportButton(discord.ui.View):#support view stup
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Invite Me!", url="https://discord.com/api/oauth2/authorize?client_id=917032103743471627&permissions=8&scope=bot%20applications.commands"))#adding invite link button 
        self.add_item(discord.ui.Button(label="Support", url="https://discord.gg/ATzc2XQNnM"))#adding support server link button
    

class TicTacToeButton(discord.ui.Button["TicTacToe"]):#tictactoe button class setup
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):#making the callbackk
        assert self.view is not None#continuing the statement if the view is not none
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if interaction.user != view.player1 and interaction.user != view.player2:#checking if the players are in the game if not then responding and returning
            return await interaction.response.send_message(embed=discord.Embed(description="**<:ceres_failure:951863495559872613> This isn't your game!**", color=discord.Color.red()), ephemeral=True)

        elif interaction.user == view.player1 and view.current_player == view.O:#checking if the users are clicking the buttons out of turn and preventing that
            return await interaction.response.send_message(embed=discord.Embed(description="**<:ceres_failure:951863495559872613> It isn't your turn!**", color=discord.Color.red()), ephemeral=True)

        elif interaction.user == view.player2 and view.current_player == view.X:#Same check as above
            return await interaction.response.send_message(embed=discord.Embed(description="**<:ceres_failure:951863495559872613> It isn't your turn!**", color=discord.Color.red()), ephemeral=True)

        if view.current_player == view.X:#responding to the clicks and adding the emoji of X
            self.emoji = "<:ttt_x:938666005427793971>"#changing the emoji
            self.disabled = True#disabling the button to not make the code anymore complicated
            view.board[self.y][self.x] = view.X#declaring the current player
            view.current_player = view.O#changing the current player in the variable
            content = f"It is now {view.player2.mention}'s turn (O)"
        else:#having an else instead of another check 
            self.emoji = "<:ttt_o:938666514914107413>"#changing the emoji
            self.disabled = True#disabling the button to not make the code anymore complicated
            view.board[self.y][self.x] = view.O#declaring the current player
            view.current_player = view.X#changing the current player by editing the variable
            content = f"It is now {view.player1.mention}'s turn (X)"

        winner = view.check_board_winner()#calling the function defined in the tictactoe class below
        if winner is not None:#working when the winner is not None
            if winner == view.X:#responding when the winner is X you can check that in the class below
                content = f"{view.player1.mention} won!"
                view.ended = True#endinig the game by changing the value of ended variable
            elif winner == view.O:#checking the winner
                content = f"{view.player2.mention} won!"
                view.ended = True#ending the game
            else:#when both the conditions are false it means its a tie so responing on that
                content = "It's a tie!"
                view.ended = True#ending the game

            for child in view.children:#looping through the buttons in the view
                child.disabled = True#disabling them all

            view.stop()#stopping the game.

        await interaction.response.edit_message(content=content, view=view)#in the code you might see content we are using that to make it easier to respond


class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1

    def __init__(self, player1: discord.Member, player2: discord.Member, message: discord.Message):
        super().__init__(timeout=80)
        self.Tie = -2#when the board's sum will be -2 it will be declared a tie so a variable to indicate that
        self.current_player = self.X#variable for the current player which is X
        self.player1 =  player1#player1 is a discord.Member object as defined
        self.player2 = player2#^
        self.ended = False#declaring the end variable
        self.message = message#message is a discord.Message object as defined
        self.board = [#this board variable is based on maths which makes the concept easier
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):#checking the game's winner
        for across in self.board:#looping through the values int he game
            value = sum(across)#adding the values
            if value == 3:#the value will be 3 if the O player got a win in the board anywhere(as its looped in across)
                return self.O#declaring the winner as O
            elif value == -3:#if the X player got a win in the board the value will be -3 hence this check
                return self.X#declaring the winner as X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]#adding the values in range to check the winner
            if value == 3:#if the value is 3 then declaring O as the winner
                return self.O
            elif value == -3:#else X as the winner
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]#adding the values
        if diag == 3:#if the evaluation is equal to 3 this will declare O as the winner
            return self.O
        elif diag == -3:#X as the winner
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]#almost the same as above
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        if all(i != 0 for row in self.board for i in row):#checking if the game nded in a tie
            return self.Tie

        return None

    async def on_timeout(self):#making a timeout function to prevent wastage of resources if the players went afk
        if self.ended == True:#editing the variable and ending the game
            return
        for child in self.children:#looping through the buttons
            child.disabled = True#disabling the buttons
        return await self.message.edit(content=None, embed=discord.Embed(description="**<:ceres_failure:951863495559872613> The game ended | Player(s) didn't respond within time!**", color=discord.Color.red()), view=self)#telling the players that the game ended because either of the players went afk


# The ticket views are not added in the repo for some reasons(@27Saumya knows them 🤣)!