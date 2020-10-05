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
	    alter user 'root'@'localhost' identified with mysql_native_password by 'admin123';
    update user set plugin="mysql_native_password";
    flush privileges;
5.创建mes专用账号
    create user 'mesServer'@'localhost' identified by 'mes@123456';
6.给新用户授权
    grant all privileges on *.* to 'mesServer'@'localhost';
    如果出错,使用下边一条:
         grant all privileges on *.* to 'mesServer'@'localhost' identified by 'mes@123456';
7.关掉数据库 (---非必须)
   sudo /etc/init.d/mysql stop
8.设置数据库数据新路径 (---非必须)
   mkdir -p /数据盘目录/mysql/data --创建文件夹
   mv /var/lib/mysql/*  /数据盘目录/mysql/data  
   chown -R mysql:mysql /数据盘目录/mysql/data  --设置权限
9.修改数据库配置文件 (---非必须)
  vi /etc/mysql/mysql.conf.d/mysqld.cnf
  datadir = /数据盘目录/mysql/data
10.修改启动文件 (---非必须)
  vi /etc/apparmor.d/usr.sbin.mysqld
  #把
  /var/lib/mysql r
  /var/lib/mysql/** rwk
  #修改成
  /数据盘目录/mysql/data r,
  /数据盘目录/mysql/data/** rwk,
11.重启AppArmor服务使生效 (---非必须)
   sudo /etc/init.d/apparmor restart
12.重新初始化数据文件   (---非必须))
   sudo mysql_install_db
13.启动MySQL数据库服务 (---非必须)
   sudo /etc/init.d/mysql start
14.安装python3
    sudo apt-get install python3
15.安装pip3
    sudo apt-get install python3-pip
16.安装虚拟环境管理器   (---非必须)
    sudo pip3 install virtualenv
17.进入应用程序目录
   cd  工程目录/mes_server/
18.更改工程配置文件中的数据库账号跟密码部分(默认'mesServer' 'mes@123456')(---非必须)
   vi 工程目录/mes_server/Mes/setting.py
19.将媒体目录设置为数据盘之下的目录节点(---非必须)
   vi  工程目录/mes_server/Mes/setting.py
   MEDIA_URL= '/media/'
   MEDIA_ROOT = os.path.join(BASE_DIR, "media")      #指定应用程序根目录下的目录
   #MEDIA_ROOT ="/media/kane/data"                   #指定为自定义的目录
20. 进入数据库命令行
   sudo mysql
21. 创建数据库
   source  工程目录/mes_server/db_tool/create.sql
22.退出数据库
   mysql>>exit; 
23.建立python虚拟运行环境   (---非必须)
	建立虚拟环境			
	virtualenv -p  /usr/bin/python3 env_name
	激活虚拟环境
	source   env_name/bin/activate
		{
			关闭虚拟环境
			deactivate 
		}
24.切换到虚拟环境           (---非必须)
    cd  /env_name		
25.安装必要的包
    pip3 install  -r  requirements.txt    目录所在位置(工程目录/mes_server/requirements.txt)
26. 建立数据表并创建超级用户
   python3 manage.py   makemigrations
   python3 manage.py   migrate   --database = 指定的数据库 (默认数据库default不需要,process,warehouse,quality,equipment,plan,production,lean)
   python3 manage.py   createsuperuser    (默认:admin  admin123)
27. 配置uwsgi  
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
28.启动uwsgi
     uwsgi  --ini   uwsgi.ini     目录所在位置(工程目录/mes_server/Mes/uwsgi.ini)
              {
                停止  uwsgi  --stop    uwsgi.pid
                重启  roouwsgi  --reload  uwsgi.pid
              }
29.安装nginx
  sudo apt-get install nginx
30.配置nginx
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
31.启动nginx        (---非必须)
	sudo /usr/sbin/nginx
		{
		停止:sudo /usr/sbin/nginx -s stop
		重启:sudo /usr/sbin/nginx -s reload
		}
32.启动应用程序   (---非必须)
    (测试)python3 manage.py runserver 0.0.0.0:8000
    (生产)uwsgi --ini 工程目录/mes_server/Mes/uwsgi.ini



