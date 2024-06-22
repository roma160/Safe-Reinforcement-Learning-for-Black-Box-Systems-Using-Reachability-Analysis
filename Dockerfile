# Source: https://github.com/alpine-ros/alpine-ros/blob/master/noetic-3.20/ros-core/Dockerfile
FROM alpine:3.20.0

ENV ALPINE_VERSION=3.20

RUN echo "https://alpine-ros.seqsense.org/v${ALPINE_VERSION}/backports" >> /etc/apk/repositories \
  && echo "https://alpine-ros.seqsense.org/v${ALPINE_VERSION}/ros/noetic" >> /etc/apk/repositories
COPY <<EOF /etc/apk/keys/builder@alpine-ros-experimental.rsa.pub
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnSO+a+rIaTorOowj3c8e
5St89puiGJ54QmOW9faDsTcIWhycl4bM5lftp8IdcpKadcnaihwLtMLeaHNJvMIP
XrgEEoaPzEuvLf6kF4IN8HJoFGDhmuW4lTuJNfsOIDWtLBH0EN+3lPuCPmNkULeo
iS3Sdjz10eB26TYiM9pbMQnm7zPnDSYSLm9aCy+gumcoyCt1K1OY3A9E3EayYdk1
9nk9IQKA3vgdPGCEh+kjAjnmVxwV72rDdEwie0RkIyJ/al3onRLAfN4+FGkX2CFb
a17OJ4wWWaPvOq8PshcTZ2P3Me8kTCWr/fczjzq+8hB0MNEqfuENoSyZhmCypEuy
ewIDAQAB
-----END PUBLIC KEY-----
EOF

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV ROS_DISTRO noetic

RUN apk add --no-cache \
    py3-rosdep \
    py3-rosdistro \
  && rosdep init \
  && sed -i -e 's|ros/rosdistro/master|alpine-ros/rosdistro/alpine-custom-apk|' /etc/ros/rosdep/sources.list.d/20-default.list

RUN apk add --no-cache \
  ros-noetic-catkin \
  ros-noetic-ros-core

# Source: https://danbruder.com/blog/what-is-the-alpine-equivalent-to-build-essential/
RUN apk --no-cache --update add build-base

# Source: https://stackoverflow.com/a/40944512/8302811
RUN apk add --no-cache bash