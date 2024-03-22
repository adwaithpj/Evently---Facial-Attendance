import os
import cv2
import face_recognition
import pickle
from loading_display import loading_bar
import multiprocessing as mp

# Importing Student Images and their ids.
IMAGE_FOLDER_PATH = 'Images'
PICKLED_FILES_DATA_PATH = 'EncodedFiles'
PATH_LIST = os.listdir(IMAGE_FOLDER_PATH)



class Encoder:
    def __init__(self):
        self.imgList = []
        self.studentIds = []
        self.encodingList=[]
        self.encodeList = []
        self.encodeList_withIds = []

    def findEncoding(self,imageList):        # Function for encoding the images
        self.encodingList = []

        for img in imageList:
            try:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                self.encodeList.append(encode)
            except Exception as encodingface:
                print(f'Error in encoding the face {encodingface}')

        print('Encoding Completed')         # Comment out the line -> don't want printing
        return self.encodeList

    def load_images(self):                  # Function for loading images from Images directory
        try:
            for path in PATH_LIST:
                try:
                    self.imgList.append(cv2.imread(os.path.join(IMAGE_FOLDER_PATH, path)))
                    self.studentIds.append(os.path.splitext(path)[0])
                except Exception as e:
                    print(f'Error in loading the image {e}')
        except Exception as e:
            print(f'Error in loading the images {e}')
        print(self.studentIds)              # Comment out the line -> don't want printing


    def pickle_data(self, event_id):        # Function for pickling the data with separate event ID
        self.encodeList_withIds = [self.encodeList, self.studentIds]
        try:
            if not os.path.exists(PICKLED_FILES_DATA_PATH):     # Checking if directory exists
                with open(PICKLED_FILES_DATA_PATH, 'wb'):
                    print('created')
                    pass

            pickle_file_path  =  os.path.join(PICKLED_FILES_DATA_PATH, f'encoded_data_{event_id}.pkl')

            with open(pickle_file_path, 'wb') as f:
                pickle.dump(self.encodeList_withIds, f)
                print(f'Pickled data with event ID {event_id}')  # Comment out the line -> don't want printing
                return True
        except Exception as e:
            print(f'Error in pickling the data: {e}')


