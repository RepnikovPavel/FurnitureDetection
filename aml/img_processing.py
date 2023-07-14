import torchvision
from torchvision import transforms
from PIL import Image
import numpy as np
from pprint import pprint as Print
import torch
import matplotlib.pyplot as plt
from matplotlib import colors
class ImageHandler:
    img_to_resnet_preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(), # convert PIL imgs values from range 0 255 to range 0 1
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
    
    def RGBToResNet(self, img):
        return self.img_to_resnet_preprocess(img)


def PILToRGB(img):
    return img.convert('RGB') 
    # if img.mode != 'RGB':
    #     w, h = img.size
    #     ima = Image.new('RGB', (w,h))
    #     data = zip(img.getdata(), img.getdata(), img.getdata())
    #     ima.putdata(list(data))
    #     return img.convert('RGB')
    # else:
    #     return img


def InsertBoxesToNpArrayXYWH(img:np.array, boxes: np.array) -> np.array:
    # Box [x,y,w,h] x is top left, y is top left. left-handed coordinate system
    Boxes = np.array(np.floor(boxes),dtype=np.intc)
    # Img [3,w,h]
    Img = np.array(img)
    for box in Boxes:
        x,y,w,h = box
        for i in range(3):
            Img[i,x:x+w,y] = 0
            Img[i,x:x+w,y+h] =0
            Img[i,x,y:y+h] =0
            Img[i,x+w,y:y+h] =0
    return Img

def InsertBoxesToNpArrayXYXY(img:np.array, boxes: np.array) -> np.array:
    # Box [x_tl,y_tl,x_dr,y_dr] x is top left, y is top left. left-handed coordinate system
    Boxes = np.array(np.floor(boxes),dtype=np.intc)
    # Img [3,w,h]
    Img = np.array(img)
    shape = Img.shape
    w= shape[1]
    h= shape[2]
    vals = np.linspace(0,1,len(boxes))
    np.random.shuffle(vals)
    cmap = plt.cm.colors.ListedColormap(plt.cm.jet(vals))
    i_ = 0
    for box in Boxes:
        # xtl,ytl,xdr,ydr = box
        ytl,xtl,ydr,xdr = box
        xtl = np.maximum(xtl,0)
        xdr = np.minimum(xdr,w-1)
        ytl = np.minimum(0,ytl)
        ydr = np.minimum(ydr,h-1)
        color = np.array(np.floor(np.array(colors.to_rgb(cmap(i_)),dtype=np.float32)*255.0),dtype=np.uint8)
        for i in range(3):
            channel_color = color[i]
            Img[i,xtl:xdr,ytl] = channel_color
            Img[i,xtl:xdr,ydr] = channel_color
            Img[i,xtl,ytl:ydr] = channel_color
            Img[i,xdr,ytl:ydr] = channel_color
        i_ +=1 
    return Img

def NPtoTensorGradFalse(arr:np.array):
    return torch.tensor(arr).requires_grad_(False)

def Norm(tensor_):
    return transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])(tensor_)

def xywh_to_xyxy(xywh:np.array):
    # input     x,y,w,h
    # output    x,y,x+w,y+h
    shape = xywh.shape
    xyxy = np.zeros(shape=shape,dtype=xywh.dtype)
    if len(shape)==1:
        xyxy[0] = xywh[0] 
        xyxy[1] = xywh[1]
        xyxy[2] = xywh[0] + xywh[2]
        xyxy[3] = xywh[1] + xywh[3]
    else:
        for i in range(shape[0]):
            xyxy[i][0] = xywh[i][0] 
            xyxy[i][1] = xywh[i][1]
            xyxy[i][2] = xywh[i][0] + xywh[i][2]
            xyxy[i][3] = xywh[i][1] + xywh[i][3]
    return xyxy

