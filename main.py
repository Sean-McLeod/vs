#!/usr/bin/env python3

# Created by Sean McLeod
# Created on June 2021
# This is the prison escape game

import time
from sprites import Sprites
import sys

import constants
import pygame
import random
from bullets import BulletClass
from check_prisoner_events import CheckPrisonerEvents
from game_features import GetModifiedButton, SoundOnOff, TextClass, TrackTime
from pygame import mixer
from set_up_scenes import SetUpScenes


def hit_sound():
    hit_sound = mixer.Sound(constants.HIT_SOUND)
    hit_sound.play()

def click_sound():
    click_sound = mixer.Sound("Sounds/click.wav")
    click_sound.play()


def did_you_win(is_win, my_time, die_reason = " "):
    pygame.mixer.music.stop()
    clock = pygame.time.Clock()
    falling_sound = mixer.Sound("Sounds/falling.wav")
    # font
    main_font = pygame.font.SysFont(constants.FONT_COMIC, constants.TITLE_SIZE)
    if is_win:
        text = "You Win!"
        # play sound
        falling_sound.play()
    else:
        text = "You Lose!"

    # text
    main_text = main_font.render(text, False, constants.BLACK)

    # background
    win_background = pygame.image.load("Backgrounds/You-Won.jpg")
    # portraits
    main_icon = pygame.image.load("Backgrounds/Main_icon.png")
    # change size
    main_icon = pygame.transform.scale(main_icon, (146, 146))

    # create object
    my_icon = Sprites(main_icon, 427, -700, 0, 0, screen)

    # prepare sound
    mixer.music.load("Sounds/win_sound.mp3")
    hit_effect = True

    # object
    my_button = GetModifiedButton()
    re_button = my_button.get_re_button()

    # fps stuff
    last_time = time.time()
    FPS = 30
    icon_vel = 5

    running = True
    while running:
        dt = time.time() - last_time
        dt *= 30
        last_time = time.time()
        # screen fill
        screen.fill(constants.WHITE)

        # display text
        if die_reason != " ":
            if die_reason == "golem":
                image = "Backgrounds/You_Lose/golem_background.png"
            elif die_reason == "dragon":
                image = "Backgrounds/You_Lose/dragon_background.jpg"
            elif die_reason == "wall":
                image = "Backgrounds/You_Lose/wall_background.jpg"
            elif die_reason == "shadow":
                image = "Backgrounds/You_Lose/shadow_background.jpg"
            elif die_reason == "ship":
                image = "Backgrounds/You_Lose/ship_background.jpg"
            elif die_reason == "laser":
                image = "Backgrounds/You_Lose/laser_background.jpg"
            # background
            background = pygame.image.load(image)
            screen.blit(background, (0, 0))
            my_time.display_static_time(constants.BLACK)
        else:
            # background
            screen.blit(win_background, (0, 0))
            # get rect
            icon_rect = my_icon.get_rect()
            pygame.draw.rect(screen, (255, 0, 0), icon_rect)
            # simple animation of icon
            if icon_rect.y < 286:
                h = icon_vel * dt
                my_icon.sprite_move(0, h)
            if hit_effect:
                if icon_rect.y == 286:
                    hit_effect = False
                    mixer.music.play()

            # upload icon
            my_icon.sprite_upload()
            my_time.display_felxible_time(constants.RED, constants.MIDDLE_X - 170, 580)

        # display time
        screen.blit(main_text, (constants.MIDDLE_X - 170, constants.TITLE_Y - 10))

        # create button
        re_button.draw_button(
            screen,
            constants.BACK_BUTTON_TEXT_SIZE,
            constants.FONT_COMIC,
            constants.BUTTON_OUTLINE,
        )

        # get mouse position
        mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if re_button.is_over(mouse_position):
                    re_button.color = constants.MINT
                else:
                    re_button.color = constants.LIGHT_GRAY
            if event.type == pygame.MOUSEBUTTONDOWN:
                if re_button.is_over(mouse_position):
                    click_sound()
                    start_screen()

        # refresh the screen every frame
        pygame.display.update()
        # slow down to see the animations move
        clock.tick(FPS)


def credits_page():
    # text
    title_font = pygame.font.SysFont(constants.TITLE_FONT, constants.TITLE_SIZE)
    title_text = title_font.render("Credits", False, constants.BLACK)

    main_font = pygame.font.SysFont(constants.FONT_COMIC, 16)

    # object
    my_button = GetModifiedButton()
    back_button = my_button.get_back_button()
    my_long_text = TextClass()
    set_scene = SetUpScenes(screen)

    # Game loop
    running = True
    while running:
        # upload image
        screen.fill(constants.GREEN)

        # display title
        screen.blit(title_text, (constants.MIDDLE_X - 100, constants.TITLE_Y))
        # display text
        my_long_text.sentence_generate(
            screen, constants.CREDIT_TEXT, (190, 210), main_font
        )

        # draw back_button
        set_scene.draw_back_button(back_button)

        # event handle
        if set_scene.credit_and_about_event(back_button):
            click_sound()
            option_page()

        # refresh the screen every frame
        pygame.display.update()


def about_page():
    # text
    title_font = pygame.font.SysFont(constants.TITLE_FONT, constants.TITLE_SIZE)
    title_text = title_font.render("About", False, constants.BLACK)

    main_font = pygame.font.SysFont(constants.FONT_COMIC, 30)

    # object
    my_button = GetModifiedButton()
    back_button = my_button.get_back_button()
    set_scene = SetUpScenes(screen)

    my_long_text = TextClass()

    # Game loop
    running = True
    while running:
        # upload image
        screen.fill(constants.LIGHT_GRAY)

        # display title
        screen.blit(title_text, (constants.MIDDLE_X - 100, constants.TITLE_Y))
        # display text
        my_long_text.sentence_generate(
            screen, constants.ABOUT_TEXT, (180, 240), main_font
        )

        # draw back_button
        set_scene.draw_back_button(back_button)

        # event handle
        if set_scene.credit_and_about_event(back_button):
            click_sound()
            option_page()

        # refresh the screen every frame
        pygame.display.update()


def option_page():
    text_size = 60

    # create objects
    my_button = GetModifiedButton()
    (
        about_button,
        sound_button,
        credits_button,
        back_button,
    ) = my_button.get_options_scene_buttons()
    sound_toggle = SoundOnOff()

    # text
    my_font = pygame.font.SysFont(constants.TITLE_FONT, constants.TITLE_SIZE)
    text_surface = my_font.render("Options", False, constants.BLACK)

    # Game loop
    running = True
    while running:
        # upload image
        screen.fill(constants.WHITE)

        # display title
        screen.blit(text_surface, (constants.MIDDLE_X - 160, constants.TITLE_Y))

        # create button
        about_button.draw_button(
            screen, text_size, constants.FONT_CORBEL, constants.BUTTON_OUTLINE
        )
        sound_button.draw_button(
            screen, text_size, constants.FONT_CORBEL, constants.BUTTON_OUTLINE
        )
        credits_button.draw_button(
            screen, text_size, constants.FONT_CORBEL, constants.BUTTON_OUTLINE
        )
        back_button.draw_button(
            screen,
            constants.BACK_BUTTON_TEXT_SIZE,
            constants.FONT_CORBEL,
            constants.BUTTON_OUTLINE,
        )

        for event in pygame.event.get():
            # get mouse position
            mouse_position = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEMOTION:
                # change color when mouse is over button
                if about_button.is_over(mouse_position):
                    about_button.color = constants.LIGHT_RED
                else:
                    about_button.color = constants.LIGHT_GRAY
                if sound_button.is_over(mouse_position):
                    sound_button.color = constants.LIGHT_RED
                else:
                    sound_button.color = constants.LIGHT_BLUE
                if credits_button.is_over(mouse_position):
                    credits_button.color = constants.LIGHT_RED
                else:
                    credits_button.color = constants.GREEN
                if back_button.is_over(mouse_position):
                    back_button.color = constants.PURPLE
                else:
                    back_button.color = constants.LIGHT_GREEN
            if event.type == pygame.MOUSEBUTTONDOWN:
                # move to certain page when button clicked
                if about_button.is_over(mouse_position):
                    click_sound()
                    about_page()
                if credits_button.is_over(mouse_position):
                    click_sound()
                    credits_page()
                if sound_button.is_over(mouse_position):
                    click_sound()
                    sound_toggle.toggle_music()
                if back_button.is_over(mouse_position):
                    click_sound()
                    start_screen()
            if event.type == pygame.QUIT:
                sys.exit()

        # refresh the screen every frame
        pygame.display.update()


def third_game_scene(my_time, prisoner_list, left_prisoner_list, one_prisoner):
    # create clock
    clock = pygame.time.Clock()
    cool_down_counter = constants.BULLET_WAIT
    first_ship_bullets = []
    second_ship_bullets = []

    # prisoner variables
    x = 120
    y = 650
    vel = 10
    left = False
    right = False
    up = False
    down = False
    walkCount = 0
    walkCount2 = 0
    left_visit = False
    right_visit = True
    counter = 0

    # create background
    background = pygame.image.load(constants.SCENE_THREE)

    # create object
    my_setup = SetUpScenes(screen)
    (
        my_prisoner,
        my_ship,
        my_ship_two,
        my_door,
    ) = my_setup.set_up_game_scene_three()

    my_bullet = BulletClass(screen, constants.BULLET_X_SPEED, constants.BULLET_Y_SPEED)

    # fps stuff
    last_time = time.time()
    FPS = 30

    running = True
    while running:
        dt = time.time() - last_time
        dt *= 30
        last_time = time.time()
        cool_down_counter += 2

        # upload image
        screen.blit(background, (0, 0))
        my_door.sprite_upload()

        # get rect
        prisoner_rect = pygame.Rect(
            x, y, constants.PRISONER_SIZE[0], constants.PRISONER_SIZE[1]
        )
        # pygame.draw.rect(screen, (255, 0, 0), prisoner_rect)
        door_rect = pygame.Rect(
            constants.DOOR_THREE_X, constants.DOOR_THREE_Y, 123, 10
        )

        # get events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

       # prisoner events
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x > 87: 
            x -= vel * dt
            left = True
            right = False
        elif keys[pygame.K_RIGHT] and x < 1000 - vel - 140:  
            x += vel * dt
            left = False
            right = True
        else: 
            left = False
            right = False
            walkCount = 0
        if keys[pygame.K_UP] and y > 0:
            up = True
            down = False
            y -= (vel - 2) * dt
        elif keys[pygame.K_DOWN] and y < 750 - vel - 79:
            up = False
            down = True
            y += (vel - 2) * dt
        else: 
            up = False
            down = False
            walkCount2 = 0

        if walkCount + 1 >= 9:
            walkCount = 0
        if walkCount2 + 1 >= 9:
            walkCount2 = 0

        counter += 0.8
        
        if left:
            left_visit = True
            right_visit = False
            screen.blit(left_prisoner_list[walkCount], (x,y))
            if counter > 1:
                counter = 0
                walkCount += 1                          
        elif right:
            right_visit = True
            left_visit = False
            screen.blit(prisoner_list[walkCount], (x,y))
            if counter > 1:
                counter = 0
                walkCount += 1   
        elif up:
            if left_visit:
                screen.blit(left_prisoner_list[walkCount2], (x,y))
            if right_visit:
                screen.blit(prisoner_list[walkCount2], (x,y))
            if counter > 1:
                counter = 0
                walkCount2 += 1
        elif down:
            if left_visit:
                screen.blit(left_prisoner_list[walkCount2], (x,y))
            if right_visit:
                screen.blit(prisoner_list[walkCount2], (x,y))
            if counter > 1:
                counter = 0
                walkCount2 += 1
        else:
            if left_visit:
                screen.blit(pygame.transform.flip((one_prisoner), True, False), (x, y))
            elif right_visit:
                screen.blit(one_prisoner, (x, y))
            walkCount = 0
            walkCount2 = 0

        # fire a bullet if the counter refreshed
        if cool_down_counter > constants.BULLET_SHOOT_RATE:
            cool_down_counter = 0
            my_bullet.create_bullets(
                first_ship_bullets,
                second_ship_bullets,
                my_ship.get_rect(),
                my_ship_two.get_rect(),
            )

        # draw the bullets
        my_bullet.draw(first_ship_bullets, second_ship_bullets)

        # check bullet events
        did_shoot = my_bullet.handle_bullets(
            first_ship_bullets, second_ship_bullets, prisoner_rect
        )

        # move ship
        my_ship.ship_move()
        my_ship_two.another_ship_move()

        # check collision
        if my_ship.attack(prisoner_rect) or my_ship_two.attack(prisoner_rect):
            hit_sound()
            did_you_win(False, my_time, "ship")
        elif did_shoot:
            hit_sound()
            did_you_win(False, my_time, "laser")

        # exit
        if my_door.check_collision(door_rect, prisoner_rect):
            did_you_win(True, my_time)


        # upload sprites
        my_ship.sprite_upload()
        my_ship_two.sprite_upload()

        # display time
        my_time.track_time()

        # refresh the screen every frame
        pygame.display.update()
        # slow down to see the animations move
        clock.tick(FPS)


def second_game_scene(my_time):
    clock = pygame.time.Clock()
    chest_open = False
    door_open = False
    key_appear = True
    shadow_appear = False
    random_number = random.randint(0, 4)
    mush_alive = True

    # prisoner variables
    x = 900
    y = 660
    vel = 7
    left = False
    right = False
    up = False
    down = False
    walkCount = 0
    walkCount2 = 0
    left_visit = True
    right_visit = False
    counter = 0

    # prisoner outfits
    prisoner_list = constants.prisoners
    left_prisoner_list = constants.prisoners_left
    one_prisoner = constants.one_prisoner

    # create background
    background = pygame.image.load(constants.SCENE_TWO)
    # upload image
    chest_opened = pygame.image.load(constants.CHEST_OPEN)

    # sound
    electrocute = mixer.Sound(constants.ELECTRIC_SOUND)
    warp_sound = mixer.Sound(constants.WARP)

    # set up objects
    my_setup = SetUpScenes(screen)

    (
        my_prisoner,
        my_door,
        my_cell_map,
        my_chest,
        my_key,
        my_shadow,
    ) = my_setup.set_up_game_scene_two()

    # increase chest size
    my_chest.modify_sprite_size(3)
    my_key.modify_sprite_size(constants.DOUBLE_SIZE)
    # dark_door = pygame.transform.scale(pygame.image.load("Doors/dark_door.png"), (72, 77))

    # fps stuff
    last_time = time.time()
    FPS = 30

    running = True
    while running:
        dt = time.time() - last_time
        dt *= 30
        last_time = time.time()
        # upload image
        screen.blit(background, (0, 0))

        mushroom_rect = pygame.Rect(47, 650, constants.MUSH_S[0], constants.MUSH_S[1])

        # get rect
        prisoner_rect = pygame.Rect(
            x, y + 5, constants.PRISONER_SIZE[0] - 5, constants.PRISONER_SIZE[1]
        )
        # pygame.draw.rect(screen, (255, 0, 0), prisoner_rect)
        door_rect = my_door.get_rect()
        chest_rect = my_chest.get_rect()
        key_rect = my_key.get_rect()
        # pygame.draw.rect(screen, (255, 0, 0), key_rect)

        # build map
        did_map_collide = my_cell_map.build_map(prisoner_rect)

        if mush_alive:
            screen.blit(constants.mushroom_list[random_number], (47, 650))
            if my_prisoner.check_collision(prisoner_rect, mushroom_rect):
                eat_sound = mixer.Sound(constants.EAT)
                eat_sound.play()
                mush_alive = False
                if random_number == 0:
                    prisoner_list = constants.red_prisoners
                    left_prisoner_list = constants.red_prisoners_left
                    one_prisoner = constants.red_one_prisoner
                elif random_number == 1:
                    prisoner_list = constants.sparta_prisoners
                    left_prisoner_list = constants.sparta_prisoner_left
                    one_prisoner = constants.sparta_one_prisoner
                elif random_number == 2:
                    prisoner_list = constants.viking_prisoners
                    left_prisoner_list = constants.viking_prisoners_left
                    one_prisoner = constants.viking_one_prisoner
                elif random_number == 3:
                    prisoner_list = constants.white_prisoners
                    left_prisoner_list = constants.white_prisoners_left
                    one_prisoner = constants.white_one_prisoner
                elif random_number == 4:
                    prisoner_list = constants.witch_prisoners
                    left_prisoner_list = constants.witch_prisoners_left
                    one_prisoner = constants.witch_one_prisoner
    

        # get events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # prisoner events
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x > 0: 
            x -= vel * dt
            left = True
            right = False
        elif keys[pygame.K_RIGHT] and x < 1000 - vel - 45:  
            x += vel * dt
            left = False
            right = True
        else: 
            left = False
            right = False
            walkCount = 0
        if keys[pygame.K_UP] and y > 0:
            up = True
            down = False
            y -= (vel-1) * dt
        elif keys[pygame.K_DOWN] and y < 750 - vel - 79:
            up = False
            down = True
            y += (vel-1) * dt
        else: 
            up = False
            down = False
            walkCount2 = 0

        if walkCount + 1 >= 9:
            walkCount = 0
        if walkCount2 + 1 >= 9:
            walkCount2 = 0

        counter += 0.8
        
        if left:
            left_visit = True
            right_visit = False
            screen.blit(left_prisoner_list[walkCount], (x,y))
            if counter > 1:
                counter = 0
                walkCount += 1                          
        elif right:
            right_visit = True
            left_visit = False
            screen.blit(prisoner_list[walkCount], (x,y))
            if counter > 1:
                counter = 0
                walkCount += 1   
        elif up:
            if left_visit:
                screen.blit(left_prisoner_list[walkCount2], (x,y))
            if right_visit:
                screen.blit(prisoner_list[walkCount2], (x,y))
            if counter > 1:
                counter = 0
                walkCount2 += 1
        elif down:
            if left_visit:
                screen.blit(left_prisoner_list[walkCount2], (x,y))
            if right_visit:
                screen.blit(prisoner_list[walkCount2], (x,y))
            if counter > 1:
                counter = 0
                walkCount2 += 1
        else:
            if left_visit:
                screen.blit(pygame.transform.flip((one_prisoner), True, False), (x, y))
            elif right_visit:
                screen.blit(one_prisoner, (x, y))
            walkCount = 0
            walkCount2 = 0

        if my_chest.check_collision(chest_rect, prisoner_rect):
            chest_open = True
            my_chest.set_sprite(chest_opened)
            my_chest.modify_sprite_size(3)

        if chest_open:
            if key_appear:
                my_key.sprite_upload()
                if my_prisoner.check_collision(prisoner_rect, key_rect):
                    key_sound = mixer.Sound(constants.KEY_SOUND)
                    key_sound.play()
                    door_open = True
                    key_appear = False
                    shadow_appear = True

        # upload sprites
        my_chest.sprite_upload()

        if shadow_appear:
            # upload door
            my_door.portal_animation(constants.portal_list)
            # upload shadows
            my_shadow.upload()

        # check collision
        if (x < 354 or x > 422) or (y < 342 or y > 396):
            if my_shadow.attack(prisoner_rect):
                hit_sound()
                did_you_win(False, my_time, "shadow")
        if did_map_collide:
            electrocute.play()
            did_you_win(False, my_time, "wall")

        # collision detection
        if my_door.check_collision(door_rect, prisoner_rect):
            if door_open:
                warp_sound.play()
                third_game_scene(my_time, prisoner_list, left_prisoner_list, one_prisoner)
            else:
                print("Cant open!!")

        # display time
        my_time.track_time()

        # refresh the screen every frame
        pygame.display.update()
        # slow down to see the animations move
        clock.tick(FPS)


def first_game_scene():
    # create clock
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    
    # prisoner variables
    x = 150
    y = 600
    vel = 7
    left = False
    right = False
    up = False
    down = False
    walkCount = 0
    walkCount2 = 0
    left_visit = False
    right_visit = True
    counter = 0

    # prisoner lists
    prisoner_list = constants.prisoners
    left_prisoner_list = constants.prisoners_left
    one_prisoner = constants.one_prisoner

    # create background
    background = pygame.image.load(constants.SCENE_ONE)
    barrel = pygame.image.load("Backgrounds/Wooden_Barrel.png")

    # font stuff
    first_font = pygame.font.SysFont("mvboli", 60)
    font_counter = 0
    message = "Use Arrow Keys To Move"


    # create music
    mixer.music.load(constants.GAME_SOUND)
    mixer.music.play(-1)

    # create objects
    my_time = TrackTime(start_time, screen)
    my_setup = SetUpScenes(screen)
    (
        my_prisoner,
        my_golem,
        my_golem_two,
        my_dragon,
        my_cell_map,
        my_door,
    ) = my_setup.set_up_game_scene_one()


    # fps stuff
    last_time = time.time()
    FPS = 30

    running = True
    while running:
        dt = time.time() - last_time
        dt *= 30
        last_time = time.time()

        # upload image
        screen.blit(background, (0, 0))

        # upload door
        my_door.sprite_upload()

        # get rect
        prisoner_rect = pygame.Rect(
            x + 15, y, constants.PRISONER_SIZE[0] - 30, constants.PRISONER_SIZE[1]
        )
        # pygame.draw.rect(screen, (255, 0, 0), prisoner_rect)
        door_rect = my_door.get_rect()

        # sound
        electrocute = mixer.Sound(constants.ELECTRIC_SOUND)
        door_sound = mixer.Sound(constants.DOOR_SOUND)

        # build map
        did_map_collide = my_cell_map.build_map(prisoner_rect)

        # get events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # prisoner events
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x > 0: 
            x -= vel * dt
            left = True
            right = False
        elif keys[pygame.K_RIGHT] and x < 1000 - vel - 45:  
            x += vel * dt
            left = False
            right = True
        else: 
            left = False
            right = False
            walkCount = 0
        if keys[pygame.K_UP] and y > 0:
            up = True
            down = False
            y -= vel * dt
        elif keys[pygame.K_DOWN] and y < 750 - vel - 79:
            up = False
            down = True
            y += vel * dt
        else: 
            up = False
            down = False
            walkCount2 = 0

        if walkCount + 1 >= 9:
            walkCount = 0
        if walkCount2 + 1 >= 9:
            walkCount2 = 0

        counter += 0.8

        if left:
            left_visit = True
            right_visit = False
            screen.blit(left_prisoner_list[walkCount], (x,y))
            if counter > 1:
                counter = 0
                walkCount += 1                        
        elif right:
            right_visit = True
            left_visit = False
            screen.blit(prisoner_list[walkCount], (x,y))
            if counter > 1:
                counter = 0
                walkCount += 1   
        elif up:
            if left_visit:
                screen.blit(left_prisoner_list[walkCount2], (x,y))
            if right_visit:
                screen.blit(prisoner_list[walkCount2], (x,y))
            if counter > 1:
                counter = 0
                walkCount2 += 1
        elif down:
            if left_visit:
                screen.blit(left_prisoner_list[walkCount2], (x,y))
            if right_visit:
                screen.blit(prisoner_list[walkCount2], (x,y))
            if counter > 1:
                counter = 0
                walkCount2 += 1
        else:
            if left_visit:
                screen.blit(pygame.transform.flip((one_prisoner), True, False), (x, y))
            elif right_visit:
                screen.blit(one_prisoner, (x, y))
            walkCount = 0
            walkCount2 = 0

        # move golem one
        my_golem.golem_move()
        # modify size
        my_golem.modify_sprite_size(constants.DOUBLE_SIZE)
        # upload golem one
        my_golem.sprite_upload()

        # move golem two
        my_golem_two.golem_move()
        # modify size
        my_golem_two.modify_sprite_size(constants.DOUBLE_SIZE)
        # upload golem two
        my_golem_two.sprite_upload()

        # upload dragon
        my_dragon.sprite_animation(constants.dragon_list)
        screen.blit(barrel, (850, 600))

        # check collision
        if my_dragon.attack(prisoner_rect):
            hit_sound()
            did_you_win(False, my_time, "dragon")
        elif my_golem.attack(prisoner_rect):
            hit_sound()
            did_you_win(False, my_time, "golem")
        elif my_golem_two.attack(prisoner_rect):
            hit_sound()
            did_you_win(False, my_time, "golem")
        elif did_map_collide:
            electrocute.play()
            did_you_win(False, my_time, "wall")

        # when prisoner gets to the door, end loop and move scene
        if my_door.check_collision(door_rect, prisoner_rect):
            door_sound.play()
            second_game_scene(my_time)

        # display time
        my_time.track_time()

        font_counter += 1
        for i in range(font_counter < 100):
            screen.blit(first_font.render(message, True, constants.BLACK), (130, 180))

        # refresh the screen every frame
        pygame.display.update()
        # slow down to see the animations move
        clock.tick(FPS)


def splash_screen():
    # create background
    background = pygame.image.load(constants.SPLASH_SCREEN)

    # create icon image
    surface = pygame.image.load("jail.png")

    # upload image
    screen.blit(background, (0, 0))

    # set caption
    pygame.display.set_caption("Prison Escape")

    # update icon
    pygame.display.set_icon(surface)

    # update splash screen once
    pygame.display.update()

    # wait 1000ms
    pygame.time.wait(constants.WAIT)


def start_screen():
    text_size = 90
    outline = 0

    # create background
    background = pygame.image.load(constants.START_SCREEN)

    # create music
    mixer.music.load(constants.START_SOUND)
    mixer.music.play()

    # create object
    my_buttons = GetModifiedButton()
    (
        start_button,
        option_button,
        quit_button,
    ) = my_buttons.get_start_scene_buttons()

    # Game loop
    running = True
    while running:
        # upload image
        screen.blit(background, (0, 0))

        # create button
        start_button.draw_button(screen, text_size, constants.FONT_COMIC, outline)
        option_button.draw_button(screen, text_size - 20, constants.FONT_COMIC, outline)
        quit_button.draw_button(screen, text_size - 20, constants.FONT_COMIC, outline)

        # get mouse position
        mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if start_button.is_over(mouse_position):
                    start_button.color = constants.LIGHT_RED
                else:
                    start_button.color = constants.LAVENDAR

                if option_button.is_over(mouse_position):
                    option_button.color = constants.MINT
                else:
                    option_button.color = constants.SKY_BLUE

                if quit_button.is_over(mouse_position):
                    quit_button.color = constants.MINT
                else:
                    quit_button.color = constants.ROYAL_BLUE
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_over(mouse_position):
                    click_sound()
                    first_game_scene()
                elif option_button.is_over(mouse_position):
                    click_sound()
                    option_page()
                elif quit_button.is_over(mouse_position):
                    click_sound()
                    sys.exit()
            if event.type == pygame.QUIT:
                sys.exit()
        # update screen
        pygame.display.update()


import random
def font_ex():
    # mvboli
    big_font = pygame.font.SysFont("mvboli", 60)
    message = "Time: " + str(32.34)
    current_image = 0
    counter = 0

    random_number = random.randint(0, 4)

    while True:
        counter += 1
        screen.fill(constants.WHITE)
        for i in range(counter < 2000):
            big_font = pygame.font.SysFont("mvboli", 60)
            screen.blit(big_font.render(message, True, constants.BLACK), (300, 400))

        mushroom_rect = pygame.Rect(300, 200, constants.MUSH_S[0], constants.MUSH_S[1])
        pygame.draw.rect(screen, (255, 0, 0), mushroom_rect)

        screen.blit(constants.mushroom_list[random_number], (300, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()

if __name__ == "__main__":
    # initialize pygame
    pygame.init()

    # create the screen
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

    my_time = TrackTime(5, screen)

    # splash_screen()
    # start_screen()
    # first_game_scene()
    third_game_scene(my_time, constants.prisoners, constants.prisoners_left, constants.one_prisoner)
  
