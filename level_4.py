import objects
import load

block_size = 96

floor = [objects.Floor((i * load.green_grass[2]) - i * 8, (load.Height - load.green_grass[3] * 2), 
            load.green_grass[2] * 2, load.green_grass[3] * 2, load.pink_grass) 
            for i in range(-load.Width // load.green_grass[2], load.Width * 2 // load.green_grass[3])
]

blocks = [objects.Block(block_size * 6, load.Height - block_size * 2, 
                        load.green_grass[2] * 2, load.green_grass[3] * 2, load.green_grass),
            objects.Block(block_size * 10, load.Height - block_size * 4,
                        load.green_grass[2] * 2, load.green_grass[3] * 2, load.green_grass),
            objects.Block(block_size * 7, block_size/5,
                          load.gold_long[2], load.gold_long[3], load.gold_long),
            objects.Block(block_size * 8, block_size/5, load.gold_long[2], load.gold_long[3], load.gold_long),
            objects.Block(block_size * 15, load.Height - block_size * 9, 
                             load.gold_long[2], load.gold_long[3], load.gold_long),
            objects.Block(block_size * 8, block_size * 3.5, 
                          load.silver_long[2], load.silver_long[3], load.silver_long),
            objects.Block(block_size * 2, block_size, load.bronze_long[2], load.bronze_long[3], load.bronze_long),
            objects.Block(block_size * 3, block_size * 2.5, load.bronze_long[2], load.bronze_long[3], load.bronze_long)
]

items = [objects.fruit(block_size * 7.2, -block_size / 2, 32, 32, "Fruits", name="Melon", subf=None),
         objects.fruit(block_size * 10, -block_size, 32, 32, "Fruits", name="Kiwi", subf=None)
]
traps = []
    #objects.Fire_trap(300+i*32, load.Height - block_size - 64, 16, 32) for i in range(1,30)]

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