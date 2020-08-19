import tensorflow as tf
import sys
import os

# Disable tensorflow compilation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf

label_lines = [line.rstrip() for line 
                    in tf.gfile.GFile("tf_files/retrained_labels.txt")]

# Unpersists graph from file
with tf.gfile.FastGFile("tf_files/retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

sess = tf.Session()
softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

def analyse(image_data):
    # Read the image_data
    # image_data = tf.gfile.FastGFile(imageObj, 'rb').read()
    # print(type(image_data))

    # Loads label file, strips off carriage return


        # Feed the image_data as input to the graph and get first prediction
        
    predictions = sess.run(softmax_tensor, \
                {'DecodeJpeg/contents:0': image_data})
    
    # Sort to show labels of first prediction in order of confidence
    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
    obj = {}
    for node_id in top_k:
        human_string = label_lines[node_id]
        score = predictions[0][node_id]
        obj[human_string] = float(score)
    # print(obj)
    
    return obj
# import cv2
# img = cv2.imread('testing.png')
# _, a_numpy = cv2.imencode('.jpg', img)
# # image = img.reshape(1, img.shape[0],img.shape[1], img.shape[2])

# print(analyse(a_numpy.tobytes()))