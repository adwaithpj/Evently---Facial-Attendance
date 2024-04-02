from encoder_cpu_pool import Encoder1
from encoder import Encoder
from faceRecognizer import FaceRecognition
import time

if __name__ == "__main__":
    # start_time = time.time()
    # encoder = Encoder1()
    # encoder.load_images()
    # encoder.findEncoding(encoder.imgList)
    # encoder.pickle_data('test_3')
    # end_time = time.time()
    #
    # elapsed_time = end_time - start_time
    # print(elapsed_time)
    #
    start_time = time.time()
    reco =FaceRecognition('6609419e257ab3e8dc733974')
    reco.recognize_face()
    end_time = time.time()
    print(start_time - end_time)