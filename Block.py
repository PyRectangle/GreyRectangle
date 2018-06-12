blocks = []


class Block():
    def __init__(self, texture, solid, death, colorkey):
        self.texture = texture
        self.solid = solid
        self.death = death
        self.colorkey = colorkey
        
        blocks.append(self)


AIR = Block(None, False, False, None)
DIRT = Block(2, True, False, None)
GRASS = Block(1, True, False, None)
PORTAL_BLOCK = Block(3, False, False, None)
GOAL = Block(4, False, False, (255, 255, 255))
HEART = Block(5, False, False, None)
LADDER = Block(6, False, False, (255, 255, 255))
DORNS = Block(7, False, True, (255, 255, 255))
LEVER = Block(8, False, False, (255, 255, 255))
PISTON = Block(9, True, False, None)
CHECKPOINT = Block(10, False, False, None)
STONE = Block(0, True, False, None)
LAVA = Block(11, False, True, None)
COAL_ORE = Block(12, True, False, None)
DIAMOND_ORE = Block(13, True, False, None)
IRON_ORE = Block(14, True, False, None)
GOLD_ORE = Block(15, True, False, None)
LAPIS_ORE = Block(16, True, False, None)
REDSTONE_ORE = Block(17, True, False, None)
WATER = Block(18, False, False, None)
OBSIDIAN = Block(3, True, False, None)
GRAVITY_BLOCK = Block(19, False, False, None)
GOLD_BLOCK = Block(20, True, False, None)
SAND = Block(21, True, False, None)
CACTUS = Block(22, False, True, None)
SANDSTONE = Block(23, True, False, None)
QUICKSAND = Block(24, False, False, None)
FALLING_SANDSTONE = Block(23, True, False, None)
TELEPORTER = Block(25, False, False, None)
PLANKS = Block(26, True, False, None)
BUTTON = Block(27, False, False, None)
GRAVEL = Block(28, True, False, None)
