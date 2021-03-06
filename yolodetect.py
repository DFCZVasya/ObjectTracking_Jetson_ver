import sys
from PIL import Image
from yolo import YOLO
from imutils.video import VideoStream
import time
import cv2
import os
import glob
import imutils
from resizevideo import take_and_resize
import numpy as np

def yolodetect(dnn_params, input, output):
    files = glob.glob('output/*.png')
    for f in files:
	    os.remove(f)

    if input == 'cam':
        vs = VideoStream(src=0).start() #or 1
        time.sleep(2.0)
        fps = 0
        yolo = YOLO(dnn_params["-mp"], dnn_params["-ap"], dnn_params["-cp"])

        while True:
            start_t = time.time()
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 314 pixels
            frame = vs.read()
            #frame = imutils.resize(frame, width=314)

            #take frame and return square(for wide angle cameras) in the desired resolution default is (314, 314)
            frame = take_and_resize(frame) #here you can also choose your own ouput resolution like take_and_resize(frame, your resolution) 
            
            # loop over the detections
            outBoxes = yolo.detect_image(frame) #Here you can make whatever you want (return[top left x, top left y, bottom right x, bottom right y, class name])
            
            frame = np.asarray(frame)
            if len(outBoxes) > 0:
                for box in outBoxes:
                    # extract the bounding box coordinates
                    (x, y) = (int(box[0]), int(box[1]))
                    (w, h) = (int(box[2]), int(box[3]))
                    bbox = [x, y, w, h, box[4]]
                    cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0,255,0), 2)
                    text = 'classID = {}'.format(box[4])
                    cv2.putText(frame, text, (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)

            # show the output frame
            #frame = imutils.resize(frame, width=500)
            cv2.imshow("Frame", frame)


            key = cv2.waitKey(1) & 0xFF

            fps = 1/(time.time() - start_t)
            #print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
            print("[INFO] approx. FPS: {:.2f}".format(fps))


            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break





        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()
        yolo.close_session()

    else:
        vs = cv2.VideoCapture(input)
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

        yolo = YOLO(dnn_params["-mp"], dnn_params["-ap"], dnn_params["-cp"])
        frameIndex = 0
        while True:
            counter = 0
            start_time = time.time()
            # read the next frame from the file
            (grabbed, frame) = vs.read()
            # if the frame was not grabbed, then we have reached the end
            # of the stream
            if not grabbed:
                break

            image = Image.fromarray(frame)

            outBoxes = yolo.detect_image(image) #Here you can make whatever you want (return[top left x, top left y, bottom right x, bottom right y, class name])

            if len(outBoxes) > 0:
                for box in outBoxes:
                    # extract the bounding box coordinates
                    (x, y) = (int(box[0]), int(box[1]))
                    (w, h) = (int(box[2]), int(box[3]))
                    bbox = [x, y, w, h, box[4]]
                    cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0,255,0), 2)
                    text = 'classID = {}'.format(box[4])
                    cv2.putText(frame, text, (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)

            print("--- %s seconds ---" % (time.time() - start_time))

            cv2.imwrite("output/frame-{}.png".format(frameIndex), frame)

            # check if the video writer is None
            if writer is None:
                # initialize our video writer
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter(output, fourcc, 30,
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
        yolo.close_session()
        writer.release()
        vs.release()
