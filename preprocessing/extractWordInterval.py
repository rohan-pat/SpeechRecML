import os
import subprocess

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
                    if f5.endswith("-op.txt"):
                        f6 = f5.replace("op.txt", "op1.txt")
                        f8 = open(f6,"w")
                        with open(f5, "r") as f7:
                            wordProcessed = False
                            first, second, third = True, True, True
                            text1, text2, text3 = "", "", ""
                            for line in f7:
                                line = line.strip()
                                if line == '"word"':
                                    wordProcessed = True
                                    continue
                                if wordProcessed:
                                    if first:
                                        text1 = line
                                        first = False
                                        second = True
                                    elif second:
                                        text2 = line
                                        second = False
                                        third = True
                                    elif third:
                                        text3 = line
                                        third = False
                                        first = True
                                        if text3 != '"sp"':
                                            if text3.isnumeric():
                                                continue
                                            text = text3 + "-" + text1 + "," + text2 + "\n"
                                            f8.write(text)
                        f8.close()
            # print("------------")
print("finished")
