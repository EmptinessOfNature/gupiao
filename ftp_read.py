from ftplib import FTP
import os

# FTP服务器的IP地址或域名
# ftp_server = '47.113.221.128'
ftp_server = '47.236.15.48'
# FTP服务器的用户名和密码
ftp_username = 'ftpuser'
ftp_password = 'NB666888nb'


class FtpRead():

    def read(self, input):
        # 连接到FTP服务器
        ftp = FTP(ftp_server)
        ftp.login(ftp_username, ftp_password)

        strs = input.split(",")
        for i in range(len(strs)):
            file_name = "gupiao/data_server/" + strs[i] + ".csv"
            path = "./data_server/" + strs[i].split('/')[0]
            local_name = "./data_server/" + strs[i] + ".csv"
            if not os.path.exists(path):
                os.makedirs(path)
            # 打开一个本地文件来保存下载的数据
            try:
                with open(local_name, 'wb') as file:
                    # 使用'RETR'命令来下载文件
                    ftp.retrbinary(f'RETR {file_name}', file.write)
            except:
                print('ftp读取数据失败',file_name)

        # 断开FTP连接
        ftp.quit()


if __name__ == '__main__':
    ftp_read = FtpRead()
    ftp_read.read("TSLA/20240514,TSLA/20240515")