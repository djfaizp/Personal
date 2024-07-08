from telethon import events
import logging

logger = logging.getLogger(__name__)

def setup(client, db):
    @client.on(events.NewMessage(pattern='/forward'))
    async def forward_files(event):
        try:
            sender = await event.get_sender()
            
            await event.reply("Please enter the source channel username or ID:")
            source = await client.wait_for_message(sender)
            
            await event.reply("Please enter the destination channel username or ID:")
            destination = await client.wait_for_message(sender)

            # Get source and destination entities
            try:
                source_entity = await client.get_entity(source.text)
                dest_entity = await client.get_entity(destination.text)
            except ValueError:
                await event.reply("Invalid source or destination. Please make sure the channel exists and you have access to it.")
                return

            # Check permissions for source channel
            source_permissions = await client.get_permissions(source_entity, client.get_me())
            if not source_permissions.read_messages:
                await event.reply("I don't have permission to read messages in the source channel.")
                return

            # Check permissions for destination channel
            dest_permissions = await client.get_permissions(dest_entity, client.get_me())
            if not dest_permissions.send_messages:
                await event.reply("I don't have permission to send messages in the destination channel.")
                return

            count = 0
            async for message in client.iter_messages(source_entity):
                if message.file:
                    await client.send_file(dest_entity, message.media)
                    count += 1

            await event.reply(f"Successfully forwarded {count} files.")
        except Exception as e:
            logger.error(f"Error in forward_files: {str(e)}")
            await event.reply("An error occurred while forwarding files.")
