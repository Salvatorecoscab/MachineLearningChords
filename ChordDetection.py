
import random
import cv2
import numpy as np
from ultralytics import YOLO
import threading
import os
import argparse
detect_params = None
DP = None
frame = None
done = True
newClass = None
def predict_on_image(model, frame):
    global detect_params
    global DP
    global done
    # Predict on image
    detect_params = model.predict(source=[frame], conf=0.45, save=False)
    # Convert tensor array to numpy
    DP = detect_params[0].numpy()
    done = True

def detect_chords(source):
    # acordes
    global detect_params
    global frame
    global done
    global newClass

    class_list = ['A', 'Am', 'B7', 'Bm', 'C', 'D', 'D7','Dm', 'Em', 'F', 'G']
    images_list = ['A.png', 'Am.png', 'B7.png', 'Bm.png', 'C.png', 'D.png', 'D7.png','Dm.png', 'Em.png', 'F.png', 'G.png']
    path = os.getcwd()
    imagesDir = os.path.join(path, "ChordImages")
    images_list = [os.path.join(imagesDir, im) for im in images_list]
    # Generate random colors for class list
    detection_colors = []
    for i in range(len(class_list)):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        detection_colors.append((b, g, r))

    # load a pretrained YOLOv8n model
    model = YOLO("detect.pt", "v8")

    # Vals to resize video frames | small frame optimise the run
    frame_wid = 640
    frame_hyt = 640

    # open the webcam
    cap = cv2.VideoCapture(source)
    # cap = cv2.VideoCapture("/Users/salvatorecoscab/Downloads/IMG_0043.MOV")

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # flip the frame
        # frame = cv2.flip(frame, 1)

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        if done:
            thread = threading.Thread(target=predict_on_image, args=(model,frame,))
            thread.start()
            done=False
        try:
            # detect one box
            boxes= detect_params[0].boxes
            box = boxes[0]
            clsID = box.cls.numpy()[0]
            conf = box.conf.numpy()[0]
            bb = box.xyxy.numpy()[0]

            cv2.rectangle(
                frame,
                (int(bb[0]), int(bb[1])),
                (int(bb[2]), int(bb[3])),
                detection_colors[int(clsID)],
                3,
            )
            # Display class name and confidence
            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(
                    frame,
                    class_list[int(clsID)],
                    (int(bb[0]), int(bb[1]) - 10),
                    font,
                    1,
                    (255, 255, 255),
                    2,
                )
            newClass = clsID
            
        except:
            pass
        if newClass is not None:
            # Load the image to overlay
            overlay_image = cv2.imread(images_list[int(newClass)])
            # Resize overlay image to desired size
            resized_overlay = cv2.resize(overlay_image, (250, 500))

            # Get the dimensions of the resized overlay
            overlay_height, overlay_width, _ = resized_overlay.shape

            # Define the position for top right placement
            top_right_x = frame.shape[1] - overlay_width
            top_right_y = 0
            # combined_frame=cv2.flip(combined_frame,1)
            # Overlay the resized image onto the frame at the defined position
            combined_frame = frame.copy()
            combined_frame[top_right_y:top_right_y + overlay_height, top_right_x:top_right_x + overlay_width] = resized_overlay
        else:
            combined_frame = frame.copy()

        # Display the resulting frame
        
        cv2.imshow("ObjectDetection", combined_frame)
        
        # Terminate run when "Q" pressed
        if cv2.waitKey(1) == ord("q"):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chord Detection')
    parser.add_argument('--source', type=str, default='webcam',
                        help='Path to the video or image file. If not provided, it uses webcam.')
    args = parser.parse_args()

    if args.source == 'webcam':
        detect_chords(0)
    else:
        detect_chords(args.source)