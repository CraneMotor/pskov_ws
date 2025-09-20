


import threading
import sys


class GetRobotPosition:
     


    robot_1_mutex = threading.Lock()
    robot_2_mutex = threading.Lock()
    robot_3_mutex = threading.Lock()
    robot_4_mutex = threading.Lock()
    robot_5_mutex = threading.Lock()

    robot_1_index = 0
    robot_2_index = 0
    robot_3_index = 0
    robot_4_index = 0
    robot_5_index = 0



    robot_1_poses = {
                0: [100,    120,   -20,     180,    0],     # С тележки взять
                1: [60,     90,    -60,     135,    0],     #  Переложить на стол 
                2: [60,     90,    -60,     135,    0],     #  Переложить на стол 
                3: [-30,    90,    -80,     200,    0],     # В станок
                4: [-30,    90,    -80,     200,    0],     # В станок
                5: [-30,    90,    -80,     200,    0],     # В станок
                6: [-120,   90,    -80,     200,    0],     # На готовый стол
                7: [-120,   90,    -80,     200,    0],     # На готовый стол
            }
    
    gripper_1_poses = {
                0: -1.0,     # С тележки взять
                1: 0.0,     #  Переложить на стол 
                2: -1.0,     #  Переложить на стол 
                3: -1.0,     # В станок
                4: 0.0,     # В станок
                5: -1.0,     # В станок
                6: -1.0,          # На готовый стол
                7: -0.0,          # На готовый стол
    }

    robot_2_poses = {
                0: [-0,     -120,     20,     180,    0],
                1: [-100,     -120,     20,     180,    0],
            }
    
    robot_3_poses = {
                0: [45,     45,     45,     200,    0],
                1: [20,     -40,    50,     135,    0],
                2: [20,     -40,    50,     135,    0],
                3: [20,     -40,    50,     135,    0],
                4: [-80,    0,      -10,    135,    0],
            }
    robot_4_poses = {0: [45,-90,45,  200, 0]}
    robot_5_poses = {
                0: [45,     45,     45,     200,    0],
                1: [45,     -120,    120,     135,    0],
                2: [45,     -120,    120,     135,    0],
                3: [-70,     -120,    120,     135,    0],
                4: [-70,     -70,    70,     135,    0],
            }
    
    
    def __init__(self):
        ...

    

    def getPoseRobot1(self):
        return self.robot_1_poses[self.robot_1_index]
    
    def getGripperRobot1(self):
        return self.gripper_1_poses[self.robot_1_index]

    def getPoseRobot2(self):
        return self.robot_2_poses[self.robot_2_index]

    def getPoseRobot3(self):
        return self.robot_3_poses[self.robot_3_index]

    def getPoseRobot4(self):
        return self.robot_4_poses[self.robot_4_index]

    def getPoseRobot5(self):
        return self.robot_5_poses[self.robot_5_index]
    

    def updatePoseRobot1(self):
        if self.robot_1_index == len(self.robot_1_poses) - 1:
            self.robot_1_index = 1
        else:
            self.robot_1_index = (self.robot_1_index + 1) % len(self.robot_1_poses)
     
    
    def updatePoseRobot2(self):
        self.robot_2_index = (self.robot_2_index + 1) % len(self.robot_2_poses)
       
    def updatePoseRobot3(self):
        self.robot_3_index = (self.robot_3_index + 1) % len(self.robot_3_poses)
    

    def updatePoseRobot4(self):
        self.robot_4_index = (self.robot_4_index + 1) % len(self.robot_4_poses)
        

    def updatePoseRobot5(self):
        self.robot_5_index = (self.robot_5_index + 1) % len(self.robot_5_poses)
        








