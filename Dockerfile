FROM ubuntu:20.04
RUN apt update
RUN apt install software-properties-common -y

# https://wiki.ros.org/ROS/Installation/UbuntuMirrors
RUN sh -c '. /etc/lsb-release && echo "deb http://ftp.tudelft.nl/ros/ubuntu $DISTRIB_CODENAME main" > /etc/apt/sources.list.d/ros-latest.list'
RUN apt install curl -y
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -
RUN apt update
RUN apt-get update
RUN apt install ros-noetic-desktop-full -y

RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3.9 -y
RUN python3.9 --version
RUN apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential -y
RUN apt install python3-pip -y # TODO: this actually installs on python 3.8

RUN pip3 install absl-py==2.1.0
RUN pip3 install gin==0.1.6
RUN pip3 install gin-config==0.5.0
RUN pip3 install tensorflow==2.13.1
RUN pip3 install tf-agents==0.17.0
RUN pip3 install scipy==1.10.1
RUN pip3 install joblib==1.4.2
RUN pip3 install omegaconf==2.0
RUN pip3 install mbrl==v0.1.4
RUN pip3 install torch==2.3.0
RUN pip3 install hydra-core==1.1.0

CMD [ "sleep", "infinity" ]
