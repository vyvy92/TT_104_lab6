import pgzrun
from random import *
import time

WIDTH = 900
HEIGHT = 540
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

game_over = False
finalized = False
raining = False
garden_happy = True
fangflower_collision = False

time_elapsed = 0
start_time = time.time()

cow = Actor("pig")
cow.pos = (100, 400)

flower_list = []
wilted_list = []
fangflower_list = []
owl_list= []

fangflower_vy_list = []
fangflower_vx_list = []
owl_vy_list = []
owl_vx_list = []


def draw():
    global game_over, time_elapsed, finalized,raining
    if (not game_over):
        if (not raining):
            screen.blit("gd", (0, 0))
        else:
            screen.blit("gd-raining", (0, 0))
        cow.draw()
        for flower in flower_list:
            flower.draw()
        for fangflower in fangflower_list:
            fangflower.draw()
            raining=True
        for owl in owl_list:
            owl.draw()
        time_elapsed = int (time.time() - start_time)
        screen.draw.text("Garden happy for: " + str(time_elapsed) +" seconds",
                         topleft=(10,10), color="black")
    else:
        if (not finalized):
            cow.draw()
            screen.draw.text("Garden happy for: " + str(time_elapsed) +" seconds",
                         topleft=(10,10), color="black")
        if (not garden_happy):
            screen.draw.text("GARDEN UNHAPPY! GAME OVER!", color="black", topleft=(10,50))
            finalized = True
        else:
            screen.draw.text("ENEMIES ATTACK! GAME OVER!", color="black", topleft=(10,50))
            finalized = True
        return

    
def new_flower():
    global flower_list, wilted_list
    flower_new = Actor("flower")
    flower_new.pos = randint(50, WIDTH - 50), randint(150, HEIGHT - 100)
    flower_list.append(flower_new)
    wilted_list.append("happy")
    return

def add_flowers():
    global game_over
    if (not game_over):
        new_flower()
        clock.schedule(add_flowers, 2)
    return

def check_wilt_times():
    global wilted_list, game_over, garden_happy
    if(len(wilted_list)>0):
       for wilted_since in wilted_list:
           if (not wilted_since == "happy"):
               time_wilted = int(time.time() - wilted_since)
               if (time_wilted > 15.0):
                   garden_happy = False
                   game_over = True
                   break
    return

def wilt_flower():
    global flower_list, wilted_list, game_over,raining
    if (not game_over):
        if(len(wilted_list)>0):
            rand_flower = randint(0, len(flower_list)-1)
            if (flower_list[rand_flower].image == "flower"):
                flower_list[rand_flower].image = "flower-wilt"
                wilted_list[rand_flower] = time.time()
            if (not raining):
                clock.schedule(wilt_flower, 3)
            else:
                clock.schedule(wilt_flower, 99)
    return




def check_flower_collision():
    global cow, flower_list, wilted_list,game_over
    index = 0
    for flower in flower_list:
        if (flower.colliderect(cow) and flower.image == "flower-wilt"):
            flower.image = "flower"
            wilted_list[index] = "happy"
            raining = True
            break
        index += 1
    return

def check_fangflower_collision():
    global cow, fangflower_list, fangflower_collision, game_over
    for fangflower in fangflower_list:
        if (fangflower.colliderect(cow)):
            cow.image = "zap"
            game_over = True
            break
    return

def check_owl_collision():
    global cow, owl_list, owl_collision, game_over
    for owl in owl_list:
        if (owl.colliderect(cow)):
            cow.image = "oh"
            game_over = True
            break
    return

def velocity():
    random_dir = randint(0,1)
    random_velocity = randint(4,6)
    if (random_dir == 0):
        return -random_velocity
    else:
        return random_velocity

def mutate():
    global flower_list, fangflower_list, fangflower_vx_list, fangflower_vy_list, game_over
    if (not game_over and flower_list):
        rand_flower = randint(0, len(flower_list) - 1)
        fangflower_pos_x = flower_list[rand_flower].x
        fangflower_pos_y = flower_list[rand_flower].y
        del flower_list[rand_flower]
        fangflower = Actor("fangflower")
        fangflower.pos = fangflower_pos_x, fangflower_pos_y
        fangflower_vx = velocity()
        fangflower_vy = velocity()
        fangflower_list.append(fangflower)
        fangflower_vx_list.append(fangflower_vx)
        fangflower_vy_list.append(fangflower_vy)
        clock.schedule(mutate, 15)


    return

def mutate_owl():
    global flower_list, owl_list, owl_vx_list, owl_vy_list, game_over
    if (not game_over and flower_list):
        rand_flower = randint(0, len(flower_list) - 1)
        owl_pos_x = flower_list[rand_flower].x
        owl_pos_y = flower_list[rand_flower].y
        del flower_list[rand_flower]
        owl = Actor("owl")
        owl.pos = owl_pos_x, owl_pos_y
        owl_vx = velocity()
        owl_vy = velocity()
        owl_list.append(owl)
        owl_vx_list.append(owl_vx)
        owl_vy_list.append(owl_vy)
        clock.schedule(mutate_owl, 10)

    return

def update_fangflowers():
    global fangflower_list, game_over,raining
    if (not game_over):
        index = 0
        for fangflower in fangflower_list:
            fangflower_vx = fangflower_vx_list[index]
            fangflower_vy = fangflower_vy_list[index]
            fangflower.x += fangflower_vx
            fangflower.y += fangflower_vy
            if fangflower.left < 0:
                fangflower_vx_list[index] = -fangflower_vx
            if fangflower.right > WIDTH:
                fangflower_vx_list[index] = -fangflower_vx
            if fangflower.top < 150:
                fangflower_vy_list[index] = -fangflower_vy
            if fangflower.bottom > HEIGHT:
                fangflower_vy_list[index] = -fangflower_vy
            index += 1
    return

def update_owls():
    global owl_list, game_over,raining
    if (not game_over):
        index = 0
        for owl in owl_list:
            owl_vx = owl_vx_list[index]
            owl_vy = owl_vy_list[index]
            owl.x += owl_vx
            owl.y += owl_vy
            if owl.left < 0:
                owl_vx_list[index] = -owl_vx
            if owl.right > WIDTH:
                owl_vx_list[index] = -owl_vx
            if owl.top < 150:
                owl_vy_list[index] = -owl_vy
            if owl.bottom > HEIGHT:
                owl_vy_list[index] = -owl_vy
            index += 1
    return

def reset_cow():
    global game_over
    if (not game_over):
        cow.image = "pig"
    return

add_flowers()
wilt_flower()


def update():
    global score, game_over, fangflower_collision, flower_list, fangflower_list, time_elapsed
    global owl_collision, owl_list
    fangflower_collision = check_fangflower_collision()
    owl_collision = check_owl_collision()
    check_wilt_times()
    if (not game_over):
        if (keyboard.space):
            cow.image = "pig-water"
            clock.schedule(reset_cow, 0.5)
            check_flower_collision()
        if (keyboard.left and cow.x > 0):
            cow.x -= 5
        if (keyboard.right and cow.x < WIDTH):
            cow.x += 5
        if (keyboard.up and cow.y > 150):
            cow.y -= 5
        if (keyboard.down and cow.y < HEIGHT):
            cow.y += 5
        if (keyboard.r):
            raining=True
        if (time_elapsed > 15 and not fangflower_list):
            mutate()
        if (time_elapsed > 10 and not owl_list):
            mutate_owl()
            
        update_fangflowers()
        update_owls()

add_flowers()
wilt_flower()
pgzrun.go()