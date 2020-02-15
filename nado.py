import jetson.inference
import jetson.utils

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.4)
camera = jetson.utils.gstCamera(1280, 720, "0")
display = jetson.utils.glDisplay()

while display.IsOpen():
	img, width, height = camera.CaptureRGBA()
	detections = net.Detect(img, width, height)
	for d in detections:
		print(d.ClassID)
		print(int(d.Left))
		print(int(d.Top))
		print(int(d.Right))
		print(int(d.Bottom))
		print(d.Center)
	display.RenderOnce(img, width, height)
	display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
