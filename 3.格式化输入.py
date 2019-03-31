import os
import matplotlib.pyplot as plt
#---------------------------------------------------------------------------
class date:
#---------------------------------------------------------------------------
    def formatex(path1,path2):#以数组的方式处理不规则图像并输出18*18图形
        t=open(path1,"r")
        l=[]#定义最后生成的列表
        z=t.read().strip().split("\n")
        t.close()
        f=open(path2,"w")
        a,b=divmod(18-len(z),2) #a是商，b是余数
        g=["1"]*18#g是一个常量列表
        for i in range(a):
            l.append(g)
            f.write(",".join(g)+"\n")
        for j in z:
            c=j.strip("\n").split(",")
            x,y=divmod(18-len(c),2) #a是商，b是余数
            e=[]#定义一个临时的列表带有行数据
            for i in range(x):
                e.append("1")
            for d in c:
                e.append(d)
            for i in range(x+y):
                e.append("1")
            l.append(e)
            f.write(",".join(e)+"\n")
        for i in range(a+b):
            l.append(g)
            f.write(",".join(g)+"\n")
        f.close()
#---------------------------------------------------------------------------
    def show(path):#以数组的方式读取数据并显示
        ls=[]
        f=open(path,"r")
        a=f.read().strip()
        c=a.split("\n")
        f.close()
        for line in c:
            s=line.split(",")
            l=[]
            for t in s:
                l.append(eval(t))
            ls.append(l)
        plt.imshow(ls)
        plt.show()
#---------------------------------------------------------------------------
    def format(path1,path2):#以文本的方式处理不规则图像并输出18*18图形
        file=open(path1,"r")
        str=file.read().strip()
        lines=str.split("\n")
        file.close()
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
        file=open(path2,"w")
        file.write(result)
        file.close()
#---------------------------------------------------------------------------
def bachoperating(path):
    for root, dirs, files in os.walk(path, topdown=False):
        counter=1
        for name in files:
            if counter<10:
                filename="0"+str(counter)+".txt"
            else:
                filename=str(counter)+".txt"
            inputfile=os.path.join(root, name)
            outputfile=root.replace("text","input")+"\\"+filename
            print(inputfile,outputfile)
            #date.regularization(inputfile,outputfile)
            #date.show(inputfile)
            date.format(inputfile,outputfile)
            counter=counter+1
#---------------------------------------------------------------------------
bachoperating("C:\\train\\Formdate\\9\\text\\")
