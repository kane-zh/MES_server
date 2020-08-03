FROM ubuntu 
#声明镜像制作者
MAINTAINER kane  <kane.zhang01@163.com>
#设置时区
ENV TZ "Asia/Shanghai"
# 设置系统环境变量
ENV DOCKER_SRC=Mes
ENV DOCKER_HOME=/root
ENV DOCKER_PROJECT=/root/project

WORKDIR $DOCKER_PROJECT

#这一步操作将会把项目中application目录下的所有文件拷贝到镜像目录DOCKER_PROJECT=/root/project下面
COPY ./ ./

#安装应用运行所需要的工具
RUN apt-get update -y
RUN apt-get install nginx -y
RUN apt-get install python3 -y 
RUN apt-get install python3-pip -y 

#这一步安装python依赖软件
RUN pip3 install  -r requirements.txt
#暴露端口8000，到时候执行docker run 的时候才好把宿主机端口映射到8000
EXPOSE 8000

#赋予start_script执行权限
#RUN chmod u+x  doc/start_script

#容器启动后要执行的命令
ENTRYPOINT ["doc/start_script"]

