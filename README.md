# Safe-Reinforcement-Learning-for-Black-Box-Systems-Using-Reachability-Analysis
This repository contains the code for the paper [Safe Reinforcement Learning Using Black-Box Reachability Analysis](https://arxiv.org/abs/2204.07417). [Demo video](https://youtube.com/playlist?list=PL7bkcpwNaUjz-S1b5KBzpgCZ1SP4DXsoi)

# Short Video for describing the idea

[![Video](https://img.youtube.com/vi/U50VOH979vE/0.jpg)](https://www.youtube.com/watch?v=U50VOH979vE)


## Installation
The repository provides two ros packages: brsl and brsl_msgs. To get everything up and running, we need to install ros and some other dependencies. Everything is tested on ubuntu 20.04 LTS

### Ros Installation.
you can find the installation steps for ros in the official [link](http://wiki.ros.org/noetic/Installation/Ubuntu).

### Libraries Installation
You need to install the following libraries.

```
python -m pip install absl-py==2.1.0
python -m pip install gin==0.1.6
python -m pip install gin-config==0.5.0
python -m pip install tensorflow==2.13.1
python -m pip install tf-agents==0.17.0
python -m pip install scipy==1.10.1
python -m pip install joblib==1.4.2
python -m pip install torch==2.3.0
python -m pip install omegaconf==2.0
python -m pip install hydra-core==1.1.0
python -m pip install mbrl==v0.1.4
python -m pip install tensorrt==10.1.0
```

If you want to utilize gpu for your training, you should install tf-gpu and torch cuda instead.

### Init usage
Given that you are located at the `init` branch, here is how you can run the project in VScode devcontainers:
1. Open folder using VScode devcontainers. It should work out of the box wihhout a need for any additional setup.
2. Open terminal `#0` and run the following commands:
```shell
cd catkin_ws
source /usr/ros/noetic/setup.bash
catkin_make

source devel/setup.bash
catkin_make
```
3. In terminal `#1`, run the following commands:
```shell
cd catkin_ws
source devel/setup.bash
roscore
```

4. In terminal `#2`, run the following commands:
```shell
cd catkin_ws
source devel/setup.bash
roslaunch brsl turtlebot.launch
```

TODO: IDK what to do next, it crashes, and should be fixed.

### Old Usage
To run the agents, first, make a catkin_ws.
```
cd
mkdir -p catkin_ws/src
cd catkin_ws
source /opt/ros/noetic/setup.bash
catkin_make
```

Then copy both `brsl` and `brsl_msgs` to `catkin_ws/src` in your home directory.

Finally, run:
```
source devel/setup.bash
cd ./src
catkin_make install
```

This should build the repository.

To run the scripts, go to your catkin_ws directory, source the workspace, and run both the environment and the launch script for the agent.

```
roscore
```
Then, in a second terminal run the environment:

```
cd ~/catkin_ws
source devel/setup.bash
rosrun brsl Turtlebot_environment
```

Finally, open a third terminal and run the agent

```
cd ~/catkin_ws
source devel/setup.bash
roslaunch brsl turtlebot.launch
```
