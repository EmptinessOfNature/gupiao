from ftplib import FTP
 
# FTP服务器的IP地址或域名
ftp_server = '47.113.221.128'
# FTP服务器的用户名和密码
ftp_username = 'ftpuser'
ftp_password = 'NB666888nb'
 
# 连接到FTP服务器
ftp = FTP(ftp_server)
ftp.login(ftp_username, ftp_password)
 
# 打印出当前工作目录下的文件列表
ftp.retrlines('LIST')
 
# 下载文件的例子
# 假设我们要下载的文件名为'example.txt'
file_name = 'buy_sell.txt'
# 进入到文件所在的目录，这里假设文件就在根目录下
# 如果文件在其他目录，使用ftp.cwd(path)切换到相应目录
# ftp.cwd('/path/to/directory')
 
# 打开一个本地文件来保存下载的数据
with open(file_name, 'wb') as file:
    # 使用'RETR'命令来下载文件
    ftp.retrbinary(f'RETR {file_name}', file.write)
 
# 断开FTP连接
ftp.quit()