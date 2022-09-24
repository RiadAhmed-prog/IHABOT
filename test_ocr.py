import numpy as np
import cv2 as cv
from paddleocr import PaddleOCR,draw_ocr
# from video_stream import WebcamVideoStream

# ocr = PaddleOCR(use_angle_cls=True, lang='en')
# cap = WebcamVideoStream("http://192.168.55.26:4747/video").start()

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

cap = cv.VideoCapture(1)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret,frame = cap.read()
    frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)
    frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #
    # # print(contours)
    # # frame = cv.drawContours(frame, [contours], 0, (0, 255, 0), 3)
    # # frame = cv.medianBlur(frame, 5)
    # # if frame is read correctly ret is True
    # if not ret:
    #     print("Can't receive frame (stream end?). Exiting ...")
    #     break
    # edged = cv.Canny(gray, 0, 180)
    #
    # # Finding Contours
    # # Use a copy of the image e.g. edged.copy()
    # # since findContours alters the image
    # contours, hierarchy = cv.findContours(edged,
    #                                        cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    #
    # # Our operations on the frame come here
    # # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # # h3 = cv.adaptiveThreshold(frame, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
    # #                           cv.THRESH_BINARY, 5, 2)
    # try:
    #
    #     contours = contours[0] if len(contours) == 4 else contours[1]
    #     for cnt in contours:
    #         # x, y, w, h = cv.boundingRect(cnt)
    #         rect = cv.minAreaRect(cnt)
    #         approx = cv.contourArea(cnt)
    #         # print(approx)
    #         box = cv.boxPoints(rect)
    #         box = np.int0(box)
    #         cv.drawContours(frame, [box], 0, (0, 0, 255), 2)
    #
    #     cv.drawContours(frame, contours, -1, (0, 255, 0), 3)
    # except Exception as e:
    #     print(e)
    #cv.imshow('edged', edged)
    try:

        result = ocr.ocr(frame, cls=True)
        boxes = [res[0] for res in result]
        # print(boxes)
        texts = [res[1][0] for res in result]
        print(texts)
        count=0
        digit_at=[]
        for text in texts:
            if has_numbers(text):
                digit_at.append(count)
            count +=1

        print(digit_at)

        digit_bbox=[]
        y_list=[]
        for digit in digit_at:
            digit_bbox.append(boxes[digit])
            y_list.append(boxes[digit][0][0])

        try:

            text_bbox=[]

            print("list",sorted(y_list, key = lambda x:float(x)))
            data=[]
            if len(sorted(y_list, key = lambda x:float(x)))==3:

                for l in sorted(y_list, key = lambda x:float(x)):
                    ind= y_list.index(l)

                    text_bbox.append(texts[ind])
                    data.append(texts[ind])
                # print("y_list: ",text_bbox)
        except:
            pass

        scores = [res[1][1] for res in result]
        font_path = 'latin.ttf'
        frame = draw_ocr(frame, boxes, texts, scores, font_path='latin.ttf')
    except Exception as e:
        print(e)
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
