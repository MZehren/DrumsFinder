import tensorflow as tf

sess = tf.InteractiveSession()
y = tf.placeholder(tf.float32)
y_ = tf.placeholder(tf.float32)
multilabel = tf.nn.sigmoid_cross_entropy_with_logits(labels=y_, logits=y)


print sess.run(multilabel, {y: 0, y_:0})
print sess.run(multilabel, {y: 0.1, y_:0})
print

print sess.run(multilabel, {y: 1, y_:1})
print sess.run(multilabel, {y: 0.9, y_:1})
