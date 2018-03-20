import tensorflow as tf
import numpy as np
from models.convolutional_model import ConvModel
from dataset import MnistDataset


epochs = 40
batch_size = 40

# Load Data from target directory
train_set = MnistDataset('kaggle_inria/train')
n_batches = len(train_set) // batch_size

# hold_prob = tf.placeholder(tf.float32)

# Construct CNN model
# model = ConvModel(resolution=[64, 64], channels=3, hold_prob=hold_prob)
model = ConvModel(resolution=[64, 64], channels=3)

# We use this to save the model. Instantiate it after all Variables have been created
saver = tf.train.Saver()

# Define tensors
label_placeholder = tf.placeholder(tf.float32, shape=[batch_size, 2])

# Define loss functions and Optimizer
loss = tf.losses.softmax_cross_entropy(label_placeholder, model.predictions)
update = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(loss)

top_predictions = tf.argmax(model.predictions, axis=1)      # probabilities -> top prediction
top_labels = tf.argmax(label_placeholder, axis=1)           # one_hot -> number
correct = tf.equal(top_predictions, top_labels)             # bool Tensor
accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))     # Average correct guesses

# TF Session
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    test_inputs = []
    for index in range(1, 41):
        test_inputs.append('kaggle_inria/validation/pedestrian/val (' + str(index) + ').jpg')
    test_inputs = [MnistDataset.read_image(input) for input in test_inputs]
    test_labels = np.ones((40,2))
    for epoch in range(1, epochs + 1):
        print('Starting epoch %d' % epoch)
        total_epoch_loss = 0

        for i in range(n_batches):
            images, labels = train_set.sample(batch_size)

            _, l, a = sess.run([update, loss, accuracy],
                               feed_dict={model.input_placeholder: images,
                                          label_placeholder: labels}) # , hold_prob: 0.5
            total_epoch_loss += l

            if i % 20 == 0:
                print('[%d / %d] Accuracy: %.2f%%     Loss: %f' % (i+1, n_batches, a*100, l))


        print('Average epoch loss: %f\n' % (total_epoch_loss / n_batches))

        _, l, a = sess.run([update, loss, accuracy],
                           feed_dict={model.input_placeholder: test_inputs,
                                      label_placeholder: test_labels})

        print('Testing Accuracy: %.2f%%\n' % (a * 100))

    digital_probabilities = tf.nn.softmax(model.predictions, name='prediction')
    # Specify the graph nodes that we want to use later
    tf.add_to_collection('model', digital_probabilities)
    # Save the entire graph and all Variables
    tf.add_to_collection('model_inputs', model.input_placeholder)
    # tf.add_to_collection('model_hold_prob', model.hold_prob)
    saver.save(sess, './saved_models/pedestrian_model.ckpt')


