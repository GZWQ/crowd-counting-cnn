import numpy as np
import cv2
import tensorflow as tf
import os
import random
import math
import sys
from heatmap import *


class MCNN:
    def __init__(self, dataset):
        self.dataset = dataset
        self.LEARNING_RATE = 1e-4

        self.x = tf.placeholder(tf.float32, [None, None, None, 1])
        self.y_act = tf.placeholder(tf.float32, [None, None, None, 1])
        self.y_pre = self.inf(self.x)

        self.loss = tf.sqrt(tf.reduce_mean(tf.square(self.y_act - self.y_pre)))
        self.act_sum = tf.reduce_sum(self.y_act)
        self.pre_sum = tf.reduce_sum(self.y_pre)
        self.MAE = tf.abs(self.act_sum - self.pre_sum)

        self.train_step = tf.train.AdamOptimizer(self.LEARNING_RATE).minimize(self.loss)

    def data_pre_train(self, kind, dataset,data_file_number):  # kind = train || val
        img_path = './data/ucf_formatted_trainval/ucf_patches_9/train_cv' + str(data_file_number) + '/'
        den_path = './data/ucf_formatted_trainval/ucf_patches_9/train_den_cv' + str(data_file_number) + '/'
        print('loading', kind, 'data from dataset', dataset, '...')
        img_names = os.listdir(img_path)  # 该目录下的所有文件名
        img_num = len(img_names)

        data = []
        for i in range(1, img_num + 1):
            if i % 100 == 0:
                print(i, '/', img_num)
            name = img_names[i - 1]
            # flags用于指定读入图像的颜色和深度,(<0)，以原始图像读取（包括alpha通道）
            # ( 0)，以灰度图像读取
            # (>0)，以RGB格式读取
            img = cv2.imread(img_path + name, flags=0)
            img = np.array(img)
            img = (img - 127.5) / 128  ###why is that?
            den = np.loadtxt(open(den_path + name[:-4] + '.csv'), delimiter=",")
            den_quarter = np.zeros((int(den.shape[0] / 4), int(den.shape[1] / 4)))
            for i in range(len(den_quarter)):
                for j in range(len(den_quarter[0])):
                    for p in range(4):
                        for q in range(4):
                            den_quarter[i][j] += den[i * 4 + p][j * 4 + q]
            data.append([img, den_quarter])
        print('load', kind, 'data from dataset', dataset, 'finished')
        return data

    def data_pre_test(self, dataset,data_file_number):
        img_path = './data/ucf_formatted_trainval/ucf_patches_9/train_cv' + str(data_file_number) + '/'
        den_path = './data/ucf_formatted_trainval/ucf_patches_9/train_den_cv' + str(data_file_number) + '/'
        print('loading test data from dataset', dataset, '...')
        img_names = os.listdir(img_path)
        img_num = len(img_names)

        data = []
        for i in range(1, img_num ):
            if i % 50 == 0:
                print(i, '/', img_num)
            name = img_names[i - 1]
            print(name)
            img = cv2.imread(img_path + name, 0)
            img = np.array(img)
            img = (img - 127.5) / 128
            den = np.loadtxt(open(den_path + name[:-4] + '.csv'), delimiter=",")
            den_sum = np.sum(den)
            data.append([img, den_sum,name])

            # if i <= 2:
            # heatmap(den, i, dataset, 'act')

        print('load test data from dataset', dataset, 'finished')
        return data

    def conv2d(self, x, w):
        return tf.nn.conv2d(x, w, strides=[1, 1, 1, 1], padding='SAME')

    def max_pool_2x2(self, x):
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    def inf(self, x):
        # s net ###########################################################
        w_conv1_1 = tf.get_variable('w_conv1_1', [5, 5, 1, 24])
        b_conv1_1 = tf.get_variable('b_conv1_1', [24])
        h_conv1_1 = tf.nn.relu(self.conv2d(x, w_conv1_1) + b_conv1_1)

        h_pool1_1 = self.max_pool_2x2(h_conv1_1)

        w_conv2_1 = tf.get_variable('w_conv2_1', [3, 3, 24, 48])
        b_conv2_1 = tf.get_variable('b_conv2_1', [48])
        h_conv2_1 = tf.nn.relu(self.conv2d(h_pool1_1, w_conv2_1) + b_conv2_1)

        h_pool2_1 = self.max_pool_2x2(h_conv2_1)

        w_conv3_1 = tf.get_variable('w_conv3_1', [3, 3, 48, 24])
        b_conv3_1 = tf.get_variable('b_conv3_1', [24])
        h_conv3_1 = tf.nn.relu(self.conv2d(h_pool2_1, w_conv3_1) + b_conv3_1)

        w_conv4_1 = tf.get_variable('w_conv4_1', [3, 3, 24, 12])
        b_conv4_1 = tf.get_variable('b_conv4_1', [12])
        h_conv4_1 = tf.nn.relu(self.conv2d(h_conv3_1, w_conv4_1) + b_conv4_1)

        # m net ###########################################################
        w_conv1_2 = tf.get_variable('w_conv1_2', [7, 7, 1, 20])
        b_conv1_2 = tf.get_variable('b_conv1_2', [20])
        h_conv1_2 = tf.nn.relu(self.conv2d(x, w_conv1_2) + b_conv1_2)

        h_pool1_2 = self.max_pool_2x2(h_conv1_2)

        w_conv2_2 = tf.get_variable('w_conv2_2', [5, 5, 20, 40])
        b_conv2_2 = tf.get_variable('b_conv2_2', [40])
        h_conv2_2 = tf.nn.relu(self.conv2d(h_pool1_2, w_conv2_2) + b_conv2_2)

        h_pool2_2 = self.max_pool_2x2(h_conv2_2)

        w_conv3_2 = tf.get_variable('w_conv3_2', [5, 5, 40, 20])
        b_conv3_2 = tf.get_variable('b_conv3_2', [20])
        h_conv3_2 = tf.nn.relu(self.conv2d(h_pool2_2, w_conv3_2) + b_conv3_2)

        w_conv4_2 = tf.get_variable('w_conv4_2', [5, 5, 20, 10])
        b_conv4_2 = tf.get_variable('b_conv4_2', [10])
        h_conv4_2 = tf.nn.relu(self.conv2d(h_conv3_2, w_conv4_2) + b_conv4_2)

        # l net ###########################################################
        w_conv1_3 = tf.get_variable('w_conv1_3', [9, 9, 1, 16])
        b_conv1_3 = tf.get_variable('b_conv1_3', [16])
        h_conv1_3 = tf.nn.relu(self.conv2d(x, w_conv1_3) + b_conv1_3)

        h_pool1_3 = self.max_pool_2x2(h_conv1_3)

        w_conv2_3 = tf.get_variable('w_conv2_3', [7, 7, 16, 32])
        b_conv2_3 = tf.get_variable('b_conv2_3', [32])
        h_conv2_3 = tf.nn.relu(self.conv2d(h_pool1_3, w_conv2_3) + b_conv2_3)

        h_pool2_3 = self.max_pool_2x2(h_conv2_3)

        w_conv3_3 = tf.get_variable('w_conv3_3', [7, 7, 32, 16])
        b_conv3_3 = tf.get_variable('b_conv3_3', [16])
        h_conv3_3 = tf.nn.relu(self.conv2d(h_pool2_3, w_conv3_3) + b_conv3_3)

        w_conv4_3 = tf.get_variable('w_conv4_3', [7, 7, 16, 8])
        b_conv4_3 = tf.get_variable('b_conv4_3', [8])
        h_conv4_3 = tf.nn.relu(self.conv2d(h_conv3_3, w_conv4_3) + b_conv4_3)

        # merge ###########################################################
        h_conv4_merge = tf.concat([h_conv4_1, h_conv4_2, h_conv4_3], 3)

        w_conv5 = tf.get_variable('w_conv5', [1, 1, 30, 1])
        b_conv5 = tf.get_variable('b_conv5', [1])
        h_conv5 = self.conv2d(h_conv4_merge, w_conv5) + b_conv5

        y_pre = h_conv5

        return y_pre

    def train(self, max_epoch,k_fold):
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            # if not os.path.exists('./model' + self.dataset):
            #     sess.run(tf.global_variables_initializer())
            # else:
            #     saver = tf.train.Saver()
            #     saver.restore(sess, 'model' + self.dataset + '/model.ckpt')
            data_train = []
            data_val = []
            for i in range(1,6):
                if i==k_fold:
                    continue
                    # data_val = self.data_pre_train('train', self.dataset, i) #validation dataset
                else:
                    data_train.extend(self.data_pre_train('train', self.dataset,i))  # 训练数据预处理，density map缩小1/4

            best_mae = sys.maxsize
            best_mse = sys.maxsize
            all_validate_mae = []
            all_validate_mse = []
            for epoch in range(max_epoch):
                # training process
                epoch_mae = 0
                random.shuffle(data_train)
                for i in range(len(data_train)):
                    data = data_train[i]
                    x_in = np.reshape(data[0],
                                      (1, data[0].shape[0], data[0].shape[1], 1))  # data[0]是image，data[1]是density map
                    y_ground = np.reshape(data[1], (1, data[1].shape[0], data[1].shape[1], 1))

                    _, l, y_a, y_p, act_s, pre_s, m = sess.run(
                        [self.train_step, self.loss, self.y_act, self.y_pre,
                         self.act_sum, self.pre_sum, self.MAE],
                        feed_dict={self.x: x_in, self.y_act: y_ground})
                    if i % 500 == 0:
                        print('fold ',k_fold,'epoch', epoch, 'step', i, 'mae:', m)
                    epoch_mae += m
                epoch_mae /= len(data_train)
                saver = tf.train.Saver()
                saver.save(sess, 'model' + self.dataset +'/fold_'+str(k_fold)+ '/model.ckpt')
                print('epoch', epoch + 1, 'train_mae:', epoch_mae)

    def test(self,k_fold):
        with tf.Session() as sess:
            saver = tf.train.Saver()
            saver.restore(sess, 'model' + self.dataset + '/fold_'+str(k_fold)+'/model.ckpt')
            data = self.data_pre_test(self.dataset,k_fold)

            mae = 0
            mse = 0
            whole_ture = [0 for _ in range(10)]
            whole_ture = np.array(whole_ture)
            whole_predict = [0 for _ in range(10)]
            whole_predict = np.array(whole_predict)
            for i in range(1, len(data) + 1):

                if i % 20 == 0:
                    print(i, '/', len(data))
                d = data[i - 1]
                x_in = d[0]
                y_a = d[1]
                name = d[2]
                pos = int(name[:-6])

                x_in = np.reshape(d[0], (1, d[0].shape[0], d[0].shape[1], 1))
                y_p_den = sess.run(self.y_pre, feed_dict={self.x: x_in})

                y_p = np.sum(y_p_den)

                whole_ture[(pos-1)%10] += y_a
                whole_predict[(pos-1)%10] += y_p


            err = np.abs(whole_predict-whole_ture)
            mae = sum(err) / len(whole_ture)
            mse = sum(err**2)/len(whole_ture)
            mse = math.sqrt(mse)
            print('mae: ', mae)
            print('mse: ', mse)
            return mae,mse