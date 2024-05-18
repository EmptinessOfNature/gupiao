from ftplib import FTP
import os

# FTP服务器的IP地址或域名
# ftp_server = '47.113.221.128'
ftp_server = '47.236.15.48'
# FTP服务器的用户名和密码
ftp_username = 'ftpuser'
ftp_password = 'NB666888nb'

local_path = "gupiao/data_server/"


class FtpRead():

    def download_file_list(self, input):
        # 连接到FTP服务器
        ftp = FTP(ftp_server)
        ftp.login(ftp_username, ftp_password)

        strs = input.split(",")
        for i in range(len(strs)):
            file_name = local_path  + strs[i] + ".csv"
            path = local_path + strs[i].split('/')[0]
            local_name = local_path + strs[i] + ".csv"
            if not os.path.exists(path):
                os.makedirs(path)
            # 打开一个本地文件来保存下载的数据
            try:
                with open(local_name, 'wb') as file:
                    # 使用'RETR'命令来下载文件
                    ftp.retrbinary(f'RETR {file_name}', file.write)
            except:
                print('ftp读取数据失败',file_name)
                os.remove(local_name)

        # 断开FTP连接
        ftp.quit()

    def download_path(self, ftp_file_path):
        # 连接到FTP服务器
        ftp = FTP(ftp_server)
        ftp.login(ftp_username, ftp_password)
        path_list = ftp.nlst(ftp_file_path)
        
        #获取单只股票数据
        for path in path_list:
            #获取股票list目录
            if not os.path.exists(path):
                    os.makedirs(path)
            file_list = ftp.nlst(path)
            for file_name in file_list: 
                
                with open(path  + "/" +file_name.split('/')[3], 'wb') as file:
                    # 使用'RETR'命令来下载文件
                    ftp.retrbinary(f'RETR {file_name}', file.write)
                
            print(path, "下载成功")
        ftp.quit()


if __name__ == '__main__':
    ftp_read = FtpRead()
    ftp_read.download_file_list("TSLA/20240514,TSLA/20240515")
    print('文件下载成功')
    ftp_read.download_path("./data_server")