import random
from datetime import datetime, timezone
import discord
from discord.ext import commands
import database as db

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bounty", aliases=["balance", "bal"])
    async def bounty(self, ctx):
        """Check your current Berry bounty (balance)."""
        user_data = await db.get_user(ctx.author.id, ctx.author.display_name)
        balance = user_data["balance"]
        
        embed = discord.Embed(
            title=f"🏴‍☠️ Bounty Record: {ctx.author.display_name}",
            description=f"**Current Stash:** 🪙 {balance:,} Berries",
            color=discord.Color.gold()
        )
        embed.set_footer(text="The Berry Broker keeps fine books.")
        await ctx.send(embed=embed)

    @commands.command(name="setsail", aliases=["daily"])
    async def setsail(self, ctx):
        """Claim daily Berries like raiding a merchant ship at dawn."""
        user_data = await db.get_user(ctx.author.id, ctx.author.display_name)
        now = datetime.now(timezone.utc)
        
        if user_data["last_daily"]:
            last_daily = datetime.fromisoformat(user_data["last_daily"])
            elapsed = (now - last_daily).total_seconds()
            cooldown = 86400  # 24 hours
            if elapsed < cooldown:
                remaining = int(cooldown - elapsed)
                hours, remainder = divmod(remaining, 3600)
                minutes, _ = divmod(remainder, 60)
                return await ctx.send(
                    f"⚠️ **Calm Belt!** You already raided a ship today. Set sail again in **{hours}h {minutes}m**."
                )

        reward = random.randint(500, 1500)
        await db.update_balance(ctx.author.id, reward)
        await db.update_cooldown(ctx.author.id, "last_daily", now.isoformat())

        embed = discord.Embed(
            title="🌅 Morning Raid Successful!",
            description=f"You ambushed a merchant vessel at dawn and plundered **🪙 {reward:,} Berries**!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name="trade", aliases=["give"])
    async def trade(self, ctx, target: discord.Member, amount: int):
        """Trade Berries with another pirate."""
        if target.bot:
            return await ctx.send("The Broker doesn't keep books for bots.")
        if target.id == ctx.author.id:
            return await ctx.send("You can't trade Berries with yourself!")
        if amount <= 0:
            return await ctx.send("The trade amount must be greater than zero Berries.")

        sender = await db.get_user(ctx.author.id, ctx.author.display_name)
        if sender["balance"] < amount:
            return await ctx.send(f"❌ You don't have enough Berries! Your balance is 🪙 {sender['balance']:,}.")

        await db.get_user(target.id, target.display_name)  # Ensure target exists in DB
        await db.update_balance(ctx.author.id, -amount)
        await db.update_balance(target.id, amount)

        embed = discord.Embed(
            title="🤝 Merchant Trade Completed",
            description=f"**{ctx.author.display_name}** handed over **🪙 {amount:,} Berries** to **{target.display_name}**.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command(name="raid", aliases=["rob"])
    async def raid(self, ctx, target: discord.Member):
        """Attempt to raid a rival crew's stash (chance-based)."""
        if target.bot:
            return await ctx.send("You can't raid a Marine bot!")
        if target.id == ctx.author.id:
            return await ctx.send("Raid your own ship? You're already there!")

        raider = await db.get_user(ctx.author.id, ctx.author.display_name)
        victim = await db.get_user(target.id, target.display_name)

        now = datetime.now(timezone.utc)
        if raider["last_rob"]:
            last_rob = datetime.fromisoformat(raider["last_rob"])
            elapsed = (now - last_rob).total_seconds()
            cooldown = 7200  # 2 hours
            if elapsed < cooldown:
                remaining = int(cooldown - elapsed)
                minutes, seconds = divmod(remaining, 60)
                return await ctx.send(
                    f"⏳ Your crew is recovering from the last raid. Try again in **{minutes}m {seconds}s**."
                )

        if victim["balance"] < 200:
            return await ctx.send(f"**{target.display_name}** is too poor to raid! Leave them be.")

        await db.update_cooldown(ctx.author.id, "last_rob", now.isoformat())

        # 45% Success Rate
        success = random.random() < 0.45

        if success:
            stolen_amount = random.randint(100, min(1000, int(victim["balance"] * 0.35)))
            await db.update_balance(ctx.author.id, stolen_amount)
            await db.update_balance(target.id, -stolen_amount)

            embed = discord.Embed(
                title="⚔️ Raid Successful!",
                description=f"You boarded **{target.display_name}**'s ship in the night and stole **🪙 {stolen_amount:,} Berries**!",
                color=discord.Color.dark_red()
            )
        else:
            penalty = random.randint(100, 400)
            await db.update_balance(ctx.author.id, -penalty)

            embed = discord.Embed(
                title="🛡️ Raid Failed!",
                description=f"**{target.display_name}** caught your crew sneaking aboard! You dropped **🪙 {penalty:,} Berries** while escaping.",
                color=discord.Color.dark_grey()
            )

        await ctx.send(embed=embed)

    @commands.command(name="worstgeneration", aliases=["top", "leaderboard"])
    async def worstgeneration(self, ctx):
        """Display the top 5 richest pirates on the server board."""
        top_pirates = await db.get_top_pirates(5)

        if not top_pirates:
            return await ctx.send("The Broker's ledger is completely blank!")

        description = ""
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

        for idx, pirate in enumerate(top_pirates):
            medal = medals[idx] if idx < len(medals) else "🏴‍☠️"
            description += f"{medal} **{pirate['username']}** — 🪙 {pirate['balance']:,} Berries\n"

        embed = discord.Embed(
            title="📜 The Worst Generation (Top Bounty Board)",
            description=description,
            color=discord.Color.purple()
        )
        embed.set_footer(text="Broker's Ledger • Postings updated live")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))
