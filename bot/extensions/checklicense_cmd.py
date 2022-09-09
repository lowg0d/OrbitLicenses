import hikari
import asyncio
import lightbulb
import bot.managers.mysql_mg as sql_mg
import bot.utils.keygenerator as keygen
from bot import __version__
from bot.utils import cc

plugin = lightbulb.Plugin("checklicense_cmd")

########################################################################
# CHECK LICENSE COMMAND - get the info from a license
@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.option('license', 'license key', required=True)
@lightbulb.command('checklicense', "Get the license key of an user.")
@lightbulb.implements(lightbulb.SlashCommand)
async def checlicense_cmd(ctx: lightbulb.Context) -> None:
    license_ = ctx.options.license

    if sql_mg.sql_fetch_license(license_) == True:
        #get both id and license form the database
        user_id = cc.clean_sql_syntax(
            sql_mg.sql_get_user_id_from_license(license_))
        id_ = cc.clean_sql_syntax(sql_mg.sql_get_license_id(user_id))
        user = cc.clean_sql_syntax(sql_mg.sql_get_user(user_id))
        date_ = cc.clean_sql_syntax(sql_mg.sql_get_date(user_id))

        row = ctx.bot.rest.build_action_row()
        button_1 = row.add_button(
            hikari.ButtonStyle.PRIMARY, "regenerate_license_for_user")
        button_1.set_label(f"Regenerate")
        button_1.add_to_container()

        button_2 = row.add_button(
            hikari.ButtonStyle.DANGER, "delete_license_for_user")
        button_2.set_label(f"Delete")
        button_2.add_to_container()

        tittle = cc.user_own_license_msg.replace("&user", user)

        # send the message
        embed_message = hikari.Embed(
            title=tittle.replace("&id", id_),
            description=f">>> License#{id_}: ||{license_}||\nUser: <@{user_id}>\nCreated at: **{date_}**",
            color=cc.main_color)
        embed_message.set_footer(
            f"@{user}'s license [license#{id_}] - {user_id}")

        message = await ctx.respond(embed_message, flags=hikari.MessageFlag.EPHEMERAL, component=row)
        event_message = await message.message()

        # generate the time out message
        timeout_message = hikari.Embed(
            title=f":timer: Message timed out",
            color=cc.intermediate_color)

        try:
            # Stream interaction create events
            with ctx.bot.stream(hikari.InteractionCreateEvent, timeout=30).filter(
                    # Filter out events that aren't our author and message
                    lambda e: (
                        isinstance(e.interaction, hikari.ComponentInteraction)
                        and e.interaction.user == ctx.author
                        and e.interaction.message == event_message
                    ))as stream:
                async for event in stream:
                    assert isinstance(event.interaction,
                                      hikari.ComponentInteraction)
                    # sort the button input
                    if event.interaction.custom_id == "regenerate_license_for_user":

                        # generate the license
                        new_license = keygen.gen_license()
                        while sql_mg.sql_fetch_license(new_license) == True:
                            new_license = keygen.gen_license()

                        sql_mg.update_license(new_license, user, user_id)

                        confirmation_embed = hikari.Embed(
                            title=cc.sucesfully_regenerated_msg.replace(
                                "&id", id_),
                            description=f">>> License#{id_}: ||{new_license}||\nUser: <@{user_id}>",
                            color=cc.correct_color)

                        confirmation_embed.set_footer(
                            f"[license#{id_}] regenerated for @{user} - {user_id}")
                        await ctx.edit_last_response(
                            confirmation_embed,
                            component=[])

                    elif event.interaction.custom_id == "delete_license_for_user":

                        date_ = cc.clean_sql_syntax(
                            sql_mg.sql_get_date(user_id))
                        sql_mg.sql_delete_license(user_id)

                        confirmation_embed = hikari.Embed(
                            title=cc.sucesfully_deleted_license_msg.replace(
                                "&id", id_),
                            description=f">>> License#{id_}: ||{license_}||\nUser: <@{user_id}>\nCreate at: **{date_}**",
                            color=cc.correct_color)
                        confirmation_embed.set_footer(
                            f"[license#{id_}] deleted for @{user} - {user_id}")

                        await ctx.edit_last_response(
                            confirmation_embed,
                            component=[])
                        return None

        except asyncio.TimeoutError:
            
            print("Timed Out")
            
            await ctx.edit_last_response(
                timeout_message,
                component=[])

    else:
        embed_message = hikari.Embed(
            title=f"License does not exist",
            description=f"**The License Do Not Exist**\n >>> License: '{license_}'",
            color=cc.wrong_color)

        message = await ctx.respond(embed_message, flags=hikari.MessageFlag.EPHEMERAL)
        event_message = await message.message()

########################################################################

@checlicense_cmd.set_error_handler
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
