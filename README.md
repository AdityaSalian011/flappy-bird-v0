

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
The action is a ndarray with shape (1,) which can take values {0, 1} indicating if the agent should be at rest or should jump.

### Observation Space
| **Num** | **Observation**                    | **Min**    | **Max**   |
|--------:|------------------------------------|------------|-----------|
| 0       | Player's vertical position         | -64        | 536       |
| 1       | Player's vertical speed            | -10        | 20        |
| 2       | Horizontal distance to next pipe   | -400* 2    | 400* 2    |
| 3       | Top pipe edge position             | -600       | 600       |
| 4       | Bottom pipe edge position          | 0          | 600       |     
