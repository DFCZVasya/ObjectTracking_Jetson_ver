import sys
from PIL import Image
from yolo import YOLO
from imutils.video import VideoStream
from imutils.video import FPS
import time
import cv2
import os
import glob
import imutils

def yolodetect(dnn_params, input, output):
    files = glob.glob('output/*.png')
    for f in files:
	    os.remove(f)

    if input == 'cam':
        vs = VideoStream(src=1).start() #or 1
        time.sleep(2.0)
        fps = FPS().start()
        w = int(vs.get_width())
        h = int(vs.get_height())
        yolo = YOLO(dnn_params["-mp"], dnn_params["-ap"], dnn_params["-cp"])
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out= cv2.VideoWriter(output, fourcc, 30, (w , h), True)
        currentFrame = 0

        while True:
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width=400)
            image = Image.fromarray(frame)
            # loop over the detections
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

            # show the output frame
            cv2.imshow("Frame", frame)
            frame = imutils.resize(frame, width=w)
            out.write(frame)
            currentFrame += 1

            key = cv2.waitKey(1) & 0xFF
            
            fps.stop()
            #print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
            print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

            # update the FPS counter
            fps.update()

        # stop the timer and display FPS information
        fps.stop()
        out.release()
        print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

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