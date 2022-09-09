import hikari
import asyncio
import lightbulb
import bot.managers.mysql_mg as sql_mg
from bot import __version__
from bot.utils import cc

plugin = lightbulb.Plugin("userliust_cmd")

########################################################################
# REGENLICENSE COMMAND - regenerate a existing license


@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command('userlist', "Return all the user with licenses in the server.")
@lightbulb.implements(lightbulb.SlashCommand)
async def userliust_cmd(ctx: lightbulb.Context) -> None:

    userlist = sql_mg.sql_get_license_user_list()
    
    userlist_string = ""
    
    user_with_licenses = 0
    
    for user, creation_date, id_ in userlist:
        user_with_licenses += 1
        user_id = cc.clean_sql_syntax(user)
        creation_date_ = cc.clean_sql_syntax(creation_date)
        userlist_string += f":green_circle: <@{user_id}> - **#{id_}** - *{creation_date_}*\n"
        
    message = hikari.Embed(title=f"list of all users with licenses",
                            color=cc.main_color)
    
    message.add_field("Count", f">>> Total: **{user_with_licenses}**", inline=True)
    message.add_field("Licenses", f">>> {userlist_string}")
    
    message.set_footer("All the users with active licenses.")
    
    await ctx.respond(message, flags=hikari.MessageFlag.EPHEMERAL)

########################################################################


@userliust_cmd.set_error_handler
async def on_ping_error(event: lightbulb.CommandErrorEvent) -> bool:
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
