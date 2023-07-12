import torchvision
from torchvision import transforms
from PIL import Image

class resnet50_tr:

    tr = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(), # convert PIL imgs values from range 0 255 to range 0 1
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def transform(self, img):
        '''
        :param img: PIL image
        :return: input for resnet
        '''
        return self.tr(img)

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
