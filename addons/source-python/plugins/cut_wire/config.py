# ../cut_wire/config.py

"""Creates server configuration and user settings."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from config.manager import ConfigManager

# Plugin
from .info import info
from .strings import CONFIG_STRINGS


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'bot_choose_wire',
    'send_menu',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
# Create the cut_wire.cfg file and execute it upon __exit__
with ConfigManager(info.name) as config:

    # Create the send menu convar
    send_menu = config.cvar('cw_send_menu', 1, CONFIG_STRINGS['SendMenu'])
    for _option in sorted([
        x for x in CONFIG_STRINGS if x.startswith('MenuOption:')
    ]):
        send_menu.Options.append(
            '{value} = {text}'.format(
                value=_option.split(':')[1],
                text=CONFIG_STRINGS[_option].get_string()
            )
        )

    # Create the bot convar
    bot_choose_wire = config.cvar(
        'cw_bot_choose_wire', 0, CONFIG_STRINGS['BotChoice']
    )
    for _option in sorted([
        x for x in CONFIG_STRINGS if x.startswith('BotChoice:')
    ]):
        bot_choose_wire.Options.append(
            '{value} = {text}'.format(
                value=_option.split(':')[1],
                text=CONFIG_STRINGS[_option].get_string()
            )
        )
