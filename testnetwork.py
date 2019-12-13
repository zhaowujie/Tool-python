import argparse
import torch
import random
import cv2
import os
import numpy as np
import torch.nn as nn
# import tensorwatch as tw
from torchviz import make_dot
import logging
from modeling.baseline import Baseline

#   pytorch1.1
#   tensorboardX    1.8
#   

version = float(torch.__version__[0:3])
logger = logging.getLogger('base')
if version >= 1.1:  # PyTorch 1.1
    from torch.utils.tensorboard import SummaryWriter
    tb_logger = SummaryWriter(log_dir='../tb_logger/')
else:
    logger.info('You are using PyTorch {}. Tensorboard will use [tensorboardX]')
    from tensorboardX import SummaryWriter
    tb_logger = SummaryWriter(log_dir='../tb_logger/')
from tensorboardX import SummaryWriter






cuda = False

# -------------testnet----------------------------------
x = torch.rand(2, 3, 128, 128)
model = Baseline(54,  last_stride=1, model_path=None, neck='bnneck', neck_feat='after', model_name='se_resnext50', pretrain_choice=False)

if cuda:
    device = torch.device('cuda')
    # x.to(device)
    x = x.cuda()
    model.to(device)
with SummaryWriter(comment='se_resnext50') as w:
    w.add_graph(model, x)
# out = model(x)
# g = make_dot(out)
# g.render('espnet_model', view=False)
# print(out.shape)
# fishnet = fishnet()print(fishnet)
# -------------testnet----------------------------------



print('iiii')