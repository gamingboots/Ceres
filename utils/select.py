import discord
import utils.helpers.help as helpems
from discord.ui import Button


class helpselect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=10)
        self.add_item(discord.ui.Button(label="Invite Me!", url="https://discord.com/api/oauth2/authorize?bot_id=919314151535419463&permissions=8&scope=bot%20applications.commands", row=1))
        self.add_item(discord.ui.Button(label="Vote", url="https://top.gg/", row=1))
        self.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/ATzc2XQNnM", row=1))
    @discord.ui.button(label="Delete", style=discord.ButtonStyle.red, emoji="🗑️", row=2)
    async def delete_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()
    @discord.ui.button(label="Home",style=discord.ButtonStyle.primary, emoji="🏠", row=2)
    async def home_button(self, button: discord.ui.Button, i: discord.Interaction):
        await i.response.edit_message(embed=helpems.main_em)
    @discord.ui.select(placeholder="Select a module...",min_values=1,max_values=1,options=[
        discord.SelectOption(label="Moderation",description="Moderation commands to help you moderate your server",emoji="<:moderation:939448699757666304>"),
        discord.SelectOption(label="Utility",description="Utility commands for your server",emoji="<:utility:939449283378311168>"),
        discord.SelectOption(label="Images",description="Part of fun commands related to images",emoji="🖼️"),
        discord.SelectOption(label="Misc",description="Miscellaneous commands",emoji="<:misc:941217770329243679>"),
        discord.SelectOption(label="Ticket",description="Ticket related commands",emoji="🎫"),
        discord.SelectOption(label="Fun",description="Fun commands to entertain you",emoji="<:fun:941216105769336913>"),
        discord.SelectOption(label="Emoji",description="Emoji related commands",emoji="<:blob:956918297406898236>"),
        ])
    async def callback(self,select : discord.ui.Select, i : discord.Interaction):
        if select.values[0] == "Moderation":
            await i.response.edit_message(embed=helpems.mod_em)
        elif select.values[0] == "Utility":
            await i.response.edit_message(embed=helpems.utils_em)
        elif select.values[0] == "Ticket":
            await i.response.edit_message(embed=helpems.ticks_em)
        elif select.values[0] == "Emoji":
            await i.response.edit_message(embed=helpems.emoji_em)
    async def on_timeout(self, select : discord.ui.Select, i : discord.Interaction):
        self.placeholder="Disabled due to timeout!"
        self.disabled = True