

https://github.com/user-attachments/assets/e4e5528f-9a3a-4e29-9ebc-1c03f76a1024

## An Automatic Flappy Bird playing Agent created using Reinforcement Learning
#### Here, I have developed a custom GYM Environment which is trained using A2C Model and MlpPolicy

### FlappyBirdEnv

| **Space**              | **Details**                                                                                                                                         |
|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| Action Space           | `Discrete(2)`                                                                                                                                       |
| Observation Space      | `Box([-64, -10, -400* 2, -600, 0], [536, 20, 400* 2, 600, 600], (5,), float32)`                                                                     |

### Description
In this custom environment, the goal is to help the agent pass through the gap between the upper and lower pipes. Each successful pass increases the score by 1. If the agent hits a pipe, touches the ground, or flies too high, the game restarts.

### Action Space
The action is a ndarray with shape (1,) which can take values {0, 1}.
- 0: Agent Stays at Rest
- 1: Agent Jumps

### Observation Space
| **Num** | **Observation**                    | **Min**    | **Max**   |
|--------:|------------------------------------|------------|-----------|
| 0       | Player's vertical position         | -64        | 536       |
| 1       | Player's vertical speed            | -10        | 20        |
| 2       | Horizontal distance to next pipe   | -400* 2    | 400* 2    |
| 3       | Top pipe edge position             | -600       | 600       |
| 4       | Bottom pipe edge position          | 0          | 600       |     

### Rewards
Since the goal is to score as much as possible, every frame our agent stays alive it gets a reward of +0.2. If our agent collides with one of the pipes, a reward of -10 is applied. If it touches the ground, or flies too high, -5 reward. Although if our agent passes through the gap between upper and lower pipes reward is incremented by 1 i.e. +1. Every jump results in -0.1 reward to avoid unnecessary flaps. If agent's vertical axis is 75% close to vertical axis of pipes gap +0.4 reward and if 50% close +0.2 reward. 
