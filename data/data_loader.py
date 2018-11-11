import sys

import torchvision.transforms as transforms
from torch.utils.data import DataLoader

sys.path.append('../')
from util.cfg import cfg
from data.datasets import EyeDiseaseDataset

data_transforms = {
    'train': transforms.Compose([
        transforms.Resize(227),
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.ColorJitter(),
        transforms.RandomRotation(180),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'test': transforms.Compose([
        transforms.Resize(227),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
}


def load_eye_disease_dataset():
    """
    load eye disease dataset
    :return:
    """
    batch_size = cfg['batch_size']

    train_dataset = EyeDiseaseDataset(train=True,
                                      transform=data_transforms['train'])
    trainloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)

    test_dataset = EyeDiseaseDataset(train=False,
                                     transform=data_transforms['test'])
    testloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=4)

    return trainloader, testloader
