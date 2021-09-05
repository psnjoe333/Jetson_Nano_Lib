
##htop
#htop is a useful tool to see the CPU, GPU status of Jetson nano, and also provide the installed libraries

sudo apt-get install python-pip python-dev build-essential
sudo pip install --upgrade pip
sudo -H pip install jetson-stats
sudo jtop

## Camera test
nvgstcapture-1.0

gst-launch-1.0 nvarguscamerasrc sensor_id=0 ! 'video/x-raw(memory:NVMM),width=3280, height=2464, framerate=21/1, format=NV12' ! nvvidconv flip-method=2 ! 'video/x-raw, width=816, height=616' !   nvvidconv ! nvegltransform ! nveglglessink -e

## Yolo test (should install darknet first)
cd darknet

./darknet detector demo cfg/coco.data cfg/yolov3-tiny.cfg yolov3-tiny.weights "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=30/1 ! nvvidconv flip-method=2 ! video/x-raw, width=1280, height=720, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink"

##Jetson nano pin config:

sudo /opt/nvidia/jetson-io/jetson-io.py