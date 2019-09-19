import cv2
import sys
import argparse
from detection_boxes import DetectBoxes


def arg_parse():
    """ Parsing Arguments for detection """

    parser = argparse.ArgumentParser(description='Pytorch Yolov3')
    parser.add_argument("--video", help="Path where video is located",
                        default="assets/drone_video_short.mp4", type=str)
    parser.add_argument("--config", help="Yolov3 config file", default="cfg/yolo-drone.cfg")
    parser.add_argument("--weight", help="Yolov3 weight file", default="weights/yolo-drone.weights")
    parser.add_argument("--conf", dest="confidence", help="Confidence threshold for predictions", default=0.5)
    parser.add_argument("--nms", dest="nmsThreshold", help="NMS threshold", default=0.4)
    parser.add_argument("--resolution", dest='resol', help="Input resolution of network. Higher "
                                                      "increases accuracy but decreases speed",
                        default="416", type=str)
    parser.add_argument("--webcam", help="Detect with web camera", default=False)
    return parser.parse_args()


def get_outputs_names(net):
    # names of network layers e.g. conv_0, bn_0, relu_0....
    layer_names = net.getLayerNames()
    return [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]


def main():
    args = arg_parse()

    VIDEO_PATH = args.video if not args.webcam else 0

    print("Loading network.....")
    net = cv2.dnn.readNetFromDarknet(args.config, args.weight)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    print("Network successfully loaded")

    # class names ex) person, car, truck, and etc.
    PATH_TO_LABELS = "cfg/drone.names"

    # load detection class, default confidence threshold is 0.5
    detect = DetectBoxes(PATH_TO_LABELS, confidence_threshold=args.confidence, nms_threshold=args.nmsThreshold)

    # Set window
    winName = 'YOLO-Opencv-DNN'

    try:
        # Read Video file
        cap = cv2.VideoCapture(VIDEO_PATH)
    except IOError:
        print("Input video file", VIDEO_PATH, "doesn't exist")
        sys.exit(1)

    while cap.isOpened():
        hasFrame, frame = cap.read()
        # if end of frame, program is terminated
        if not hasFrame:
            break

        # Create a 4D blob from a frame.
        blob = cv2.dnn.blobFromImage(frame, 1/255, (int(args.resol),int(args.resol)), (0, 0, 0), True, crop=False)

        # Set the input to the network
        net.setInput(blob)

        # Runs the forward pass
        network_output = net.forward(get_outputs_names(net))

        # Extract the bounding box and draw rectangles
        detect.detect_bounding_boxes(frame, network_output)

        # Efficiency information
        t, _ = net.getPerfProfile()
        elapsed = abs(t * 1000.0 / cv2.getTickFrequency())
        label = 'Time per frame : %0.0f ms' % elapsed
        cv2.putText(frame, label, (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)

        cv2.imshow(winName, frame)
        print("FPS {:5.2f}".format(1000/elapsed))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("Video ended")

    # releases video and removes all windows generated by the program
    cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()