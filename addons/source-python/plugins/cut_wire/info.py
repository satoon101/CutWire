# ../cut_wire/info.py

"""Provides/stores information about the plugin."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Cvars
from cvars.public import PublicConVar
#   Plugins
from plugins.info import PluginInfo


# =============================================================================
# >> PLUGIN INFO
# =============================================================================
info = PluginInfo()
info.name = 'Cut Wire'
info.author = 'Satoon101'
info.version = '1.2'
info.basename = 'cut_wire'
info.variable = info.basename + '_version'
info.url = 'http://forums.sourcepython.com/showthread.php?779'
info.convar = PublicConVar(info.variable, info.version, info.name + ' Version')
