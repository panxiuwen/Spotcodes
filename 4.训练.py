import os
import random
import tensorflow as tf
#---------------------------------------------------------------------------
def val(x):
    c=eval(x)*2+1
    return(c)
#---------------------------------------------------------------------------
def read(path):
    f=open(path,"r")
    a=f.read().strip().replace("\n",",")
    f.close()
    l=a.split(",")
    c=list(map(val,l))
    return(c)
#---------------------------------------------------------------------------
class task:
    def train(train_images,train_labels):
        random.seed(100)
        random.shuffle(train_images)
        random.seed(100)
        random.shuffle(train_labels)
        #打乱训练集
        Count= len(train_images)#输入的个
        print(len)
        x=tf.placeholder(tf.float32,[None,324])#神经网络的输入#18*18
        w1=tf.Variable(tf.random_normal([324,108],stddev=0.1))#权重
        rw1=tf.contrib.layers.l2_regularizer(0.0001)(w1)#设定w的正则化
        b1=tf.Variable(tf.zeros([108]))# 偏置
        y1=tf.nn.relu(tf.matmul(x,w1)+b1)
        w2=tf.Variable(tf.random_normal([108,36],stddev=0.1))#权重
        rw2=tf.contrib.layers.l2_regularizer(0.0001)(w2)#设定w的正则化
        b2=tf.Variable(tf.zeros([36]))# 偏置
        y=tf.matmul(y1, w2)+b2
        y_=tf.placeholder(tf.float32,[None,36])#神经网络的标签#10+26
        global_step=tf.Variable(0, trainable=False)
        learning_rate=tf.train.exponential_decay(0.005,global_step,Count, 0.99,staircase=True)#设定学习率
        ema=tf.train.ExponentialMovingAverage(0.99,global_step).apply(tf.trainable_variables())#设定滑动平均
        cross_entropy=tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y,  labels=tf.argmax(y_, 1)))#计算损失的交叉熵函数
        loss=cross_entropy+rw1+rw2 #将交叉熵与正则化合计到loss里
        train_step=tf.train.GradientDescentOptimizer(learning_rate).minimize(loss,global_step=global_step)#优化交叉熵
        with tf.control_dependencies([train_step, ema]):
            train= tf.no_op(name='train')
        saver=tf.train.Saver()#定义保存模型
        sess=tf.Session()
        sess.run(tf.global_variables_initializer())#初始化参数
        for i in range (Count-1):
            batch_xs,batch_ys=[train_images[i]],[train_labels[i]]
            sess.run(train,feed_dict={x:batch_xs,y_:batch_ys})#喂入数据
        print(sess.run(loss,feed_dict={x:batch_xs,y_:batch_ys}))
        saver.save(sess,"C:\\train\\Python\\model\\code",global_step=global_step)
        sess.close()
#---------------------------------------------------------------------------
#---------main----------------------------
train_image=[]
train_label=[]
w=range(36)
for i in range(10):
    for root, dirs, files in os.walk("C:\\train\\Formdate\\{0:}\\input\\".format(i), topdown=False):
        sl=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        char=ord(root[-1])
        if char in range(48,58):
            l=char-48
        elif char in range(97,123):
            l=char-87
        if l in w:
            sl[l]=1
            label=sl
            for name in files:
                train_image.append(read(os.path.join(root, name)))
                train_label.append(label)
task.train(train_image,train_label)