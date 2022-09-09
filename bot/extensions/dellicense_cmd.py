import hikari
import asyncio
import lightbulb
import bot.managers.mysql_mg as sql_mg
import bot.managers.license_mg as license_mg
from bot import __version__
from bot.utils import cc

plugin = lightbulb.Plugin("dellicense_cmd")

########################################################################
# DELETE LICENSE COMMAND - delete an exisitng license from the database
@plugin.command
# ADMINISTRATOR permission needed for execute
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.option('user', 'user id', hikari.User, required=True)
@lightbulb.command('dellicense', "Delte an existing license.")
@lightbulb.implements(lightbulb.SlashCommand)
async def dellicense_cmd(ctx: lightbulb.Context) -> None:

    # get the user from the options & get the user's id
    user = ctx.options.user
    user_id = user.id

    # check if there is instance of user discord id in the database
    if license_mg.check_if_user_on_db(user_id) == True:
        # if there is isntace, delete user's license from the database
        try:
            # get both id and license form the database
            id_ = cc.clean_sql_syntax(sql_mg.sql_get_license_id(user_id))
            license_ = cc.clean_sql_syntax(sql_mg.sql_get_license(user_id))
            date_ = cc.clean_sql_syntax(sql_mg.sql_get_date(user_id))

            ## (
            # generate the confirmation message
            msg = hikari.Embed(
                title=f"Are you sure you want to delete [License#{id_}]",
                description=f">>> Owned by: <@{user_id}>\nCreated at: **{date_}**",
                color=cc.intermediate_color)

            # generate the time out message
            timeout_message = hikari.Embed(
                title=f":timer: Message timed out",
                color=cc.intermediate_color)

            row = ctx.bot.rest.build_action_row()
            button_1 = row.add_button(hikari.ButtonStyle.SUCCESS, "yes")
            button_1.set_label(f"Yes")
            button_1.add_to_container()

            button_2 = row.add_button(hikari.ButtonStyle.DANGER, "no")
            button_2.set_label(f"No")
            button_2.add_to_container()

            # send the message
            message = await ctx.respond(msg, flags=hikari.MessageFlag.EPHEMERAL,
                                        component=row)

            event_message = await message.message()
            ## )

            try:
                # Stream interaction create events
                with ctx.bot.stream(hikari.InteractionCreateEvent, 10).filter(
                        # Filter out events that aren't our author and message
                        lambda e: (
                            isinstance(e.interaction,
                                       hikari.ComponentInteraction)
                            and e.interaction.user == ctx.author
                            and e.interaction.message == event_message
                        ))as stream:
                    async for event in stream:
                        assert isinstance(event.interaction,
                                          hikari.ComponentInteraction)
                        # sort the button input
                        if event.interaction.custom_id == "yes":

                            sql_mg.sql_delete_license(user_id)

                            confirmation_embed = hikari.Embed(
                                title=cc.sucesfully_deleted_license_msg.replace(
                                    "&id", id_),
                                description=f">>> License#{id_}: ||{license_}||\nUser: <@{user_id}>",
                                color=cc.correct_color)
                            confirmation_embed.set_footer(
                                f"[license#{id_}] deleted for @{user} - {user_id}")

                            await ctx.edit_last_response(
                                confirmation_embed,
                                components=[])
                            return None

                        elif event.interaction.custom_id == "no":
                            skipped_embed = hikari.Embed(
                                title=f"[Licence#{id_}] deleting skipped Sucesfully",
                                color=cc.correct_color)

                            await ctx.edit_last_response(
                                skipped_embed,
                                component=[])
                            return None

            except asyncio.TimeoutError:
                await message.edit(timeout_message, component=[])

        except:
            # in case there is an error executing the above code, send a error message
            message = hikari.Embed(title=f":no_entry_sign: Unknown error deleting the license",
                                   color=cc.wrong_color)
            await ctx.respond(message, flags=hikari.MessageFlag.EPHEMERAL)

    # if there is not instance, return a error message
    else:
        # generate the error message
        message = hikari.Embed(title=f":no_entry_sign: Error deleting the license",
                               description=f">>> user <@{user_id}> has no license registered.",
                               color=cc.wrong_color)

        # send the error message
        await ctx.respond(message, flags=hikari.MessageFlag.EPHEMERAL)

#################################################################
# ERROR HANDLING
@dellicense_cmd.set_error_handler
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
