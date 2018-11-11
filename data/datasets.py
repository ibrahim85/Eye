"""
definition of datasets
Author: LucasX
"""
import os
import sys

import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
from skimage import io
from torch.utils.data import Dataset

sys.path.append('../')
from util.cfg import cfg


class EyeDiseaseDataset(Dataset):
    """
    Eye Disease Dataset
    """

    def __init__(self, train=True, transform=None):
        """
        PyTorch Dataset definition
        :param train_val:
        :param transform:
        """
        images = []
        labels = []
        for i, cls_dir in os.listdir(cfg['image_base']):
            labels.append(i)
            for _ in os.listdir(os.listdir(cfg['image_base'], cls_dir)):
                images.append(os.path.join(cfg['image_base'], cls_dir, _))

        X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42,
                                                            stratify=labels)

        if train:
            self.img_files = X_train
            self.labels = y_train
        else:
            self.img_files = X_test
            self.labels = y_test

        self.transform = transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        img_path = self.img_files[idx]

        image = io.imread(img_path)
        label = self.labels[idx]

        sample = {'image': image, 'label': label, 'filename': self.img_files[idx]}

        if self.transform:
            sample['image'] = self.transform(Image.fromarray(sample['image'].astype(np.uint8)))

        return sample
