import cv2
import pickle
import random
import os



# dataset has greyscale images.240X320X8 i.e 8 is the depth of each pixel. each pixel can store 8bit info. i.e any number between 0-255 can be taken by each pixel 
combined = []

X = []
Y = []

dictionary_angles = {
    "018_X": [], "036_X": [], "054_X": [], "072_X": [], "018_Y": [], "036_Y": [],
    "054_Y": [], "072_Y": [], "090_X": [], "108_X": [], "126_X": [], "144_X": [],
    "162_X": [], "180_X": [], "090_Y": [], "108_Y": [],"126_Y": [], "144_Y": [],
    "162_Y": [], "180_Y": [], "000_X": [], "000_Y": []
}

#GEI_PATH = "D:\\MINOR_PROJECT\\Gait Recognition\\src\\gei"
GEI_PATH="G:\\minor\\casia b\\silhouettes\\silhouette"



print("Reading Images ...")
#This method returns a list containing the names of the entries in the directory given by path.

for l in os.listdir(GEI_PATH):  # is giving all items in that path's info in a list 
    print(l)
    #l=003-cl-01-036-001
    #image=G:\minor\casia b\silhouettes\silhouette\003\cl-01\036\003-cl-01-036-001
    image = cv2.imread(os.path.join(GEI_PATH,l))
    id = "{0:03}".format(int(l.split("-")[0]) + 1) # adding 1 to subject name 
    angle = l.split("-")[3]
    if angle == "000":
        dictionary_angles[angle + "_X"].append(image) # image=  contain the image of that folder 
        dictionary_angles[angle + "_Y"].append(id)    # id = subject_id i.e 003+1 -> 004
    elif angle == "018":
        dictionary_angles[angle + "_X"].append(image)
        dictionary_angles[angle + "_Y"].append(id)
    elif angle == "036":
        dictionary_angles[angle + "_X"].append(image)
        dictionary_angles[angle + "_Y"].append(id)
    elif angle == "054":
        dictionary_angles[angle + "_X"].append(image)
        dictionary_angles[angle + "_Y"].append(id)
    elif angle == "072":
        dictionary_angles[angle + "_X"].append(image)
        dictionary_angles[angle + "_Y"].append(id)
    elif angle == "090":
        dictionary_angles[angle + "_X"].append(image)
        dictionary_angles[angle + "_Y"].append(id)
    elif angle == "108":
        dictionary_angles[angle + "_X"].append(image)
        dictionary_angles[angle + "_Y"].append(id)
    elif angle == "126":
        dictionary_angles[angle + "_X"].append(image)
        dictionary_angles[angle + "_Y"].append(id)
    elif angle == "144":
        dictionary_angles[angle + "_X"].append(image)
        dictionary_angles[angle + "_Y"].append(id)
    elif angle == "162":
        dictionary_angles[angle + "_X"].append(image)
        dictionary_angles[angle + "_Y"].append(id)
    elif angle == "180":
        dictionary_angles[angle + "_X"].append(image)
        dictionary_angles[angle + "_Y"].append(id)


     combined.append([image, id])

'''     what's the need of finding this sum '''
sum = 0

for i in dictionary_angles:
    sum += len(dictionary_angles[i])
    print(len(dictionary_angles[i]))
print(sum)

print("Shuffling the Data ...")
 random.shuffle(combined)

 for i in combined:
     X.append(i[0])
     Y.append(i[1])

 print(len(X))
 print(len(Y))


'''   X contains images in shuffled form and Y contains it's subsequent subject_id'''
print("Generating Sweet Pickle ...")

#Pickling is a way to convert a python object (list, dict, etc.) into a character stream. The idea is that this character stream contains all the information necessary to reconstruct the object in another python script.
# all in all pickle saves this created 'combined list' ,so that it need not be constructed again and again and can be used as it is
with open('dictionary.pkl', 'wb') as f:
    pickle.dump(dictionary_angles, f)
    f.close()

# with open('Y.pkl', 'wb') as f:
#     pickle.dump(Y, f)
#     f.close()