import torchvision
from torchvision import transforms
from PIL import Image
import numpy as np
from pprint import pprint as Print

class ImageHandler:
    img_to_resnet_preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(), # convert PIL imgs values from range 0 255 to range 0 1
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
    
    def ToRGB(self,img):
        return img.convert('RGB') 
        # if img.mode != 'RGB':
        #     w, h = img.size
        #     ima = Image.new('RGB', (w,h))
        #     data = zip(img.getdata(), img.getdata(), img.getdata())
        #     ima.putdata(list(data))
        #     return img.convert('RGB')
        # else:
        #     return img


    def RGBToResNet(self, img):
        return self.img_to_resnet_preprocess(img)

def InsertBoxesToNpArray(img:np.array, boxes: np.array) -> np.array:
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
