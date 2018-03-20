import tensorflow as tf


class ConvModel:

    def __init__(self, resolution, channels):
        self.input_placeholder = tf.placeholder(tf.float32, shape=[None] + resolution + [channels],
                                                name='image')

        x = tf.layers.conv2d(inputs=self.input_placeholder,
                             filters=32,
                             padding='same',
                             kernel_size=5) # 64

        x = tf.layers.max_pooling2d(inputs=x,
                                    pool_size=2,
                                    strides=2)   # 32
        # ==================================================

        x = tf.layers.conv2d(inputs=x,
                             filters=64,
                             padding='same',
                             kernel_size=5)

        x = tf.layers.max_pooling2d(inputs=x,
                                    pool_size=2,
                                    strides=2)  # 16
        # ===================================================

        x = tf.layers.conv2d(inputs=x,
                             filters=128,
                             padding='same',
                             kernel_size=4)

        '''x = tf.layers.conv2d(inputs=x,
                             filters=128,
                             padding='same',
                             kernel_size=4)'''

        x = tf.layers.max_pooling2d(inputs=x,
                                    pool_size=2,
                                    strides=2)  # 8
        # ===================================================

        x = tf.layers.conv2d(inputs=x,
                             filters=256,
                             padding='same',
                             kernel_size=4)

        '''x = tf.layers.conv2d(inputs=x,
                             filters=256,
                             padding='same',
                             kernel_size=4)'''

        x = tf.layers.max_pooling2d(inputs=x,
                                    pool_size=2,
                                    strides=2)  # 4

        # ===================================================
        x = tf.reshape(x, shape=[-1, x.shape[1]*x.shape[2]*x.shape[3]])

        x = tf.layers.dense(inputs=x,
                            units=2048,
                            activation=tf.nn.relu)

        x = tf.layers.dense(inputs=x,
                            units=2)

        self.predictions = x
