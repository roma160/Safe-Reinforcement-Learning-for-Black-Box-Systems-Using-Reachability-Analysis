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

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

CMD [ "sleep", "infinity" ]
