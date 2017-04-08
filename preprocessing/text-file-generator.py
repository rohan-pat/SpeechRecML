import os
import subprocess

path = "/Users/Rohan/Documents/Studies/Spring2017/ML/ProjectCode/preprocessing/speech-dev"

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
                for f4 in os.listdir(f3):
                    if f4.endswith(".trans.txt"):
                        # print("subsubdir->", end="")
                        print(f4)
                        f5 = os.path.join(f3, f4)
                        with open(f5, "r") as trans_txt:
                            for lines in trans_txt:
                                text = lines.split(" ")
                                print(text[0],end="->")
                                fileName = os.path.join(f3, text[0]+".txt")
                                # print(fileName)
                                s = " sp ".join(text[1:])
                                with open(fileName, "w") as writer:
                                    writer.write(s)
                    # if f5.endswith(".flac"):
                    #     f6 = f5.replace("flac","wav")
                    #     args = "ffmpeg -i " + f5 + " " + f6
                    #     # print(args)
                    #     subprocess.call(args, shell=True)
            # print("------------")
print("finished")
