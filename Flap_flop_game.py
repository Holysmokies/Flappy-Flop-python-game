#Flippy flop platforming game
#1713 lines of code across all files

import os
import random
import math
from os import listdir
from os.path import isfile, join

import pygame
import load
import player_char
import draw
import objects
import collision
import button

import level_1
import level_2
import level_3
import level_4
import level_5

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = load.get_background("Brown.png", load.Width, load.Height)
    experience = 0
    talents = [0,0,0,0,0,0]
    previous_level = 0
    #talents = [HEALTH, RUN SPEED, LEVEL TIME, JUMP, AVAILABLE, USED]
    player = player_char.Player(100, 500, 50, 50, experience, talents)
    offset_x = 0
    offset_y = 0
    scroll_area_width = load.Width / 2.5
    scroll_area_height = load.Height / 3.5
    level = 0
    lvl1_exp_given = False
    lvl2_exp_given = False
    lvl3_exp_given = False
    lvl4_exp_given = False
    lvl5_exp_given = False
    lvl6_exp_given = False
    
    #Main Menu buttons
    start = button.Button(load.Width / 3.5, load.Height / 4, "Play.png", "Play", 8)  
    exit = button.Button(load.Width - (load.Width / 2.5), load.Height/4, "Close.png", "Exit", 11.2)
    settings = button.Button(load.Width / 3.5, load.Height / 2, "Settings.png", "Settings", 8)
    lvl_select = button.Button(load.Width - (load.Width / 2.5), load.Height / 2, "Levels.png", "Level Select", 8)
    main_talent_tree = button.Button(load.Width / 3.5 + start.rect.width * 0.94, load.Height / 2.8, "Achievements.png", "Talents", 8)

    #in level buttons
    restart_btn = button.Button(load.Width / 4, load.Height/1.5, "Restart.png", "Restart", 5)
    next_btn = button.Button(load.Width / 4 + restart_btn.rect.width * 4, load.Height / 1.5, "Next.png", "Next", 5)
    back_btn = button.Button(load.Width / 4 + restart_btn.rect.width * 2, load.Height / 1.5, "Back.png", "Back", 7)
    level_restart_btn = button.Button(2 + restart_btn.rect.width / 1.7, load.Height - restart_btn.rect.height / 1.7, "Restart.png", "Restart", 3)
    level_back_btn = button.Button(2, load.Height - back_btn.rect.height / 1.7, "Back.png", "Back", 4.3)
    talent_tree_btn = button.Button(2 + 2 * (restart_btn.rect.width / 1.7), load.Height - restart_btn.rect.height / 1.7, "Achievements.png", "Talents", 3)
    
    #talent tree buttons
    health_btn = button.talent_button(load.Width / 4, load.Height / 4, 200, 150, (255, 0, 0), "Max  Health", 1)
    run_speed_btn = button.talent_button(load.Width / 4 + 1.5 * health_btn.rect.width , load.Height / 4, 200, 150, (255, 0, 0), "Run  Speed", 1)
    level_time_btn = button.talent_button(load.Width / 4, load.Height / 2, 200, 150, (255, 0, 0), "Level Time", 2)
    jump_upgrade_btn = button.talent_button(load.Width / 4 + 1.5 *health_btn.rect.width , load.Height / 2, 200, 150, (255, 0, 0), "Jump Power", 3)
    talent_reset_btn = button.level_button(load.Width - health_btn.rect.width, load.Height - health_btn.rect.height, 150, 100, (255, 50, 255), "Reset Talents")
    talent_tree = [health_btn, run_speed_btn, level_time_btn, jump_upgrade_btn]
    resume_btn = button.Button(2 + level_back_btn.rect.width, load.Height - back_btn.rect.height / 1.7, "Play.png", "Resume", 3)
    
    #level selection screen buttons
    all_levels = [button.level_button(20, load.Height / 9 * i, 
                    400, 50, (255,0,0), str(i)) for i in range(1, 10)]
    
    #general buttons inside levels
    level_buttons = [start, exit, settings, lvl_select, restart_btn, next_btn, 
                     back_btn, level_restart_btn, level_back_btn, 
                     talent_tree_btn, *talent_tree]

    #random, undulating floor terain
    #-(block_size*(0.1)*random.randint(0,2)
    #dynamic x coord (i*x, in intervals of 96 (or specified block size)), but static y coord


    run = True
    #while window/program is running (all game code must be inside this)
    while run:
        #regulate FPS
        clock.tick(load.FPS)
        #if click red X -> quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            #if a key is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        #BUTTON FUNCTIONALITY
        if start.draw_button(window):
            level = 1
            if level >= load.MAX_LEVEL:
                load.MAX_LEVEL += level
            player = player_char.Player(100, 500, 50, 50, experience, talents)
            player.heal()
            talent_fix = player.level_up()
            if talent_fix[0]:
                talents[4] += talent_fix[1]
        elif settings.draw_button(window):
            level = 999
        elif exit.draw_button(window):
            pygame.quit()
        elif lvl_select.draw_button(window):
            talent_fix = player.level_up()
            if talent_fix[0]:
                talents[4] += talent_fix[1]
            level = 998
        elif back_btn.draw_button(window) or level_back_btn.draw_button(window):
            player.health = player.MAX_HEALTH
            offset_x = 0
            offset_y = 0
            player = player_char.Player(100, 500, 50, 50, experience, talents)
            talent_fix = player.level_up()
            if talent_fix[0]:
                talents[4] += talent_fix[1]
            level = 0
            player.coins = 0
            player.low_grav = False
            player.low_grav_timer = 0
        elif next_btn.draw_button(window):
            player.health = player.MAX_HEALTH
            offset_x = 0
            offset_y = 0
            player = player_char.Player(100, 500, 50, 50, experience, talents)
            talent_fix = player.level_up()
            if talent_fix[0]:
                talents[4] += talent_fix[1]
            level += 1
            if level >= load.MAX_LEVEL:
                load.MAX_LEVEL += level
            player.coins = 0
            player.low_grav = False
            player.low_grav_timer = 0
            player.heal()
        elif restart_btn.draw_button(window) or level_restart_btn.draw_button(window):
            if level == 1:
                level_1.reset(level_1.removed_items)
            elif level == 2:
                level_2.reset(level_2.removed_items)
            elif level == 3:
                level_3.reset(level_3.removed_items)
            elif level == 4:
                level_4.reset(level_4.removed_items)
            elif level == 5:
                level_5.reset(level_5.removed_items)
            offset_x = 0
            offset_y = 0
            player.coins = 0
            player.low_grav = False
            player.low_grav_timer = 0
            player = player_char.Player(100, 500, 50, 50, experience, talents)
            player.heal()
            talent_fix = player.level_up()
            if talent_fix[0]:
                talents[4] += talent_fix[1]
        elif talent_tree_btn.draw_button(window) or main_talent_tree.draw_button(window):
            talent_fix = player.level_up()
            if talent_fix[0]:
                talents[4] += talent_fix[1]
            previous_level = level
            level = 997
        elif resume_btn.draw_button(window):
            level = previous_level
            if level == 1:
                level_1.reset(level_1.removed_items)
            elif level == 2:
                level_2.reset(level_2.removed_items)
            elif level == 3:
                level_3.reset(level_3.removed_items)
            elif level == 4:
                level_4.reset(level_4.removed_items)
            elif level == 5:
                level_5.reset(level_5.removed_items)
            offset_x = 0
            offset_y = 0
            player.coins = 0
            player.low_grav = False
            player.low_grav_timer = 0
            player = player_char.Player(100, 500, 50, 50, experience, talents)
            player.heal()
            talent_fix = player.level_up()
            if talent_fix[0]:
                talents[4] += talent_fix[1]

        #checks for button click on talent tree
        if level == 997: 
            for btn in talent_tree:
                if btn.draw_lvl_btn(window, player.talent_points, talents):
                    #print(btn.name, "CLICKED")
                    if btn.name == "Max  Health":
                        talents[0] += btn.req
                        player.talent_points -= btn.req
                        talents[4] -= btn.req
                        player.used_talent_points += btn.req
                        talents[5] += btn.req
                    if btn.name == "Run  Speed":
                        talents[1] += btn.req
                        player.talent_points -= btn.req
                        talents[4] -= btn.req
                        player.used_talent_points += btn.req
                        talents[5] += btn.req
                    if btn.name == "Jump Power":
                        talents[3] += btn.req
                        player.talent_points -= btn.req
                        talents[4] -= btn.req
                        player.used_talent_points += btn.req
                        talents[5] += btn.req
                    if btn.name == "Level Time":
                        talents[2] += btn.req
                        player.talent_points -= btn.req
                        talents[4] -= btn.req
                        player.used_talent_points += btn.req
                        talents[5] += btn.req
                    player = player_char.Player(100, 500, 50, 50, experience, talents)
                    offset_x = 0
                    offset_y = 0
                    player.heal()
                    player.check_level()
            if talent_reset_btn.draw_lvl_btn(window):
                talents[0] = 0
                talents[1] = 0
                talents[2] = 0
                talents[3] = 0
                talents[4] = player.player_level - 1
                talents[5] = 0
                player.talent_points = talents[4]
                player.used_talent_points = 0
                player = player_char.Player(100, 500, 50, 50, experience, talents)
                offset_x = 0
                offset_y = 0
                player.check_level()

        #checks for button click on level select
        if level == 998:
            for level_name in all_levels:
                if level_name.draw_lvl_btn(window):
                    level = int(level_name.name)
        


        #MAIN MENU
        if level == 0:
            player.loop(load.FPS)
            draw.draw(window, background, bg_image, None, level_1.floor, offset_x, offset_y)
            collision.handle_movement(player, level_1.floor, [])
            
            start.drawn = True
            exit.drawn = True
            lvl_select.drawn = True
            settings.drawn = True
            main_talent_tree.drawn = True
            exit.draw_button(window)
            lvl_select.draw_button(window)
            main_talent_tree.draw_button(window)
            start.draw_button(window)
            settings.draw_button(window)

            draw.draw_text("Flap Flop", 90, (50,150,0), load.Width / 2 - 100, load.Height / 9, surface=window)
            player.draw(window, 0, 0)
            pygame.display.update()
        

        #LEVEL 1
        elif level == 1:
            player.in_level = True
            for trap in level_1.traps:
                trap.on()
                
            level_1.finish_flag.idle()

            for btn in level_buttons:
                btn.drawn = False

            if player.victory:
                draw.draw(window, background, bg_image, player, level_1.level_objects, offset_x, offset_y, level_1.level_items)
                draw.draw_text("To the winner, go the spoils...", 45, (255,150,0), load.Width / 4, load.Height / 4, None, surface = window)
                if not lvl1_exp_given:
                    experience += 10
                    lvl1_exp_given = True
                    load.MAX_LEVEL += 1
                draw.draw_text("Player Level: "+str(player.player_level), 28, (255,255,255), 20, 10, True, surface=window)
                draw.draw_text("Experience: "+str(player.experience), 24, (255,255,255), 20, 55, True, surface = window)
                draw.draw_text("+"+str(experience - player.experience), 35, (0,255,0), 90, 90, surface=window)
                restart_btn.drawn = True
                back_btn.drawn = True
                next_btn.drawn = True
                restart_btn.draw_button(window)
                back_btn.draw_button(window)
                next_btn.draw_button(window)
                pygame.display.update()

            elif player.health == 0:
                draw.draw(window, background, bg_image, player, level_1.level_objects, offset_x, offset_y, level_1.level_items)
                draw.draw_text("You Died... Retry?", 40, (255,0,0), load.Width / 2.6, load.Height / 4, None, surface = window)
                draw.draw_text("Player Level: "+str(player.player_level), 28, (255,255,255), 20, 10, True, surface=window)
                draw.draw_text("Experience: "+str(player.experience), 24, (255,255,255), 20, 55, True, surface = window)
                restart_btn.drawn = True
                back_btn.drawn = True
                restart_btn.draw_button(window)
                back_btn.draw_button(window)
                pygame.display.update()

            else:
                player.loop(load.FPS)
                for trap in level_1.traps:
                    trap.loop()
                for item in level_1.level_items:
                    item.loop()
                player.victory = False
                collision.handle_movement(player, level_1.level_objects, level_1.level_items)
                #draw, text must come after draw player since it references player location
                draw.draw(window, background, bg_image, player, level_1.level_objects, offset_x, offset_y, items=level_1.level_items)
                
                draw.draw_text("Player Level: "+str(player.player_level), 28, (255,255,255), 20, 10, True, surface=window)
                draw.draw_text("Experience: "+str(player.experience), 24, (255,255,255), 20, 55, True, surface = window)
                draw.draw_text(str(player.health), 30, (255,0,0), player.rect.left + 20, player.rect.top - 40, None, offset_x, offset_y, surface=window)
                draw.draw_text("Level 1: Get to the FLAG!", 32, (255,255,255), 200, 300, None, offset_x, offset_y, surface=window)
                
                talent_tree_btn.drawn = True
                talent_tree_btn.draw_button(window)
                level_restart_btn.drawn = True
                level_restart_btn.draw_button(window)
                level_back_btn.drawn = True
                level_back_btn.draw_button(window)
                
                #HORIZONTAL SCROLLING
                if ((player.rect.right - offset_x >= load.Width - scroll_area_width) and player.x_vel > 0) or (
                        (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                    offset_x += player.x_vel
                #VERTICAL SCROLLING
                if ((player.rect.bottom - offset_y >= load.Height - scroll_area_height) and player.y_vel > 0) or (
                        (player.rect.top - offset_y <= scroll_area_height) and player.y_vel < 0):
                    offset_y += player.y_vel
                pygame.display.update()


        #LEVEL 2
        elif level == 2:
            player.in_level = True
            for btn in level_buttons:
                btn.drawn = False
            level_2.finish_flag.idle()

            for item in level_2.level_items:
                if item.vanish == load.FPS:
                    level_2.level_items.remove(item)
                    level_2.removed_items.append(item)

            if player.victory and player.coins == 1:
                draw.draw(window, background, bg_image, player, level_2.level_objects, offset_x, offset_y, level_2.level_items)
                draw.draw_text("To the winner, go the spoils...", 45, (255,200,0), load.Width / 4, load.Height / 4, None, surface = window)
                level_2.reset(level_2.removed_items)
                if not lvl2_exp_given:
                    experience += 20
                    lvl2_exp_given = True
                    load.MAX_LEVEL += 1
                draw.draw_text("Player Level: "+str(player.player_level), 28, (255,255,255), 20, 10, True, surface=window)
                draw.draw_text("Experience: "+str(player.experience), 24, (255,255,255), 20, 55, True, surface = window)
                draw.draw_text("+"+str(experience - player.experience), 35, (0,255,0), 90, 90, surface=window)
                restart_btn.drawn = True
                back_btn.drawn = True
                next_btn.drawn = True
                restart_btn.draw_button(window)
                back_btn.draw_button(window)
                next_btn.draw_button(window)
                pygame.display.update()

            elif player.health == 0:
                draw.draw(window, background, bg_image, player, level_2.level_objects, offset_x, offset_y, level_2.level_items)
                draw.draw_text("You Died... Retry?", 40, (255,0,0), load.Width / 2.6, load.Height / 4, None, surface = window)
                level_2.reset(level_2.removed_items)
                draw.draw_text("Player Level: "+str(player.player_level), 28, (255,255,255), 20, 10, True, surface=window)
                draw.draw_text("Experience: "+str(player.experience), 24, (255,255,255), 20, 55, True, surface = window)
                restart_btn.drawn = True
                back_btn.drawn = True
                restart_btn.draw_button(window)
                back_btn.draw_button(window)
                pygame.display.update()

            else:
                player.loop(load.FPS)
                for trap in level_2.traps:
                    trap.loop()
                for item in level_2.level_items:
                    item.loop()
                player.victory = False
                collision.handle_movement(player, level_2.level_objects, level_2.level_items)
                draw.draw(window, background, bg_image, player, level_2.level_objects, offset_x, offset_y, items=level_2.level_items)
                draw.draw_text("Player Level: "+str(player.player_level), 28, (255,255,255), 20, 10, True, surface=window)
                draw.draw_text("Experience: "+str(player.experience), 24, (255,255,255), 20, 55, True, surface = window)
                draw.draw_text(str(player.health), 30, (255,0,0), player.rect.left + 20, player.rect.top - 40, None, offset_x, offset_y, surface=window)
                draw.draw_text("Coins: "+str(player.coins)+"/1", 35, (255,255,255), load.Width - load.Width / 7.5, 10, True, surface=window)
                draw.draw_text("Level 2", 35, (255,0,0), 270, 450, None, offset_x, offset_y, window)
                draw.draw_text("You will need to collect some items in order to finish levels...", 27, (255,255,255), 80, 500, None, offset_x, offset_y, window)
                
                talent_tree_btn.drawn = True
                talent_tree_btn.draw_button(window)
                level_restart_btn.drawn = True
                level_restart_btn.draw_button(window)
                level_back_btn.drawn = True
                level_back_btn.draw_button(window)
                
                #HORIZONTAL SCROLLING
                if ((player.rect.right - offset_x >= load.Width - scroll_area_width) and player.x_vel > 0) or (
                        (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                    offset_x += player.x_vel

                #VERTICAL SCROLLING
                if ((player.rect.bottom - offset_y >= load.Height - scroll_area_height) and player.y_vel > 0) or (
                        (player.rect.top - offset_y <= scroll_area_height) and player.y_vel < 0):
                    offset_y += player.y_vel

                pygame.display.update()


        #LEVEL 3
        elif level == 3:
            for trap in level_3.traps:
                trap.on()
            level_3.finish_flag.idle()

            for btn in level_buttons:
                btn.drawn = False
            
            for item in level_3.level_items:
                if item.vanish == load.FPS:
                    level_3.level_items.remove(item)
                    level_3.removed_items.append(item)

            if player.victory and player.coins == 1:
                if not lvl3_exp_given:
                    experience += 30
                    lvl3_exp_given = True
                    load.MAX_LEVEL += 1
                draw.draw(window, background, bg_image, player, level_3.level_objects, offset_x, offset_y, level_3.level_items)
                draw.draw_text("To the winner, go the spoils...", 45, (255,200,0), load.Width / 4, load.Height / 4, None, surface = window)
                level_3.reset(level_3.removed_items)
                draw.draw_text("Player Level: "+str(player.player_level), 28, (255,255,255), 20, 10, True, surface=window)
                draw.draw_text("Experience: "+str(player.experience), 24, (255,255,255), 20, 55, True, surface = window)
                draw.draw_text("+"+str(experience - player.experience), 35, (0,255,0), 90, 90, surface=window)
                restart_btn.drawn = True
                back_btn.drawn = True
                next_btn.drawn = True
                restart_btn.draw_button(window)
                back_btn.draw_button(window)
                next_btn.draw_button(window)
                pygame.display.update()

            elif player.health == 0:
                draw.draw(window, background, bg_image, player, level_3.level_objects, offset_x, offset_y, level_3.level_items)
                draw.draw_text("You Died... Retry?", 40, (255,0,0), load.Width / 2.6, load.Height / 4, None, surface = window)
                level_3.reset(level_3.removed_items)
                draw.draw_text("Player Level: "+str(player.player_level), 28, (255,255,255), 20, 10, True, surface=window)
                draw.draw_text("Experience: "+str(player.experience), 24, (255,255,255), 20, 55, True, surface = window)
                restart_btn.drawn = True
                back_btn.drawn = True
                restart_btn.draw_button(window)
                back_btn.draw_button(window)
                pygame.display.update()

            else:
                player.loop(load.FPS)
                for trap in level_3.traps:
                    trap.loop()
                for item in level_3.level_items:
                    item.loop()
                player.victory = False
                collision.handle_movement(player, level_3.level_objects, level_3.level_items)
                draw.draw(window, background, bg_image, player, level_3.level_objects, offset_x, offset_y, items=level_3.level_items)
                draw.draw_text("Player Level: "+str(player.player_level), 28, (255,255,255), 20, 10, True, surface=window)
                draw.draw_text("Experience: "+str(player.experience), 24, (255,255,255), 20, 55, True, surface = window)
                draw.draw_text(str(player.health), 30, (255,0,0), 
                               player.rect.left + 20, player.rect.top - 40, None, offset_x, offset_y, surface=window)
                draw.draw_text("Coins: "+str(player.coins), 35, (255,255,255), 
                               load.Width - load.Width / 7.5, 10, True, surface=window)
                draw.draw_text("Level 3", 35, (255,0,0), 270, 450, None, offset_x, offset_y, window)
                draw.draw_text("Some items will give you a limited boost needed to complete the level...", 
                               27, (255,255,255), 80, 500, None, offset_x, offset_y, window)
                if player.low_grav:
                    draw.draw_text(str(round(((300 - player.low_grav_timer) / 60), 1)), 35, (255,255,255), 
                                   player.rect.left + 50, player.rect.top - 30, None, offset_x, offset_y, window)
                
                talent_tree_btn.drawn = True
                talent_tree_btn.draw_button(window)
                level_restart_btn.drawn = True
                level_restart_btn.draw_button(window)
                level_back_btn.drawn = True
                level_back_btn.draw_button(window)
            
                #HORIZONTAL SCROLLING
                if ((player.rect.right - offset_x >= load.Width - scroll_area_width) and player.x_vel > 0) or (
                        (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                    offset_x += player.x_vel

                #VERTICAL SCROLLING
                if ((player.rect.bottom - offset_y >= load.Height - scroll_area_height) and player.y_vel > 0) or (
                        (player.rect.top - offset_y <= scroll_area_height) and player.y_vel < 0):
                    offset_y += player.y_vel

            pygame.display.update()


        #LEVEL 4
        elif level == 4:
            player.in_level = True
            level_timer = 1500 + (player.level_time_talent_point * 150)
            for trap in level_4.traps:
                trap.on()
            level_4.finish_flag.idle()

            for btn in level_buttons:
                btn.drawn = False
            
            for item in level_4.level_items:
                if item.vanish == load.FPS:
                    level_4.level_items.remove(item)
                    level_4.removed_items.append(item)

            if player.victory and player.coins == 1:
                if not lvl4_exp_given:
                    experience += round(((level_timer - player.lvl_timer) / 60), 0)
                    lvl4_exp_given = True
                    load.MAX_LEVEL += 1
                draw.draw(window, background, bg_image, player, level_4.level_objects, offset_x, offset_y, level_4.level_items)
                draw.draw_text("To the winner, go the spoils...", 45, (255,200,0), load.Width / 4, load.Height / 4, None, surface = window)
                level_4.reset(level_4.removed_items)
                draw.draw_text("Player Level: "+str(player.player_level), 28, (255,255,255), 20, 10, True, surface=window)
                draw.draw_text("Experience: "+str(player.experience), 24, (255,255,255), 20, 55, True, surface = window)
                draw.draw_text("+"+str(experience - player.experience), 35, (0,255,0), 90, 90, surface=window)
                restart_btn.drawn = True
                back_btn.drawn = True
                next_btn.drawn = True
                restart_btn.draw_button(window)
                back_btn.draw_button(window)
                next_btn.draw_button(window)
                pygame.display.update()

            elif player.health == 0:
                draw.draw(window, background, bg_image, player, level_4.level_objects, offset_x, offset_y, level_4.level_items)
                draw.draw_text("You Died... Retry?", 40, (255,0,0), load.Width / 2.6, load.Height / 4, None, surface = window)
                level_4.reset(level_4.removed_items)
                draw.draw_text("Player Level: "+str(player.player_level), 28, (255,255,255), 20, 10, True, surface=window)
                draw.draw_text("Experience: "+str(player.experience), 24, (255,255,255), 20, 55, True, surface = window)
                restart_btn.drawn = True
                back_btn.drawn = True
                restart_btn.draw_button(window)
                back_btn.draw_button(window)
                pygame.display.update()

            elif player.lvl_timer == level_timer:
                player.countdown = False
                draw.draw(window, background, bg_image, player, level_4.level_objects, offset_x, offset_y, level_4.level_items)
                draw.draw_text("You ran out of time... Retry?", 40, (255,0,0), load.Width / 2.6, load.Height / 4, None, surface = window)
                level_4.reset(level_4.removed_items)
                draw.draw_text("Player Level: "+str(player.player_level), 28, (255,255,255), 20, 10, True, surface=window)
                draw.draw_text("Experience: "+str(player.experience), 24, (255,255,255), 20, 55, True, surface = window)
                restart_btn.drawn = True
                back_btn.drawn = True
                restart_btn.draw_button(window)
                back_btn.draw_button(window)
                pygame.display.update()

            else:
                player.loop(load.FPS)
                player.victory = False
                player.countdown = True
                for trap in level_4.traps:
                    trap.loop()
                for item in level_4.level_items:
                    item.loop()
                collision.handle_movement(player, level_4.level_objects, level_4.level_items)       
                draw.draw(window, background, bg_image, player, level_4.level_objects, offset_x, offset_y, items=level_4.level_items)
                level_4.pointer_helper.draw(window, offset_x, offset_y)
                if player.low_grav:
                    draw.draw_text(str(round(((300 - player.low_grav_timer) / 60), 1)), 35, (255,255,255), 
                                   player.rect.left + 50, player.rect.top - 30, None, offset_x, offset_y, window)
                draw.draw_text("Player Level: "+str(player.player_level), 28, (255,255,255), 20, 10, True, surface=window)
                draw.draw_text("Experience: "+str(player.experience), 24, (255,255,255), 20, 55, True, surface = window)
                draw.draw_text(str(player.health), 30, (255,0,0), 
                    player.rect.left + 20, player.rect.top - 40, None, offset_x, offset_y, surface=window)
                draw.draw_text("Coins: "+str(player.coins), 35, (255,255,255), 
                    load.Width - load.Width / 7.5, 10, True, surface=window)
                if ((level_timer - player.lvl_timer) / 60 > 10):
                    draw.draw_text(str(round(((level_timer - player.lvl_timer) / 60), 1)), 45, (255,255,255), 
                        load.Width / 2, load.Height / 10, None, surface=window)
                else:
                    draw.draw_text(str(round(((level_timer - player.lvl_timer) / 60), 1)), 70, (255,50,50), 
                        load.Width / 2, load.Height / 10, None, surface=window)
                draw.draw_text("Level 4", 35, (255,0,0), 270, 450, None, offset_x, offset_y, window)
                draw.draw_text("Beat the CLOCK!", 
                               27, (255,255,255), 250, 500, None, offset_x, offset_y, window)
                
                talent_tree_btn.drawn = True
                talent_tree_btn.draw_button(window)
                level_restart_btn.drawn = True
                level_restart_btn.draw_button(window)
                level_back_btn.drawn = True
                level_back_btn.draw_button(window)
            
                #HORIZONTAL SCROLLING
                if ((player.rect.right - offset_x >= load.Width - scroll_area_width) and player.x_vel > 0) or (
                        (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                    offset_x += player.x_vel

                #VERTICAL SCROLLING
                if ((player.rect.bottom - offset_y >= load.Height - scroll_area_height) and player.y_vel > 0) or (
                        (player.rect.top - offset_y <= scroll_area_height) and player.y_vel < 0):
                    offset_y += player.y_vel

                pygame.display.update()

        #LEVEL 5
        elif level == 5:
            player.in_level = True
            level_timer = 1500 + (player.level_time_talent_point * 150)
            
            level_5.finish_flag.idle()
            for trap in level_5.traps:
                trap.on()
            for btn in level_buttons:
                btn.drawn = False
            for item in level_5.level_items:
                if item.vanish == load.FPS:
                    level_5.level_items.remove(item)
                    level_5.removed_items.append(item)

            #if all victory conditions are met
            if player.victory and player.coins == 1:
                if not lvl5_exp_given:
                    experience += round(((level_timer - player.lvl_timer) / 60), 0)
                    lvl5_exp_given = True
                    load.MAX_LEVEL += 1
                draw.draw(window, background, bg_image, player, level_5.level_objects, offset_x, offset_y, level_5.level_items)
                draw.draw_text("To the winner, go the spoils...", 45, (255,200,0), load.Width / 4, load.Height / 4, None, surface = window)
                level_5.reset(level_5.removed_items)
                draw.draw_text("Player Level: "+str(player.player_level), 28, (255,255,255), 20, 10, True, surface=window)
                draw.draw_text("Experience: "+str(player.experience), 24, (255,255,255), 20, 55, True, surface = window)
                draw.draw_text("+"+str(experience - player.experience), 35, (0,255,0), 90, 90, surface=window)
                restart_btn.drawn = True
                back_btn.drawn = True
                next_btn.drawn = True
                restart_btn.draw_button(window)
                back_btn.draw_button(window)
                next_btn.draw_button(window)
                pygame.display.update()

            #if player health reaches zero
            elif player.health == 0:
                draw.draw(window, background, bg_image, player, level_5.level_objects, offset_x, offset_y, level_5.level_items)
                draw.draw_text("You Died... Retry?", 40, (255,0,0), load.Width / 2.6, load.Height / 4, None, surface = window)
                level_5.reset(level_5.removed_items)
                draw.draw_text("Player Level: "+str(player.player_level), 28, (255,255,255), 20, 10, True, surface=window)
                draw.draw_text("Experience: "+str(player.experience), 24, (255,255,255), 20, 55, True, surface = window)
                restart_btn.drawn = True
                back_btn.drawn = True
                restart_btn.draw_button(window)
                back_btn.draw_button(window)
                pygame.display.update()

            #if player runs out of time
            elif player.lvl_timer == level_timer:
                player.countdown = False
                draw.draw(window, background, bg_image, player, level_5.level_objects, offset_x, offset_y, level_5.level_items)
                draw.draw_text("You ran out of time... Retry?", 40, (255,0,0), load.Width / 2.6, load.Height / 4, None, surface = window)
                level_5.reset(level_5.removed_items)
                draw.draw_text("Player Level: "+str(player.player_level), 28, (255,255,255), 20, 10, True, surface=window)
                draw.draw_text("Experience: "+str(player.experience), 24, (255,255,255), 20, 55, True, surface = window)
                restart_btn.drawn = True
                back_btn.drawn = True
                restart_btn.draw_button(window)
                back_btn.draw_button(window)
                pygame.display.update()

            #general level state
            else:
                player.loop(load.FPS)
                player.victory = False
                player.countdown = True
                for trap in level_5.traps:
                    trap.loop()
                for item in level_5.level_items:
                    item.loop()
                collision.handle_movement(player, level_5.level_objects, level_5.level_items)       
                draw.draw(window, background, bg_image, player, level_5.level_objects, offset_x, offset_y, items=level_5.level_items)
                level_5.pointer_helper.draw(window, offset_x, offset_y)

                #load player UI
                if player.low_grav:
                    draw.draw_text(str(round(((300 - player.low_grav_timer) / 60), 1)), 35, (255,255,255), 
                                   player.rect.left + 50, player.rect.top - 30, None, offset_x, offset_y, window)
                draw.draw_text("Player Level: "+str(player.player_level), 28, (255,255,255), 20, 10, True, surface=window)
                draw.draw_text("Experience: "+str(player.experience), 24, (255,255,255), 20, 55, True, surface = window)
                draw.draw_text(str(player.health), 30, (255,0,0), 
                            player.rect.left + 20, player.rect.top - 40, None, offset_x, offset_y, surface=window)
                draw.draw_text("Coins: "+str(player.coins), 35, (255,255,255), 
                    load.Width - load.Width / 7.5, 10, True, surface=window)
                if ((level_timer - player.lvl_timer) / 60 > 7):
                    draw.draw_text(str(round(((level_timer - player.lvl_timer) / 60), 1)), 45, (255,255,255), 
                        load.Width / 2, load.Height / 10, None, surface=window)
                else:
                    draw.draw_text(str(round(((level_timer - player.lvl_timer) / 60), 1)), 70, (255,50,50), 
                        load.Width / 2, load.Height / 10, None, surface=window)
                    
                draw.draw_text("Level 5", 35, (255,0,0), 270, 450, None, offset_x, offset_y, window)
                
                talent_tree_btn.drawn = True
                talent_tree_btn.draw_button(window)
                level_restart_btn.drawn = True
                level_restart_btn.draw_button(window)
                level_back_btn.drawn = True
                level_back_btn.draw_button(window)
            
                #HORIZONTAL SCROLLING
                if ((player.rect.right - offset_x >= load.Width - scroll_area_width) and player.x_vel > 0) or (
                        (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                    offset_x += player.x_vel

                #VERTICAL SCROLLING
                if ((player.rect.bottom - offset_y >= load.Height - scroll_area_height) and player.y_vel > 0) or (
                        (player.rect.top - offset_y <= scroll_area_height) and player.y_vel < 0):
                    offset_y += player.y_vel

                pygame.display.update()


        #TALENT PAGE
        elif level == 997:
            for btn in level_buttons:
                btn.drawn = False
            draw.draw(window, background, bg_image)
            draw.draw_text("Talents", 35, (255,255,255), load.Width / 2.2, load.Height / 10, True, surface = window)
            draw.draw_text("Player Level: "+str(player.player_level), 28, (255,255,255), 20, 10, True, surface=window)
            draw.draw_text("Experience: "+str(player.experience), 24, (255,255,255), 20, 55, True, surface = window)
            draw.draw_text("Available Talent Points: "+str(player.talent_points), 32, (255,255,255), load.Width / 2.8, load.Height - load.Height / 3.9, surface=window)
            for btn in talent_tree:
                btn.drawn = True
                btn.draw_lvl_btn(window, player.talent_points, talents)
            resume_btn.drawn = True
            resume_btn.draw_button(window)
            talent_reset_btn.drawn = True
            talent_reset_btn.draw_lvl_btn(window)
            level_back_btn.drawn = True
            level_back_btn.draw_button(window)
            pygame.display.update()


        #LEVEL SELECT
        if level == 998:
            for btn in level_buttons:
                btn.drawn = False
            draw.draw(window, background, bg_image)
            draw.draw_text("Level Selection", 35, (255,255,255), 30, 30, True, surface = window)
            
            #draw level buttons
            i = 0
            for level_name in all_levels:
                i += 1
                if i <= load.MAX_LEVEL:
                    level_name.drawn = True
                    level_name.draw_lvl_btn(window)
                    draw.draw_text("Level " + str(i), 30, (255,255,255), 160, 90 * i, surface = window)
                else:
                    break

            back_btn.drawn = True
            back_btn.draw_button(window)
            pygame.display.update()


        #SETTINGS
        if level == 999:
            for btn in level_buttons:
                btn.drawn = False

            draw.draw(window, background, bg_image)
            draw.draw_text("Work in progress ;D", 45, (255,255,255), load.Width/3, load.Height/3, surface = window)
            
            
            back_btn.drawn = True
            back_btn.draw_button(window)

            pygame.display.update()
    

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(load.window)