

https://github.com/user-attachments/assets/e4e5528f-9a3a-4e29-9ebc-1c03f76a1024

## An Automatic Flappy Bird playing Agent created using Reinforcement Learning
#### Here, I have developed a custom GYM Environment which is trained using A2C Model and MlpPolicy

### FlappyBirdEnv
| Action Space           | Discrete(2)                                                                                           |
|------------------------|-------------------------------------------------------------------------------------------------------|
| Observation Space      | Box(                                                                                                  |
|                        |  low = np.array([MIN_PLAYER_Y, MIN_VELOCITY, -window_w* 2, -window_h, 0], dtype=np.float32),          |
|                        |  high = np.array([MAX_PLAYER_Y, MAX_VELOCITY, window_w* 2, window_h, window_h], dtype=np.float32),    |
|                        |  shape = (5,),                                                                                        |
|                        |  dtype = np.float32,                                                                                  |
|                        |  )                                                                                                    |
|------------------------|-------------------------------------------------------------------------------------------------------|
