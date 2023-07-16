import os

data_folder = r'/home/user/ds_project_data/COCO2017dataset'
all_lables_location = os.path.join(data_folder,r'annotations/instances_train2017.json') 
sqlannotationsdb = os.path.join(data_folder,r'annotations.db')

all_images_folder = os.path.join(data_folder,'train2017')
BoxesLabelsByPath_filename = os.path.join(data_folder,'BoxesLablesByPath.txt') 
imgs_labels_encoder_filename = os.path.join(data_folder,'imgs_labels_encoder_filename.txt')

base_row_data_path = os.path.join(data_folder, 'row_images')
base_algs_path = os.path.join(data_folder, 'models')
models_for_img_base_path = os.path.join(base_algs_path, 'models_for_imgs')


img_models = {
    'resnet152v1':
        {
            'pytorch_model_name': 'resnet152',
            'start_weights': 'IMAGENET1K_V2',
            'repo': 'pytorch/vision:v0.13.1',
            'local_path': os.path.join(models_for_img_base_path, 'resnet152'),
            'filename': 'model.txt'
        },
    'resnet50v1':
        {
            'pytorch_model_name': 'resnet50',
            'start_weights': 'IMAGENET1K_V2',
            'repo': 'pytorch/vision:v0.13.1',
            'local_path': os.path.join(models_for_img_base_path, 'resnet50'),
            'filename': 'model.txt',
            'cache_dir': os.path.join(models_for_img_base_path, 'resnet50cache')
        },
    # 'fasterrcnn_resnet50_fpn':
    #     {
    #         'pytorch_model_name': 'fasterrcnn_resnet50_fpn',
    #         'start_weights': 'DEFAULT',
    #         'repo': 'pytorch/vision:v0.13.1',
    #         'local_path': os.path.join(models_for_img_base_path, 'fasterrcnn_resnet50_fpn'),
    #         'filename': 'model.txt',
    #         'cache_dir': os.path.join(models_for_img_base_path, 'fasterrcnn_resnet50_fpn_cache')
    #     }
    
}
