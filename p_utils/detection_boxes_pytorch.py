import cv2
from p_utils.utils import non_max_suppression, prep_image
from colors import *
from torch.autograd import Variable
import torch


def get_class_names(label_path):
    with open(label_path, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')
    classes.insert(0, '__background__')
    return classes if classes else None


class DetectBoxes:
    def __init__(self, label_path, conf_threshold=0.5, nms_threshold=0):
        self.classes = get_class_names(label_path)
        self.confThreshold = conf_threshold
        self.nmsThreshold = nms_threshold
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def bounding_box_yolo(self, frame, inp_dim, model):
        img, orig_im, dim = prep_image(frame, inp_dim)
        im_dim = torch.FloatTensor(dim).repeat(1, 2).to(self.device)
        img = img.to(self.device)

        input_imgs = Variable(img)

        with torch.no_grad():
            detections = model(input_imgs)
            detections = non_max_suppression(detections, self.confThreshold, self.nmsThreshold)

        detections = detections[0]
        if detections is not None:
            im_dim = im_dim.repeat(detections.size(0), 1)
            scaling_factor = torch.min(inp_dim / im_dim, 1)[0].view(-1, 1)

            detections[:, [0, 2]] -= ((inp_dim - scaling_factor * im_dim[:, 0].view(-1, 1)) / 2).cpu()
            detections[:, [1, 3]] -= ((inp_dim - scaling_factor * im_dim[:, 1].view(-1, 1)) / 2).cpu()

            detections[:, 0:4] /= scaling_factor.cpu()

            for index, out in enumerate(detections):
                outs = out.tolist()
                left = int(outs[0])
                top = int(outs[1])
                right = int(outs[2])
                bottom = int(outs[3])

                cls = int(outs[-1])
                color = STANDARD_COLORS[(cls + 1) % len(STANDARD_COLORS)]

                self.draw_boxes(frame, self.classes[cls+1], outs[4], left, top, right, bottom, color)


    def draw_boxes(self, frame, class_id, score, left, top, right, bottom, color):
        txt_color = (0, 0, 0)
        if sum(color) < 500:
            txt_color = (255, 255, 255)

        cv2.rectangle(frame, (left, top), (right, bottom), color=color, thickness=3)

        label = '{}%'.format(round((score * 100), 1))
        if self.classes:
            label = '%s %s' % (class_id, label)

        label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        top = max(top, label_size[1])
        cv2.rectangle(frame, (left, top - round(1.5 * label_size[1])),
                      (left + round(1.5 * label_size[0]), top + base_line), color=color, thickness=cv2.FILLED)
        cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color=txt_color, thickness=2)


