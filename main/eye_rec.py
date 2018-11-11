"""
train and eval ResNet on EyeDisease Dataset
Author: LucasX
"""
import os
import sys
import time
import copy

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from sklearn.metrics import confusion_matrix
from torch.optim import lr_scheduler
from torchvision import models

sys.path.append('../')
from data import data_loader
from util.utils import mkdirs_if_not_exist
from util.cfg import cfg


def train_model_with_ft(model, dataloaders, criterion, optimizer, scheduler, num_epochs, inference=False):
    """
    train model with fine-tune
    :param model:
    :param dataloaders:
    :param criterion:
    :param optimizer:
    :param scheduler:
    :param num_epochs:
    :param inference:
    :return:
    """
    model = model.float()
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    if torch.cuda.device_count() > 1:
        print("Let's use", torch.cuda.device_count(), "GPUs!")
        model = nn.DataParallel(model)
    model = model.to(device)

    dataset_sizes = {x: dataloaders[x].__len__() for x in ['train', 'test']}

    for _ in dataset_sizes.keys():
        print('Dataset size of {0} is {1}...'.format(_, dataloaders[_].__len__()))

    if not inference:
        print('Start training %s...' % model.__class__.__name__)
        since = time.time()

        best_model_wts = copy.deepcopy(model.state_dict())
        best_acc = 0.0

        for epoch in range(num_epochs):
            print('-' * 100)
            print('Epoch {}/{}'.format(epoch, num_epochs - 1))

            # Each epoch has a training and validation phase
            for phase in ['train', 'test']:
                if phase == 'train':
                    scheduler.step()
                    model.train()  # Set model to training mode
                else:
                    model.eval()  # Set model to evaluate mode

                running_loss = 0.0
                running_corrects = 0

                # Iterate over data.
                # for inputs, labels, filenames in dataloaders[phase]:
                for i, data in enumerate(dataloaders[phase], 0):

                    inputs, labels = data['image'], data['label']
                    inputs = inputs.to(device)
                    labels = labels.to(device)

                    # zero the parameter gradients
                    optimizer.zero_grad()

                    # forward
                    # track history if only in train
                    with torch.set_grad_enabled(phase == 'train'):
                        outputs = model(inputs)
                        _, preds = torch.max(outputs, 1)
                        loss = criterion(outputs, labels)

                        # backward + optimize only if in training phase
                        if phase == 'train':
                            loss.backward()
                            optimizer.step()

                    # statistics
                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)

                epoch_loss = running_loss / (dataset_sizes[phase] * cfg['batch_size'])
                epoch_acc = running_corrects.double() / (dataset_sizes[phase] * cfg['batch_size'])

                print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                    phase, epoch_loss, epoch_acc))

                # deep copy the model
                if phase == 'test' and epoch_acc > best_acc:
                    tmp_correct = 0
                    tmp_total = 0
                    tmp_y_pred = []
                    tmp_y_true = []
                    tmp_filenames = []

                    for data in dataloaders['val']:
                        images, labels, filename = data['image'], data['label'], data['filename']
                        images = images.to(device)
                        labels = labels.to(device)

                        outputs = model(images)
                        _, predicted = torch.max(outputs.data, 1)
                        tmp_total += labels.size(0)
                        tmp_correct += (predicted == labels).sum().item()

                        tmp_y_pred += predicted.to("cpu").detach().numpy().tolist()
                        tmp_y_true += labels.to("cpu").detach().numpy().tolist()
                        tmp_filenames += filename

                    tmp_acc = tmp_correct / tmp_total

                    print('Confusion Matrix of {0} on test set: '.format(model.__class__.__name__))
                    cm = confusion_matrix(tmp_y_true, tmp_y_pred)
                    print(cm)
                    cm = np.array(cm)

                    print('Accuracy = {0}'.format(tmp_acc))
                    precisions = []
                    recalls = []

                    for i in range(len(cm)):
                        precisions.append(cm[i][i] / sum(cm[:, i].tolist()))
                        recalls.append(cm[i][i] / sum(cm[i, :].tolist()))

                    print("Precision of {0} on test set = {1}".format(model.__class__.__name__,
                                                                      sum(precisions) / len(precisions)))
                    print(
                        "Recall of {0} on test set = {1}".format(model.__class__.__name__, sum(recalls) / len(recalls)))

                    best_acc = epoch_acc
                    best_model_wts = copy.deepcopy(model.state_dict())

                    model.load_state_dict(best_model_wts)
                    model_path_dir = './model'
                    mkdirs_if_not_exist(model_path_dir)
                    torch.save(model.state_dict(),
                               './model/{0}_best_epoch-{1}.pth'.format(model.__class__.__name__, epoch))

        time_elapsed = time.time() - since
        print('Training complete in {:.0f}m {:.0f}s'.format(
            time_elapsed // 60, time_elapsed % 60))
        print('Best test Acc: {:4f}'.format(best_acc))

        # load best model weights
        model.load_state_dict(best_model_wts)
        model_path_dir = './model'
        mkdirs_if_not_exist(model_path_dir)
        torch.save(model.state_dict(), './model/%s.pth' % model.__class__.__name__)

    else:
        print('Start testing %s...' % model.__class__.__name__)
        model.load_state_dict(torch.load(os.path.join('./model/%s.pth' % model.__class__.__name__)))

    model.eval()

    correct = 0
    total = 0
    y_pred = []
    y_true = []
    filenames = []
    probs = []

    with torch.no_grad():
        for data in dataloaders['test']:
            images, labels, filename = data['image'], data['label'], data['filename']
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)

            outputs = F.softmax(outputs)
            # get TOP-K output labels and corresponding probabilities
            topK_prob, topK_label = torch.topk(outputs, 2)
            probs += topK_prob.to("cpu").detach().numpy().tolist()

            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            y_pred += predicted.to("cpu").detach().numpy().tolist()
            y_true += labels.to("cpu").detach().numpy().tolist()
            filenames += filename

    print('Accuracy of {0} on test set: {1}% '.format(model.__class__.__name__, 100 * correct / total))
    print(
        'Confusion Matrix of {0} on test set: '.format(model.__class__.__name__))

    cm = confusion_matrix(y_true, y_pred)
    print(cm)

    cm = np.array(cm)

    precisions = []
    recalls = []
    for i in range(len(cm)):
        precisions.append(cm[i][i] / sum(cm[:, i].tolist()))
        recalls.append(cm[i][i] / sum(cm[i, :].tolist()))

    print('Precision List: ')
    print(precisions)
    print('Recall List: ')
    print(recalls)

    print("Precision of {0} on test set = {1}".format(model.__class__.__name__,
                                                      sum(precisions) / len(precisions)))
    print(
        "Recall of {0} on test set = {1}".format(model.__class__.__name__, sum(recalls) / len(recalls)))

    print('Output CSV...')
    col = ['filename', 'gt', 'pred', 'prob']
    df = pd.DataFrame([[filenames[i], y_true[i], y_pred[i], probs[i][0]] for i in range(len(filenames))],
                      columns=col)
    df.to_csv("./output-%s.csv" % model.__class__.__name__, index=False)
    print('CSV has been generated...')


def run_eye_disease_rec(model, epoch):
    """
    recognize eye disease
    :param model:
    :param epoch:
    :return:
    """
    criterion = nn.CrossEntropyLoss()

    optimizer_ft = optim.SGD(model.parameters(), lr=0.001, momentum=0.9, weight_decay=1e-4)

    exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=50, gamma=0.1)

    print('start loading PlantsDiseaseDataset...')
    trainloader, testloader = data_loader.load_eye_disease_dataset()

    dataloaders = {
        'train': trainloader,
        'test': testloader,
    }

    train_model_with_ft(model=model, dataloaders=dataloaders, criterion=criterion, optimizer=optimizer_ft,
                        scheduler=exp_lr_scheduler, num_epochs=epoch, inference=False)


if __name__ == '__main__':
    resnet = models.resnet18(pretrained=True)
    num_ftrs = resnet.fc.in_features
    resnet.fc = nn.Linear(num_ftrs, 5)

    run_eye_disease_rec(model=resnet, epoch=200)
