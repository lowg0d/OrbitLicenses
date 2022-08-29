import hikari
import lightbulb
from bot.utils import cc
from bot import __version__
from bot.bot import globalbot

##################################################################

plugin = lightbulb.Plugin("ping_cmd")

##################################################################

# PING COMMAND
@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command('ping', "The bot's ping.")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping_cmd(ctx: lightbulb.Context) -> None:
    message = hikari.Embed(title=f"PONG !",
                         description=f"*>>> latency: {int(globalbot.heartbeat_latency*1000):.2f}ms*",
                         color=cc.main_color)
    await ctx.respond(message, flags=hikari.MessageFlag.EPHEMERAL)


##################################################################

# VERSION COMMAND
@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command('version', 'the version of the bot.')
@lightbulb.implements(lightbulb.SlashCommand)
async def version_cmd(ctx: lightbulb.Context) -> None:
    message = hikari.Embed(title=f"Orbit Licenses v{__version__}",
                         description=f"*>>> Author: <@814476198733152266>*",
                         color=cc.main_color)

    await ctx.respond(message, flags=hikari.MessageFlag.EPHEMERAL)

##################################################################
# ERROR HANDLING

@ping_cmd.set_error_handler
async def on_ping_error(event: lightbulb.CommandErrorEvent) -> bool:
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond(cc.embed_no_permission, flags=hikari.MessageFlag.EPHEMERAL)
        return True

    return False

@version_cmd.set_error_handler
async def on_version_error(event: lightbulb.CommandErrorEvent) -> bool:
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond(cc.embed_no_permission, flags=hikari.MessageFlag.EPHEMERAL)
        return True

    return False

##################################################################

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)