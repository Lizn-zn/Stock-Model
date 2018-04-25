# _*_ coding:utf-8 _*_
import sys
import os
import stat
import socket
import paramiko


def data_download():
    FILES = ["估值指标", "成长能力与偿债能力", "技术指标", "财务质量",  "收盘价格"]
    USERNAME = "root"
    PASSWORD = "FhWJ4J6k"
    HOST = "210.28.133.11"
    PORT = 21030
    remotefile = "/root/things/"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    t = paramiko.Transport(sock)
    t.start_client()
    t.auth_password(USERNAME, PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(t)
    for f in FILES:
        if not os.path.exists(f):
            os.makedirs(f)
        localdir = sys.path[0] + "\\" + f
        remotedir = remotefile + f
        files = sftp.listdir_attr(remotedir)
        for temp in files:
            # Continue if it is not a table
            if not (temp.endswith(".csv") or temp.endswith(".xlsx")):
                continue
            elif temp.startswith("~$"):
                continue
            remotepath = remotedir + "/" + temp.filename
            localpath = localdir + "\\" + temp.filename
            if(os.path.exists(localpath)):
                print('exists {}, continue...'.format(temp.filename))
                continue
            sftp.get(remotepath, localpath)
            print('download {}...'.format(temp.filename))
    sftp.close()
    t.close()
    sock.close()


if __name__ == '__main__':
    data_download()
