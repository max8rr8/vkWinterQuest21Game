
from game import Game
from opathplugin import OptimalPathPlugin
from plugins import CmdRollbackPlugin, ExportPlugin, ManualMovementPlugin, MarkedPresentsPlugin, PositionPlugin, SaveLoadPlugin

game = Game()

game.plugins.append(CmdRollbackPlugin())
game.plugins.append(MarkedPresentsPlugin())
game.plugins.append(SaveLoadPlugin())
game.plugins.append(ExportPlugin())

game.plugins.append(OptimalPathPlugin())

game.plugins.append(PositionPlugin())
game.plugins.append(ManualMovementPlugin())

game.run()

exit(0)