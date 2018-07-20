from shanghaitech_large_kernel import MCNN as L_MCNN
from shanghaitech_medium_kernel import MCNN as M_MCNN
from shanghaitech_small_kernel import MCNN as S_MCNN

data_name = 'A'
kernel_size = 'L'

if __name__ == '__main__':
    if kernel_size=='L':
        EPOCH = 100
        mcnn = L_MCNN(data_name)
        mcnn.train(EPOCH)
        mcnn.test()
    elif kernel_size == 'M':
        EPOCH = 100
        mcnn = M_MCNN(data_name)
        mcnn.train(EPOCH)
        mcnn.test()
    elif kernel_size == 'S':
        EPOCH = 100
        mcnn = S_MCNN(data_name)
        mcnn.train(EPOCH)
        mcnn.test()