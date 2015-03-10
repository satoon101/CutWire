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
from menus import Text
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
wire_strings = LangStrings(info.basename + '/strings')

config_strings = LangStrings(info.basename + '/config_strings')

_colors = ('Blue', 'Yellow', 'Red', 'Green')


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with ConfigManager(info.basename) as config:

    send_menu = config.cvar(
        'cw_send_menu', 1, ConVarFlags.NONE, config_strings['SendMenu'])
    for _option in range(1, 4):
        send_menu.Options.append(
            config_strings['MenuOption{0}'.format(_option)])

    bot_choose_wire = config.cvar(
        'cw_bot_choose_wire', 0, ConVarFlags.NONE, config_strings['BotChoice'])
    for _option in range(3):
        bot_choose_wire.Options.append(
            config_strings['BotChoice{0}'.format(_option)])


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event
def bomb_begindefuse(game_event):
    """Send a menu to the defuser."""
    player = PlayerEntity(index_from_userid(game_event.get_int('userid')))

    for bomb in EntityIter('planted_c4', return_types='entity'):

        break

    gonna_blow = bomb.defuse_length > bomb.timer_length

    if player.is_fake_client():

        bot_setting = bot_choose_wire.get_int()

        if (bot_setting == 1 and gonna_blow) or bot_setting == 2:

            cut_chosen_wire(choice(_colors))

        return

    send_setting = send_menu.get_int()

    has_kit = game_event.get_bool('haskit')

    if (send_setting == 1 or (send_setting == 2 and gonna_blow)
            or (send_setting == 3 and (gonna_blow or not has_kit))):

        wire_menu.send(player.index)


@Event
def bomb_abortdefuse(game_event):
    """Close the menu for the defuser."""
    wire_menu.close()


# =============================================================================
# >> MENU CALLBACKS
# =============================================================================
def bomb_choice(menu, index, option):
    """Cut the chosen wire."""
    cut_chosen_wire(option.value)


# =============================================================================
# >> MENU CREATION
# =============================================================================
wire_menu = PagedMenu(
    description=wire_strings['Title'], select_callback=bomb_choice)

for _color in _colors:

    wire_menu.append(PagedOption(wire_strings[_color], _color))


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def cut_chosen_wire(chosen_wire):
    """Cut a wire to defuse or explode the bomb."""
    for bomb in EntityIter('planted_c4', return_types='entity'):

        break

    if chosen_wire == choice(_colors):

        print('defusing')
        bomb.defuse_count_down = 0.0

    else:

        print('exploding')
        bomb.c4_blow = 0.0
