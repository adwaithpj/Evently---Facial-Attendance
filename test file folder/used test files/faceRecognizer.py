import numpy as np
import cv2
import face_recognition
import pickle
import threading
import time

PICKLED_FILE_PATH = '../../assets/EncodedFiles'
global recognize_face

class FaceRecognition:
    def __init__(self,event_ID):
        self.encodedList_withIDS = []
        self.encodeListKnown = []
        self.studentIDs = []
        self.counter = 0
        self.event_id = ''
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        self.encodeCurFrame = []
        self.faceCurFrame = []
        self.face_match = False
        self.last_attendance_time = 0
        self.encodeFace = []


        try:
            threading.Thread(target=self.load_pickle, args=(self.event_id,)).start()
        except Exception as e:
            print(f'Error in loading the encoded files: {e}')


    def load_pickle(self, event_id):
        try:
            with open(f'{PICKLED_FILE_PATH}/encoded_data_{event_id}.pkl', 'rb') as f:
                self.encodedList_withIDS = pickle.load(f)
                print('Encoded file loaded')                # Comment out -> after testing/if you don't want to print
            self.encodeListKnown, self.studentIDs = self.encodedList_withIDS

        except Exception as e:
            print(f'Error in loading the encoded files: {e}')

    def check_face(self,frame):
        print(self.encodeCurFrame)
        print(self.faceCurFrame)
        for encodeFace, faceLoc in zip(self.encodeCurFrame, self.faceCurFrame):
            matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
            print(f'this is matches{matches}')
            print(f' this is face dis{faceDis}')


            matchIndex = np.argmin(faceDis)
            print(f' this is face dis{matchIndex}')
            if matches[matchIndex]:
                    y1,x2,y2,x1 = faceLoc
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    studentIDs = self.studentIDs[matchIndex]   # check database if the student ID is present
                                                                    # have to implement a function here
                    print(f'studentID : {studentIDs}')         # Printing the student ID
                    self.face_match = True
                    print("face matched")
                    return self.face_match
            else:
                    self.face_match = False
                    print('didnt match')
                    return self.face_match


    def recognize_face(self):
        while True:

            check, frame = self.cap.read()
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # img = np.int16(img)
            self.faceCurFrame = face_recognition.face_locations(img)
            print(f'this is faceCurFrame {self.faceCurFrame}')

            if len(self.faceCurFrame) == 0:
                self.counter += 1
                print("Searching")
                cv2.imshow('Face Recognition', frame)


            elif len(self.faceCurFrame) == 1:
                self.encodeCurFrame = face_recognition.face_encodings(img, self.faceCurFrame)  # changes
                print(f'this is encodeCurFrame {self.encodeCurFrame}')
                threading.Thread(target=self.check_face, args= (frame,)).start()

            if self.face_match:
                current_time = time.time()
                if current_time - self.last_attendance_time <= 30:
                    print("Attendance already given")
                else:
                    self.counter = 1
                    self.last_attendance_time = current_time
                    print("Face Matched")
            else:
                print("Face not Matched")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cv2.imshow('Face Recognition', frame)
        cv2.waitKey(1)


        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":

    reco =FaceRecognition('test_2')
    reco.recognize_face()
