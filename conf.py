import os

data_folder = r'/home/user/ds_project_data'
all_lables_location = os.path.join(r'/home/user/UnityProjects/MakeDataset/Assets/DATASET/ANNOTATIONS/annotations.json') 
sqlannotationsdb = os.path.join(data_folder,r'annotations.db')


real_images_folder = os.path.join(data_folder,r'REAL_IMAGES')
all_images_folder = os.path.join(r'/home/user/UnityProjects/MakeDataset/Assets/DATASET/IMAGES')
font_file_ = r'/usr/share/fonts/fonts-go/Go-Bold-Italic.ttf'

BoxesLabelsByPath_filename = os.path.join(data_folder,'BoxesLablesByPath.txt') 
imgs_labels_encoder_filename = os.path.join(data_folder,'imgs_labels_encoder_filename.txt')

train_logging_folder = os.path.join(data_folder,'train_log')
ssd300_vgg16_save_path = os.path.join(data_folder,'ssd300_vgg16.txt')


base_row_data_path = os.path.join(data_folder, 'row_images')
base_algs_path = os.path.join(data_folder, 'models')
models_for_img_base_path = os.path.join(base_algs_path, 'models_for_imgs')

# Categories.Add("stool",0);
# Categories.Add("chair",1);
# Categories.Add("sofa",2);
# Categories.Add("bench",3);
# Categories.Add("bed",4);
# Categories.Add("TV",5);
# Categories.Add("table",6);
# Categories.Add("wardrobe",7);
# Categories.Add("storage",8);
# Categories.Add("refrigerator",9);
# Categories.Add("microwave",10);

from_category_id_to_category_name = {
    0:"stool",
    1:"chair",
    2:"sofa",
    3:"bench",
    4:"bed",
    5:"TV",
    6:"table",
    7:"wardrobe",
    8:"storage",
    9:"refrigerator",
    10:"microwave",
}
background_label = len(from_category_id_to_category_name)

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
