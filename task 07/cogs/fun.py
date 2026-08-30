import random
import aiohttp
import discord
from discord.ext import commands

ONE_PIECE_ROASTS = [
    "You have a lower bounty than a Buggy's Delivery rookie!",
    "Even Usopp wouldn't believe a word coming out of your mouth.",
    "Your crew's navigator must be Zoro, because you are completely lost.",
    "You look like you accidentally swallowed the Weak-Weak Fruit.",
    "The Marines wouldn't even print a poster for a pirate like you.",
    "Sanji wouldn't even cook food scraps for a scallywag of your caliber.",
    "Your pirate emblem looks like it was drawn by a Sea Beast with a crayon.",
    "You're the kind of pirate who gets seasick on a docked ship."
]

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="logpose")
    async def logpose(self, ctx):
        """Spin the Log Pose for random One Piece intel from an API."""
        async with ctx.typing():
            category = random.choice(["monsters", "fruits"])
            url = f"https://api.api-onepiece.com/v2/{category}/en"

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=5) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            item = random.choice(data)

                            if category == "fruits":
                                title = f"🍇 Devil Fruit Intel: {item.get('filename', 'Unknown Fruit')}"
                                desc = f"**Type:** {item.get('type', 'Unknown')}\n\n{item.get('description', 'No details recorded in the Grand Line files.')}"
                            else:
                                title = f"🐉 Sea Intel: {item.get('name', 'Unknown Creature')}"
                                desc = item.get('description', 'A dangerous creature spotted in the Grand Line depths.')

                            embed = discord.Embed(title=title, description=desc, color=discord.Color.teal())
                            embed.set_footer(text="Log Pose lock acquired • Grand Line Archives")
                            return await ctx.send(embed=embed)
            except Exception:
                pass

            # Fallback intel if the public API request fails or times out
            fallback_intel = [
                ("🏴‍☠️ Ancient Map", "You uncovered coordinates pointing towards an uncharted island near Skypiea!"),
                ("🍈 Devil Fruit Rumor", "Word is the Gomu Gomu no Mi was recently spotted in a Marine convoy."),
                ("⚓ Sea Monster Alert", "A giant Sea King was sighted floating near the Calm Belt borders.")
            ]
            title, desc = random.choice(fallback_intel)
            embed = discord.Embed(title=title, description=desc, color=discord.Color.dark_teal())
            embed.set_footer(text="Log Pose magnetic wobble • Local rumors")
            await ctx.send(embed=embed)

    @commands.command(name="roast")
    async def roast(self, ctx, target: discord.Member):
        """Hurl a pirate-themed insult at a rival pirate."""
        if target.id == ctx.author.id:
            return await ctx.send("Don't roast yourself, matey—the Grand Line will do that for you!")
        
        insult = random.choice(ONE_PIECE_ROASTS)
        await ctx.send(f"🏴‍☠️ **{target.mention}**, {insult}")

async def setup(bot):
    await bot.add_cog(Fun(bot))