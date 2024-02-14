## Using FCAF3D for 3D Apple detection

> **FCAF3D: Fully Convolutional Anchor-Free 3D Object Detection**<br>
> [FCAF3D] (https://github.com/SamsungLabs/fcaf3d)


<p align="center">
  <img src="https://github.com/joshiaLee/3D_Object_Detection/assets/93809073/2278455e-af2a-416b-93c7-c0b2be09e397" alt="img1" width="50%"/>
</p>

<p align="center">
  <img src="https://github.com/joshiaLee/3D_Object_Detection/assets/93809073/e731a6f3-4511-441a-b3f9-7b0f6fef05d1" alt="img2" width="50%"/>
</p>



### Installation
For convenience, Docker is available [Dockerfile](docker/Dockerfile).

**create bin file**
```shell
python tools/create_data.py sunrgbd --root-path ./data/sunrgbd --out-dir ./data/sunrgbd --extra-tag sunrgbd
```

**Training**
```shell
python tools/train.py configs/fcaf3d/fcaf3d_sunrgbd-3d-10class.py
```



