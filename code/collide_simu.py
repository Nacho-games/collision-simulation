import math
import pygame # type: ignore
import sys
from decimal import Decimal, getcontext
getcontext().prec = 50

#inicalizamos todo
pygame.init()
pygame.font.init()
pygame.mixer.init()

# PANTALLA
screen_width = 1200
screen_length = 600
half_width = screen_width / 2
half_length = screen_length / 2
screen = pygame.display.set_mode((screen_width, screen_length))

#list for masses
small_mass_list = ['0.1', '0.2', '0.5', '1', '2', '5', '7', '10', '12', '15', '20', '25']
big_mass_list = ['10', '20', '50', '100', '150', '200', '300', '400', '500', '750', '1000', '1500', '2000', '3000']
mode = 1
mode_tick = 0
mode_tick2 = 0
list_number1 = 3
list_number2 = 3

#simulation
simulation = True
clock = pygame.time.Clock()
menu = True

#variables
change_time = 30
collisions = 0

#colores
Black = (0, 0, 0)
White = (255, 255, 255)
Blue = (100, 149, 237)
Red = (199, 42, 10)

#font
font_size = 60  
font = pygame.font.Font("./files//lato.ttf", font_size)
font_size2 = 70  
font2 = pygame.font.Font("./files//lato.ttf", font_size2)
font_size3 = 30  
font3 = pygame.font.Font("./files//lato.ttf", font_size3)
font_size4 = 25  
font4 = pygame.font.Font("./files//lato.ttf", font_size4)
font_size5 = 40  
font5 = pygame.font.Font("./files//lato.ttf", font_size5)
font_size6 = 32 
font6 = pygame.font.Font("./files//lato.ttf", font_size6)

#sound
clack = pygame.mixer.Sound('./files/click.mp3')

#start button
start_i = pygame.image.load("./files/start.png")
start_adjus = pygame.transform.scale(start_i,(300, 160))
start_button = pygame.Rect(half_width - 150, 352.5, 300, 160)

#sprite
sprite_i = pygame.image.load("./files/sprite.png")
sprite_adjus = pygame.transform.scale(sprite_i,(12, 12))
sprite_animation = False
sprite_value = 0

#rect parameters
small_rect_x = Decimal('300')
small_rect_y = Decimal('500')
small_rect_size = Decimal('50')
big_rect_x = Decimal('800')
big_rect_y = Decimal('450')
big_rect_size = Decimal('100')

small_mass = Decimal('1')
big_mass = Decimal('100')

binit = '-1'
sinit = '0'
big_rect_vel = Decimal(binit)
small_rect_vel = Decimal(sinit)

while menu:

    #exit 
    key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                menu = False
                clack.play()

        #choice logic
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN or event.key == pygame.K_KP_MINUS:
                if mode and list_number1 > 0:
                    list_number1 -= 1
                elif not mode and list_number2 > 0:
                    list_number2 -= 1
            if event.key == pygame.K_UP or event.key == pygame.K_KP_PLUS:
                if mode and list_number1 < 11:
                    list_number1 += 1
                elif not mode and list_number2 < 13:
                    list_number2 += 1

            if event.key == pygame.K_RIGHT and mode:
                mode = not mode
            if event.key == pygame.K_LEFT and not mode:
                mode = not mode
                
    if key[pygame.K_ESCAPE]:
        pygame.quit()
    if key[pygame.K_SPACE] or key[pygame.K_RETURN]:
        menu = False
        clack.play()

    #limpiamos
    screen.fill(Black)

    #rectangles selector
    if mode:
        mode_rect = pygame.Rect(60, 370, 325, 70)
        mode_rect_inside = pygame.Rect(65, 375, 315, 60)
    if not mode:
        mode_rect = pygame.Rect(800, 370, 350, 70)
        mode_rect_inside = pygame.Rect(805, 375, 340, 60)

    if mode_tick >= 30:

        pygame.draw.rect(screen, White, mode_rect)

        if mode_tick2 <= 30:
            mode_tick2 += 1
        else:
            mode_tick2 = 0
            mode_tick = 0

    mode_tick += 1

    pygame.draw.rect(screen, Black, mode_rect_inside)
        
    
    #mass choice
    small_mass = Decimal(small_mass_list[list_number1])
    big_mass = Decimal(big_mass_list[list_number2])

    #for drawing convert to float
    draw_small_mass = float(small_mass) 
    draw_big_mass   = float(big_mass)

    #text
    title_txt = font2.render(str(f"1D collisions simulation"), True, White)
    title_txt_rect = title_txt.get_rect(center=(half_width, 50 ))
    subtitle_txt = font4.render(str(f"In this simulation I used the 1D Elastic Collision Equation."), True, White)
    subtitle_txt_rect = subtitle_txt.get_rect(center=(half_width, 130 ))
    subtitle2_txt = font4.render(str(f"The calculations are not accurate with high numbers because of the simulation being real-time."), True, White)
    subtitle2_txt_rect = subtitle2_txt.get_rect(center=(half_width, 170 ))
    subtitle3_txt = font4.render(str(f" If the ratio of the masses are 100 to 1, the number of collisions will be exactly pi."), True, White)
    subtitle3_txt_rect = subtitle3_txt.get_rect(center=(half_width, 210 ))
    subtitle4_txt = font4.render(str(f" Because of the lack of accuracy, this only works when the ratio is 100 to 1."), True, White)
    subtitle4_txt_rect = subtitle3_txt.get_rect(center=(half_width, 250 ))
    footer_txt = font6.render(str(f"(Use the arrows keys to change the masses)"), True, White)
    footer_txt_rect = footer_txt.get_rect(center=(half_width, 550 ))

    #mass selectors
    select_small_txt = font5.render(str(f"Small mass: {float(small_mass)}kg"), True, Blue)
    select_small_txt_rect = select_small_txt.get_rect(center=(225, start_button.centery - 30 ))
    select_big_txt = font5.render(str(f"Big mass: {float(big_mass)}kg"), True, Red)
    select_big_txt_rect = select_big_txt.get_rect(center=(975, start_button.centery - 30))


    #pintamos
    screen.blit(title_txt, title_txt_rect)
    screen.blit(subtitle_txt, subtitle_txt_rect)
    screen.blit(subtitle2_txt, subtitle2_txt_rect)
    screen.blit(subtitle3_txt, subtitle3_txt_rect)
    screen.blit(subtitle4_txt, subtitle4_txt_rect)
    screen.blit(select_small_txt, select_small_txt_rect)
    screen.blit(select_big_txt, select_big_txt_rect)
    screen.blit(start_adjus, start_button )
    screen.blit(footer_txt, footer_txt_rect)


    pygame.display.update()


#simulation
while simulation:

    #for drawing convert to float
    draw_x_small = float(small_rect_x) 
    draw_x_big   = float(big_rect_x) 
    draw_y_small = float(small_rect_y) 
    draw_y_big   = float(big_rect_y) 
    draw_size_small = float(small_rect_size) 
    draw_size_big   = float(big_rect_size)
    draw_small_mass = float(small_mass) 
    draw_big_mass   = float(big_mass)

    #exit 
    key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if key[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    #rects
    small_rect = pygame.Rect(draw_x_small, draw_y_small, draw_size_small, draw_size_small)
    big_rect = pygame.Rect(draw_x_big, draw_y_big, draw_size_big, draw_size_big)
    
    #fps
    clock.tick()

    if change_time > 29:
        fps = clock.get_fps()
        fps = round(fps)
        change_time = 0
    change_time += 1    

    fps_txt = font.render(str(f"{fps}"), True, White)
    fps_txt_rect = fps_txt.get_rect(center=(60, 50))

    #mass text
    small_mass_txt = font3.render(str(f"mass = {round(draw_small_mass, 1)}kg"), True, White)
    small_mass_txt_rect = small_mass_txt.get_rect(center=(draw_x_small + draw_size_small / 2, draw_y_small -25))
    big_mass_txt = font3.render(str(f"mass = {round(draw_big_mass, 1)}kg"), True, White)
    big_mass_txt_rect = big_mass_txt.get_rect(center=(draw_x_big + draw_size_big / 2,draw_y_big -25))

    #colisions counter
    collisions_txt = font2.render(str(f"Collisions: {collisions}"), True, White)
    collisions_txt_rect = collisions_txt.get_rect(center=(900, 50))

    #limpiamos
    screen.fill(Black)

    #moving the rects
    big_rect_x += big_rect_vel
    small_rect_x += small_rect_vel

    #bounce in wall
    if big_rect_x <= 50:
        big_rect_x = 50
        big_rect_vel = -big_rect_vel
        clack.play()
        collisions += 1
        sprite_rect = pygame.Rect(draw_x_big - 6, (draw_y_big + (draw_size_big / 2) - 6), 12, 12)
        sprite_animation = True
        print("overlapping")


    if small_rect_x <= 50:
        small_rect_x = 50
        small_rect_vel = -small_rect_vel
        clack.play()
        collisions += 1
        sprite_rect = pygame.Rect(draw_x_small -6, (draw_y_small + (draw_size_small / 2) -6), 12, 12)
        sprite_animation = True

    #RECT COLLIDING
    if float(big_rect_x) <= float(small_rect_x + Decimal(small_rect_size)):

        #The 1D Elastic Collision Equations
        v_big_old = big_rect_vel
        v_small_old = small_rect_vel
        big_rect_vel = (big_rect_vel * (big_mass - small_mass) + 2 * small_mass * v_small_old) / (big_mass + small_mass)
        small_rect_vel = (small_rect_vel * (small_mass - big_mass) + 2 * big_mass * v_big_old) / (big_mass + small_mass)
        
        collisions += 1

        sprite_rect = pygame.Rect(draw_x_big - 6, (draw_y_small + (draw_size_small / 2) -6), 12, 12)
        sprite_animation = True

        clack.play()

    #position logic for rects
    big_rect_y = 550 - big_rect_size
    small_rect_y = 550 - small_rect_size

    #size logic for rects
    if big_mass <= 200:
        big_rect_size = math.sqrt(big_mass) * 20
    elif big_mass <= 400:
        big_rect_size = math.sqrt(200) * 20 + math.sqrt(big_mass - 200) * 4
    else:
        big_rect_size = math.sqrt(400) * 20 

    if small_mass >= 10:
        small_rect_size = math.sqrt(small_mass) * 20
    else:
        small_rect_size = math.sqrt(10) * 20 - math.sqrt(10 - small_mass) * 10
    

    #pintamos 
    screen.blit(fps_txt, fps_txt_rect)
    screen.blit(collisions_txt, collisions_txt_rect)
    screen.blit(small_mass_txt, small_mass_txt_rect)
    screen.blit(big_mass_txt, big_mass_txt_rect)
    pygame.draw.rect(screen, Blue, small_rect )
    pygame.draw.rect(screen, Red, big_rect)


    #lineas
    pygame.draw.line(screen, White, (50, 110), (50, 550))
    pygame.draw.line(screen, White, (50, 550), (1200, 550))

    #sprite animation
    if sprite_animation:
        sprite_value += 1
        screen.blit(sprite_adjus, sprite_rect)
        if sprite_value >= 10:
            sprite_value = 0
            sprite_animation = 0

    if big_rect_x > 1200:
        big_rect_x = 1200
        pygame.quit()
        sys.exit()

    #actualizamos
    pygame.display.update()



