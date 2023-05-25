import matplotlib.pyplot as plt
import json
import time

import numpy as np
from scipy import stats
from score import Score
from subject import Subject
from utils import Utils
import warnings
warnings.filterwarnings("ignore")


class Train:
    def __init__(self):
        subject = Subject()
        # get all subjects
        self.subjects = subject.subjects
        # print(self.subjects)
        self.results = {
            "data": [],
            "number_of_data": 0,
            "time_train": 0
        }
        #current time
        self.start_time = time.time()
        print("Start train time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.start_time)))
        #progress bar
        self.utils = Utils()
        self.number_of_progress = len(self.subjects) * len(self.subjects);
        self.index_progress = 0

    
    def start(self):
        for name_subject_y in self.subjects:
            for name_subject_x in self.subjects:
                a = Score()
                a.train(name_subject_x, name_subject_y)
                self.results['number_of_data'] = a.number_of_file;
                x = a.x
                y = a.y
                
                slope, intercept = 0, 0
                try:
                    slope, intercept, r, p, std_err = stats.linregress(x, y)
                    # check slope is Nan
                    if np.isnan(slope) or np.isnan(intercept):
                        slope, intercept = 0, 0
                except:
                    slope, intercept = 0, 0
                # if name_subject_x == "Tin học đại cương" and name_subject_y == "Cấu trúc dữ liệu và giải thuật":
                #     print(x, y)
                #     print(slope, intercept)
                self.results['data'].append({
                    'name_subject_x': name_subject_x,
                    'name_subject_y': name_subject_y,
                    'slope': slope,
                    'intercept': intercept,
                    'x': x,
                    'y': y
                })

                self.index_progress += 1
                self.utils.printProgressBar(self.index_progress, self.number_of_progress, prefix = ' Progress:', suffix = 'Complete', length = 50)
        #current time
        self.end_time = time.time()
        self.results['time_train'] = self.end_time - self.start_time
        timestr = time.strftime("%Y%m%d-%H%M%S")
        with open("result/" + str(timestr) + ".json","w", encoding='utf-8') as jsonfile:
            json.dump(self.results, jsonfile,ensure_ascii=False)

        print("End train time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.end_time)))
        print("Result file: ", self.utils.getLocation('./result') + "\\result\\" + str(timestr) + ".json")


train = Train()
train.start()
