WIN_WIDTH = 900
WIN_HEIGHT = 600
FPS = 60

OVERLAY_LAYER = 5
PLAYER_LAYER = 4
NPC_LAYER = 2
BUILDING_LAYER = 3
GROUND_LAYER = 1

PLAYER_SPEED = 3
NPC_SPEED = 1.8

TILESIZE = 25

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (180, 0, 0)

REFERENCE_SPRITE =  ['1']

ground_map_lv1 = [
    'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD',
    'DDDDDDDDDDDDDDDD111111111111111111111DDDDDDDDDDDDDDDDDDDDD',
    'DDDDDDDDDDDDDDDD.....................DDDDDDDDDDDDDDDDDDDDD',
    'DDDDDDDDDDDDDDDDDDDD2.DYH.DDDYC.DDDDDDDDDDDDDDDDDDDDDDDDDD',
    'DDDDDDDDDDDDDDDDDDDD..DY..DDDY..DDDDDDDDDDDDDDDDDDDDDDDDDD',
    'DDDDDDDDDDDDDDDDDDDDDDDYH.DDDYH.DDDDDDDDDDDDDDDDDDDDDDDDDD',
    'DDDDDDDDDDXXXXXXXXXXXXXY..DDDY..DDDDDDDDDDDD2.DDDDDDDDDDDD',
    'DDDDDDDDDDYDDDP.DDDDDDDrXXXXXlDDDDDDDDDDDDDD..DDDDDDDDDDDD',
    'DDDDDDDDDDYDDD..DDDDDDDDH.DDDDDDDDDDDDDDDDDDYDDDDDDDDDDDDD',
    'DDDDDDDDDDYDDDDDDDDDDDDD..DDDDDDDDDDDDDDDDDDYDDDDDDDDDDDDD',
    'DDDDDDDDDDYDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDYDDDDDDDDDDDDD',
    'DDDDDDDDDDYDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDYDDDDDDDDDDDDD',
    'DDDDDDDDDDYDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDYDDDDDDDDDDDDD',
    'DDDDDDDDDDYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXDDDDDDDDDDDDD',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDYYDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDYYDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDYYDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDYYDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDYYDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDYYDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDYYDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDYYDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDYYDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDYYDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDYYDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDYDDDDDDDDDD',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDYH.YYH.YYH.',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDY..YY..YY..',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDYDDYYDDYYDD',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDYXXXXXXXXDD',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDY2.YYH.YYH.',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDY..YY..YY..'
]

vehicle_map_lv1 = [
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................',
    '..........................................................'
]