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
from torchvision.ops import nms 
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


def ssd300vgg16_remove_background_labels(ans: Dict[str,Any]) -> Tuple[torch.tensor,np.array,torch.tensor]:
    # ans on one image
    boxes = ans['boxes'].cpu().detach() # torch tensor
    ls = np.squeeze(ans['labels'].cpu().detach().numpy())
    scores = np.squeeze(ans['scores'].cpu().detach().numpy()) 
    boxes_ = []  # 
    labels_ = [] # List[str]
    scores_ = [] # List[np.float32]
    print(ls)
    for i in range(ls.shape[0]):
        if ls[i] != conf.background_label:
            labels_.append(conf.from_category_id_to_category_name[labels_encoder.inverse_transform([ls[i]])[0]])
            boxes_.append(boxes[i].cpu().detach().numpy())
            scores_.append(scores[i])
    return torch.tensor(np.array(boxes_)).requires_grad_(False), np.array(labels_), torch.tensor(scores_).requires_grad_(False)

def list_of_tensors_to_tensor(x_):
    l_ = [x_[i].cpu().detach().numpy() for i in range(len(x_))]
    return torch.tensor(np.array(l_)).requires_grad_(False)

def multiclass_NMS(boxes,labels,scores, iou_threshold):
    # boxes, labels, scores for one image

    # GROUP BY labels
    l_group_ = {k_:{'boxes':[],'scores':[]} for k_ in list(set(labels))}

    for i in range(len(labels)):
        l_group_[labels[i]]['boxes'].append(boxes[i])
        l_group_[labels[i]]['scores'].append(scores[i])

    l_indices = {}
    for k_ in l_group_.keys():
        boxes_ = list_of_tensors_to_tensor(l_group_[k_]['boxes'])
        scores_ = list_of_tensors_to_tensor(l_group_[k_]['scores'])
        l_indices.update({k_:nms(boxes_,scores_,iou_threshold).cpu().detach().numpy()})
    o_boxes = []
    o_scores = []
    o_labels = []
    for k_ in l_indices.keys():
        indxs = l_indices[k_]
        for ind in indxs:
            o_boxes.append(l_group_[k_]['boxes'][ind])    
            o_labels.append(k_)    
            o_scores.append(l_group_[k_]['scores'][ind])    

    return list_of_tensors_to_tensor(o_boxes),o_labels,list_of_tensors_to_tensor(o_scores)

def NMS(boxes,labels,scores, iou_threshold):
    indices = nms(boxes,scores,iou_threshold).cpu().detach().numpy()
    o_boxes = []
    o_scores = []
    o_labels = []
    for i in indices:
        o_boxes.append(boxes[i])
        o_scores.append(scores[i])
        o_labels.append(labels[i])
    return list_of_tensors_to_tensor(o_boxes),o_labels,list_of_tensors_to_tensor(o_scores)

delete_content('./Print/PredictedImages')
last_img_i_ = 0
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
            boxes, labels, scores = ssd300vgg16_remove_background_labels(BatchAns[i])
            boxes_,labels_,scores_ = multiclass_NMS(boxes=boxes,labels=labels,scores=scores,iou_threshold=0.1)
            boxes_,labels_,scores_ = NMS(boxes_,labels_,scores_,iou_threshold=0.1)
            # print('number of dropped detections {}'.format(len(labels)-len(labels_)))
            # print(labels_)
            # nms_ = nms(boxes=boxes,scores=scores,iou_threshold=0.6)
            # print(ls)

            # labels=  [conf.from_category_id_to_category_name[l_] for l_ in labels_encoder.inverse_transform(ls)]
            # labels=  [conf.from_category_id_to_category_name[l_] for l_ in ls]

            # boxes = torch.unsqueeze(BatchAns[i]['boxes'][0],dim=0)
            # labels=  [str(l_) for l_ in labels_encoder.inverse_transform([BatchAns[i]['labels'][0].cpu().detach().numpy()])]
            imgwithboxes = draw_bounding_boxes(
                    image=read_image(el[0]),
                    boxes=boxes_,
                    labels=labels_,
                    colors="red",
                    # width = 4,
                    # font_size = 80,
                    font= conf.font_file_
                    )
            pil_ = to_pil_image(imgwithboxes)
            imgs_.append(pil_)
        
        # imgs_ = [InsertBoxesToNpArrayXYXY(cv2.imread(el[0],cv2.IMREAD_COLOR),
        #             boxes=BatchAns[i]['boxes'].cpu().detach().numpy()[0]) 
        #             for i,el in zip(range(len(batch)),batch)]
        plot_many_images(imgs_,OutDir='./Print/PredictedImages',start_index=last_img_i_)
        last_img_i_+=len(batch)



        
        


