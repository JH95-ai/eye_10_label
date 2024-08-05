
# Facial landmark annotation tool(FLAT)

## Realse Note
### V0.1.8-beta
+ [x] add Dcokerfile.
+ [x] upgrade landmark model file.

### V0.1.7
Update date 2020/3/19
+ [x] fix for window

## install
+ Ubuntu
```
conda create -n flat python==3.7
conda activate flat
# install protobuf
pip install protobuf==3.19
# install tensorflow
conda install tensorflow==1.14
or 
pip install tensorflow==2.3
# install pyqt5
conda install pyqt==5.12.3
or 
pip install PyQt5==5.12.3
# install opencv
conda install opencv==4.1.0
or 
pip install opencv-python==4.1.0.25
```

+ window10 isntall
1. 下载并安装anaconda
下载地址：
https://www.anaconda.com/distribution/

2. 创建conda环境
添加清华源,打开"Anaconda Powershell prompt"输入如下命令：
```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --append channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/fastai/
conda config --append channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
conda config --append channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/
conda config --set show_channel_urls yes
```
2. 安装软件
- 安装pip
参考地址：https://blog.csdn.net/esting_tang/article/details/80973478

- 安装tensorflow
```
conda create -n flat python=3.7
conda activate flat
conda install tensorflow==1.14.0
```
- 安装OpenCV
pip install opencv-python==4.1.0.25
- 安装pyqt
conda install pyqt==5.12.3

## 运行
```
python main.py
```

## pyinstaller打包应用程序
```
pyinstaller -F main.py -n flat_v0.1.3_for_ubuntu18.04
```
+ pyinstaller可能遇到的问题
```
+ install pyinstaller
pip install pyinstaller
# pyinstaller package run error
"No module named 'pkg_resources.py2_warn'"
setuptools降级到44.0.0
```
conda install setuptools==44.0.0
```
+ pyinstaller cmd
pyinstaller -F main.py -n flat_v0.1.6_for_win10
```

## docker
### build
```
docker build --tag=ts/flat:0.1.7 .
```
### create
```
sudo apt-get install x11-xserver-utils
export DISPLAY=:0
xhost +
docker create --name flat -it -e DISPLAY=$DISPLAY -p 8888:8888 -v /tmp/.X11-unix:/tmp/.X11-unix -v ~/iwork/share:/mnt:rw ts/flat:0.1.7
```
### start & run
1. docker ps -a 查看container
```
$ docker ps -a
CONTAINER ID        IMAGE                              COMMAND             CREATED             STATUS                         PORTS               NAMES
5a22b5bd015a        ts/flat:0.1.7                      "/bin/bash"         5 seconds ago       Created                                            flat
```
2. run
```
docker start 5a22b5bd015a
docker exec -it 5a22b5bd015a /bin/bash
root@5a22b5bd015a:/flat#
```

## ui to py
```
pyuic5 -o output.py test.ui
```
