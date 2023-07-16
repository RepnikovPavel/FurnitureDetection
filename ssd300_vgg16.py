import conf
from UI.LOG import *
import cv2
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

models_manager = managers.ModelsManager()
model = ssd300_vgg16(weights=SSD300_VGG16_Weights.DEFAULT)

num_anchors = model.anchor_generator.num_anchors_per_location()
# channels_to_classification_head = det_utils.retrieve_out_channels(model.backbone,size=(333,1024))
# the backbone must be FCN to avoid ...
# input image must be \geq \approx 300 \times 300 and aspet ratio and h,w doesnt make sense
channels_to_classification_head = det_utils.retrieve_out_channels(model.backbone,size=(300,300))
model.head.classification_head = SSDClassificationHead(in_channels=channels_to_classification_head,
                                                       num_anchors=num_anchors,
                                                       num_classes=3)


model.to(device)
model.train()

params = [p for p in model.parameters() if p.requires_grad]

# https://arxiv.org/pdf/1512.02325.pdf p.7
optimizer = torch.optim.SGD(params, lr=0.001,
                            momentum=0.9, weight_decay=0.0005)

DatasetIterator = DictToListOfPairs(BoxLabelByImgURL)
URL_of_image_to_model_input = lambda fp_: IMGtoSSD300_VGG16(cv2.imread(fp_,cv2.IMREAD_COLOR),device)
TargetDict_to_model_input = lambda dict_: {
        'boxes':NPtoTensorGradFalse(xywh_to_xyxy(np.array(dict_['boxes']))).to(device),
        'labels':NPtoTensorGradFalse(np.array(dict_['labels'])).to(device)
    }
criterion = lambda classification_loss, regression_loss: classification_loss+regression_loss

get_estimate_exec_time = lambda time_of_one_batch, index_of_batch,index_of_ep,NumOfBatches, num_of_EPOCHS: 'time left '+format((time_of_one_batch*(index_of_batch+1) + time_of_one_batch*NumOfBatches*index_of_ep)/3600,'.1E')+'h '+'total time '+format((time_of_one_batch*NumOfBatches*num_of_EPOCHS)/3600,'.1E')+'h' 

sprintf_loss = lambda torchvalue,ep_index,ep_index_max,BatchIndex,BatchIndexMax: str((
    'loss', format(torchvalue.cpu().detach().numpy(),'.1E'),
    'ep_progress','{}/{}'.format(ep_index,ep_index_max),str(np.round((ep_index)/(ep_index_max)*100,0))[:3]+'%',
    'batches_progress','{}/{}'.format(BatchIndex,BatchIndexMax), str(np.round((BatchIndex)/(BatchIndexMax)*100,0))[:3]+ '%'
    ))


BATCH_SIZE = 32
GetPairsSplittedIntoBathces = lambda DatasetIterator: [batch_ for batch_ in  batch(DatasetIterator,BATCH_SIZE)] 

EPOCH = 50 
timer = time_mesuarment.Timer()
for ep in range(EPOCH):
    np.random.shuffle(DatasetIterator)
    BathcesOfPairs = GetPairsSplittedIntoBathces(DatasetIterator)
    for b_i,batch in zip(range(len(BathcesOfPairs)),BathcesOfPairs):
        timer.start()
        optimizer.zero_grad()
        # GET batch
        # tagret: List[Dict['boxes','labels']]
        # input to model : List[image tensor]
        imgs = [URL_of_image_to_model_input(el[0]) for el in batch]
        targets = [TargetDict_to_model_input(el[1]) for el in batch]
        
        # GET loss on batch
        dict_ = model(imgs,targets)
        loss = criterion(dict_['bbox_regression'],dict_['classification'])

        # GRADIEN STEP
        loss.backward()
        optimizer.step()

        timer.stop()
        # CONSOLE_LOGGING
        if ((b_i+1))%10==0:
            print('\n')
        print('\r'+stack_str(
            sprintf_loss(loss,ep,EPOCH-1,b_i,len(BathcesOfPairs)-1),' ',
            get_estimate_exec_time(timer.get_execution_time(),b_i,ep,len(BathcesOfPairs),EPOCH)),
            end= '')
    torch.save(model,conf.ssd300_vgg16_save_path)    


        
        


