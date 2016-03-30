import tensorflow as tf
import numpy as np
import data

def init_weight(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.1))

def init_bias(shape):
    return tf.Variable(tf.constant(0.1, shape=shape))

training, test = data.load_data()

sess = tf.Session()

# 24 x 24
x = tf.placeholder(tf.float32, shape=[None, 24 * 24])
y_ = tf.placeholder(tf.float32, shape=[None, 2])


W = init_weight([24 * 24, 2])
b = init_bias([2])

y = tf.nn.softmax(tf.matmul(x,W) + b)
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
ce_summ = tf.scalar_summary("cross entropy", cross_entropy)

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

accuracy_summary = tf.scalar_summary("accuracy", accuracy)

train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
sess.run(tf.initialize_all_variables())

merged = tf.merge_all_summaries()
writer = tf.train.SummaryWriter("./tmp/logs", sess.graph_def)

for i in range(10000):
  batch = data.next_batch(training, 50)
  sess.run(train_step, feed_dict={x: batch[0], y_: batch[1]})

  test_images, test_labels = test
  if i % 100 == 0:
      (m, a) = sess.run([merged, accuracy], feed_dict={x: test_images, y_: test_labels})

      writer.add_summary(m, i)

      print('Epoch: %d' % i)
      print('Accuracy: %0.04f' % a)