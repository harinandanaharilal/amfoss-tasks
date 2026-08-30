import random
import discord
from discord.ext import commands
import database as db

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="duel", aliases=["rps"])
    async def duel(self, ctx, choice: str = None, wager: int = 100):
        """Swordfight RPS vs the bot for Berries. Usage: !duel <rock|paper|scissors> [wager]"""
        valid_choices = {"rock": "🪨", "paper": "📜", "scissors": "⚔️"}
        
        if not choice or choice.lower() not in valid_choices:
            return await ctx.send("⚠️ You must pick a weapon! Usage: `!duel <rock|paper|scissors> [wager]`")
        
        user_choice = choice.lower()
        if wager <= 0:
            return await ctx.send("⚠️ Your wager must be greater than 0 Berries.")

        user_data = await db.get_user(ctx.author.id, ctx.author.display_name)
        if user_data["balance"] < wager:
            return await ctx.send(f"❌ You don't have **🪙 {wager:,} Berries** to bet on this duel!")

        bot_choice = random.choice(list(valid_choices.keys()))
        
        # Determine winner
        if user_choice == bot_choice:
            result = "draw"
        elif (
            (user_choice == "rock" and bot_choice == "scissors") or
            (user_choice == "paper" and bot_choice == "rock") or
            (user_choice == "scissors" and bot_choice == "paper")
        ):
            result = "win"
        else:
            result = "lose"

        user_icon = valid_choices[user_choice]
        bot_icon = valid_choices[bot_choice]

        if result == "draw":
            embed = discord.Embed(
                title="⚔️ Duel Stalemate!",
                description=f"You chose {user_icon} **{user_choice.title()}**, Broker chose {bot_icon} **{bot_choice.title()}**.\n"
                            f"Blades clashed and bounced! Your **🪙 {wager:,} Berries** remain safe.",
                color=discord.Color.gold()
            )
        elif result == "win":
            await db.update_balance(ctx.author.id, wager)
            embed = discord.Embed(
                title="⚔️ Victory in Duel!",
                description=f"You chose {user_icon} **{user_choice.title()}**, Broker chose {bot_icon} **{bot_choice.title()}**.\n"
                            f"You disarmed the Broker and claimed **🪙 {wager:,} Berries**!",
                color=discord.Color.green()
            )
        else:
            await db.update_balance(ctx.author.id, -wager)
            embed = discord.Embed(
                title="⚔️ Defeat in Duel!",
                description=f"You chose {user_icon} **{user_choice.title()}**, Broker chose {bot_icon} **{bot_choice.title()}**.\n"
                            f"The Broker struck you down! You lost **🪙 {wager:,} Berries**.",
                color=discord.Color.red()
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Games(bot))