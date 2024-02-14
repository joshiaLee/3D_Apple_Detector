from argparse import ArgumentParser
from requests import request
from mmdet3d.apis import inference_detector, init_model, show_result_meshlab, apple_inspector
from os import path as osp
import numpy as np
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from plyfile import PlyData

# build the model from a config file and a checkpoint files
config = '/home/yolo/fcaf3d/configs/fcaf3d/fcaf3d_sunrgbd-3d-10class.py'
checkpoint = '/home/yolo/fcaf3d/work_dirs/fcaf3d_sunrgbd-3d-10class/latest.pth'
mydevice = 'cuda:0'

class Start:
    start = 0
    end = 0

# prior load the pre_trained model
model = init_model(config, checkpoint, device=mydevice)


class Target:
    watchDir = '/home/yolo/fcaf3d/data/sunrgbd/demo_test'
    #directory to inspect

    def __init__(self):
        self.observer = Observer()   #making the observer object

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDir, 
                                                       recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(10)
        except:
            self.observer.stop()
            print("Error")
            self.observer.join()

class Handler(FileSystemEventHandler):
#inherity the FileSystemEventHandler Class


    # if file or directory moved or renamed
    def on_moved(self, event):
        pass

    def on_created(self, event): # if file or directory produced 
        
        
        a = event
        pcd = a.key[1]
        ex = pcd.split('.')[-1]

        if (ex == 'ply'):
            # Start.start = time.time()
            # Start.end = 0


            print('==================================')
            print('Receiving ply file Success')
            
            plyfile = PlyData.read(pcd)
            d = np.vstack((plyfile['vertex']['x'], plyfile['vertex']['y'], plyfile['vertex']['z'],
                        plyfile['vertex']['red'] / 255.0, plyfile['vertex']['green'] / 255.0, plyfile['vertex']['blue'] / 255.0))
            d = d.T
            d = d.astype('float32')
            file_name = pcd.split('.')[0]
            d.tofile(file_name + '.bin')

            
            print('converting ply to bin file Success')
            print('==================================')
            # result, data = inference_detector(model, pcd)


            # show_result_meshlab(
            #     data,
            #     result,
            #     '/home/yolo/fcaf3d/data/sunrgbd/demo_result', # --out-dir
            #     0.2, # --score_trh
            #     show=False,
            #     snapshot=False,
            #     task='det')
            # '''

            # '''
            # command = 'python /home/yolo/fcaf3d/demo/ply2bin.py '  + pcd 
            # os.system(command)
            

        
        if  (ex == 'bin'):
            

            # print('converting ply to bin file Success')
            # print('==================================')
            Start.start = time.time()
            Start.end = 0
            result, data = inference_detector(model, pcd)

            print('inference time :', time.time() - Start.start + Start.end)
            Start.end = time.time() - Start.start + Start.end
            Start.start = time.time()
            
            show_result_meshlab(
                data,
                result,
                '/home/yolo/fcaf3d/data/sunrgbd/demo_result', # --out-dir
                0.2, # --score_trh
                show=False,
                snapshot=False,
                task='det',
                Start_time=Start.start,
                End_time=Start.end)
        
        
    
    def on_deleted(self, event): # if file or directory deleted
        pass

    def on_modified(self, event): # if file or directory modified
        pass



w = Target()
w.run()

'''
def main():
    
    parser = ArgumentParser()
    parser.add_argument('pcd', help='Point cloud file')
    parser.add_argument('config', help='Config file')
    parser.add_argument('checkpoint', help='Checkpoint file')
    parser.add_argument(
        '--device', default='cuda:0', help='Device used for inference')
    parser.add_argument(
        '--score-thr', type=float, default=0.0, help='bbox score threshold')
    parser.add_argument(
        '--out-dir', type=str, default='demo', help='dir to save results')
    parser.add_argument(
        '--show', action='store_true', help='show online visuliaztion results')
    parser.add_argument(
        '--snapshot',
        action='store_true',
        help='whether to save online visuliaztion results')
    args = parser.parse_args()


# test a single image
result, data = inference_detector(model, pcd)

    # show the results
    show_result_meshlab(
        data,
        result,
        args.out_dir,
        args.score_thr,
        show=args.show,
        snapshot=args.snapshot,
        task='det')

if __name__ == '__main__':
    main()
'''