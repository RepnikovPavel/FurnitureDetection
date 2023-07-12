import os
problem_folder = '/home/user/ds_project_data/'
base_row_data_path = os.path.join(problem_folder, 'row_images')
base_algs_path = os.path.join(problem_folder, 'models')
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
        }
}
