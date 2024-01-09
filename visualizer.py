import argparse
import os
import time

import numpy as np
import torch
from tqdm import tqdm

import config
from datasets.dataset import get_dataset
from tools.viz import SLAMFrontend


def dict_to_numpy(input_dict: dict) -> np.ndarray:
    # co-slam保存出来的pose都是dict类型的，{frame_id:int, pose:tensor}
    # 而我们可视化需要的是numpy格式
    output_np = input_dict[0].numpy()[np.newaxis, :]
    for i in range(1, len(input_dict)):
        output_np = np.vstack((output_np, input_dict[i].numpy()[np.newaxis, :]))
    return output_np


def list_tensor_to_numpy(input_list: list) -> np.ndarray:
    # co-slam dataset 默认的pose居然是list类型的，list里面保存的还是tensor
    # 我们可视化需要的还是numpy的格式
    # 使用循环逐个将每个张量转换为 NumPy 数组
    numpy_arrays_list = [tensor.numpy() for tensor in input_list]
    return np.array(numpy_arrays_list)


if __name__ == '__main__':
    print('Start visualizer...')
    parser = argparse.ArgumentParser(description='Arguments for running the visualizer.')
    parser.add_argument('--config', type=str, help='Path to config file.')
    parser.add_argument('--input_folder', type=str,
                        help='input folder, this have higher priority, can overwrite the one in config file')
    parser.add_argument('--output', type=str,
                        help='output folder, this have higher priority, can overwrite the one in config file')
    parser.add_argument('--use_gt', type=bool,
                        help='use gt pose or not', default=True)
    args = parser.parse_args()

    cfg = config.load_config(args.config)
    if args.input_folder is not None:
        cfg['data']['datadir'] = args.input_folder
    if args.output is not None:
        cfg['data']['output'] = args.output

    gt_c2w_list = list_tensor_to_numpy(get_dataset(cfg).poses)
    estimate_c2w_list = None

    output_fix = os.path.join(cfg['data']['output'], cfg['data']['exp_name'])
    if os.path.exists(output_fix):
        ckpts = [os.path.join(output_fix, f)
                 for f in sorted(os.listdir(output_fix)) if 'checkpoint' in f]
        if len(ckpts) > 0:
            ckpt_path = ckpts[-1]
            print('Get ckpt :', ckpt_path)
            ckpt = torch.load(ckpt_path, map_location=torch.device('cpu'))
            # 这里只能够拿到pose，而gt_pose和N都拿不到，要另外想办法
            estimate_c2w_list = ckpt['pose']
    estimate_c2w_list = dict_to_numpy(estimate_c2w_list)

    frontend = SLAMFrontend(output_fix, init_pose=estimate_c2w_list[0], cam_scale=0.3,
                            save_rendering=False, near=0,
                            estimate_c2w_list=estimate_c2w_list, gt_c2w_list=gt_c2w_list).start()

    for i in tqdm(range(0, len(estimate_c2w_list))):
        # show every second frame for speed up
        time.sleep(0.03)
        meshfile = f'{output_fix}/mesh_track{i}.ply'
        if os.path.isfile(meshfile):
            frontend.update_mesh(meshfile)
        frontend.update_pose(1, estimate_c2w_list[i], gt=False)

        if args.use_gt:
            frontend.update_pose(1, gt_c2w_list[i], gt=True)

        # the visualizer might get stucked if update every frame
        # with a long sequence (10000+ frames)
        if i % 10 == 0:
            frontend.update_cam_trajectory(i, gt=False)
            if args.use_gt:
                frontend.update_cam_trajectory(i, gt=True)
