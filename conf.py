import os

data_folder = r'/home/user/ds_project_data/COCO2017dataset'
all_lables_location = os.path.join(data_folder,r'annotations/instances_train2017.json') 
sqlannotationsdb = os.path.join(data_folder,r'annotations.db')

all_images_folder = os.path.join(data_folder,'train2017')
BoxesLabelsByPath_filename = os.path.join(data_folder,'BoxesLablesByPath.txt') 