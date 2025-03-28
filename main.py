import pygame
from sys import exit
from random import randint


def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surface = test_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 8

            if obstacle_rect.bottom == sky_height:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle in obstacles:
            if player.colliderect(obstacle):
                return False
    return True


def player_animation():
    global player_surface, player_index

    if player_rect.bottom < sky_height:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Hello")
clock = pygame.time.Clock()
test_font = pygame.font.Font("fonts/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0

# test_surface = pygame.Surface((100, 200))
# test_surface.fill("Blue")

sky_surface = pygame.image.load("graphics/Sky.png").convert()
sky_height = sky_surface.get_height()

ground_surface = pygame.image.load("graphics/ground.png").convert()

# text_surface = test_font.render("My Game", False, (64, 64, 64))
# # text_width = text_sufrace.get_width()
# # text_start = (800 - text_width) // 2
# text_rect = text_surface.get_rect(center=(400, 50))

start_text = test_font.render("Press space to start", False, (111, 196, 169))
start_text_rect = start_text.get_rect(center=(400, 325))

snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()

fly_surface = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()

obstacle_rect_list = []

player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom=(80, sky_height))
player_gravity = 0


player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))


obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and player_rect.bottom >= sky_height:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= sky_height:
                    player_gravity = -20

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                # snail_rect.left = 800
                start_time = pygame.time.get_ticks()

        if game_active and event.type == obstacle_timer:
            if randint(0, 2):
                obstacle_rect_list.append(
                    snail_surface.get_rect(bottomright=(randint(900, 1100), sky_height))
                )
            else:
                obstacle_rect_list.append(
                    fly_surface.get_rect(
                        bottomright=(randint(900, 1100), sky_height - 90)
                    )
                )

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, sky_height))
        # pygame.draw.rect(screen, "#c0e8ec", text_rect)
        # pygame.draw.rect(screen, "#c0e8ec", text_rect, 6)
        # pygame.draw.line(screen, "Pink", (0, 0), pygame.mouse.get_pos(), 10)
        # pygame.draw.circle(screen, "Pink", pygame.mouse.get_pos(), 10)
        # screen.blit(text_surface, text_rect)
        score = display_score()

        # snail_rect.left -= 5
        # if snail_rect.left <= -100:
        #     snail_rect.left = 800
        # screen.blit(snail_surface, snail_rect)

        player_gravity += 1
        player_rect.y += player_gravity
        player_animation()
        screen.blit(player_surface, player_rect)

        if player_rect.bottom >= sky_height:
            player_rect.bottom = sky_height
            player_gravity = 0

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        game_active = collisions(player_rect, obstacle_rect_list)

        # collison
        # if snail_rect.colliderect(player_rect):
        #     game_active = False

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, sky_height)

        score_message = test_font.render(f"Your score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 90))
        if score > 0:
            screen.blit(score_message, score_message_rect)
        screen.blit(start_text, start_text_rect)

    pygame.display.update()
    clock.tick(60)

    # if player_rect.colliderect(snail_rect):
    #     print("Collision")

    # mouse_pos = pygame.mouse.get_pos()

    # if player_rect.collidepoint((mouse_pos)):
    # print("Collision")
    # print(pygame.mouse.get_pressed())
