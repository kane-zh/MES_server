# 说明　
#本教程为ubuntu18.04安装方式，要求客户掌握基本的linux指令，并安装git
# 软件下载git clone https://gitee.com/kane_zhang/mes.git

1.安装数据库
   sudo apt-get install mysql-server
   sudo apt-get install mysql-client
   sudo apt-get install libmysqlclient-dev
2.查看数据库临时账号及密码 (---非必须)
   sudo  vi  /etc/mysql/debain.cnf
3.通过临时账号进入mysql (或通过操作系统root权限)
    mysql -u [临时账号] -p [临时密码]
4.设置root账号密码(密码要包含大写字母,小写字母,数字,特殊符号)(---非必须)
    use mysql;
    update user set authentication_string=password('admin123') where User='root' and Host='localhost';
    如果出错,使用下边两条:
	    update user set authentication_string='' where User='root' and Host='localhost';
	    ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'admin123';
    update user set plugin="mysql_native_password";
    flush privileges;
5.创建mes专用账号
    CREATE USER 'mesServer'@'localhost' IDENTIFIED BY 'mes@123456';
6.给新用户授权
    grant all privileges on *.* to 'mesServer'@'localhost';
    如果出错,使用下边一条:
         grant all PRIVILEGES on *.* to 'mesServer'@'localhost' identified by 'mes@123456';
7.安装python3
    sudo apt-get install python3
8.安装pip3
    sudo apt-get install python3-pip
9.进入应用程序目录
   cd  工程目录/mes_server/
10. 进入数据库命令行
   sudo mysql
11. 创建数据库
   source  工程目录/mes_server/db_tool/create.sql
12.退出数据库
   mysql>>exit;
13.安装必要的包
    pip3 install  -r  requirements.txt    目录所在位置(工程目录/mes_server/requirements.txt)
14. 建立数据表并创建超级用户
   python3 manage.py   makemigrations
   python3 manage.py   migrate   --database = 指定的数据库 (默认数据库default不需要,process,warehouse,quality,equipment,plan,production,lean)
   python3 manage.py   createsuperuser    (默认:admin  admin123)
15. 配置uwsgi
	[uwsgi]
	# 使用nginx连接时使用
	socket=127.0.0.1:8080
	# 直接做web服务器使用
	#http=127.0.0.:8080
	# 项目目录
	chdir=  工程目录/mes_server
	# 项目中wsgi.py文件的目录，相对于项目目录
	wsgi-file= Mes/wsgi.py
	processes=4
	threads=2
	master=True
	pidfile = uwsgi.pid
	daemonize = uswgi.log
16.启动uwsgi
     uwsgi  --ini   uwsgi.ini     目录所在位置(工程目录/mes_server/Mes/uwsgi.ini)
              {
                停止  uwsgi  --stop    uwsgi.pid
                重启  roouwsgi  --reload  uwsgi.pid
              }
17.安装nginx
  sudo apt-get install nginx
18.配置nginx
   vi   /etc/nginx/sites-enabled/default
   server {
      listen 8000;
      server_name mes_server;
      charset   utf-8;
      client_max_body_size 75M;

      location / {
            proxy_send_timeout 6000;
            proxy_connect_timeout 6000;
            proxy_read_timeout 6000;
            uwsgi_pass   127.0.0.1:8080;
            include  /etc/nginx/uwsgi_params;
       }
       location /static {
       # 指定静态文件存放的目录
       root 工程目录/mes_server;
         }
      }
19.启动应用程序   (---非必须)
    (测试)python3 manage.py runserver 0.0.0.0:8000
    (生产)uwsgi --ini 工程目录/mes_server/Mes/uwsgi.ini



