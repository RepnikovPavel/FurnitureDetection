import torchvision
from torchvision import transforms
from PIL import Image
import numpy as np
from pprint import pprint as Print
import torch
import matplotlib.pyplot as plt
from matplotlib import colors
import os,shutil
import cv2
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
    # Img [h,w,c]
    Img = np.array(img)
    shape = Img.shape
    h= shape[0]
    w= shape[1]
    vals = np.linspace(0,1,len(boxes))
    np.random.shuffle(vals)
    cmap = plt.cm.colors.ListedColormap(plt.cm.jet(vals))
    i_ = 0
    if len(Boxes.shape)==1:
        xtl,ytl,xdr,ydr = Boxes
        # ytl,xtl,ydr,xdr = box
        if ((xtl<0 or xtl>=w) or
            (xdr<0 or xdr>=w) or
            (ytl<0 or ytl>=h) or
            (ydr<0 or ydr>=h)):
            print('box is outside the permitted area')
            return Img 
        xtl = np.maximum(xtl,0)
        xdr = np.minimum(xdr,w-1)
        ytl = np.minimum(0,ytl)
        ydr = np.minimum(ydr,h-1)
        color = np.array(np.floor(np.array(colors.to_rgb(cmap(i_)),dtype=np.float32)*255.0),dtype=np.uint8)
        for i in range(3):
            channel_color = color[i]
            Img[ytl,xtl:xdr,i] = channel_color
            Img[ydr,xtl:xdr,i] = channel_color
            Img[ytl:ydr,xtl,i] = channel_color
            Img[ytl:ydr,xdr,i] = channel_color
        i_ +=1 
    else:
        for box in Boxes:
            xtl,ytl,xdr,ydr = box
            # ytl,xtl,ydr,xdr = box
            if ((xtl<0 or xtl>=w) or
                (xdr<0 or xdr>=w) or
                (ytl<0 or ytl>=h) or
                (ydr<0 or ydr>=h)):
                print('box is outside the permitted area')
                continue 
            xtl = np.maximum(xtl,0)
            xdr = np.minimum(xdr,w-1)
            ytl = np.minimum(0,ytl)
            ydr = np.minimum(ydr,h-1)
            color = np.array(np.floor(np.array(colors.to_rgb(cmap(i_)),dtype=np.float32)*255.0),dtype=np.uint8)
            for i in range(3):
                channel_color = color[i]
                Img[ytl,xtl:xdr,i] = channel_color
                Img[ydr,xtl:xdr,i] = channel_color
                Img[ytl:ydr,xtl,i] = channel_color
                Img[ytl:ydr,xdr,i] = channel_color
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


img_to_resnet_preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(), # convert PIL imgs values from range 0 255 to range 0 1
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

def IMGtoSSD300_VGG16(img:np.array)->torch.tensor:
    (h,w,c)= img.shape
    # cv2.imshow('image',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    img_= transforms.ToTensor()(img)
    # (h,w)
    img_= transforms.Resize((np.maximum(300, h),np.maximum(300, w)))(img_)
    img_ = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])(img_)    
    return img_.requires_grad_(False)


img0_html = '''
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge" />
		<meta
			name="viewport"
			content="width=device-width, initial-scale=1.0"
		/>
		<title>Viewer.js</title>

		<script
			src="https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.10.5/viewer.min.js"
			integrity="sha512-i5q29evO2Z4FHGCO+d5VLrwgre/l+vaud5qsVqQbPXvHmD9obORDrPIGFpP2+ep+HY+z41kAmVFRHqQAjSROmA=="
			crossorigin="anonymous"
			referrerpolicy="no-referrer"
		></script>
		<link
			rel="stylesheet"
			href="https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.10.5/viewer.css"
			integrity="sha512-c7kgo7PyRiLnl7mPdTDaH0dUhJMpij4aXRMOHmXaFCu96jInpKc8sZ2U6lby3+mOpLSSlAndRtH6dIonO9qVEQ=="
			crossorigin="anonymous"
			referrerpolicy="no-referrer"
		/>
	</head>
    <body>
        <div id="gallery">
            <ul class="images">

'''
img1_html = '''
            </ul>
        </div>
        <!-- <script src="./index.js"></script> -->
    </body>
</html>

'''

def delete_content(dir:str):
    if os.path.exists(dir):
        elements_of_dir = [os.path.join(dir,el) for el in os.listdir(dir)]
        for el in elements_of_dir:
            try:
                if os.path.isfile(el) or os.path.islink(el):
                    os.unlink(el)
                elif os.path.isdir(el):
                    shutil.rmtree(el)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (el, e))

def plot_many_images(imgs:np.array,OutDir:str, start_index: int)->None:
    # m - number of images along the matrix row index
    # n - number of images along the matrix column index
    if not os.path.exists(OutDir):
        os.makedirs(OutDir)
    im2 = ''
    # toimg = transforms.ToPILImage()
    for i in range(len(imgs)):
        # npim = imgs[i].astype(np.uint8)
        # img = cv2.merge((npim[1],npim[0],npim[2]))
        # im = toimg(npim)
        # im = Image.fromarray(npim,'RGB')
        im2+='''
                <li>
                    <img src="{}.png" alt="pink background" />
                </li>'''.format(i)
        imgs[i].save(os.path.join(OutDir,'{}.png'.format(start_index+i)))
        # cv2.imwrite(os.path.join(OutDir,'{}.png'.format(i)),imgs[i])
    # with open(os.path.join(OutDir,'index.html'),'w') as f:
    #     f.write(img0_html+im2+img1_html)
    # os.system('google-chrome {}'.format(os.path.join(OutDir,'index.html')))

    # fig,axs = plt.subplots(nrows=m, ncols=n)
    # for k in range(m*n):
    #     print(k)
    #     i = k//n
    #     j = np.mod(k,n)
    #     axs[i][j].imshow(imgs[k])



