import gymnasium as gym
from stable_baselines3 import A2C, PPO
import os
import v0_flappy_bird_env


MODEL_DIR = 'new_model/PPO'
LOGS_DIR = 'new_logs'

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

env = gym.make('flappy-bird-v0')
env.reset()

model = PPO('MlpPolicy', env=env, tensorboard_log=LOGS_DIR, verbose=1)

TIMESTEPS = 100000
i = 0

while True:
    model.learn(total_timesteps=TIMESTEPS, tb_log_name='PPO', reset_num_timesteps=False)
    i += 1
    model.save(f'{MODEL_DIR}/{i*TIMESTEPS}')