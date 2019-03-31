import os
import cv2
import numpy
import matplotlib.pyplot as plt
#---------------------------------------------------------------------------
class date:
#---------------------------------------------------------------------------
    def read(f):
        B,G,R=cv2.split(cv2.imread(f))
        gray=numpy.zeros((20, 60))#生成二维数组
        for i in range(60):
            for j in range(20):
                a=1/3 *B[j][i]+1/3*G[j][i]+1/3*R[j][i] #转换灰度
                if a<130: #生成灰度图
                    gray[j,i]=0
                else:
                    gray[j,i]=1
        return(gray)
#---------------------------------------------------------------------------
    def splite1(a):#传入60*20矩阵
        f=[] #最终返回的矩阵列表，分割成功的话返回四个
        c=[]#二维数组用于存储整块图像
        for i in range(60):#对行进行扫描
            b=False
            for j in range(20): #对列进行扫描
                if int(a[j][i])==0:#列固定，对行进行扫描
                    b=True #扫描到行有数据
                    break #跳出循环
            if b: #如果扫描的有数据
                d=[] #d为临时数组,用于存储整列数据
                for j in range(20):
                    d.append(a[j][i]) #将单个像素加入临时列数组
                c.append(d) #将临时列数组加入整块图像
            else:
                if len(c)>0:
                    f.append(c)
                    c.clear()
        else:
            if len(c)>0:
                f.append(c)
        return(f)#返回整块数据
#---------------------------------------------------------------------------
def batchoperating(path):
    counter=0
    for root, dirs, files in os.walk(path, topdown=False):
        print(root)
        for name in files:
            picture=date.read(os.path.join(root, name)) #读入图片
            cuts=date.splite1(picture) #将图片分割为单个字符
            if len(cuts)!=4:
                os.remove(os.path.join(root, name))
                print(name+"分割失败"+"分割了"+str(len(cuts))+"段字符")
                counter=counter+1
    print("分割失败了"+str(counter)+"个文件")
batchoperating("C:\\train\\Source\\6\\")