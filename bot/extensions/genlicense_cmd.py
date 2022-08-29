from logging import exception
from msilib.schema import Component
import hikari
import asyncio
import lightbulb
import bot.managers.mysql_mg as sql_mg
import bot.utils.keygenerator as keygen
import bot.managers.license_mg as license_mg

from bot import __version__
from bot.utils import cc

# license managament commands

plugin = lightbulb.Plugin("genlicense_cmd")

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
        
        # send the license to the user
        message = hikari.Embed(title=
        f"You own [license#{id_}] already.",
                            description=
        f">>> License#{id_}: ||{license_}||",
                            color=cc.main_color)
                
        message.set_footer("You can only create a lisence once. If you have a problem open a ticket.")
        await ctx.respond(message, flags=hikari.MessageFlag.EPHEMERAL)

    # if there is not instance, generate a new license associated to the user id 
    else:
        try:
            #generate new license and upload it to the database
            new_license = license_mg.generate_new_license(user_id, user)
        except:
            message = hikari.Embed(title=
            f":no_entry_sign: Error storing the license",
                            color=cc.wrong_color)
            await ctx.respond(message, flags=hikari.MessageFlag.EPHEMERAL)
            
        # get id from the database & send confirmation message
        id_ = cc.clean_sql_syntax(sql_mg.sql_get_license_id(user_id))
        
        # generate confirmation message
        message = hikari.Embed(title=
        f"Sucesfully generated a new license",
                            description=
        f">>> License#{id_}: ||{new_license}||",
                            color=cc.correct_color)
        
        # send confirmation message
        message.set_footer("This license can be used in any of our plugins. If you have any problem open a ticket.")
        await ctx.respond(message, flags=hikari.MessageFlag.EPHEMERAL)

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

            ## (
            # generate the confirmation message
            msg = hikari.Embed(
                title=f"Are you sure you want to delete [License#{id_}]",
                description=f">>> Owned by: <@{user_id}>",
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

                        elif event.interaction.custom_id == "no":
                            skipped_embed = hikari.Embed(
                                                title=f"[Licence#{id_}] deleting skipped Sucesfully",
                                                color=cc.correct_color)
                            
                            await ctx.edit_last_response(
                                skipped_embed,
                                components=[])
                            return None
                        
            except asyncio.TimeoutError:
                await message.edit(timeout_message, components=[])
            
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
                            
                            # send the confirmation message
                            sucesfully_embed = hikari.Embed(title=f"[license#{id_}] sucesfully generated for @{user}",
                                                description=f">>> License#{id_}: ||{new_license}||\nUser: <@{user_id}>",
                                                color=cc.correct_color)
                            sucesfully_embed.set_footer(f"[license#{id_}] generated for @{user} - {user_id}")
                            
                            await ctx.edit_last_response(
                                sucesfully_embed,
                                components=[])
                            return None

                        elif event.interaction.custom_id == "no":
                            skipped_embed = hikari.Embed(
                                                title=f"License generation sucesfully cancelled",
                                                color=cc.correct_color)
                            await ctx.edit_last_response(
                                skipped_embed,
                                components=[])
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

        # generate the confirmation message
        msg = hikari.Embed(title=f"The user has a license alredy.",
                            description=f">>> License#{id_}: ||{license_}||\nUser: <@{user_id}>",
                            color=cc.wrong_color)
        
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
                            description=f">>> License#{id_}: ||{license_}||\nUser: <@{user_id}>",
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
                            title=f"[license#{id_}] Sucesfully Regenerated",
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

# CHECK USER LICENSE COMMAND - check a license from an user
@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.option('user', 'user id', hikari.User, required=True)
@lightbulb.command('checkuser', "Get the license key of an user.")
@lightbulb.implements(lightbulb.SlashCommand)
async def checkuser_cmd(ctx: lightbulb.Context) -> None:
    user = ctx.options.user
    user_id = ctx.options.user.id
    
    if sql_mg.sql_fetch_user_id(user_id) == True:
        
        #get both id and license form the database
        id_ = cc.clean_sql_syntax(sql_mg.sql_get_license_id(user_id))
        license_ = cc.clean_sql_syntax(sql_mg.sql_get_license(user_id))

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
                            description=f">>> License#{id_}: ||{license_}||\nUser: <@{user_id}>",
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
                            title=f"[license#{id_}] Sucesfully Regenerated",
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
              
    else:
        
        row = ctx.bot.rest.build_action_row()
        button_1 = row.add_button(hikari.ButtonStyle.SECONDARY, "generate_new_license_for_user")
        button_1.set_label(f"Generate")
        button_1.add_to_container()

        embed_message = hikari.Embed(
                            title=f"@{user} has not license registered.",
                            description=f">>> User: <@{user_id}>",
                            color=cc.wrong_color)
    
        message = await ctx.respond(embed_message, flags=hikari.MessageFlag.EPHEMERAL, component=row)
        event_message = await message.message()
        
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
                    if event.interaction.custom_id == "generate_new_license_for_user":
                        # generate the license
                        new_license = keygen.gen_license()
                        while sql_mg.sql_fetch_license(new_license) == True:
                            new_license = keygen.gen_license()
                        
                        # store the new license in the database
                        sql_mg.sql_store_license(f"{new_license}", f"{user}", f"{user_id}")
                        
                        # get both id and license form the database
                        id_ = cc.clean_sql_syntax(sql_mg.sql_get_license_id(user_id))
                        
                        # send the confirmation message
                        sucesfully_embed = hikari.Embed(title=f"[license#{id_}] sucesfully generated for @{user}",
                                            description=f">>> License#{id_}: ||{new_license}||\nUser: <@{user_id}>",
                                            color=cc.correct_color)
                        sucesfully_embed.set_footer(f"[license#{id_}] generated for @{user} - {user_id}")
                        
                        await ctx.edit_last_response(
                            sucesfully_embed,
                            components=[])
                        return None
                
        except asyncio.TimeoutError:
            await message.edit(timeout_message, components=[])
                    
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
        user_id = cc.clean_sql_syntax(sql_mg.sql_get_user_id_from_license(license_))
        id_ = cc.clean_sql_syntax(sql_mg.sql_get_license_id(user_id))
        user = cc.clean_sql_syntax(sql_mg.sql_get_user(user_id))
        
        row = ctx.bot.rest.build_action_row()
        button_1 = row.add_button(hikari.ButtonStyle.PRIMARY, "regenerate_license_for_user")
        button_1.set_label(f"Regenerate")
        button_1.add_to_container()
        
        button_2 = row.add_button(hikari.ButtonStyle.DANGER, "delete_license_for_user")
        button_2.set_label(f"Delete")
        button_2.add_to_container()
        
        # send the message
        embed_message = hikari.Embed(
                            title=f"@{user}'s owns [license#{id_}]",
                            description=f">>> License#{id_}: ||{license_}||\nUser: <@{user_id}>",
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
                            title=f"[license#{id_}] Sucesfully Regenerated",
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
    
    else:
        embed_message = hikari.Embed(
                            title=f"License do not exist",
                            description=f"**The License Do Not Exist**\n >>> License(entered by you): {license_}",
                            color=cc.wrong_color)
    
        message = await ctx.respond(embed_message, flags=hikari.MessageFlag.EPHEMERAL)
        event_message = await message.message()
        
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
        
        message.set_footer("If you generated a license by error, or have any issue open a ticket.")
        
        await event.context.respond(message, 
                                    flags=hikari.MessageFlag.EPHEMERAL)
        return True
    elif isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond(cc.embed_no_permission, flags=hikari.MessageFlag.EPHEMERAL)
        return True
    return False

@dellicense_cmd.set_error_handler
async def on_ping_error(event: lightbulb.CommandErrorEvent) -> bool:
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond(cc.embed_no_permission, flags=hikari.MessageFlag.EPHEMERAL)
        return True

    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        
        message = hikari.Embed(title=f":no_entry_sign: This command is in cooldown",
                        description=f">>> Time Remaining: **{keygen.time_conversion(int(exception.retry_after))}**.",
                        color=cc.wrong_color)
        
        message.set_footer("If you generated a license by error, or have any issue open a ticket.")
        
        await event.context.respond(message, 
                                    flags=hikari.MessageFlag.EPHEMERAL)
        return True
    
    elif isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond(cc.embed_no_permission, flags=hikari.MessageFlag.EPHEMERAL)
        return True
    return False

@genlicense_cmd.set_error_handler
async def on_ping_error(event: lightbulb.CommandErrorEvent) -> bool:
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond(cc.embed_no_permission, flags=hikari.MessageFlag.EPHEMERAL)
        return True

    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        message = hikari.Embed(title=f":no_entry_sign: This command is in cooldown",
                        description=f">>> Time Remaining: **{keygen.time_conversion(int(exception.retry_after))}**.",
                        color=cc.wrong_color)
        
        message.set_footer("If you generated a license by error, or have any issue open a ticket.")
        
        await event.context.respond(message, 
                                    flags=hikari.MessageFlag.EPHEMERAL)
        return True
    elif isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond(cc.embed_no_permission, flags=hikari.MessageFlag.EPHEMERAL)
        return True
    return False

@checkuser_cmd.set_error_handler
async def on_ping_error(event: lightbulb.CommandErrorEvent) -> bool:
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond(cc.embed_no_permission, flags=hikari.MessageFlag.EPHEMERAL)
        return True

    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        
        message = hikari.Embed(title=f":no_entry_sign: This command is in cooldown",
                        description=f">>> Time Remaining: **{keygen.time_conversion(int(exception.retry_after))}**.",
                        color=cc.wrong_color)
        
        message.set_footer("If you generated a license by error, or have any issue open a ticket.")
        
        await event.context.respond(message, 
                                    flags=hikari.MessageFlag.EPHEMERAL)
        return True
    elif isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond(cc.embed_no_permission, flags=hikari.MessageFlag.EPHEMERAL)
        return True
    
    return False

@checlicense_cmd.set_error_handler
async def on_ping_error(event: lightbulb.CommandErrorEvent) -> bool:
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond(cc.embed_no_permission, flags=hikari.MessageFlag.EPHEMERAL)
        return True

    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        
        message = hikari.Embed(title=f":no_entry_sign: This command is in cooldown",
                        description=f">>> Time Remaining: **{keygen.time_conversion(int(exception.retry_after))}**.",
                        color=cc.wrong_color)
        
        message.set_footer("If you generated a license by error, or have any issue open a ticket.")
        
        await event.context.respond(message, 
                                    flags=hikari.MessageFlag.EPHEMERAL)
        return True

    elif isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond(cc.embed_no_permission, flags=hikari.MessageFlag.EPHEMERAL)
        return True
    
    return False

##################################################################

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)