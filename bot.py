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

weakling_quotes = [
    "admiration is the emotion furthest from understanding. You are beneath me.",
    "You were never even worth the effort of defeating.",
    "Did you really think you could challenge me? How disappointing.",
    "I have not once considered you a threat. Not even for a moment.",
    "You are nothing more than a stepping stone on my path to the heavens.",
    "Your existence is so insignificant I almost forgot you were there.",
    "Even your despair is boring to me.",
    "You fought well. Unfortunately, well was never going to be enough.",
    "I expected more from you. I was wrong to even expect that much.",
    "ratio'd + no maidens + your reiatsu is mid + Aizen would never.",
    "Everything has gone according to my plan. Including your failure.",
]

@bot.command()
async def weakling(ctx, member: discord.Member):
    quote = random.choice(weakling_quotes)
    await ctx.send(f"{member.mention} — {quote}")


@bot.command()
async def bankai(ctx, member: discord.Member):
    await ctx.send(f"⚔️ {member.mention} — BANKAI.")

@bot.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def reiatsu(ctx, member: discord.Member):
    role_names = [r.name.lower() for r in member.roles]
    admin_roles = ["head captain", "soul king", "shadow government"]
    mod_roles = ["vice lieutenant"]
    captain_roles = ["captain", "lieutenant"]
    if member.guild_permissions.administrator or any(r in role_names for r in admin_roles):
        level = random.randint(150, 999)
        comment = "This reiatsu... it's incomprehensible. The very air bends around them!"
    elif any(r in role_names for r in mod_roles):
        level = random.randint(70, 120)
        if level < 100:
            comment = "A powerful reiatsu. Captain level at minimum."
        else:
            comment = "Impossible... this reiatsu is off the charts."
    elif any(r in role_names for r in captain_roles):
        level = random.randint(70, 100)
        if level < 85:
            comment = "Respectable. Vice Lieutenant level reiatsu."
        else:
            comment = "Impressive. This is captain level reiatsu."
    else:
        level = random.randint(1, 69)
        if level < 20:
            comment = "Pathetic. A Hollow has more reiatsu than this."
        elif level < 50:
            comment = "Average at best. Not worth my time."
        else:
            comment = "Not terrible. But nowhere near captain level."
    await ctx.send(f"⚡ {member.mention}'s reiatsu level: **{level}/100** — {comment}")

@reiatsu.error
async def reiatsu_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        hours = int(error.retry_after // 3600)
        minutes = int((error.retry_after % 3600) // 60)
        await ctx.send(f"{ctx.author.mention} — your reiatsu has already been measured mongrel. Try again in {hours}h {minutes}m.")






    
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
