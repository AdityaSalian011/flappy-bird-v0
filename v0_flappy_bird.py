import pygame, sys, random


pygame.init()

game_state = 1
score = 0
has_moved = False

window_w = 400
window_h = 600

screen = pygame.display.set_mode((window_w, window_h))
clock = pygame.time.Clock()
fps = 60

# Load Fonts
font = pygame.font.Font('fonts/BaiJamjuree-Bold.ttf', 60)

# Load Sounds
slap_sfx = pygame.mixer.Sound('sounds/slap.wav')
woosh_sfx = pygame.mixer.Sound('sounds/woosh.wav')
score_sfx = pygame.mixer.Sound('sounds/score.wav')

# Load Images
player_img = pygame.image.load('images/player.png')
pipe_up_img = pygame.image.load('images/pipe_up.png')
pipe_down_img = pygame.image.load('images/pipe_down.png')
ground_img = pygame.image.load('images/ground.png')

bg_img = pygame.image.load('images/background.png')
bg_width = bg_img.get_width()

bg_scroll_spd = 1
ground_scroll_spd = 2

# print(bg_width)
print(pipe_down_img.get_height())
print(pipe_up_img.get_height())

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0

    def jump(self):
        self.velocity = -10

    def update(self):
        self.velocity += 0.75
        self.y += self.velocity

    def draw(self):
        screen.blit(player_img, (self.x, self.y))


class Pipe:
    def __init__(self, x, height, gap, velocity):
        self.x = x
        self.height = height
        self.gap = gap
        self.velocity = velocity
        self.scored = False

    def update(self):
        self.x -= self.velocity

    def draw(self):
        # Draw top pipe
        screen.blit(pipe_down_img, (self.x, 0 - pipe_down_img.get_height() + self.height))

        # Draw bottom pipe
        screen.blit(pipe_up_img, (self.x, self.height + self.gap))


def scoreboard():
    show_score = font.render(str(score), True, (10, 40, 9))
    score_rect = show_score.get_rect(center=(window_w//2, 64))
    screen.blit(show_score, score_rect)


def game(action):
    global game_state
    global score
    global has_moved

    bg_x_pos = 0
    ground_x_pos = 0

    player = Player(168, 300)
    pipes = [Pipe(600, random.randint(30, 250), 220, 2.4)]


    while game_state != 0:
        while game_state == 1:
            terminated = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # elif event.type == pygame.KEYDOWN:
            if action == 1:
                player.jump()   
                has_moved = True
                    # if event.key == pygame.K_SPACE:
                pygame.mixer.Sound.play(woosh_sfx)
            elif action == 0:
                has_moved = True
            
            if not terminated and has_moved:
                player.update()

                player_rect = pygame.Rect(player.x, player.y, player_img.get_width(), player_img.get_height())
                
                for pipe in pipes:
                    pipe_width = pipe_up_img.get_width()
                    pipe_top_height = pipe.height
                    pipe_gap = pipe.gap
                    pipe_bottom_y = pipe_top_height + pipe_gap

                    pipe_top_rect = pygame.Rect(pipe.x, 0, pipe_width, pipe_top_height)
                    
                    pipe_bottom_rect = pygame.Rect(pipe.x, pipe_bottom_y, pipe_width, window_h - pipe_bottom_y)

                    if player_rect.colliderect(pipe_top_rect) or player_rect.colliderect(pipe_bottom_rect):
                        player = Player(168, 300)
                        pipes = [Pipe(600, random.randint(30, 250), 220, 2.4)]
                        score = 0
                        has_moved = False
                        terminated = True
                        pygame.mixer.Sound.play(slap_sfx)

                if player.y < -64 or player.y > 536:
                    player = Player(168, 300)
                    pipes = [Pipe(600, random.randint(30, 250), 220, 2.4)]
                    score = 0
                    has_moved = False
                    terminated = True
                    pygame.mixer.Sound.play(slap_sfx)
                
                for pipe in pipes:
                    pipe.update()

                if pipes[0].x < -pipe_up_img.get_width():
                    pipes.pop(0)
                    pipes.append(Pipe(400, random.randint(30, 280), 220, 2.4))
                
                for pipe in pipes:
                    if not pipe.scored and pipe.x + pipe_up_img.get_width() < player.x:
                        score += 1
                        pygame.mixer.Sound.play(score_sfx)
                        pipe.scored = True
                
            bg_x_pos -= bg_scroll_spd
            ground_x_pos -= ground_scroll_spd

            if bg_x_pos <= -bg_width:
                bg_x_pos = 0

            if ground_x_pos <= -bg_width:
                ground_x_pos = 0

            screen.fill('blue')
            screen.blit(bg_img, (bg_x_pos, 0))
            screen.blit(bg_img, (bg_x_pos + bg_width, 0))
            screen.blit(ground_img, (ground_x_pos, 536))
            screen.blit(ground_img, (ground_x_pos + bg_width, 536))

            for pipe in pipes:
                pipe.draw()

            player.draw()
            scoreboard()

            pygame.display.flip()     
            clock.tick(fps)    


if __name__ == '__main__':
    game(1)