import pygame, sys, random
# Functions in game 
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos+432,650))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos-680))

    return bottom_pipe,top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rec.colliderect(pipe):
            hit_sound.play()
            return False
        if bird_rec.top <= -75 or bird_rec.bottom >= 650:
            return False
    return True
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_move*3,1)
    return new_bird
def  bird_animation():
    new_bird = bird_list[ bird_index]
    new_bird_rec = new_bird.get_rect(center = (100, bird_rec.centery))
    return new_bird, new_bird_rec
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(f'Score; {int(score)}', True,(255,255,255))
        score_rec = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rec)

    if game_state == 'game_over':
        hight_score_surface = game_font.render(f'Hight score; {int(hight_score)}', True,(255,255,255))
        hight_score_rec = hight_score_surface.get_rect(center = (216,280))
        screen.blit(hight_score_surface,hight_score_rec)
def update_score(score,hight_score):
    if score > hight_score:
        hight_score= score
    return hight_score

pygame.mixer.pre_init(frequency=44100,size=-16,channels=2,buffer=512)
pygame.init()

pygame.display.set_caption("Flappy Bird")
icon = pygame.image.load('FileGame/assets/bird-midflap.png')
  
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('FileGame/04B_19.TTF',40)
# Create variable 
gravity = 0.2
bird_move = 0
game_active = True
score = 0
hight_score = 0
# Background
bg = pygame.image.load('FileGame/assets/background-night.png')
bg = pygame.transform.scale2x(bg)
# Insert floor 
floor = pygame.image.load('FileGame/assets/floor.png')
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
# Create bird
bird_mid = pygame.image.load('FileGame/assets/bird-midflap.png')
bird_mid = pygame.transform.scale2x(bird_mid)

bird_down = pygame.image.load('FileGame/assets/bird-down.png')
bird_down = pygame.transform.scale2x(bird_down)

bird_up = pygame.image.load('FileGame/assets/bird-up.png')
bird_up = pygame.transform.scale2x(bird_up)

bird_list= [bird_down,bird_mid,bird_up]
bird_index = 2
bird = bird_list[bird_index]
bird_rec = bird.get_rect(center =(100, 384))

# Create timer 
birdFlap= pygame.USEREVENT + 1
pygame.time.set_timer(birdFlap,200)
# Create pipe 
pipe_surface = pygame.image.load('FileGame/assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
# Create timer 
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1200)
pipe_height = [200,300,400]
# Create game over screen 
 
game_over_surface  = pygame.image.load('FileGame/assets/message.png')
game_over_surface  = pygame.transform.scale2x(game_over_surface )
game_over_rec = game_over_surface.get_rect(center= (216, 384))
# Insert sound 
flap_sound = pygame.mixer.Sound('FileGame/sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('FileGame/sound/sfx_hit.wav')
down_sound = pygame.mixer.Sound('FileGame/sound/sfx_swooshing.wav')
score_sound = pygame.mixer.Sound('FileGame/sound/sfx_point.wav')
score_sound_countdown = 100

pygame.display.set_icon(icon)
# Running Game
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_move = 0
                down_sound.play()
                bird_move -=10
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active==False:
                game_active=True
                pipe_list.clear()
                bird_rec.center = (100,384)
                bird_move = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())      
        if event.type == birdFlap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rec = bird_animation()
           
    screen.blit(bg,(0,0))
    if game_active:
        # Bird 
        bird_move += gravity
        rotated_bird = rotate_bird(bird)
        screen.blit(rotated_bird,bird_rec)
        game_active=check_collision(pipe_list)
        bird_rec.centery += bird_move
        # Pipe 
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100

    else:
        screen.blit(game_over_surface, game_over_rec)
        hight_score = update_score(score,hight_score)
        score_display('game_over')
    # Floor 
    floor_x_pos -=1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)

