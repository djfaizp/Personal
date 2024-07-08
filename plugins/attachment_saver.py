from telethon import events
import os
import logging

logger = logging.getLogger(__name__)

def setup(client, db):
    @client.on(events.NewMessage(pattern='/save_attachments'))
    async def save_attachments(event):
        try:
            sender = await event.get_sender()
            chat = await event.get_chat()
            
            if event.is_private:
                await event.reply("This command can only be used in channels.")
                return

            # Check if the bot has the necessary permissions
            permissions = await client.get_permissions(chat, client.get_me())
            if not permissions.read_messages:
                await event.reply("I don't have permission to read messages in this channel.")
                return

            count = 0
            async for message in client.iter_messages(chat):
                if message.file:
                    file_info = {
                        'id': message.id,
                        'name': message.file.name,
                        'size': message.file.size,
                        'mime_type': message.file.mime_type,
                        'channel_id': chat.id,
                    }
                    db.save_attachment_info(file_info)
                    count += 1

            await event.reply(f"Saved information for {count} attachments to the database.")
        except Exception as e:
            logger.error(f"Error in save_attachments: {str(e)}")
            await event.reply("An error occurred while saving attachment information.")
