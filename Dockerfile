FROM ubuntu:20.04
RUN apt update
RUN apt install software-properties-common -y

RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN apt install curl -y
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -
RUN apt update
RUN apt-get update
RUN apt install ros-noetic-desktop-full -y

RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3.9 -y
RUN python3.9 --version
RUN apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential -y
RUN apt install python3-pip -y
RUN python3 -m pip install absl-py
RUN python3 -m pip install gin
RUN python3 -m pip install tensorflow
RUN python3 -m pip install gin-config
RUN python3 -m pip install tf-agents==0.17.0
RUN python3 -m pip install scipy
RUN python3 -m pip install joblib
RUN python3 -m pip install tensorboardX
RUN python3 -m pip install torch
RUN python3 -m pip install omegaconf==2.0
RUN python3 -m pip install hydra-core==1.1.0
RUN python3 -m pip install mbrl==v0.1.4

CMD [ "sleep", "infinity" ]
