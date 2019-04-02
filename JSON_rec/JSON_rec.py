import threading
import socket
import sys
import cv2
import numpy
import json

HOST=' '
PORT=50000
threads=[]
sc={}
ID={}
global s,user_num

def recieve_send(conn_1,address_1):                         #conn_1為寄出方
    name_d=""
    while True:
            data=conn_1.recv(1024)                    #收到conn_1寄出的訊息
            if data==str.encode("name_d"):
                name_dir=str(conn_1.recv(1024),encoding='utf-8')
                continue
            elif data==str.encode("start"):
                get_image(conn_1,name_dir)
                continue


def get_image(conn,name_dir):
    img_json=""
    print("\nplese wait...\n")
    while True:
        data=conn.recv(1024)
        if len(data)<1024:
            img_json=img_json+str(data,encoding="utf-8")
            imga=json.loads(img_json)
            imgf=(numpy.array(imga)).astype(numpy.uint8)
            cv2.imwrite(name_dir,imgf)
            print("finished\n")
            break
        img_json=img_json+str(data,encoding="utf-8")

def connect(cli):
    while True:
        conn,address=cli.accept()#在收到連線要求後准許連線，conn為client產生出的socket物件，address為客戶端地址
        t=threading.Thread(target=recieve_send,args=(conn,address))
        t.start()
        threads.append(t)
        sc[address]=conn
        
def main():
    global s,user_num
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #設定socket的參數
    s.bind((HOST,PORT))                                #設定address跟port
    s.listen(2)                                        #最多同時連線2個
    T=threading.Thread(target=connect,args=(s,))    #透過threading來跑connect函式
    T.start()
    temp_2=0
    while True:
        temp=input("欲離開請按0：")      
        if temp=='0':
            break
        else:
            print("錯誤的輸入，請重新輸入\n")
    sys.exit(0)

if __name__=='__main__':
    main()

        
