import logging

import discord
import discord.ext.commands
from discord.app_commands import command, context_menu

from hotdogbot.config import config

logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, config.log_level))


HOT_DOG = "🌭"


class Client(discord.ext.commands.Bot):
    def __init__(self, **kwargs):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.reactions = True
        intents.members = True
        super().__init__("", intents=intents, **kwargs)

    async def on_ready(self):
        logger.info("We have logged in as %s", self.user)
        logger.info("%s", self.invite_link())
        self.tree.add_command(convert)
        self.tree.add_command(convert_context)
        logger.debug(self.tree)
        logger.debug(self.tree.get_commands())
        logger.debug(await self.tree.sync())

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith("$hello"):
            await message.add_reaction(HOT_DOG)
            await message.channel.send("Hello!")

    async def on_reaction_add(self, reaction, user):
        if user == self.user:
            return
        if not reaction.me:
            return
        if reaction.emoji != HOT_DOG:
            return
        if reaction.count > 2:
            return
        logger.debug(repr(reaction))
        logger.debug(reaction.message)
        logger.debug(user)
        await reaction.message.reply(HOT_DOG)

    async def on_reaction_remove(self, reaction, user):
        logger.debug(repr(reaction))
        logger.debug(reaction.message)
        logger.debug(repr(user))
        if user == self.user or not reaction.me:
            return
        await reaction.remove(self.user)

    def invite_link(self):
        permissions = discord.Permissions(
            add_reactions=True,
            send_messages=True,
            send_messages_in_threads=True,
            read_messages=True,
        )
        return discord.utils.oauth_url(self.user.id, permissions=permissions)


@command()
async def convert(interaction, value: str):
    logger.debug(await interaction.response.send_message(value))


@context_menu(name="Convert Units")
async def convert_context(interaction: discord.Interaction, message: discord.Message):
    logger.debug(interaction)
    logger.debug(message)
    await interaction.response.send_message("ok")
