import torch
import torch.nn as nn
from torchsummary import summary
from typing import Any

class ModelBuilder:
    @staticmethod
    def create_sequential(resnet_):
        # all layers
        # https://pytorch.org/docs/stable/nn.html
        layer1 = nn.Sequential(
            nn.Linear(1000, 512),
            nn.LeakyReLU(negative_slope=0.3),
            nn.BatchNorm1d(512),
            nn.Dropout(p=0.3)
        )
        layer2 = nn.Sequential(
            nn.Linear(512, 256),
            nn.LeakyReLU(negative_slope=0.3),
            nn.BatchNorm1d(256),
            nn.Dropout(p=0.3)
        )
        layer3 = nn.Sequential(
            nn.Linear(256, 128),
            nn.LeakyReLU(negative_slope=0.3),
            nn.BatchNorm1d(128)
        )
        layer4 = nn.Sequential(
            nn.Linear(128, 2),
            nn.LeakyReLU(negative_slope=0.3),
            nn.BatchNorm1d(2)
        )
        layer5 = nn.Sequential(
            nn.Softmax(1)
        )
        sequence = nn.Sequential(
            resnet_,
            layer1,
            layer2,
            layer3,
            layer4,
            layer5
        )
        return sequence

