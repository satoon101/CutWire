# ../cut_wire/config.py

"""Creates server configuration and user settings."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from enum import IntEnum

# Source.Python
from config.manager import ConfigManager

# Plugin
from .info import info
from .strings import CONFIG_STRINGS

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "BotChooseWire",
    "SendMenu",
    "bot_choose_wire",
    "send_menu",
)


# =============================================================================
# >> ENUM CLASSES
# =============================================================================
class BotChooseWire(IntEnum):
    """Settings for Bots choosing a wire."""

    NO = 0
    IF_NO_TIME = 1
    ALWAYS = 2


class SendMenu(IntEnum):
    """Settings for sending the menu."""

    ALWAYS = 1
    NO_TIME_TO_DEFUSE = 2
    NO_TIME_OR_NO_KIT = 3


# =============================================================================
# >> CONFIGURATION
# =============================================================================
# Create the cut_wire.cfg file and execute it upon __exit__
with ConfigManager(info.name) as config:

    # Create the convar for send menu
    send_menu = config.cvar("cw_send_menu", 1, CONFIG_STRINGS["SendMenu"])
    for _option in sorted([
        x for x in CONFIG_STRINGS if x.startswith("MenuOption:")
    ]):
        send_menu.Options.append(
            f'{_option.split(":")[1]} = {CONFIG_STRINGS[_option].get_string()}',
        )

    # Create the bot convar
    bot_choose_wire = config.cvar(
        "cw_bot_choose_wire", 0, CONFIG_STRINGS["BotChoice"],
    )
    for _option in sorted([
        x for x in CONFIG_STRINGS if x.startswith("BotChoice:")
    ]):
        bot_choose_wire.Options.append(
            f'{_option.split(":")[1]} = {CONFIG_STRINGS[_option].get_string()}',
        )
