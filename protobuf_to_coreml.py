import tfcoreml

# To go from protobuf -> CoreML model, just call
# a function and specify the inputs/outputs

coreml_model = tfcoreml.convert(
    tf_model_path='pedestrian_model.pb',
    mlmodel_path='kaggleInria_128.mlmodel',
    input_name_shape_dict={'image:0': [1, 128, 128, 3]},
    #input_name_shape_dict={'image:0': [1, 12288]},
    output_feature_names=['prediction:0'],
    image_input_names=['image:0'],
    # class_labels=['Daisy', 'Rose', 'Tulip', 'Dandelion', 'Sun Flower']
    class_labels=['No Pedestrian', 'Pedestrian']
    )

