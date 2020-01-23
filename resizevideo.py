import sys
from get_params import GetArguments
import cv2
import glob
import os
from PIL import Image

def get_params():
    _defaults = {
        "-w":"314",
        "-h":"314",
        "-i":"",
        "-o":"output/outfile.avi",
    }

    arg = sys.argv

    arg = GetArguments(arg)
    for a in _defaults:
        arg.add_default(a, _defaults[a])

    arg.update_values()
    i, o = arg.get_io_params()
    return arg.get_other_params(), i , o

def main(video_params, i, o):
    vs = cv2.VideoCapture(i)
    writer = None
    try:
        prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
            else cv2.CAP_PROP_FRAME_COUNT
        total = int(vs.get(prop))
        print("[INFO] {} total frames in video".format(total))
    # an error occurred while trying to determine the total
    # number of frames in the video file
    except:
        print("[INFO] could not determine # of frames in video")
        print("[INFO] no approx. completion time can be provided")
        total = -1
    frameIndex = 0
    while True:
        counter = 0
        # read the next frame from the file
        (grabbed, frame) = vs.read()
        # if the frame was not grabbed, then we have reached the end
        # of the stream
        if not grabbed:
            break
        frame = cv2.resize(frame, (int(video_params["-w"]),int(video_params["-h"])))
        cv2.imwrite("output/frame-{}.png".format(frameIndex), frame)

        # check if the video writer is None
        if writer is None:
            # initialize our video writer
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            writer = cv2.VideoWriter(o, fourcc, 30,
                (frame.shape[1], frame.shape[0]), True)
        # write the output frame to disk
        writer.write(frame)

        # increase frame index
        frameIndex += 1

    # release the file pointers
    print("[INFO] cleaning up...")
    files = glob.glob('output/*.png')
    for f in files:
        os.remove(f)
    writer.release()
    vs.release()

def take_and_resize(frame, output_size = 314):
    crop_coords = []
    height = frame.shape[0]
    width = frame.shape[1]
    min_side = min(height, width)
    frame = Image.fromarray(frame)
    if min_side == height:
        crop_coords.append(int((width / 2) - (height /2)))
        crop_coords.append(int((width / 2) + (height /2)))
        frame = frame.crop((crop_coords[0], 0, crop_coords[1], height))
        frame = frame.resize((output_size,output_size),Image.ANTIALIAS)
    else:
        pass
    
    return frame

if __name__ == "__main__":
    a,b,c = get_params()
    main(a,b,c)
