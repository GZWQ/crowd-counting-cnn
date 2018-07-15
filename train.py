from network import MCNN as MCNN_ShanghaiTech
from network_ucsd import MCNN as MCNN_UCSD
from network_ucf import MCNN as MCNN_UCF

# 'A'或者 ‘B  则处理ShanghaiTech数据
# ‘ucsd’ 则处理UCSD数据
# 'ucf' 则处理UCF_CC_50数据
# data_name = 'A'
# data_name = 'ucsd'
data_name = 'ucf'

if __name__ == '__main__':
    EPOCH = 2
    if data_name=='A' or data_name=='B':
        mcnn = MCNN_ShanghaiTech(data_name)
        mcnn.train(EPOCH)
    elif data_name == 'ucsd':
        mcnn = MCNN_UCSD(data_name)
        mcnn.train(EPOCH)
        mcnn.test()
    elif data_name == 'ucf':
        mcnn = MCNN_UCF(data_name)
        mae_file = []
        mse_file = []
        for k_fold in range(1,6):
            mae,mse = mcnn.train(EPOCH,k_fold)
            print("The mae of fold ",k_fold,' is:',mae)
            print('The mse of fold ',k_fold,' is : ',mse)
            mae_file.append(mae)
            mse_file.append(mse)
        print("After 5-folder cross validation, the average mae is :",sum(mae_file)/5)
        print('The average mse is :',sum(mse_file)/5)










