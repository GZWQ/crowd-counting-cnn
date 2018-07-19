from network import MCNN as MCNN_ShanghaiTech
from network_ucsd import MCNN as MCNN_UCSD
from network_ucf import MCNN as MCNN_UCF

# 'A'or ‘B  dealing with ShanghaiTech
# ‘ucsd’ dealing with UCSD
# 'ucf' dealing with UCF_CC_50
# data_name = 'A'
# data_name = 'ucsd'
data_name = 'ucf'

if __name__ == '__main__':
    if data_name=='A' or data_name=='B':
        EPOCH = 2
        mcnn = MCNN_ShanghaiTech(data_name)
        mcnn.train(EPOCH)
    elif data_name == 'ucsd':
        EPOCH = 2
        mcnn = MCNN_UCSD(data_name)
        mcnn.train(EPOCH)
        mcnn.test()
    elif data_name == 'ucf':
        EPOCH = 1
        mcnn = MCNN_UCF(data_name)
        mae_file = []
        mse_file = []
        for k_fold in range(1,6):
            # mcnn.train(EPOCH,k_fold)
            mae,mse=mcnn.test(k_fold)
            print("The mae of fold ",k_fold,' is:',mae)
            print('The mse of fold ',k_fold,' is : ',mse)
            mae_file.append(mae)
            mse_file.append(mse)
        print("After 5-folder cross validation, the average mae is :",sum(mae_file)/5)
        print('The average mse is :',sum(mse_file)/5)










