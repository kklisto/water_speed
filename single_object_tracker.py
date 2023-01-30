import argparse
import cv2
import sys
import numpy as np

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
print(cv2.__version__)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Read video file')
    parser.add_argument('video', help='input video filename')
    parser.add_argument(
        "--out",
        default="out",
        help="Output name",
        type=str,
    )
    args = parser.parse_args()

    # Set up tracker.
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE']
    tracker_type = tracker_types[6]

    if int(major_ver) < 4 and int(minor_ver) < 3:
        tracker = cv2.legacy.TrackerMOSSE_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'CSRT':
            tracker = cv2.TrackerCSRT_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.legacy.TrackerMOSSE_create()
            

    # Read video
    video = cv2.VideoCapture(args.video)

    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()

    # Define an initial bounding box
    bbox = (287, 23, 86, 320)

    # Uncomment the line below to select a different bounding box
    bbox = cv2.selectROI(frame, False)

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)

    POS = (int(bbox[0]), int(bbox[1]))

    img_array = []
    out = cv2.VideoWriter(args.out+'.mp4',cv2.VideoWriter_fourcc(*'XVID'), 30, (frame.shape[1],frame.shape[0]))

    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            #cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        # Display tracker type on frame
        #cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);

        # Display FPS on frame
        #cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

        # Correct bbox position in frame by shifting columns and rows
        diffx = POS[0]-p1[0]
        diffy = POS[1]-p1[1]
        if (diffx>0):
            frame[:,frame.shape[1]-diffx-1:,:] = 0
        else:
            frame[:,:abs(diffx),:] = 0
        if (diffy>0):
            frame[frame.shape[0]-diffy-1:,:,:] = 0
        else:
            frame[:abs(diffy),:,:] = 0
        diffy = POS[1]-p1[1]
        frame = np.roll(frame,diffx,axis=1)
        frame = np.roll(frame,diffy,axis=0)

        # Display result
        cv2.imshow("Tracking", frame)
        img_array.append(frame)

        # Exit if ESC pressed
        key = cv2.waitKey(5)
        if key == ord('e'):
            break

    for i in range(len(img_array)):
        out.write(img_array[i])

    out.release()
    print(args.out+".mp4 file created")
    
cv2.destroyAllWindows()
