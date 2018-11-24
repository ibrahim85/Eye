# Eye Disease Recognition
## Introduction
Deep Learning for Eye Disease Recognition. :eye:

### Data Description
| Type | Capacity |
| :---: | :---: |
| Norm | 7770 |
| AMD | 720 |
| DR | 270 |
| Glaucoma | 450 |
| Myopia | 790 |
 

## Solutions
1. Apply _transfer learning_ to recognize eye disease. Namely, we first pretrain ResNeXt on ImageNet, and fine-tune on target source.
2. Apply _mixup_ and _sample paring_ for data augmentation.
3. Apply _multi-task learning_ to boost performance.
4. Apply _visual attention model_ to boost performance.
5. Adopt [Easy Ensemble](https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/tsmcb09.pdf) to handle severe data imbalance problem.


## Performance
| Model | Epoch | Accuracy | Precision | Recall |
| :---: | :---: | :---: | :---: | :---: |
| ResNet50 | - | 83.75% | 67.60% | 44.33% |


## Contributors
* [Xueying Zhang](https://github.com/Schneey)
* [Lucas Xu](https://github.com/lucasxlu)

For more details, plz do hot hesitate to contact us! :smile:


## Reference
1. He, Kaiming, et al. ["Deep residual learning for image recognition."](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/He_Deep_Residual_Learning_CVPR_2016_paper.pdf) Proceedings of the IEEE conference on computer vision and pattern recognition. 2016.
2. Tajbakhsh, Nima, et al. ["Convolutional neural networks for medical image 
analysis: Full training or fine tuning?."](https://arxiv.org/pdf/1706.00712.pdf) IEEE transactions on medical 
imaging 35.5 (2016): 1299-1312.
3. De Fauw, Jeffrey, et al. ["Clinically applicable deep learning for diagnosis and referral in retinal disease."](https://www.nature.com/articles/s41591-018-0107-6) Nature medicine 24.9 (2018): 1342. 
4. Kermany, Daniel S., et al. ["Identifying medical diagnoses and treatable 
diseases by image-based deep learning."](https://www.cell.com/cell/fulltext/S0092-8674(18)30154-5?code=cell-site) Cell 172.5 (2018): 1122-1131.
5. Gulshan, Varun, et al. ["Development and validation of a deep learning 
algorithm for detection of diabetic retinopathy in retinal fundus photographs
."](https://static.googleusercontent.com/media/research.google.com/zh-CN//pubs/archive/45732.pdf) Jama 316.22 (2016): 2402-2410.