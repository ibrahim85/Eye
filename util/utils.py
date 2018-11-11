# utils toolkit
# Author: LucasX

import os
import shutil
import json

import pandas as pd


def mkdirs_if_not_exist(dir_name):
    """
    create new folder if not exist
    :param dir_name:
    :return:
    """
    if not os.path.isdir(dir_name) or not os.path.exists(dir_name):
        os.makedirs(dir_name)


def over_sample(from_target_dir, to_target_dir, copy_time):
    """
    over sample
    :param from_target_dir:
    :param to_target_dir:
    :param copy_time:
    :return:
    """
    mkdirs_if_not_exist(to_target_dir)

    for i in range(copy_time):
        print('Copying Round %d...' % i)
        for _ in os.listdir(from_target_dir):
            shutil.copyfile(os.path.join(from_target_dir, _), os.path.join(to_target_dir, 'cp_{0}_{1}'.format(i, _)))

    print('Processing done!')
