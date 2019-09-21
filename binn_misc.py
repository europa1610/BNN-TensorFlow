import tensorflow as tf

#Implements y = +1 for x > 0 and y = -1 for x <= 0
def sign_binarize(inp):
    h_sig = tf.clip_by_value((inp+1.)/2., 0, 1)
    with tf.get_default_graph().gradient_override_map({'Round': 'Identity'}):
        round_out = tf.round(h_sig)
    round_fin = round_out # h_sig + tf.stop_gradient(round_out - h_sig)
    return (2.*round_fin - 1.)
#    with tf.get_default_graph().gradient_override_map({'Sign': 'Identity'}):
#        return tf.sign(tf.sign(inp)+1e-8)

def bin_dense_layer(in_act, num_out, use_bias=True, bin_inp=True, training=True, name='Bin_Dense_L'):
    with tf.variable_scope(name+'_w', reuse=False):
        cont_weights = tf.get_variable('weight', [in_act.get_shape().as_list()[1], num_out], initializer=tf.contrib.layers.xavier_initializer(), trainable=training)
    clip_w = tf.clip_by_value(cont_weights, -1, 1)
    bin_w = sign_binarize(clip_w)
    bin_act = sign_binarize(in_act) if bin_inp else in_act
    #print(name+str(bin_act.shape)+' '+str(bin_w.shape))
    res = tf.matmul(bin_act, bin_w)
    with tf.variable_scope(name+'_b', reuse=False):
        res = tf.nn.bias_add(res, tf.get_variable('bias', [num_out], initializer=tf.zeros_initializer(), trainable=training)) if use_bias else res
    #tf.add_to_collection(tf.GraphKeys.ACTIVATIONS, res)
    return res
