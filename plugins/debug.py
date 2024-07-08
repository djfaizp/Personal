from telethon import events
import logging

logger = logging.getLogger(__name__)

def setup(client, db):
    @client.on(events.NewMessage(pattern='/debug'))
    async def debug_info(event):
        try:
            sender = await event.get_sender()
            chat = await event.get_chat()

            if not event.is_private and not chat.creator and not chat.admin_rights:
                await event.reply("This command can only be used by channel administrators.")
                return

            me = await client.get_me()
            debug_msg = f"Debug Information:\n\n"
            debug_msg += f"Bot ID: {me.id}\n"
            debug_msg += f"Bot Username: @{me.username}\n"
            debug_msg += f"Current Chat ID: {chat.id}\n"
            debug_msg += f"Current Chat Type: {chat.__class__.__name__}\n"

            if not event.is_private:
                permissions = await client.get_permissions(chat, me)
                debug_msg += f"\nPermissions in this chat:\n"
                debug_msg += f"Admin: {permissions.is_admin}\n"
                debug_msg += f"Read Messages: {permissions.read_messages}\n"
                debug_msg += f"Send Messages: {permissions.send_messages}\n"
                debug_msg += f"Send Media: {permissions.send_media}\n"

            await event.reply(debug_msg)
        except Exception as e:
            logger.error(f"Error in debug_info: {str(e)}")
            await event.reply("An error occurred while fetching debug information.")
