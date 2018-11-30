import os
import shutil
import sys

sys.path.append('../')
from util.utils import mkdirs_if_not_exist


def split_to_n_parts(source_dir, n):
    """
    split images to n parts
    :param source_dir:
    :param n:
    :return:
    """
    target_dirs = [source_dir.split('/')[-1] + '_{0}'.format(_) for _ in range(n)]

    for target_dir in target_dirs:
        mkdirs_if_not_exist(target_dir)

    capacity = int(len(os.listdir(source_dir)) / n)

    for i, f in enumerate(os.listdir(source_dir)):
        dir_idx = int(i / capacity)
        shutil.copy(os.path.join(source_dir, f), os.path.join(target_dirs[dir_idx], f))

    print('Copying images successfully~')


if __name__ == '__main__':
    split_to_n_parts('/var/log/EyeDiseaseDataSet/img_data_norm', 10)
