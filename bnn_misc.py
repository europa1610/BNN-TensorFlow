import tensorflow as tf
import numpy as np

#Implements y = +1 for x > 0 and y = -1 for x <= 0
layer_names = []
def sign_binarize(inp):
    h_sig = tf.clip_by_value((inp+1.)/2., 0, 1)
    round_out = tf.round(h_sig)
    round_fin = h_sig + tf.stop_gradient(round_out - h_sig)
    return (2.*round_fin - 1.)

def bin_dense_layer(in_act, num_out, training=True, name='Bin_Dense_L'):
    with tf.variable_scope(name+'_params', reuse=False):
        l_w = tf.get_variable('weight', [in_act.shape[1], num_out], initializer = tf.random_uniform_initializer(-1, 1), constraint=lambda w: tf.clip_by_value(w, -1., 1.), trainable=True)
        #l_w1 = tf.get_variable('weight1', [in_act.shape[1], num_out], initializer = tf.random_uniform_initializer(-1, 1), constraint=lambda w: tf.clip_by_value(w, -1., 1.), trainable=True)
        l_b = tf.get_variable('bias', [num_out], initializer=tf.zeros_initializer(), trainable=True)
        #l_mod = tf.get_variable('modulo', [1], initializer=tf.random_uniform_initializer(-1, 1), constraint=lambda w: w, dtype=tf.float32, trainable=True)
        #l_mod1 = tf.get_variable('modulo1', [1], initializer=tf.random_uniform_initializer(-1, 1), constraint=lambda w: w, dtype=tf.float32, trainable=True)

    tf.add_to_collection(name+'_w', l_w)
    layer_names.append(name)
    bin_w = sign_binarize(l_w)
    res = tf.matmul(in_act, bin_w)
    res = (tf.nn.bias_add(res, sign_binarize(l_b)))
    #res = tf.floormod(res, l_mod)
    #res = l_mod1*tf.math.sin(res/l_mod)
    #res = tf.floormod(res, 0.21) #+ tf.floormod(0.98, l_mod)
    return res

def dense_layer(in_act, num_out, training=True, name='dense_l'):
    with tf.variable_scope(name + '_params', reuse=False):
        l_w = tf.get_variable('weight', [in_act.shape[1], num_out], initializer=tf.random_uniform_initializer(-1., 1.), trainable=True)
        l_w1 = tf.get_variable('weight1', [num_out, num_out], initializer=tf.random_uniform_initializer(-1., 1.), trainable=True)
    #res = tf.matmul(tf.math.square(in_act), l_w1) + tf.matmul(in_act, l_w)
    res = tf.math.sin(tf.matmul(2*np.pi*in_act, l_w)) #*(tf.matmul(in_act, l_w1))
    res = tf.matmul(res, l_w1)
    return res

def compute_gradients(loss, optimizer):
    gradient_list = []
    weight_updates = []
    for l_name in layer_names:
        params = tf.get_collection(l_name + '_w')
        print("-----> Prams: --------->")
        print(params)
        if params:
            grad = optimizer.compute_gradients(loss, var_list=params[0])
            gradient_list.append(grad[0][0])
            weight_updates.extend(params)
    return zip(gradient_list, weight_updates)

'''
inp = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],[-2, 0, -8, -9, 3, 9, -2, 9, 0.25, 0.75, -0.25, -0.75]], dtype=np.float32)
inp1 = tf.placeholder(dtype=tf.float32, shape=(2, 12))
res = bin_dense_layer(inp1, 2048)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    ret=sess.run(res, feed_dict={inp1:inp})
    print(ret)
'''
