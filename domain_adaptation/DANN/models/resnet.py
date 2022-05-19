from torchvision import models
import torch
import torch.nn.functional as F
import torch.nn as nn
from torch.autograd import Function, Variable
from utils import ReverseLayerF


class ResBase(nn.Module):
    def __init__(self, option='resnet50', pret=False, num_classes=1000):
        super(ResBase, self).__init__()
        self.dim = 2048
        if option == 'resnet18':
            model_ft = models.resnet18(pretrained=pret)
            self.dim = 512
        if option == 'resnet34':
            model_ft = models.resnet34(pretrained=pret)
            self.dim = 512
        if option == 'resnet50':
            model_ft = models.resnet50(pretrained=pret)
        if option == 'resnet101':
            model_ft = models.resnet101(pretrained=pret)
        if option == 'resnet152':
            model_ft = models.resnet152(pretrained=pret)
            
        self.fc = nn.Linear(self.dim, num_classes)
        mod = list(model_ft.children())
        mod.pop()
        self.features = nn.Sequential(*mod)
        
        self.domain_fc = nn.Linear(self.dim, 2)

    def forward(self, x, alpha):
        x = self.features(x)
        x = x.view(x.size(0), self.dim)
        y1 = self.fc(x)
        y2 = ReverseLayerF.apply(x, alpha)
        y2 = self.domain_fc(y2)
        
        return y1, y2
        
        
