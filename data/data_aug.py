# data augmentation
import Augmentor


def zoom_aug_on_disk(orig_img_path):
    """
    zoom data augmentation and save them on disk
    :param orig_img_path:
    :return:
    """
    p = Augmentor.Pipeline(orig_img_path)
    p.zoom(probability=0.5, min_factor=1.1, max_factor=1.5)
    p.sample(7000)
    p.process()
