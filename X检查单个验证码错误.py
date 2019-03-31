import cv2
import numpy
import matplotlib.pyplot as plt
def show(a):
    plt.imshow(a)
    plt.show()
#---------------------------------------------------------------------------
def cover(a):#
    z = numpy.zeros((20, len(a))) #建立一个二维数组
    for j in range(20):
        for k in range(len(a)):
            z[j][k]=a[k][j] #将二维数组的横纵坐标倒置生成图像
    return(z)
#---------------------------------------------------------------------------
class code:
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
                if i==59:
                    b=True #如果最后一列有字符最后就不会返回最后一个分割
                    break
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
                    f.append(cover(c))
                    c.clear()
        else:
            f.append(cover(c))
        return(f)#返回整块数据
#---------------------------------------------------------------------------
    def splite2(a):#传入一个高度为20的矩阵
        b=False
        for i in range(20):#对矩阵进行自上向下扫描
            if b:
                break
            else:
                for j in range(len(a[i])): #行固定对列进行横向扫描
                    if int(a[i][j])==0:#扫描到行有数据
                        f = i #记录扫描到的行数
                        b=True
                        break
        b=False
        for i in reversed(range(20)):#对矩阵进行自下向上扫描
            if b:
                break #跳出双重循环
            else:
                for j in range(len(a[i])): #行固定对列进行横向扫描
                     if int(a[i][j])==0: #行固定，对列进行扫描
                         b=True #反向扫描到行有数据
                         l=i #，记录扫描到的最后行数
        return(a[f:l+1])
#---------------------------------------------------------------------------
p=code.read("C:\\train\\Source\\1\\1.jpg") #读入图片
s=code.splite1(p) #将图片分割为单个字符
print(type(s[0]))
#for i in s:
show(s[0])
