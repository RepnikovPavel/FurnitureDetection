import conf
from UI.LOG import *
import cv2
from aml.train_pipeline import *  
from aml.train_pipeline import *
 

import os
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor,FasterRCNN_ResNet50_FPN_Weights
from torchinfo import summary

# from torchvision.models.detection import ssd300_vgg16,SSD300_VGG16_Weights
from torchvision.models.detection.ssd import SSDClassificationHead,SSD300_VGG16_Weights,det_utils
from torchvision.models.detection import ssd300_vgg16

import torch

import aml.model_using as model_using
import aml.support_func as support_func
import aml.time_mesuarment as time_mesuarment
import sys

import aml.managers as managers
import aml.img_processing as img_processing
import random
import numpy as np
import pprint
from torchinfo import summary
from aml.img_processing import *

from PIL import Image
import aml.models as models
import matplotlib.pyplot as plt
import data_manip as dm
from pprint import pprint as Print
from PIL import Image
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

BoxLabelByImgURL = torch.load(conf.BoxesLabelsByPath_filename)

device = 'cuda'

# models_manager = managers.ModelsManager()
# model = ssd300_vgg16(weights=SSD300_VGG16_Weights.DEFAULT)

# num_anchors = model.anchor_generator.num_anchors_per_location()
# # channels_to_classification_head = det_utils.retrieve_out_channels(model.backbone,size=(333,1024))
# # the backbone must be FCN to avoid ...
# # input image must be \geq \approx 300 \times 300 and aspet ratio and h,w doesnt make sense
# channels_to_classification_head = det_utils.retrieve_out_channels(model.backbone,size=(300,300))
# model.head.classification_head = SSDClassificationHead(in_channels=channels_to_classification_head,
#                                                        num_anchors=num_anchors,
#                                                        num_classes=3)

model = torch.load(conf.ssd300_vgg16_save_path)
model.to(device)
model.eval()

DatasetIterator = DictToListOfPairs(BoxLabelByImgURL)
URL_of_image_to_model_input = lambda fp_: IMGtoSSD300_VGG16(cv2.imread(fp_,cv2.IMREAD_COLOR))
TargetDict_to_model_input = lambda dict_: {
        'boxes':NPtoTensorGradFalse(xywh_to_xyxy(np.array(dict_['boxes']))).to(device),
        'labels':NPtoTensorGradFalse(np.array(dict_['labels'])).to(device)
    }

BATCH_SIZE = 32
GetPairsSplittedIntoBathces = lambda DatasetIterator: [batch_ for batch_ in  BatchMaker(DatasetIterator,BATCH_SIZE)] 
imgbyURL = {URL:URL_of_image_to_model_input(URL) for URL in BoxLabelByImgURL.keys()}



np.random.shuffle(DatasetIterator)
BathcesOfPairs = GetPairsSplittedIntoBathces(DatasetIterator)

for b_i,batch in zip(range(len(BathcesOfPairs)),BathcesOfPairs):
    # GET batch
    # tagret: List[Dict['boxes','labels']]
    # input to model : List[image tensor]
    imgs = [imgbyURL[el[0]].to(device) for el in batch]
    targets = [TargetDict_to_model_input(el[1]) for el in batch]
    
    # GET loss on batch
    BatchAns = model(imgs)

    imgs_ = [InsertBoxesToNpArrayXYXY(cv2.imread(el[0],cv2.IMREAD_COLOR),
                boxes=BatchAns[i]['boxes'].cpu().detach().numpy()) 
                for i,el in zip(range(len(batch)),batch)]
    plot_many_images(imgs_,OutDir='./Print/PredictedImages')
    raise SystemExit
    boxes
    print(1)



        
        


