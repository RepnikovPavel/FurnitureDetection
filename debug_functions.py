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
from aml.img_processing import InsertBoxesToNpArray,PILToRGB,NPtoTensorGradFalse,Norm,xywh_to_xyxy

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


imgs = []
targets = []
for fp_ in BoxLabelByImgURL.keys():
    BoxLabel= BoxLabelByImgURL[fp_]
    # Print(BoxLabel)
    imgs.append(Norm(NPtoTensorGradFalse(np.transpose(np.array(PILToRGB(Image.open(fp_)),dtype=np.float32)))))
    targets.append({
        'boxes':NPtoTensorGradFalse(xywh_to_xyxy(np.array(BoxLabel['bboxes']))),
        'labels':NPtoTensorGradFalse(np.array(BoxLabel['labels']))
    })
    break