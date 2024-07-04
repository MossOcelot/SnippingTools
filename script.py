from PIL import ImageGrab

import cv2
import numpy as np
import os
# ตัวแปรเก็บตำแหน่งมุมซ้ายบนและขวาล่าง
start_point = None
end_point = None
drawing = False

# ฟังก์ชัน callback สำหรับการวาดสี่เหลี่ยม
def drawing_rectangle(event, x, y, flags, param):
    global start_point, end_point, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)
        end_point = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            end_point = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_point = (x, y)

def capture_screen():
    screen = ImageGrab.grab()
    screen_np = np.array(screen)
    screen_np = cv2.cvtColor(screen_np, cv2.COLOR_BGR2RGB)

    return screen_np

def draw_rectangle(image, top_left, bottom_right, color=(0, 255, 0), thickness=2):
    cv2.rectangle(image, top_left, bottom_right, color, thickness)
    return image

def croppedimage(image, top_left, bottom_right):
    top_x, top_y = top_left
    bottom_x, bottom_y = bottom_right

    return image[top_y:bottom_y, top_x:bottom_x]

def main():
    global start_point, end_point
    cv2.namedWindow('Screen')
    cv2.setMouseCallback('Screen', drawing_rectangle)

    while True:
        screen_image = capture_screen()

        top_left = (285, 101)
        bottom_right = (1856, 1012)
        
        # if start_point and end_point:
        #     cv2.rectangle(screen_image, top_left, bottom_right, (0, 255, 0), 2)

        screen_imaged = draw_rectangle(screen_image.copy(), top_left, bottom_right)
        cropped_image = croppedimage(screen_image, top_left, bottom_right)
        screen_imaged = cv2.resize(screen_imaged, (720, 480))
        cropped_imaged = cv2.resize(cropped_image.copy(), (540, 360))
        cv2.imshow("Screen", screen_imaged)
        cv2.imshow("CroppedImage", cropped_imaged)
        
        if cv2.waitKey(1) & 0xFF == ord('c'):
            print("Captured")
            folders = os.listdir("./datasets")
            print(len(folders))
            cv2.imwrite(f"./datasets/picture{len(folders) + 1}.jpg", cropped_image, [cv2.IMWRITE_JPEG_QUALITY, 100])

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()