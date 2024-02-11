import pygame
import load

def handle_vertical_collision(player, objects, dy):
    keys = pygame.key.get_pressed()
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):
            if dy > 0: #if moving down
                if obj.rect.top - player.rect.bottom < 35:
                    player.rect.bottom = obj.rect.top
                    player.landed()
            elif dy < 0: #if moving up
                if obj.rect.bottom - player.rect.top < 35:
                    player.rect.top = obj.rect.bottom
                    player.hit_head()
            collided_objects.append(obj)
    return collided_objects


def horizontal_collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break
    player.move(-dx,0)
    player.update()
    return collided_object


def handle_movement(player, objects, items):
    keys = pygame.key.get_pressed()
    #adds slight decay in move speed after finished
    player.x_vel = player.x_vel / 1.15
    if player.x_vel < 2:
        player.x_vel = 0

    #move if not colliding horizontally
    collide_left = horizontal_collide(player, objects, -load.player_velocity * 3)
    collide_right = horizontal_collide(player, objects, load.player_velocity * 6)
    if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and not collide_left:
        player.move_left(load.player_velocity)
    elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not collide_right:
        player.move_right(load.player_velocity)

    #move if not colliding vertically
    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    for obj in vertical_collide:
        if obj.name == 'fire':
            player.make_hit()

    for item in items:
        if pygame.sprite.collide_mask(player, item):
            #COIN
            if "Melon" in item.name:
                if item.collected:
                    pass
                else:
                    player.coins += 1
                    item.touch()
            #LOW GRAVITY
            elif "Kiwi" in item.name:
                if item.collected:
                    pass
                else:
                    player.moon_grav()
                    player.low_grav_timer = 0
                    item.touch()
            #VICTORY
            elif "goal" in item.name:
                player.victorious()