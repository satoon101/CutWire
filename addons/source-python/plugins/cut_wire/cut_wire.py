# ../cut_wire/cut_wire.py

"""Allows bomb defusers to choose a wire to cut."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Random
from random import choice

# Source.Python Imports
#   Config
from config.manager import ConfigManager
#   Entities
from entities.entity import Entity
#   Events
from events import Event
#   Menus
from menus import PagedMenu
from menus import PagedOption
#   Messages
from messages import SayText2
#   Players
from players.entity import Player
from players.helpers import index_from_userid
#   Translations
from translations.strings import LangStrings

# Script Imports
from cut_wire.info import info


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Get the in-game strings to use
wire_strings = LangStrings(info.basename + '/strings')

# Get the config strings to use
config_strings = LangStrings(info.basename + '/config_strings')

# Store the wire color choices
_wire_colors = tuple(x for x in wire_strings if x.startswith('Color:'))

# Store the defused/exploded messages
defused_message = SayText2(message=wire_strings['Defused'])
exploded_message = SayText2(message=wire_strings['Exploded'])


# =============================================================================
# >> CONFIGURATION
# =============================================================================
# Create the config file
with ConfigManager(info.basename) as config:

    # Create the send menu convar
    send_menu = config.cvar('cw_send_menu', 1, config_strings['SendMenu'])
    for _option in [x for x in config_strings if x.startswith('MenuOption:')]:
        send_menu.Options.append('{0} = {1}'.format(
            _option.split(':')[1], config_strings[_option].get_string()))

    # Create the bot convar
    bot_choose_wire = config.cvar(
        'cw_bot_choose_wire', 0, config_strings['BotChoice'])
    for _option in [x for x in config_strings if x.startswith('BotChoice:')]:
        bot_choose_wire.Options.append('{0} = {1}'.format(
            _option.split(':')[1], config_strings[_option].get_string()))


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('bomb_begindefuse')
def begin_defuse(game_event):
    """Send a menu to the defuser."""
    # Get the defuser
    player = Player(index_from_userid(game_event['userid']))

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
            cut_chosen_wire(choice(_wire_colors), player)

        # No need to go further
        return

    # Get the send menu convar's value
    send_setting = send_menu.get_int()

    # Should the wire cut menu be sent to the defuser?
    if (send_setting == 1 or
            (send_setting == 2 and gonna_blow) or
            (send_setting == 3 and (gonna_blow or not game_event['haskit']))):

        # Send the wire cut menu to the defuser
        wire_menu.send(player.index)


@Event('bomb_defused', 'bomb_abortdefuse')
def close_menu(game_event):
    """Close the menu for the defuser."""
    wire_menu.close(index_from_userid(game_event['userid']))


@Event('bomb_exploded')
def close_menu_all(game_event):
    """Close the menu for any defusers."""
    wire_menu.close()


# =============================================================================
# >> MENU CALLBACKS
# =============================================================================
def bomb_choice(menu, index, option):
    """Cut the chosen wire."""
    cut_chosen_wire(option.value, Player(index))


# =============================================================================
# >> MENU CREATION
# =============================================================================
# Create the wire cut menu
wire_menu = PagedMenu(
    description=wire_strings['Title'], select_callback=bomb_choice)

# Loop through all choices of wire colors
for _color in _wire_colors:

    # Add the color to the menu
    wire_menu.append(PagedOption(wire_strings[_color], _color))


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def cut_chosen_wire(chosen_wire, player):
    """Cut a wire to defuse or explode the bomb."""
    # Get the bomb's instance
    bomb = Entity.find('planted_c4')

    # Did the defuser choose the correct wire?
    if chosen_wire == choice(_wire_colors):

        # Defuse the bomb
        bomb.c4_blow += 1.0
        bomb.defuse_count_down = 1.0

        # Tell the server that the player cut the correct wire
        defused_message.index = player.index
        defused_message.send(name=player.name)

    # Did the defuser choose one of the wrong wires?
    else:

        # Explode the bomb
        bomb.defuse_count_down += 1.0
        bomb.c4_blow = 1.0

        # Tell the server that the player cut the wrong wire
        exploded_message.index = player.index
        exploded_message.send(name=player.name)
