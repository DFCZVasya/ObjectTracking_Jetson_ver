import sys
from get_params import GetArguments
from yolodetect import yolodetect

def get_params():
    _defaults = {
        "-mp": 'model_data/yolo-tiny.h5',
        "-ap": 'model_data/tiny_yolo_anchors.txt',
        "-cp": 'model_data/coco_classes.txt',
        "score" : 0.3,
        "iou" : 0.45,
        "model_image_size" : (416, 416),
        "-gpnum" : 1,
        "-i":"input/outfile.webm",
        "-o":"output/outfile.avi",
    }

    arg = sys.argv

    arg = GetArguments(arg)
    for a in _defaults:
        arg.add_default(a, _defaults[a])

    arg.update_values()
    i, o = arg.get_io_params()
    return arg.get_other_params(), i , o 


def main(dnn_params, input, output):
    print("start main")
    #print(dnn_params, input, output)
    if "yolo" in dnn_params["-mp"]:
        yolodetect(dnn_params, input, output)
    else:
        pass




if __name__ == "__main__":
    dnn_params, input, output = get_params()
    main(dnn_params, input, output)
