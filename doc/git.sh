git init                      #初始化git仓库
git add .                     #添加仓库中所有文件
git commit -m "add file"      #提交   
git remote add origin https://gitee.com/kane_zhang/mes.git  #设置码云上对应项目的ssh链接,origin为链接名称,可自定义
#若要删除可用命令:  git remote rm origin
git pull --rebase origin master             #取回项目的master分支,并与本地的合并,若不合并push会失败
git push origin master                      #推送master分支到码云上，登录码云即可看见刚推送的项目了


