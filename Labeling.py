import os
import aml.config as config
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


from PIL import Image

import aml.models as models


if __name__ == '__main__':
    timer = time_mesuarment.Timer()
    timer.start()

    pretrained_model = config.img_models['resnet152v1']
    test_image_path = os.path.join(config.base_row_data_path, 'img0.png')


    models_manager = managers.ModelsManager()
    pr_resnet_ = models_manager.load_model(description_of_the_model=pretrained_model,
                                      reload_from_internet=False)

    model = models.ModelBuilder.create_sequential(resnet_=pr_resnet_)

    embeddings = []

    # pprint.pprint(summary(model))
    # print(model)

    model_controller = model_using.ModelController(model=model)
    gpu_device = torch.device('cuda', index=0)
    cpu_device = torch.device('cpu', index=0)

    image_handler = img_processing.ImageHandler()
    img = Image.open(test_image_path)
    preprocessed_img_as_tensor = image_handler.RGBToResNet(image_handler.ToRGB(img))

    X_batch = [preprocessed_img_as_tensor]
    model_controller.eval_model_on_the_list_of_elements(input_storage=X_batch,
                                                        output_storage=embeddings,
                                                        output_storage_device=cpu_device,
                                                        run_on_device=gpu_device,
                                                        batch_size=1000)
    pprint.pprint(embeddings)

    timer.stop()
    timer.print_execution_time()
