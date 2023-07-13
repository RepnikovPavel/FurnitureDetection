import os
import torchvision
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
from aml.img_processing import InsertBoxesToNpArray

from PIL import Image
import aml.models as models
import matplotlib.pyplot as plt
import data_manip as dm
from pprint import pprint as Print
from PIL import Image
import conf

BoxLabelByImgURL = torch.load(conf.BoxesLabelsByPath_filename)
# bbox = [x,y,w,h]
keys_ = BoxLabelByImgURL.keys()
BoxLabel = 0
Img_ = 0
for key_ in keys_:
    BoxLabel = BoxLabelByImgURL[key_]
    imgURL = key_
    Img_= np.transpose(np.array(Image.open(imgURL)))
    break
Print(BoxLabel)
ImgWithBox_ = Img_
Print(Img_.shape)
plt.imshow(np.transpose(InsertBoxesToNpArray(Img_,BoxLabel['bboxes'])))
plt.show()