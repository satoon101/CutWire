# ../cut_wire/cut_wire.py

"""Allows bomb defusers to choose a wire to cut."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from random import choice

# Source.Python
from entities.entity import Entity
from events import Event
from menus import PagedMenu, PagedOption
from messages import SayText2
from players.entity import Player
from players.helpers import index_from_userid

# Plugin
from .config import BotChooseWire, SendMenu, bot_choose_wire, send_menu
from .strings import MESSAGE_STRINGS

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store the wire color choices
_wire_colors = tuple(_ for _ in MESSAGE_STRINGS if _.startswith("Color:"))

# Store the defused/exploded messages
DEFUSED_MESSAGE = SayText2(message=MESSAGE_STRINGS["Defused"])
EXPLODED_MESSAGE = SayText2(message=MESSAGE_STRINGS["Exploded"])


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event("bomb_begindefuse")
def _begin_defuse(game_event):
    """Send a menu to the defuser."""
    player = Player.from_userid(game_event["userid"])

    # Get whether the defuser has time to defuse
    bomb = Entity.find("planted_c4")
    gonna_blow = bomb.defuse_length > bomb.timer_length

    # Is the defuser a bot?
    if player.is_fake_client():
        # Should the bot cut a wire?
        bot_setting = int(bot_choose_wire)
        if (
            (bot_setting == BotChooseWire.IF_NO_TIME and gonna_blow) or
            bot_setting == BotChooseWire.ALWAYS
        ):
            _cut_chosen_wire(choice(_wire_colors), player)
        return

    # Send the wire cut menu to the defuser
    send_setting = int(send_menu)
    if send_setting == SendMenu.NO_TIME_TO_DEFUSE and not gonna_blow:
        return
    if (
        send_setting == SendMenu.NO_TIME_OR_NO_KIT and
        (game_event["haskit"] or not gonna_blow)
    ):
        return

    wire_menu.send(player.index)


@Event("bomb_defused", "bomb_abortdefuse")
def _close_menu(game_event):
    """Close the menu for the defuser."""
    wire_menu.close(index_from_userid(game_event["userid"]))


@Event("bomb_exploded")
def _close_menu_all(game_event):
    """Close the menu for any defusers."""
    wire_menu.close()


# =============================================================================
# >> MENU CALLBACKS
# =============================================================================
def _bomb_choice(menu, index, option):
    """Cut the chosen wire."""
    _cut_chosen_wire(option.value, Player(index))


# =============================================================================
# >> MENU CREATION
# =============================================================================
# Create the wire cut menu
wire_menu = PagedMenu(
    description=MESSAGE_STRINGS["Title"], select_callback=_bomb_choice,
)

# Loop through all choices of wire colors
for _color in _wire_colors:

    # Add the color to the menu
    wire_menu.append(PagedOption(MESSAGE_STRINGS[_color], _color))


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _cut_chosen_wire(chosen_wire, player):
    """Cut a wire to defuse or explode the bomb."""
    # Get the bomb's instance
    bomb = Entity.find("planted_c4")

    # Did the defuser choose the correct wire?
    if chosen_wire == choice(_wire_colors):

        # Defuse the bomb
        bomb.c4_blow += 1.0
        bomb.defuse_count_down = 1.0

        # Tell the server that the player cut the correct wire
        DEFUSED_MESSAGE.index = player.index
        DEFUSED_MESSAGE.send(name=player.name)

    # Did the defuser choose one of the wrong wires?
    else:

        # Explode the bomb
        bomb.defuse_count_down += 1.0
        bomb.c4_blow = 1.0

        # Tell the server that the player cut the wrong wire
        EXPLODED_MESSAGE.index = player.index
        EXPLODED_MESSAGE.send(name=player.name)
