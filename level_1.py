import objects
import load

block_size = 96

floor = [objects.Floor((i * load.green_grass[2]) - i * 8, (load.Height - load.green_grass[3] * 2), 
            load.green_grass[2] * 2, load.green_grass[3] * 2, load.green_grass) 
            for i in range(-load.Width // load.green_grass[2], load.Width * 2 // load.green_grass[3])
]

blocks = [objects.Block(load.green_grass[2] * 6, load.Height - load.green_grass[3] * 8, 
                        load.green_grass[2], load.green_grass[3], load.green_grass), 
            objects.Block(0, load.Height - load.green_grass[3] * 4, load.green_grass[2], 
                        load.green_grass[3], load.green_grass),
            objects.Block(load.green_grass[2] * 14, load.Height - load.green_grass[3] * 4, 
                        load.green_grass[2], load.green_grass[3], load.green_grass),
            objects.Block(block_size * 7, load.Height - block_size * 6, 
                        load.gold_long[2], load.gold_long[3], load.gold_long),
            objects.Block(block_size * 13, load.Height - block_size * 4, 
                             load.gold_long[2], load.gold_long[3], load.gold_long)
]

finish_flag = objects.Goal(block_size * 13 + load.gold_long[2] / 2, load.Height - block_size * 5 - load.gold_long[3]*2, 
                           64, 64, "Checkpoints", "Checkpoint")

traps = [objects.Fire_trap(300, load.Height - block_size - 64, 16, 32),
            objects.Fire_trap(332, load.Height - block_size - 64, 16, 32)
]

level_objects = [*floor, *blocks, *traps]
level_items = [finish_flag]

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