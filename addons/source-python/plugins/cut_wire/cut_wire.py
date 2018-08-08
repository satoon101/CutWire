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
from menus import PagedMenu
from menus import PagedOption
from messages import SayText2
from players.entity import Player
from players.helpers import index_from_userid

# Plugin
from .config import bot_choose_wire, send_menu
from .strings import MESSAGE_STRINGS


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store the wire color choices
_wire_colors = tuple(x for x in MESSAGE_STRINGS if x.startswith('Color:'))

# Store the defused/exploded messages
DEFUSED_MESSAGE = SayText2(message=MESSAGE_STRINGS['Defused'])
EXPLODED_MESSAGE = SayText2(message=MESSAGE_STRINGS['Exploded'])


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('bomb_begindefuse')
def _begin_defuse(game_event):
    """Send a menu to the defuser."""
    # Get the defuser
    player = Player.from_userid(game_event['userid'])

    # Get the bomb's instance
    bomb = Entity.find('planted_c4')

    # Get whether the defuser has time to defuse
    gonna_blow = bomb.defuse_length > bomb.timer_length

    # Is the defuser a bot?
    if player.is_fake_client():

        # Get the bot convar's value
        bot_setting = bot_choose_wire.get_int()

        # Should the bot cut a wire?
        if (bot_setting == 1 and gonna_blow) or bot_setting == 2:

            # Cut a wire
            _cut_chosen_wire(choice(_wire_colors), player)

        # No need to go further
        return

    # Get the send menu convar's value
    send_setting = send_menu.get_int()

    # Send the wire cut menu to the defuser
    if send_setting == 2 and not gonna_blow:
        return
    if send_setting == 3 and (game_event['haskit'] or not gonna_blow):
        return
    wire_menu.send(player.index)


@Event('bomb_defused', 'bomb_abortdefuse')
def _close_menu(game_event):
    """Close the menu for the defuser."""
    wire_menu.close(index_from_userid(game_event['userid']))


@Event('bomb_exploded')
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
    description=MESSAGE_STRINGS['Title'], select_callback=_bomb_choice
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
    bomb = Entity.find('planted_c4')

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
