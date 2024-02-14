from argparse import ArgumentParser
from plyfile import PlyData
import numpy as np

def main():
    
    parser = ArgumentParser()
    parser.add_argument('pcd', help='Point cloud file')
    args = parser.parse_args()
    plyfile = PlyData.read(args.pcd)
    d = np.vstack((plyfile['vertex']['x'], plyfile['vertex']['y'], plyfile['vertex']['z']))
    d = np.vstack((d, plyfile['vertex']['red'] / 255.0, plyfile['vertex']['green'] / 255.0, plyfile['vertex']['blue'] / 255.0))
    d = d.T
    d = d.astype('float32')
    file_name = args.pcd.split('.')[0]
            
    d.tofile(file_name + '.bin')
    

if __name__ == '__main__':
    main()
