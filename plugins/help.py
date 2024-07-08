from telethon import events
import logging

logger = logging.getLogger(__name__)

def setup(client, db):
    @client.on(events.NewMessage(pattern='/help'))
    async def help_command(event):
        try:
            help_text = """
Available commands:

/save_attachments - Save information about attachments from a specified channel.
/forward - Forward files from one channel to another.
/debug - Get debug information about the bot (use in a channel).

To use /save_attachments or /forward, start a private chat with me and send the command. I'll guide you through the process.

Remember to add me as a member to any channel you want me to interact with!
            """
            await event.reply(help_text)
        except Exception as e:
            logger.error(f"Error in help_command: {str(e)}")
            await event.reply("An error occurred while displaying help information.")
