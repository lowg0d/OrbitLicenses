import hikari
import asyncio
import lightbulb
import bot.managers.mysql_mg as sql_mg
import bot.utils.keygenerator as keygen
import bot.managers.license_mg as license_mg
from bot import __version__
from bot.utils import cc

plugin = lightbulb.Plugin("genlicense_cmd")

########################################################################
# GENERATE LICENSE COMMAND - generate a new license for an user // in case the user has a license it reply to you with the license
# and the option to delete or regenerate the license
@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.option('user', 'user id', hikari.User, required=True)
@lightbulb.command('genlicense', "Delte an existing license.")
@lightbulb.implements(lightbulb.SlashCommand)
async def genlicense_cmd(ctx: lightbulb.Context) -> None:

    # get the user from the options & get the user's id
    user = ctx.options.user
    user_id = user.id
    
    # check if there is instance of user discord id in the database
    if license_mg.check_if_user_on_db(user_id) == False:  
        try:
            # get both id and license form the database
            id_ = cc.clean_sql_syntax(sql_mg.sql_get_license_id(user_id))
            license_ = cc.clean_sql_syntax(sql_mg.sql_get_license(user_id))

            ## (
            # generate the confirmation message
            msg = hikari.Embed(
                title=f"Are you sure you want to generate @{user}'s license",
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
                        isinstance(e.interaction, hikari.ComponentInteraction)
                        and e.interaction.user == ctx.author
                        and e.interaction.message == event_message
                ))as stream:
                    async for event in stream:
                        assert isinstance(event.interaction, hikari.ComponentInteraction)
                        # sort the button input
                        if event.interaction.custom_id == "yes":
            
                            # generate the license
                            new_license = keygen.gen_license()
                            while sql_mg.sql_fetch_license(new_license) == True:
                                new_license = keygen.gen_license()
                            
                            # store the new license in the database
                            sql_mg.sql_store_license(f"{new_license}", f"{user}", f"{user_id}")
                            
                            # get both id and license form the database
                            id_ = cc.clean_sql_syntax(sql_mg.sql_get_license_id(user_id))
                            
                            tittle = cc.sucesfully_generated_license_for_msg.replace("&id", id_)
                            
                            # send the confirmation message
                            sucesfully_embed = hikari.Embed(
                                                title=tittle.replace("&user", user),
                                                description=f">>> License#{id_}: ||{new_license}||\nUser: <@{user_id}>",
                                                color=cc.correct_color)
                            sucesfully_embed.set_footer(f"[license#{id_}] generated for @{user} - {user_id}")
                            
                            await ctx.edit_last_response(
                                sucesfully_embed,
                                component=[])
                            return None

                        elif event.interaction.custom_id == "no":
                            skipped_embed = hikari.Embed(
                                                title=f"License generation sucesfully cancelled",
                                                color=cc.correct_color)
                            await ctx.edit_last_response(
                                skipped_embed,
                                component=[])
                            return None
            
            except asyncio.TimeoutError:
                await message.edit(timeout_message, components=[])
          
        except:
            message = hikari.Embed(title=f":no_entry_sign: Error generating the license",
                            color=cc.wrong_color)
            await ctx.respond(message, flags=hikari.MessageFlag.EPHEMERAL)
        
    else:
        # get both id and license form the database
        id_ = cc.clean_sql_syntax(sql_mg.sql_get_license_id(user_id))
        license_ = cc.clean_sql_syntax(sql_mg.sql_get_license(user_id))
        date_ = cc.clean_sql_syntax(sql_mg.sql_get_date(user_id))
        
        # generate the time out message
        timeout_message = hikari.Embed(
            title=f":timer: Message timed out",
            color=cc.intermediate_color)
        
        row = ctx.bot.rest.build_action_row()
        button_1 = row.add_button(hikari.ButtonStyle.PRIMARY, "regenerate_license_for_user")
        button_1.set_label(f"Regenerate")
        button_1.add_to_container()
        
        button_2 = row.add_button(hikari.ButtonStyle.DANGER, "delete_license_for_user")
        button_2.set_label(f"Delete")
        button_2.add_to_container()
        
        # send the message
        embed_message = hikari.Embed(
                            title=f"@{user}'s owns [license#{id_}] already",
                            description=f">>> License#{id_}: ||{license_}||\nUser: <@{user_id}>\nCreated at: **{date_}**",
                            color=cc.main_color)
        embed_message.set_footer(f"@{user}'s license [license#{id_}] - {user_id}")
        
        message = await ctx.respond(embed_message, flags=hikari.MessageFlag.EPHEMERAL ,component=row)
        event_message = await message.message()
        
        # generate the time out message
        timeout_message = hikari.Embed(
            title=f":timer: Message timed out",
            color=cc.intermediate_color)
        
        try:
            # Stream interaction create events
            with ctx.bot.stream(hikari.InteractionCreateEvent, 10).filter(
                # Filter out events that aren't our author and message
                lambda e: (
                    isinstance(e.interaction, hikari.ComponentInteraction)
                    and e.interaction.user == ctx.author
                    and e.interaction.message == event_message
            ))as stream:
                async for event in stream:
                    assert isinstance(event.interaction, hikari.ComponentInteraction)
                    # sort the button input
                    if event.interaction.custom_id == "regenerate_license_for_user":
                        
                        # generate the license
                        new_license = keygen.gen_license()
                        while sql_mg.sql_fetch_license(new_license) == True:
                            new_license = keygen.gen_license()
                            
                        sql_mg.update_license(new_license, user, user_id)
                        
                        confirmation_embed = hikari.Embed(
                            title=cc.sucesfully_regenerated_msg.replace("&id", id_),
                            description=f">>> License#{id_}: ||{new_license}||\nUser: <@{user_id}>",
                            color=cc.correct_color)
                        
                        confirmation_embed.set_footer(f"[license#{id_}] regenerated for @{user} - {user_id}")                    
                        await ctx.edit_last_response(
                            confirmation_embed,
                            components=[])
                    
                    elif event.interaction.custom_id == "delete_license_for_user":
                        
                        sql_mg.sql_delete_license(user_id) 
                        
                        confirmation_embed = hikari.Embed(
                                            title=f"[license#{id_}] Sucesfully deleted ",
                                            description=f">>> License#{id_}: ||{license_}||\nUser: <@{user_id}>",
                                            color=cc.correct_color)
                        confirmation_embed.set_footer(f"[license#{id_}] deleted for @{user} - {user_id}")
                        
                        await ctx.edit_last_response(
                            confirmation_embed,
                            components=[])
                        return None
                
        except asyncio.TimeoutError:
            await message.edit(timeout_message, components=[])

                        
        except asyncio.TimeoutError:
            await message.edit(timeout_message, components=[])

########################################################################

@genlicense_cmd.set_error_handler
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