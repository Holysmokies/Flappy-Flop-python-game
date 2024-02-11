import objects
import load

block_size = 96

floor = [objects.Floor((i * load.green_grass[2]) - i * 8, (load.Height - load.green_grass[3] * 2), 
            load.green_grass[2] * 2, load.green_grass[3] * 2, load.pink_grass) 
            for i in range(-load.Width // load.green_grass[2], load.Width * 2 // load.green_grass[3])
]

blocks = []

items = []

traps = []

pointer_helper = objects.pointer(block_size * 8.5, -block_size * 1.15, 26, 64, "Checkpoints", "Start", "Pointer")
finish_flag = objects.Goal(block_size * 15 + load.gold_long[2] / 2, load.Height - block_size * 10 - load.gold_long[3]*2, 
                           64, 64, "Checkpoints", "Checkpoint")


level_objects = [*floor, *blocks, *traps]
level_items = [finish_flag, *items]

removed_items = []


def reset(list):
    for item in list:
        level_items.append(item)
        removed_items.remove(item)
        item.collected = False
        item.vanish = 0
        item.animation_name = item.name
        item.animation_count = 0
        item.ANIMATION_DELAY = 4
reset(removed_items)