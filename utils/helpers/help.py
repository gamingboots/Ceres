import discord


main_em=discord.Embed(
            title="***CERES HELP***",
            description=f"""
            > I am an open source multi feature discord bot based on\n> <:slash:940890213926965329>Application commands.\n
            **Please use the select menu to navigate the coressponding categories!**\n
            [Invite](dsc.gg/ceresbot) | [Source!](https://github.com/gamingboots/Ceres) | [Vote](https://top.gg/bot/919314151535419463) | [Support](https://discord.gg/ATzc2XQNnM)
            """,
        )
main_em.add_field(name="<:modules:939446528475533393> **Modules:**",value="**• Fun**\n**• Moderation**\n**• Utility**\n**• Misc**\n**• Images**\n**Ticekt**")
main_em.add_field(name="**<:soontm:956839952325414942> Plans**",value="**•AUTOMOD**\n**•IMPROVED TICKET SYSTEM**\n**•MUSIC SYSTEM**\n**•ALOT MORE**")
main_em.colour = discord.Color.embed_background()


mod_em=discord.Embed(title="Moderation Module",description="`timeout` - Mutes the member for the mentioned amount of time\n`unmute` - Unmute the member if muted\n`kick` - Kicks a member for specific reason\n`ban` - Ban a member for misbehaving\n`unban` - You can unban a member if banned\n`slowmode` - Adds slowmode on a channel\n`role` - Adds or removes a role from the specified user\n`purge` - Delets the mentioned amount of messages\n`nuke` - Deletes the current channel and makes a new one\n",color=discord.Color.embed_background())
utils_em=discord.Embed(title="Utility Module",description="`avatar` - Gets the avatar of a user\n`nick` - Changes the nickname of a user\n`lock` - Locks the current channel\n`unlock` - Unlocks the current channel\n`userinfo` - Gets the information of a user\n`serverinfo` - Gets the server information\n`membercount` - Gets the number of members in the server\n`msgcount` - Gets the number of messages in the channel\n`embed` - Build an embed\n`support` - Sends the invite to the support server of the bot",color=discord.Color.embed_background())
emoji_em=discord.Embed(title="Emoji Module",description="`emoji rename` - Renames an emoji\n`emoji enlarge` - Sends an emoji enlarged\n`emoji remove` - Removes or deletes an emoji from the server\n`emojify` - Converts text to emoji\n`emoji stats` - Returns the emoji stats of the server\n`emojiadd` - adds an emoji from url\n`emoji steal` - Adds an emoji from a discord emoji",color=discord.Color.embed_background())
ticks_em=discord.Embed(title="Ticket Module",description="`panel create` - Creates a panel in the mentioned channel\n`panel delete` - Deletes the panel with the panel id\n`ticket category` - Sets the category for the tickets\n`ticket cleanup` - Delets all the tickets present in the server\n`ticket role` - Adds a role to the ticket\n`ticket reset` - Resets the ticket count of the server\n`ticket close` - Closes a ticket",color=discord.Color.embed_background())
