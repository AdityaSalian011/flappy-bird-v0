import pygame
import random
import gymnasium as gym
from gymnasium import spaces
from gymnasium.envs.registration import register
from gymnasium.utils.env_checker import check_env
import v0_flappy_bird as fb
import numpy as np
import sys

register(
    id = 'flappy-bird-v0',
    entry_point = 'v0_flappy_bird_env:FlappyBirdEnv'
)


game_state = 1

window_w = 400
window_h = 600

fps = 60

# Load Sounds
# slap_sfx = pygame.mixer.Sound('sounds/slap.wav')
# woosh_sfx = pygame.mixer.Sound('sounds/woosh.wav')
# score_sfx = pygame.mixer.Sound('sounds/score.wav')

# # Load Images
# player_img = pygame.image.load('images/player.png')
# pipe_up_img = pygame.image.load('images/pipe_up.png')
# pipe_down_img = pygame.image.load('images/pipe_down.png')
# ground_img = pygame.image.load('images/ground.png')

# bg_img = pygame.image.load('images/background.png')
# bg_width = bg_img.get_width()

PIPE_WIDTH = 79
PLAYER_WIDTH = 64
PLAYER_HEIGHT = 62
PIPE_HEIGHT = 360

bg_scroll_spd = 1
ground_scroll_spd = 2

MIN_VELOCITY = -10  # our player can make a jump of -10 px y-axis
MAX_VELOCITY = 20  # our player can go at most 
MIN_PLAYER_Y = -64 # above this the player hits the top and terminates
MAX_PLAYER_Y = 536 # below this is groung img and hence can't go below this


def scoreboard(font, score, screen):
    show_score = font.render(str(score), True, (10, 40, 9))
    score_rect = show_score.get_rect(center=(window_w//2, 64))
    screen.blit(show_score, score_rect)

class FlappyBirdEnv(gym.Env):

    metadata = {'render_modes': ['human'], 'render_fps': 60}

    def __init__(self, render_mode=None):
        self.render_mode = render_mode
        self.screen = None
        self.clock = None
        self.score = 0
        self.has_moved = False
        self.bg_x_pos = 0
        self.ground_x_pos = 0
        self.np_random = None

        if self.render_mode == 'human':
            pygame.init()
            self.screen = pygame.display.set_mode((window_w, window_h))
            self.clock = pygame.time.Clock()
            # Load Sounds5
            self.slap_sfx = pygame.mixer.Sound('sounds/slap.wav')
            self.woosh_sfx = pygame.mixer.Sound('sounds/woosh.wav')
            self.score_sfx = pygame.mixer.Sound('sounds/score.wav')

            # Load Images
            self.player_img = pygame.image.load('images/player.png')
            self.pipe_up_img = pygame.image.load('images/pipe_up.png')
            self.pipe_down_img = pygame.image.load('images/pipe_down.png')
            self.ground_img = pygame.image.load('images/ground.png')

            self.bg_img = pygame.image.load('images/background.png')
            self.bg_width = self.bg_img.get_width()

            # Load font
            self.font = pygame.font.Font('fonts/BaiJamjuree-Bold.ttf', 60)

        # initializing our player
        self.player = fb.Player(168, 300)

        # initializing pipes
        self.pipes = [fb.Pipe(600, random.randint(30, 280), 220, 2.4)]

        # pipe_height = self.pipe_down_img.get_height() if self.render_mode == 'human' else PIPE_HEIGHT

        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(
            low = np.array([MIN_PLAYER_Y, MIN_VELOCITY, -window_w* 2, -window_h, 0], dtype=np.float32),
            high = np.array([MAX_PLAYER_Y, MAX_VELOCITY, window_w* 2, window_h, window_h], dtype=np.float32),
            shape = (5,),
            dtype = np.float32,
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.np_random = np.random.default_rng(seed)

        self.player = fb.Player(168, 300)

        pipe_height_value = self.np_random.integers(30, 280)
        self.pipes = [fb.Pipe(600, pipe_height_value, 220, 2.4)]

        pipe_height = self.pipe_down_img.get_height() if self.render_mode == 'human' else PIPE_HEIGHT

        obs_list = [float(self.player.y), 
                    float(self.player.velocity), 
                    float(self.pipes[0].x - self.player.x), 
                    float(0 - pipe_height + self.pipes[0].height), 
                    float(self.pipes[0].height + self.pipes[0].gap)]
        obs = np.array(obs_list, dtype=np.float32)

        info = {}
        
        if self.render_mode == 'human':
            self.render()       

        return obs, info
    
    def step(self, action):
        reward = 0.2  # giving record every frame player stays alive

        terminated = False

        # defining player height, width
        player_width = self.player_img.get_width() if self.render_mode == 'human' else PLAYER_WIDTH
        player_height = self.player_img.get_height() if self.render_mode == 'human' else PLAYER_HEIGHT

        # defining pipe height/ width
        pipe_width = self.pipe_down_img.get_width() if self.render_mode == 'human' else PIPE_WIDTH
        pipe_height = self.pipe_down_img.get_height() if self.render_mode == 'human' else PIPE_HEIGHT

        if self.render_mode == 'human':
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit() 
                    sys.exit()               
        
        if action == 1:
            self.player.jump()
            self.has_moved = True
            if self.render_mode == 'human':
                pygame.mixer.Sound.play(self.woosh_sfx)
        elif action == 0:
            self.has_moved = True
        
        if not terminated and self.has_moved:
            self.player.update()
            player_rect = pygame.Rect(self.player.x, self.player.y, player_width, player_height)

            # updating pipe
            for pipe in self.pipes:
                pipe.update()

            # player death condition starts here
            for pipe in self.pipes:
                pipe_top = pipe.height
                pipe_gap = pipe.gap
                pipe_bottom = pipe_top + pipe_gap

                pipe_top_rect = pygame.Rect(pipe.x, 0, pipe_width, pipe_top)
                pipe_bottom_rect = pygame.Rect(pipe.x, pipe_bottom, pipe_width, window_h - pipe_bottom)

                if player_rect.colliderect(pipe_top_rect) or player_rect.colliderect(pipe_bottom_rect):
                    # self.reset()
                    if self.render_mode == 'human':
                        pygame.mixer.Sound.play(self.slap_sfx)
                    self.has_moved = False
                    self.score = 0
                    terminated = True
                    reward = -10
            
            if self.player.y < MIN_PLAYER_Y or self.player.y > MAX_PLAYER_Y:
                # self.reset()
                if self.render_mode == 'human':
                    pygame.mixer.Sound.play(self.slap_sfx)
                self.has_moved = False
                self.score = 0
                terminated = True
                reward = -5
            # player death condition ends here

            # removing and adding pipes after a certain threshold
            if self.pipes[0].x <= -pipe_width:
                self.pipes.pop(0)
                self.pipes.append(fb.Pipe(400, random.randint(30, 280), 220, 2.4))

            # adding score after passing through pipe
            for pipe in self.pipes:
                if not pipe.scored and pipe.x + pipe_width < self.player.x:
                    self.score += 1
                    if self.render_mode == 'human':
                        pygame.mixer.Sound.play(self.score_sfx)
                    reward += 1 # +1 everytime player passes through pipe gap

                    pipe.scored = True

        if self.render_mode == 'human':
            # running an infinite loop of our background
            self.bg_x_pos -= bg_scroll_spd
            self.ground_x_pos -= ground_scroll_spd

            if self.bg_x_pos <= -self.bg_width:
                self.bg_x_pos = 0

            if self.ground_x_pos <= -self.bg_width:
                self.ground_x_pos = 0
            self.render()

        # obs_list = [self.player.y, self.player.velocity, 
        #             self.pipes[0].x - self.player.x, 
        #             0 - pipe_height + self.pipes[0].height, 
        #             self.pipes[0].height + self.pipes[0].gap]
        # obs = np.array(obs_list, dtype=np.float32)
        obs_list = [float(self.player.y), 
                    float(self.player.velocity), 
                    float(self.pipes[0].x - self.player.x), 
                    float(0 - pipe_height + self.pipes[0].height), 
                    float(self.pipes[0].height + self.pipes[0].gap)]
        obs = np.array(obs_list, dtype=np.float32)

        # reward code starts here

        if action == 1:
            reward -= 0.1  # jump penalty

        gap_center_y = self.pipes[0].height + (self.pipes[0].gap / 2)
        distance_to_center = abs(self.player.y - gap_center_y)

        # reward += 0.5 - (distance_to_center/ (self.pipes[0].gap / 2))  # giving reward if player is close to pipe gaps
        if distance_to_center < self.pipes[0].gap * 0.25:
            reward += 0.4
        elif distance_to_center < self.pipes[0].gap * 0.5:
            reward += 0.2

        # if terminated:
        #     reward = -5  # -10 reward if agent terminates
        
        info = {}

        return obs, reward, terminated, False, info

    def render(self):
        if self.render_mode != 'human':
            return
        self.screen.fill('blue')
        self.screen.blit(self.bg_img, (self.bg_x_pos, 0))
        self.screen.blit(self.bg_img, (self.bg_x_pos + self.bg_width, 0))       

        # Draw pipes
        for pipe in self.pipes:
            pipe.draw()
         
        self.player.draw()

        self.screen.blit(self.ground_img, (self.ground_x_pos, MAX_PLAYER_Y))
        self.screen.blit(self.ground_img, (self.ground_x_pos + self.bg_width, MAX_PLAYER_Y))  
        # infinite background code ends here

        scoreboard(self.font, self.score, self.screen)

        pygame.display.flip()
        self.clock.tick(fps)  



if __name__ == '__main__':
    env = gym.make('flappy-bird-v0', render_mode='human')

    for ep in range(10):
        obs, _  = env.reset()
        terminated = False
        reward_per_ep = 0
        while not terminated:
            action = env.action_space.sample()
            obs, reward, terminated, _, _ = env.step(action)
            # print(reward)
            reward_per_ep += reward
        print(reward_per_ep)
    