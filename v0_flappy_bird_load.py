import gymnasium as gym
from stable_baselines3 import PPO, A2C
import v0_flappy_bird_env


MODEL_DIR = 'new_model/PPO'
MODEL_PATH = f'{MODEL_DIR}/600000.zip'

env = gym.make('flappy-bird-v0', render_mode='human')

model = PPO.load(MODEL_PATH, env=env)

episodes = 10

for ep in range(episodes):
    obs, _ = env.reset()
    terminated = False
    reward_per_ep = 0
    while not terminated:
        action, _ = model.predict(obs)
        obs, reward, terminated, _, _ = env.step(action)
        reward_per_ep += reward

    print(reward_per_ep)