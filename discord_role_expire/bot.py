import os
from datetime import timedelta, datetime

import discord
from discord.ext import commands
from discord.ext import tasks

from discord_role_expire import db
from discord_role_expire.types import Expiry
from discord_role_expire.checks import is_mod

TEST_GUILD = discord.Object(id=os.getenv("TEST_GUILD"))

description = """A bot to automatically expire roles."""

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", description=description, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("--------")
    if not expire_roles.is_running():
        expire_roles.start()


@bot.command()
@commands.is_owner()
async def sync(ctx: commands.Context):
    print("Syncing commands to Test Guild...")
    bot.tree.copy_global_to(guild=TEST_GUILD)
    commands = await bot.tree.sync()
    message = "Synced commands:\n"
    for idx, command in enumerate(commands):
        message += f"{command}"
        if idx < len(commands):
            message += "\n"
    await ctx.reply(message)
    

@bot.hybrid_command()
@is_mod()
async def ping(ctx: commands.Context):
    await ctx.send("Pong!")


@bot.hybrid_command()
@is_mod()
async def add_role(
    ctx: commands.Context,
    member: discord.Member,
    role: discord.Role,
    duration: int,
):
    expiry = Expiry(
        dict(
            member_id=member.id,
            guild_id=member.guild.id,
            role_id=role.id,
            expires_at=(datetime.now() + timedelta(seconds=duration)),
        )
    )
    await db.insert(expiry)
    await member.add_roles(role, reason=f"Added for {duration}s")
    await ctx.reply(f"Added {role.name} to {member.name} for {duration}s")


@add_role.error
@ping.error
@sync.error
async def command_error(ctx: commands.Context, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("Not allowed...")


@tasks.loop(seconds=30)
async def expire_roles():
    print("Checking for expired roles...")
    for expiry in db.list_expiries():
        if expiry["expires_at"] <= datetime.now():
            print("Found expired role:", f"{expiry=}")
            guild = bot.get_guild(expiry["guild_id"])
            member = await guild.fetch_member(expiry["member_id"])
            role = guild.get_role(expiry["role_id"])
            await member.remove_roles(role, reason="Role expired")
            await db.remove(expiry)


@expire_roles.before_loop
async def before_expire_rles():
    await bot.wait_until_ready()
