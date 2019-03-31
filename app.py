import cv2
import numpy
import tensorflow as tf
#import tensorflow as tf
#import matplotlib.pyplot as plt
#---------------------------------------------------------------------------
class date:
#---------------------------------------------------------------------------
    def __cover(a):#
        z = numpy.zeros((20, len(a))) #建立一个二维数组
        for j in range(20):
            for k in range(len(a)):
                z[j][k]=a[k][j] #将二维数组的横纵坐标倒置生成图像
        return(z)
#---------------------------------------------------------------------------
    def __fts(a):#
        return(str(int(a)))
#---------------------------------------------------------------------------
    def __read(f):
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
    def __splite1(a):#传入60*20矩阵
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
                    f.append(date.__cover(c))
                    c.clear()
        else:
            if len(c)>0:
                f.append(date.__cover(c))
        return(f)#返回整块数据
#---------------------------------------------------------------------------
    def __splite2(a):#传入一个高度为20的矩阵
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
    def __format(str):#以文本的方式处理不规则图像并输出18*18图形
        str=str.strip()
        lines=str.split("\n")
        result=""
        line_len=len(lines)
        column_len=len(lines[0].replace(",",""))
        space1,remain1=divmod(18-line_len,2) #space是商，remain是余数
        space2,remain2=divmod(18-column_len,2) #space是商，remain是余数
        spaceline="1,"*17+"1"+"\n"
        result=spaceline*space1+result
        space=space2+remain2
        for line in lines:
            result=result+"1,"*space2+line+",1"*space+"\n"
        space=space1+remain1
        result=result+spaceline*space
        return result
#---------------------------------------------------------------------------
    def __spot(image):
        x = tf.placeholder(tf.float32, [None, 324])
        y_ = tf.placeholder(tf.float32, [None, 36])
        w1=tf.Variable(tf.random_normal([324,108],stddev=0.1))#权重
        rw1=tf.contrib.layers.l2_regularizer(0.0001)(w1)#设定w的正则化
        b1=tf.Variable(tf.zeros([108]))# 偏置
        y1=tf.nn.relu(tf.matmul(x,w1)+b1)
        w2=tf.Variable(tf.random_normal([108,36],stddev=0.1))#权重
        rw2=tf.contrib.layers.l2_regularizer(0.0001)(w2)#设定w的正则化
        b2=tf.Variable(tf.zeros([36]))# 偏置
        y=tf.matmul(y1, w2)+b2
        ema = tf.train.ExponentialMovingAverage(0.99)
        ema_restore = ema.variables_to_restore()
        saver = tf.train.Saver(ema_restore)
        prediction=tf.argmax(y, 1)
        sess=tf.Session()
        saver.restore(sess, "./model/code-3999")
        result = sess.run(prediction, feed_dict={x: image})
        s=""
        for i in result:
            if i in range(10):
                s=s+chr(i+48)
            if i in range(10,36):
                s=s+chr(i+87)
        return s
#---------------------------------------------------------------------------
    def betch(p):
        p=date.__read(p)#读入图片，返回二值图
        l=date.__splite1(p)#将返回的图片尝试分割
        if len(l)==4:
            images=[]
            for i in range(4):
                z=date.__splite2(l[i])
                str=""
                for j in z:
                    str=str+",".join(list(map(date.__fts,j)))+"\n"
                images.append(date.__format(str).strip().replace("\n",",").split(","))
            print(date.__spot(images))
        else:
            print("分割失败，因为返回了"+str(len(l))+"个字符")
#---------------------------------------------------------------------------
date.betch("C:\\Users\\Sean\\Desktop\\371.jpg")
