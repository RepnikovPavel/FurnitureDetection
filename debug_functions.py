import conf

import os
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor,FasterRCNN_ResNet50_FPN_Weights
from torchinfo import summary

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


BoxLabelByImgURL = torch.load(conf.BoxesLabelsByPath_filename)
# # bbox = [x,y,w,h]
# keys_ = BoxLabelByImgURL.keys()
# BoxLabel = 0
# Img_ = 0
# for key_ in keys_:
#     BoxLabel = BoxLabelByImgURL[key_]
#     imgURL = key_
#     Img_= np.transpose(np.array(Image.open(imgURL)))
#     break
# Print(BoxLabel)
# ImgWithBox_ = Img_
# Print(Img_.shape)
# plt.imshow(np.transpose(InsertBoxesToNpArray(Img_,BoxLabel['bboxes'])))
# plt.show()

device = 'cuda'
imgs = []
targets = []
fps = []
i_ =0
for fp_ in BoxLabelByImgURL.keys():
    BoxLabel= BoxLabelByImgURL[fp_]
    fps.append(fp_)
    # Print(BoxLabel)
    npimage= np.transpose(np.array(PILToRGB(Image.open(fp_)),dtype=np.float32))
    imgs.append(Norm(NPtoTensorGradFalse(npimage)).to(device))
    targets.append({
        'boxes':NPtoTensorGradFalse(xywh_to_xyxy(np.array(BoxLabel['bboxes']))).to(device),
        'labels':NPtoTensorGradFalse(np.array(BoxLabel['labels'])).to(device)
    })
    i_+=1
    if i_ >=10:
        break


models_manager = managers.ModelsManager()
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights=FasterRCNN_ResNet50_FPN_Weights.COCO_V1)
num_classes = 81 # 80 classes + background
in_features = model.roi_heads.box_predictor.cls_score.in_features
model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
model.to(device)
model.eval()
with torch.no_grad():
    print('before')
    out = [model([imgs[i]],[targets[i]])[0] for i in range(len(imgs))]
    print(out)
    # Print(torch.hub.list('pytorch/vision:v0.13.1'))
    # Print(out)

    npimages = []
    for i in range(len(out)):
        predicted_boxes = out[i]['boxes'].cpu().detach().numpy()
        img = np.array(PILToRGB(Image.open(fps[i])))
        npimage = np.transpose(img)
        for j in range(len(predicted_boxes)):
            npimage = InsertBoxesToNpArrayXYXY(npimage,boxes = predicted_boxes)
        
        npimages.append(np.transpose(npimage))
    plot_many_images(npimages,5,2,OutDir='./Print/PredictedImages')

    # Print(predicted_boxes)
    # npimage = InsertBoxesToNpArrayXYXY(npimage,boxes = predicted_boxes)
    # plt.imshow(np.transpose(npimage))
    # plt.show()
