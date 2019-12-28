# ObjectTracking Jetson version
## Created for training on Nvidia Jetson TX1/nano
_________________
To start work you need to download the project:
```
$ git clone https://github.com/DFCZVasya/ObjectTracking_Jetson_ver.git
$ cd ObjectTracking_Jetson_ver
```
After downloading the project you need to install all the necessary libraries. 
 - For Jetson TX1:
```
$ chmod +x ./MakeFileTX1
$ ./MakeFileTX1
```
 - For Jetson nano:
 ```
$ chmod +x ./MakeFilenano
$ ./MakeFilenano
```
If errors occur during the execution of the file try to enter all the lines from MakeFile in turn:

Weights for tiny yolo is already in project. 
But if you want to test big yolo, you can download weights from: https://drive.google.com/open?id=1P2WuPcOaWAajFZFw09TnZWdwb4DecIzT in model_data dir.
_____________________________
For run the stream detection with tiny yolo model you need to write next command in terminal:
```
$ python3 main.py -i cam
```

Other aguments:
```
-i [path to file or cam for stream detect (default - 'input/outfile.webm')]
-o [path to output file (default - 'output/outfile.avi')]
-mp [path to model (default - 'model_data/yolo-tiny.h5')]
-ap [path to anchors (default - 'model_data/tiny_yolo_anchors.txt')]
-cp [path to classes (default - "-cp": 'model_data/coco_classes.txt')]
```

Dont forget to do pull request until working, I am constantly trying to improve the program and add new models, as well as fix bugs.
You can write me on my mail if you found bugs : loopatkin.2002@gmail.com
