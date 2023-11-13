import tensorflow as tf
import scipy.io
import time
import network_model
import os
import numpy as np
from utils import *
import sys

#
# Description :
#   Inference code of QSMnet and QSMnet+
#   Save susceptibility map in Matlab and NII format
# Outputs :
#   results_<network_name>.mat & results_<network_name>.nii
#   ppm unit
#
# Copyright @ Woojin Jung & Jaeyeon Yoon
# Laboratory for Imaging Science and Technology
# Seoul National University
# email : wjjung93@snu.ac.kr
#
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

args = sys.argv
output_path = args[1]

'''
Network model
'''
network_name = 'QSMnet+_64'
epoch = 25
sub_num = 99 # number of subjects in testset
voxel_size = [1, 1, 1] # resolution of subject
dir_net = '../Checkpoints/'
'''
File Path
'''
FILE_PATH_INPUT = output_path
FILE_PATH_copy_nii = output_path + '.nii'   ## original nii data for copying header information
FILE_PATH_PRED = output_path

def inf():
    f = scipy.io.loadmat(dir_net + network_name + '/' + 'norm_factor_' + network_name + '.mat')
    net_info = np.load(dir_net + network_name + '/network_info_' + network_name + '.npy')
    act_func = net_info[0]
    net_model = net_info[1]
    
    b_mean = f['input_mean']
    b_std = f['input_std']
    y_mean = f['label_mean']
    y_std = f['label_std']
    
    for i in range(1, 2): # range(1, sub_num+1)
        input_data = scipy.io.loadmat(FILE_PATH_INPUT + '/QSMnet_input.mat')
        copy_dir = FILE_PATH_copy_nii + '.nii'
        tf.compat.v1.reset_default_graph()
        
        print('Subject path: ' + FILE_PATH_INPUT)
        field = input_data["phs_tissue"]
        field = (field - b_mean) / b_std
        [pfield, N_difference, N] = padding_data(field)
        
        Z = tf.compat.v1.placeholder("float", [None, N[0], N[1], N[2], 1])
        keep_prob = tf.compat.v1.placeholder("float")
    
        net_func = getattr(network_model, net_model)
        feed_result = net_func(Z, act_func, False, False)
    
        saver = tf.compat.v1.train.Saver()
        with tf.compat.v1.Session() as sess:
            sess.run(tf.compat.v1.global_variables_initializer())
            print('##########Restore Network##########')
            saver.restore(sess, dir_net + network_name + '/' + network_name + '-' + str(epoch))
            print('Done!')
            print('##########Inference...##########')
            result_im = y_std * sess.run(feed_result, feed_dict={Z: pfield, keep_prob: 1.0}) + y_mean
            result_im = crop_data(result_im.squeeze(), N_difference)
            
            display_slice_inf([52,72,92], result_im)
            print('##########Saving MATLAB & NII file...##########')
            scipy.io.savemat(FILE_PATH_PRED + '/QSMnet_' + str(network_name) + '_' + str(epoch) + '.mat', mdict={'sus': result_im})
            if os.path.exists(copy_dir):
                save_nii_with_copy_existing_nii(copy_dir, result_im, voxel_size,  FILE_PATH_PRED, 'subject' + str(i) + '_' + str(network_name) + '_' + str(epoch))
            else:
                save_nii(result_im, voxel_size, FILE_PATH_PRED, 'QSMnet_' + str(network_name) + '_' + str(epoch))
        print('All done!')

if __name__ == '__main__':
    start_time = time.time()
    inf()
    print("Total inference time : {} sec".format(time.time() - start_time))
    




