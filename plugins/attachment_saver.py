from telethon import events
import logging
from telethon.tl.types import InputPeerChannel
from telethon.tl.functions.channels import GetParticipantRequest

logger = logging.getLogger(__name__)

def setup(client, db):
    @client.on(events.NewMessage(pattern='/save_attachments'))
    async def save_attachments(event):
        try:
            if not event.is_private:
                await event.reply("This command can only be used in private messages with the bot.")
                return

            sender = await event.get_sender()
            
            # Ask for the channel
            await event.reply("Please enter the channel username or ID where you want to save attachments from:")
            channel_msg = await client.wait_for_message(sender)
            
            try:
                channel = await client.get_entity(channel_msg.text)
            except ValueError:
                await event.reply("Invalid channel. Please make sure the channel exists and the bot has access to it.")
                return

            # Check if the bot is a member of the channel
            try:
                await client(GetParticipantRequest(channel, 'me'))
            except:
                await event.reply("I'm not a member of this channel. Please add me to the channel first.")
                return

            # Check if the bot has the necessary permissions
            bot_permissions = await client.get_permissions(channel, 'me')
            if not bot_permissions.read_messages:
                await event.reply("I don't have permission to read messages in this channel.")
                return

            await event.reply("Saving attachment information. This may take a while...")

            count = 0
            async for message in client.iter_messages(channel):
                if message.file:
                    file_info = {
                        'id': message.id,
                        'name': message.file.name,
                        'size': message.file.size,
                        'mime_type': message.file.mime_type,
                        'channel_id': channel.id,
                    }
                    db.save_attachment_info(file_info)
                    count += 1

            await event.reply(f"Saved information for {count} attachments from the channel to the database.")
        except Exception as e:
            logger.error(f"Error in save_attachments: {str(e)}")
            await event.reply("An error occurred while saving attachment information.")
