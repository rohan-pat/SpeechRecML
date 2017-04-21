import os
import subprocess
import scipy.io.wavfile

path = "/Users/Rohan/Documents/Studies/Spring2017/ML/ProjectCode/SpeechRecML/preprocessing/speech-dev"

print("Start")
for f in os.listdir(path):
    if f != ".DS_Store":
        f1 = os.path.join(path, f)
        # if os.path.isfile(f1):
        #     print(f1)
        if os.path.isdir(f1):
            if f1 == ".DS_Store":
                continue
            # print("dir->", end="")
            # print(f1)
            for f2 in os.listdir(f1):
                if f2 == ".DS_Store":
                    continue
                # print("subdir->", end="")
                f3 = os.path.join(f1, f2)
                # print(f3)
                # subprocess.call("rm -f *.flac", shell=True)
                for f4 in os.listdir(f3):
                    # print("subsubdir->", end="")
                    # print(f4)
                    f5 = os.path.join(f3, f4)
                    if f5.endswith("wav"):
                        f6 = f5.replace(".wav","-op1.txt")
                        wFile = scipy.io.wavfile.read(f5)
                        wav_array = wFile[1][100:110]
                        print(wav_array)
                        f7 = open(f6,"r")
                        for line in f7:
                            line = line.strip()
                            print(line)
                        # key id.
                        f8 = f5.replace(".wav","")
                        print(f8)
                        # print(len(wFile[1]))
            # print("------------")
print("finished")
