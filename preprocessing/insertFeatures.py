# from __future__ import print_function
import os
import re
import subprocess
from dbInsert import DBOperation
import scipy.io.wavfile
import librosa
import numpy as np
# from scikits.talkbox.features import mfcc

path = "/Users/Push/Documents/SpeechRecML/preprocessing/speech-dev"

dbOp = DBOperation()
print("Start")
# for f in os.listdir(path):
#     if f != ".DS_Store":
#         f1 = os.path.join(path, f)
#         # if os.path.isfile(f1):
#         #     print(f1)
#         if os.path.isdir(f1):
#             if f1 == ".DS_Store":
#                 continue
#             # print("dir->", end="")
#             # print(f1)
#             for f2 in os.listdir(f1):
#                 if f2 == ".DS_Store":
#                     continue
#                 # print("subdir->", end="")
#                 f3 = os.path.join(f1, f2)
#                 # print(f3)
#                 # subprocess.call("rm -f *.flac", shell=True)
#                 for f4 in os.listdir(f3):
#                     # print("subsubdir->", end="")
#                     # print(f4)
#                     f5 = os.path.join(f3, f4)
#                     if f5.endswith("wav"):
#                         f6 = f5.replace(".wav","-op1.txt")
#                         wFile = scipy.io.wavfile.read(f5)
#                         wav_array = wFile[1]
#                         f7 = open(f6,"r")
#                         f8 = f5.replace(".wav","")
#                         pathArr = f8.split('/')
#                         key = pathArr[len(pathArr)-1]
#                         sentArr = []
#                         tempArr = []
#                         cepsArr = []
#                         for line in f7:
#                             line = line.strip()
#                             lineArr = line.split('-')
#                             word = re.sub('[\"]+', '', lineArr[0])
#                             intervals = lineArr[1].split(',')
#                             start = float(intervals[0])*16000
#                             end = float(intervals[1])*16000
#                             wordArr = wav_array[int(start):int(end)]
#                             ceps = librosa.feature.mfcc(y=wordArr, sr=16000, hop_length=20480, n_mfcc=13)
#                             sentArr.append(word)
#                             cepsArr.append(ceps.tolist())
#                             #tempArr.append(wordArr.tolist())
#                         sent = ' '.join(sentArr)
#                         # dbOp.insertFeatureData(key, sent, cepsArr)
#                         # dbOp.insertRawData(key, sent, tempArr)
#                         # print(len(wFile[1]))
#             # print("------------")
print("finished")
