"""
This is the object module, which will be used for object in RL environment.
"""

import numpy as np

class Drone:
    """
    This is the drone class, which will be used for drone in RL environment.
    """
    def __init__(self, drone_id, x=0, y=0, battery=100):
        self.drone_id = drone_id
        self.x = x
        self.y = y
        self.battery = battery
        self.alive = True
    
    @property
    def state(self):
        return np.array([
            self.x,
            self.y,
            self.battery
        ],dtype=np.float32)
    
    def step(self,action):
        """
        0 = up
        1 = down
        2 = left
        3 = right
        4 = hover
        """
        if self.battery <=0:
            self.alive = False
            return
        
        if action == 0:
            self.y += 1    
        elif action == 1:
            self.y -= 1
        elif action == 2:
            self.x -= 1
        elif action == 3:
            self.x += 1
        
        self.battery -= 1

class DroneEnv:
    def __init__(self, n_drones=3):
        self.drones = [Drone(i) for i in range(n_drones)]
        self.target = np.array([10, 10])

    def get_obs(self):
        return np.concatenate([d.state for d in self.drones])

    def step(self, actions):
        rewards = []

        for drone, action in zip(self.drones, actions):
            drone.step(action)

            pos = np.array([drone.x, drone.y])
            dist = np.linalg.norm(pos - self.target)

            reward = -dist
            rewards.append(reward)

        done = all(not d.alive for d in self.drones)

        return self.get_obs(), rewards, done