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
from torchvision.utils import draw_bounding_boxes  
from torchvision.io.image import read_image
from torchvision.transforms.functional import to_pil_image
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
model.score_tresh = 0.5
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

labels_encoder = torch.load(conf.imgs_labels_encoder_filename)


def ssd300vgg16_output_to_human_format(ans):
    # ans on one image
    boxes = ans['boxes'].cpu().detach() # torch tensor
    ls = np.squeeze(ans['labels'].cpu().detach().numpy())
    scores = np.squeeze(ans['scores'].cpu().detach().numpy()) 
    h_boxes = []  # 
    h_labels = [] # List[str]
    h_scores = [] # List[np.float32]
    for i in range(len(ls)):
        if ls[i] != conf.background_label:
            h_labels.append(conf.from_category_id_to_category_name[labels_encoder.inverse_transform([ls[i]])[0]])
            h_boxes.append(boxes[i].cpu().detach().numpy())
            h_scores.append(scores[i])
    return torch.tensor(np.array(h_boxes)).requires_grad_(False), h_labels, h_scores

with torch.no_grad():
    for b_i,batch in zip(range(len(BathcesOfPairs)),BathcesOfPairs):
        # GET batch
        # tagret: List[Dict['boxes','labels']]
        # input to model : List[image tensor]
        imgs = [imgbyURL[el[0]].to(device) for el in batch]
        targets = [TargetDict_to_model_input(el[1]) for el in batch]
        
        # GET boxes,lables,scores on batch
        BatchAns = model(imgs)



        imgs_= []
        for i,el in zip(range(len(batch)),batch):
            fp_ = el[0]
            img = read_image(el[0])
            boxes, labels, scores = ssd300vgg16_output_to_human_format(BatchAns[i])
            Print(BatchAns[i])
            Print(boxes)
            Print(labels)
            Print(scores)
            # print(ls)

            # labels=  [conf.from_category_id_to_category_name[l_] for l_ in labels_encoder.inverse_transform(ls)]
            # labels=  [conf.from_category_id_to_category_name[l_] for l_ in ls]

            # boxes = torch.unsqueeze(BatchAns[i]['boxes'][0],dim=0)
            # labels=  [str(l_) for l_ in labels_encoder.inverse_transform([BatchAns[i]['labels'][0].cpu().detach().numpy()])]
            imgwithboxes = draw_bounding_boxes(
                    image=read_image(el[0]),
                    boxes=boxes,
                    labels=labels,
                    colors="red",
                    # width = 4,
                    # font_size = 80
                    )
            pil_ = to_pil_image(imgwithboxes)
            imgs_.append(pil_)
            break
        
        # imgs_ = [InsertBoxesToNpArrayXYXY(cv2.imread(el[0],cv2.IMREAD_COLOR),
        #             boxes=BatchAns[i]['boxes'].cpu().detach().numpy()[0]) 
        #             for i,el in zip(range(len(batch)),batch)]
        plot_many_images(imgs_,OutDir='./Print/PredictedImages')
        raise SystemExit
        boxes
        print(1)



        
        


