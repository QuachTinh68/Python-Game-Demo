
import pygame, random
pygame.init()
# Change header, icon, background 

# Các biếm khởi tạo trong game
p=0.2 #Down (gravity)
bird_y=0 #Tọa độ y (dọc)

score = 0 #Fist score
hight_score=0

game_play= True
game_font = pygame.font.Font(r'D:\PythonGame\FileGame\04B_19.TTF',40)
# Các hàm trong game 
# Hàm xuất điểm
def score_view():
    if game_play:
        score_f = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rec = score_f.get_rect(center=(200,100))
        screen.blit(score_f,score_rec)
    if game_play==False:
        score_f = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rec = score_f.get_rect(center=(200,25))
        screen.blit(score_f,score_rec)

        hight_f = game_font.render(f'High score: {int(hight_score)}',True,(255,255,255))
        hight_rec = hight_f.get_rect(center=(200,60))
        screen.blit(hight_f,hight_rec)
# Hàm tạo ống
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop= (500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop= (500, random_pipe_pos-650))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -=5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 768:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False, True)
            screen.blit(flip_pipe,pipe)

pygame.display.set_caption("Flappy Bird")
icon = pygame.image.load(r'D:\PythonGame\FileGame\assets\yellowbird-downflap.png')
# Create backgound 
back_ground = pygame.image.load(r'D:\PythonGame\FileGame\assets\background-night.png')
back_ground = pygame.transform.scale2x(back_ground)
# Create Floor 
floor = pygame.image.load(r'D:\PythonGame\FileGame\assets\floor.png')
floor = pygame.transform.scale2x(floor)
floor_x=0
# Create tuble
pipe_surface= pygame.image.load(r'D:\PythonGame\FileGame\assets\pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list=[]
# Craete timer 

spawpipe = pygame.USEREVENT
pygame.time.set_timer(spawpipe, 1200)
pipe_height = [200,300,350]

pygame.display.set_icon(icon)

# Game window
screen = pygame.display.set_mode((432, 768))

# Add bird
bird = pygame.image.load(r'D:\PythonGame\FileGame\assets\yellowbird-midflap.png')     
bird = pygame.transform.scale2x(bird)
bird_rec = bird.get_rect(center=(100,386))
# Game over

screen_over = pygame.image.load(r'D:\PythonGame\FileGame\assets\message.png')     
screen_over = pygame.transform.scale2x(screen_over)
screen_over_rec = screen_over.get_rect(center=(216,334))

# Hàm check va chạm
def check_va():
    if bird_rec.bottom >= 668 or bird_rec.top <= -75:
        return False
    else:
        return True

# Loop setting game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_play: 
                bird_y =-9
            if event.key == pygame.K_SPACE and game_play == False: 
                game_play= True
                bird_y=0
                bird_rec.center=(100,386)
                score=0
        if event.type == spawpipe:
            pipe_list.extend(create_pipe())

    screen.blit(back_ground, (0, 0))
    floor_x -= 1
    screen.blit(floor, (floor_x, 600))
    screen.blit(floor, (floor_x + 432, 600))

    # Nếu floor_x chạm đến -432, reset lại floor_x
    if floor_x == -432:
        floor_x = 0

    if game_play:
    # Add bird in game
        screen.blit(bird,bird_rec)
        bird_y += p
        bird_rec.centery += bird_y

        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        # Score 
        score += 0.01
        if score > hight_score: hight_score = score
        score_view()
        game_play=check_va()
    else:
        screen.blit(screen_over, screen_over_rec)
        score_view()
    pygame.display.update()
