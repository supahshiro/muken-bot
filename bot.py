import discord
from discord.ext import commands
import asyncio
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

saved_roles = {}

aizen_quotes = [
    "Fear is necessary for evolution. The fear that one could be destroyed at any moment.",
    "I have not betrayed anyone. Everyone has always been beneath me.",
    "No one stands on top of the world. Not you, not me, not even God.",
    "Admiration is the emotion furthest from understanding.",
    "I have no interest in things that can be described in words.",
    "It is I who is standing in the heavens, not you lowly Soul Reapers.",
    "All creatures want to believe in something greater than themselves.",
]

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def muken(ctx, member: discord.Member, duration: str = None):
    muken_role = discord.utils.get(ctx.guild.roles, name="Muken")
    if muken_role is None:
        await ctx.send("The Muken role doesn't exist!")
        return
    if muken_role in member.roles:
        await ctx.send(f"{member.mention} is already mukened!")
        return
    saved_roles[member.id] = [r for r in member.roles if r != ctx.guild.default_role and r < ctx.guild.me.top_role]
    await member.remove_roles(*saved_roles[member.id])
    await member.add_roles(muken_role)
    if duration:
        seconds = parse_duration(duration)
        if seconds is None:
            await ctx.send(f"Done! {member.mention} has been mukened. (Invalid duration, mukened indefinitely)")
            return
        await ctx.send(f"⛓️ {member.mention} has been sealed in Muken for {duration}. *Hadō #99: Muken*")
        await asyncio.sleep(seconds)
        if muken_role in member.roles:
            await member.remove_roles(muken_role)
            if member.id in saved_roles:
                await member.add_roles(*saved_roles[member.id])
                del saved_roles[member.id]
            await ctx.send(f"🔓 {member.mention}'s sentence is complete. Roles restored.")
    else:
        await ctx.send(f"⛓️ {member.mention} has been sealed in Muken indefinitely. There is no escape.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmuken(ctx, member: discord.Member):
    muken_role = discord.utils.get(ctx.guild.roles, name="Muken")
    if muken_role is None:
        await ctx.send("The Muken role doesn't exist!")
        return
    if muken_role not in member.roles:
        await ctx.send(f"{member.mention} is not mukened!")
        return
    await member.remove_roles(muken_role)
    if member.id in saved_roles:
        await member.add_roles(*saved_roles[member.id])
        del saved_roles[member.id]
        await ctx.send(f"🔓 {member.mention} has been released from Muken. Roles restored.")
    else:
        await ctx.send(f"Muken role removed but no saved roles found for {member.mention}.")

@bot.command()
async def aizen(ctx):
    quote = random.choice(aizen_quotes)
    await ctx.send(f"*Aizen Sosuke:* \"{quote}\"")

@bot.command()
async def weakling(ctx, member: discord.Member):
    await ctx.send(f"{member.mention} — admiration is the emotion furthest from understanding. You are beneath me.")

@bot.command()
async def bankai(ctx, member: discord.Member):
    await ctx.send(f"⚔️ {member.mention} — BANKAI.")

@bot.command()
async def reiatsu(ctx, member: discord.Member):
    level = random.randint(1, 100)
    if level < 20:
        comment = "Pathetic. A Hollow has more reiatsu than this."
    elif level < 50:
        comment = "Average at best. Not worth my time."
    elif level < 80:
        comment = "Respectable. But still nowhere near my level."
    elif level < 100:
        comment = "Impressive. You might actually be useful."
    else:
        comment = "Impossible... this reiatsu rivals my own."
    await ctx.send(f"⚡ {member.mention}'s reiatsu level: **{level}/100** — {comment}")

@bot.command()
async def gimmick(ctx):
    await ctx.send("Watashi No Gimmick Society 😈")

def parse_duration(duration: str):
    try:
        if duration.endswith('s'):
            return int(duration[:-1])
        elif duration.endswith('m'):
            return int(duration[:-1]) * 60
        elif duration.endswith('h'):
            return int(duration[:-1]) * 3600
        elif duration.endswith('d'):
            return int(duration[:-1]) * 86400
        else:
            return None
    except ValueError:
        return None


import os
bot.run(os.environ['TOKEN'])
