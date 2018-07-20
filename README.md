# crowd-counting-cnn

This implementation is from [mcnn-tensorflow](https://github.com/uestcchicken/crowd-counting-MCNN) The author implements MCNN model on Shanghaitech dataset. 

I just modified some details to create UCSD dataset and UCF_50 dataset and test the MCNN model on these dataset.  

I am not sure whether it is okay to upload the modified implementation and if it is wrong, please contatct me and I will delete it. wqingdaniel@gmail.com.



### UCF_50

在**MCNN**上测试UCF_50dataset，根据[论文](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7780439)设置，使用5折交叉验证，所以，数据集分成了5份。而且，每一张图片截取9个patch，这样总数据大小是$50\times9=450$. 训练的时候每一个输入是一个patch，测试的时候也是一个patch。但是，在计算mae​和mse时，一定要将9个patch合并计算，这样得到的mae​和mse才是一张图片的测试结果。