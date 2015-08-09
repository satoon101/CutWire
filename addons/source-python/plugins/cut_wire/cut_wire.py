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
#   Cvars
from cvars.flags import ConVarFlags
#   Events
from events import Event
#   Filters
from filters.entities import EntityIter
#   Menus
from menus import PagedMenu
from menus import PagedOption
#   Messages
from messages import SayText2
#   Players
from players.entity import PlayerEntity
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
_colors = ('Blue', 'Yellow', 'Red', 'Green')

# Store the defused/exploded messages
defused_message = SayText2(message=wire_strings['Defused'])
exploded_message = SayText2(message=wire_strings['Exploded'])


# =============================================================================
# >> CONFIGURATION
# =============================================================================
# Create the config file
with ConfigManager(info.basename) as config:

    # Create the send menu convar
    send_menu = config.cvar(
        'cw_send_menu', 1, ConVarFlags.NONE, config_strings['SendMenu'])
    for _option in range(1, 4):
        send_menu.Options.append(
            config_strings['MenuOption{0}'.format(_option)])

    # Create the bot convar
    bot_choose_wire = config.cvar(
        'cw_bot_choose_wire', 0, ConVarFlags.NONE, config_strings['BotChoice'])
    for _option in range(3):
        bot_choose_wire.Options.append(
            config_strings['BotChoice{0}'.format(_option)])


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('bomb_begindefuse')
def begin_defuse(game_event):
    """Send a menu to the defuser."""
    # Get the defuser
    player = PlayerEntity(index_from_userid(game_event.get_int('userid')))

    # Get the bomb's instance
    bomb = get_bomb_entity()

    # Get whether the defuser has time to defuse
    gonna_blow = bomb.defuse_length > bomb.timer_length

    # Is the defuser a bot?
    if player.is_fake_client():

        # Get the bot convar's value
        bot_setting = bot_choose_wire.get_int()

        # Should the bot cut a wire?
        if (bot_setting == 1 and gonna_blow) or bot_setting == 2:

            # Cut a wire
            cut_chosen_wire(choice(_colors), player)

        # No need to go further
        return

    # Get the send menu convar's value
    send_setting = send_menu.get_int()

    # Get whether the defuser has a kit
    has_kit = game_event.get_bool('haskit')

    # Should the wire cut menu be sent to the defuser?
    if (send_setting == 1 or (send_setting == 2 and gonna_blow) or
            (send_setting == 3 and (gonna_blow or not has_kit))):

        # Send the wire cut menu to the defuser
        wire_menu.send(player.index)


@Event('bomb_defused', 'bomb_abortdefuse')
def close_menu(game_event):
    """Close the menu for the defuser."""
    wire_menu.close(index_from_userid(game_event.get_int('userid')))


@Event('bomb_exploded')
def close_menu_all(game_event):
    """Close the menu for any defusers."""
    wire_menu.close()


# =============================================================================
# >> MENU CALLBACKS
# =============================================================================
def bomb_choice(menu, index, option):
    """Cut the chosen wire."""
    cut_chosen_wire(option.value, PlayerEntity(index))


# =============================================================================
# >> MENU CREATION
# =============================================================================
# Create the wire cut menu
wire_menu = PagedMenu(
    description=wire_strings['Title'], select_callback=bomb_choice)

# Loop through all choices of wire colors
for _color in _colors:

    # Add the color to the menu
    wire_menu.append(PagedOption(wire_strings[_color], _color))


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def get_bomb_entity():
    """Return the bomb's BaseEntity instance."""
    for entity in EntityIter('planted_c4', return_types='entity'):
        return entity


def cut_chosen_wire(chosen_wire, player):
    """Cut a wire to defuse or explode the bomb."""
    # Get the bomb's instance
    bomb = get_bomb_entity()

    # Did the defuser choose the correct wire?
    if chosen_wire == choice(_colors):

        # Defuse the bomb
        bomb.c4_blow += 1.0
        bomb.defuse_count_down = 1.0

        # Tell the server that the player cut the correct wire
        defused_message.tokens = {'name': player.name}
        defused_message.index = player.index
        defused_message.send()

    # Did the defuser choose one of the wrong wires?
    else:

        # Explode the bomb
        bomb.defuse_count_down += 1.0
        bomb.c4_blow = 1.0

        # Tell the server that the player cut the wrong wire
        exploded_message.tokens = {'name': player.name}
        exploded_message.index = player.index
        exploded_message.send()
