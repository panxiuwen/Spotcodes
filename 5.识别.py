import os
import random
import tensorflow as tf
#---------------------------------------------------------------------------
def read(path):
    f=open(path,"r")
    a=f.read().strip().replace("\n",",")
    return(a.split(","))
#---------------------------------------------------------------------------
def test(test_image,test_label,label):
    random.seed(100)
    random.shuffle(test_image)
    random.seed(100)
    random.shuffle(test_label)
    random.seed(100)
    random.shuffle(label)
    Count=len(test_image)
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
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    sess=tf.Session()
    saver.restore(sess, "./model/code-3999")
    accuracy_score = sess.run(accuracy, feed_dict={x: test_image, y_: test_label})
    #for i in range(Count-1):
    #    print(accuracy_score[i],label[i])
    print(accuracy_score)
train_image=[]
train_label=[]
labels=[]
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
                labels.append(l)
test(train_image,train_label,labels)

