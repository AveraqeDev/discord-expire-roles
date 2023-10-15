import logging
from datetime import timedelta, datetime

import discord
from discord.ext import commands
from discord.ext import tasks

from discord_role_expire import db
from discord_role_expire.types import Expiry

log = logging.getLogger(__name__)

TEST_GUILD = discord.Object(id=1162657981175959573)

description = """A bot to automatically expire roles."""

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", description=description, intents=intents)
bot.tree.copy_global_to(guild=TEST_GUILD)


@bot.event
async def on_ready():
    log.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    log.info("--------")
    if not expire_roles.is_running():
        expire_roles.start()


@bot.command()
async def ping(ctx: commands.Context):
    await ctx.send("Pong!")


@bot.hybrid_command(name="add_role")
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


@tasks.loop(seconds=10)
async def expire_roles():
    log.info("Checking for expired roles...")
    for expiry in db.list_expiries():
        if expiry["expires_at"] <= datetime.now():
            log.info("Found expired role:", f"{expiry=}")
            guild = bot.get_guild(expiry["guild_id"])
            member = await guild.fetch_member(expiry["member_id"])
            role = guild.get_role(expiry["role_id"])
            await member.remove_roles(role, reason="Role expired")
            await db.remove(expiry)


@expire_roles.before_loop
async def before_expire_rles():
    await bot.wait_until_ready()
