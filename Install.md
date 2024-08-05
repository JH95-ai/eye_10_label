# Install

## Install from docker

1. Install dependent software.
```
sudo apt-get install x11-xserver-utils
export DISPLAY=:0
xhost +
```

2. install docker and environment, refer to [How To Install and Use Docker on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)

3. download docker iamges and load it.
```
sudo docker load -i docker_flat_vx.x.x.tar
$ docker images
REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
ts/flat                 0.1.7               1d360e8d7d48        47 minutes ago      1.84GB
```

4. create docker container
```
cd ~
mkdir docker_space
docker create --name flat -it -e DISPLAY=$DISPLAY -p 8888:8888 -v /tmp/.X11-unix:/tmp/.X11-unix -v ~/docker_space:/mnt:rw ts/flat:0.1.7
$ docker ps -a
CONTAINER ID        IMAGE                              COMMAND             CREATED             STATUS                    PORTS               NAMES
ce4a1faced97        ts/flat:0.1.7                      "/bin/bash"         3 seconds ago       Created                                       flat
```

5. docker container start and run.
```
docker start ce4a1faced97
docker exec -it ce4a1faced97 /bin/bash

# start-up flat tool
python main.py
```
