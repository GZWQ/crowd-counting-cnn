from network import MCNN as MCNN_ShanghaiTech
from network_ucsd import MCNN as MCNN_UCSD
                
data_name = 'ucsd'  # 或者 ‘B
                            
mcnn = MCNN_UCSD(data_name)
mcnn.test()