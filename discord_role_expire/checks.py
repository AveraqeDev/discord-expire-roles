import os
from discord.ext import commands

MOD_ROLE = int(os.getenv("MOD_ROLE"))

def is_mod():
    async def predicate(ctx: commands.Context):
        return ctx.author.get_role(MOD_ROLE) is not None
    return commands.check(predicate)