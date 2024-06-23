###################################################################################################
# @Author: Mahmoud-Selim 
# @Date: 2021-09-16 09:53:47 
# @Last Modified by:   Mahmoud-Selim 
# @Last Modified time: 2021-09-16 09:53:47 
###################################################################################################

class MetricsCollector():
    def __init__(self, safety_dir):
        pass
    
    # Each Episode
    def add_collision_rate(self, step, rate):
        pass

    # Each Episode
    def add_goal_rate(self, step, rate):
        pass

    # Each Episode
    def add_time_to_goal(self, step, time):
        pass

    # Each Time Step
    def add_safety_interventions(self, step, rate):
        pass

    # Each Time Step
    def add_plan_time(self, step, plan_t):
        pass

    # Each Time Step
    def add_robot_speed(self, step, speed):
        pass

    # Each Time Step
    def add_lr(self, step, lr):
        pass



