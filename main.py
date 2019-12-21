import sys
from get_params import GetArguments

def get_params():
    _defaults = {
        "model_path": 'model_data/yolo-tiny.h5',
        "anchors_path": 'model_data/tiny_yolo_anchors.txt',
        "classes_path": 'model_data/coco_classes.txt',
        "score" : 0.3,
        "iou" : 0.45,
        "model_image_size" : (416, 416),
        "gpu_num" : 1,
    }

    arg = sys.argv

    arg = GetArguments(arg)
    for a in _defaults:
        arg.add_defaults(a, _defaults[a])

    arg.update_values()


def main(model, anchors, input, output):
    pass



if __name__ == "__main__":
    main()
