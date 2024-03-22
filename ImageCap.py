import cv2
from PIL import Image
import os

class CaptureImg :

    def save_image(self, image, name):
        directory = f"Images/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = f"{directory}/{name}.jpg"  # Corrected filename path
        image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # Convert to PIL Image
        image_pil.save(filename)
        print(f"Image saved at: {filename}")
        return True
    def capture_image(self):
        name = input("Enter the name of the person : ")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return
        while True:
            ret, frame = cap.read()
            cv2.imshow('Capturing', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):  # Press 's' to capture the image
                print(f"Saved {name}.jpg")
                break
            elif key == 27:  # Press Esc to exit without saving
                break

        cap.release()
        cv2.destroyAllWindows()
        if self.save_image(frame, name=name):
            print("Image saved successfully")


if __name__ == "__main__":
    capture = CaptureImg()
    capture.capture_image()