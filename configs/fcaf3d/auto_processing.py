import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from plyfile import PlyData
import numpy as np
from os import path as osp

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
                time.sleep(100)
        except:
            self.observer.stop()
            print("Error")
            self.observer.join()

class Handler(FileSystemEventHandler):
#inherity the FileSystemEventHandler Class 
#overriding

    # if file or directory moved or renamed
    def on_moved(self, event):
        pass

    def on_created(self, event): # if file or directory produced 
        '''
        a = event
        filename = a.key[1].split('/')[-1]
        print('===========================')
        print('Receiving ply file Success')
        print('===========================')
        command = 'python /home/yolo/fcaf3d/demo/pcd_demo.py ' + filename + \
                  ' /home/yolo/fcaf3d/configs/fcaf3d/fcaf3d_sunrgbd-3d-10class.py' + \
                  ' /home/yolo/fcaf3d/work_dirs/fcaf3d_sunrgbd-3d-10class/latest.pth' + \
                  ' --score-thr' + ' 0.13' + ' --out-dir' + ' /home/yolo/fcaf3d/data/sunrgbd/demo_result'
        os.system(command)
        '''

        a = event
        filename = a.key[1].split('/')[-1]
        ex = filename.split('.')[-1]
        
        if  (ex == 'ply'):
            print('===========================')
            print('Receiving ply file Success')
            print('===========================')
            
            # directly translate ply to bin format
            plyfile = PlyData.read(osp.join('/home/yolo/fcaf3d/data/sunrgbd/demo_test', filename))
            d = np.vstack((plyfile['vertex']['x'], plyfile['vertex']['y'], plyfile['vertex']['z']))
            d = np.vstack((d, plyfile['vertex']['red'] / 255.0, plyfile['vertex']['green'] / 255.0, plyfile['vertex']['blue'] / 255.0))
            d = d.T
            d = d.astype('float32')
            file_name = filename.split('.')[0]
        
    
    def on_deleted(self, event): # if file or directory deleted
        pass

    def on_modified(self, event): # if file or directory modified
        pass



w = Target()
w.run()

