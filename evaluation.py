import tensorflow as tf
from dataset import MnistDataset
from scipy.misc import imread
import numpy as np

with tf.Session() as sess:
    saver = tf.train.import_meta_graph('saved_models/model.ckpt.meta')      # Don't have to recreate the entire graph
    saver.restore(sess, 'saved_models/model.ckpt')                          # Restore all graph variables

    model = tf.get_collection('model')[0]
    inputs = tf.get_collection('model_inputs')[0]

    test_inputs = []
    for index in range(1, 177):
        test_inputs.append('kaggle_inria/validation/pedestrian/val (' + str(index) + ').jpg')
    #test_inputs = ['pedestriankaggle/validation/no pedestrian/val (2).jpg']
    #test_inputs = [MnistDataset.read_image(input) for input in test_inputs]

    test_inputs = [MnistDataset.read_image(input) for input in test_inputs]

    predictions = sess.run(model,
                           feed_dict={inputs: test_inputs})

    labels = np.ones(176)
    matches = tf.equal(np.argmax(predictions, 1), labels)

    acc = tf.reduce_mean(tf.cast(matches, tf.float32))

    print(np.argmax(predictions, 1))
    print(sess.run(acc))
    #print (predictions)
    #print(np.argmax(predictions, 1))
