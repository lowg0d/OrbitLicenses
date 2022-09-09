import hikari
import lightbulb
import bot.managers.mysql_mg as sql_mg
import bot.utils.keygenerator as keygen
import bot.managers.license_mg as license_mg
from bot import __version__
from bot.utils import cc

plugin = lightbulb.Plugin("license_cmd")

########################################################################
# LICENSE COMMAND - generate a new license or get an existing license from the database
@plugin.command
# 5 seccond cooldown
@lightbulb.add_cooldown(5, 1, lightbulb.UserBucket)
# SEND_MESSAGES permission needed for execute
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.SEND_MESSAGES))
@lightbulb.command('license', "Generate a new license or Get your existing license.")
@lightbulb.implements(lightbulb.SlashCommand)
async def license_cmd(ctx: lightbulb.Context) -> None:

    #get the user from the options & get the user's id
    user = ctx.user
    user_id = ctx.user.id

    #check if there is instance of user discord id in the database
    if license_mg.check_if_user_on_db(user_id) == True:
        # if there is instance, respond with the license associated to the user id

        #get both id and license form the database
        id_ = cc.clean_sql_syntax(sql_mg.sql_get_license_id(user_id))
        license_ = cc.clean_sql_syntax(sql_mg.sql_get_license(user_id))
        date_ = cc.clean_sql_syntax(sql_mg.sql_get_date(user_id))

        # send the license to the user
        message = hikari.Embed(title=cc.you_own_license_msg.replace("&id", id_),
                               description=f">>> License#{id_}: ||{license_}||\nCreated at: **{date_}**",
                               color=cc.main_color)

        message.set_footer(
            "You can only create a lisence once. If you have a problem open a ticket.")
        await ctx.respond(message, flags=hikari.MessageFlag.EPHEMERAL)

    # if there is not instance, generate a new license associated to the user id
    else:
        try:
            #generate new license and upload it to the database
            new_license_ = license_mg.generate_new_license(user_id, user)

        except:
            message = hikari.Embed(title="<:icons_outage:996016805049028649> Error storing the license",
                                   color=cc.wrong_color)
            await ctx.respond(message, flags=hikari.MessageFlag.EPHEMERAL)

        # get id from the database & send confirmation message
        id_ = cc.clean_sql_syntax(sql_mg.sql_get_license_id(user_id))

        # generate confirmation message
        message = hikari.Embed(title=cc.sucesfully_generated_license_msg,
                               description=f">>> License#{id_}: ||{new_license_}||",
                               color=cc.correct_color)

        # send confirmation message
        message.set_footer(
            "This license can be used in any of our plugins. If you have any problem open a ticket.")
        await ctx.respond(message, flags=hikari.MessageFlag.EPHEMERAL)
        
#################################################################
# ERROR HANDLING
@license_cmd.set_error_handler
async def on_ping_error(event: lightbulb.CommandErrorEvent) -> bool:
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond(cc.embed_no_permission, flags=hikari.MessageFlag.EPHEMERAL)
        return True

    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        message = hikari.Embed(title=f":no_entry_sign: This command is in cooldown",
                               description=f">>> Time Remaining: **{keygen.time_conversion(int(exception.retry_after))}**.",
                               color=cc.wrong_color)

        message.set_footer(
            "If you generated a license by error, or have any issue open a ticket.")

        await event.context.respond(message,
                                    flags=hikari.MessageFlag.EPHEMERAL)
        return True

    return False

##################################################################
def load(bot):
    bot.add_plugin(plugin) 
def unload(bot):
    bot.remove_plugin(plugin)
