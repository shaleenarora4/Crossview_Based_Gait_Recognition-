import cv2
import os
import imutils
import math
import numpy as np
import random

class Features:
    def __init__(self):
        self.distance_list = []
        self.height_list = []
        self.cycleLength = []
        self.width_list = []

    def extractFeatures(self, path):
        sample_image = cv2.imread(path,0)  # here 0 loads the image in grayscale mode 
        
        #First argument is the source image, which should be a grayscale image. Second argument is the threshold value which is used to classify the pixel values. Third argument is the maxVal which represents the value to be given if pixel value is more than (sometimes less than) the threshold value.the fourth argument is describing hwat kind of image we want, thresh_binary gievs a binary image
        # the binary or the thresholded image is stored in thresh
        thresh = cv2.threshold(sample_image, 45, 255, cv2.THRESH_BINARY)[1]
        #contours is a Python list of all the contours in the image,Each individual contour is a Numpy array of (x,y) coordinates of boundary points of the object.
        #RETR_EXTERNAL flag to get the outer most contour of the shape.  ,  cv2.CHAIN_APPROX_SIMPLE does. It removes all redundant points and compresses the contour, thereby saving memory.
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # contours that give the biggest area, give that contour list in c 
        c = max(cnts, key=cv2.contourArea)



        '''
            finds the smallest x-coordinate (i.e., the “west” value) in the entire contour array c  by calling argmin()  on the x-value and grabbing the entire (x, y)-coordinate associated with the index returned by argmin() .

            Similarly, Line 37 finds the largest x-coordinate (i.e., the “east” value) in the contour array using the argmax()  function.

            Lines 39 and 40 perform the same operation, only for the y-coordinate, giving us the “north” and “south” coordinates, respectively.
        '''
        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])

        maximum_y_r = -999
        maximum_x_r = -999

        for i in cnts[0]:
            for k in i:
                if k[1] > 150:  # if y coordinate greater than 150, to avoid getting hand coordinate 
                    if maximum_x_r < k[0]:
                        maximum_x_r = k[0] # to get max x coordinate 
                        maximum_y_r = k[1] # to get corresponding y coordinate of max x obtained above 

        maximum_x_l = maximum_x_r
        maximum_y_l = -999
        for i in cnts[0]:
            for k in i:
                if k[1] > maximum_y_r - 10: # checking y coordinate satisfies 150 condition 
                    if maximum_x_l > k[0]:  # finding put minimum value of x coordinate and storing corresponding y coordinate 
                        maximum_x_l = k[0]  # the leftmost point 
                        maximum_y_l = k[1]

        if maximum_y_l > maximum_y_r:
            b = maximum_y_l
        else:
            b = maximum_y_r
            
        dx2 = (maximum_x_r - extBot[0]) ** 2  
        dy2 = (maximum_y_r - extBot[1]) ** 2
        distance = math.sqrt(dx2 + dy2)
        hgt = b - extTop[1]
        w = extRight[0] - extLeft[0]
        return distance,w,hgt

    def getFeatures(self):
        dist = self.distance_list
        width = self.width_list
        height = self.height_list
        return dist, width, height

    def getcycleLength(self,distance_list):
        index_list = []
        for sub_list in distance_list:
            min_ = sub_list[0]
            trimmed_list = sub_list[:20]
            m = 9999
            index = 0
            for i in range(1, len(trimmed_list)):
                diff = abs(trimmed_list[0] - trimmed_list[i]) # why taken minimum? should't we take maximum??
                if diff < m:
                    m = diff
                    index = i
            index *= 2
            if index > 24:
                index = random.randrange(20, 25)
            if index < 20:
                index = random.randrange(20, 25)
            index_list.append(index)
        return index_list


    def getSubjectPath(self):
#        PATH_SIHOUETTES = "D:\\MINOR_PROJECT\\casia b\\silhouettes"
        PATH_SIHOUETTES="G:\\minor\\casia b\\silhouettes\\silhouette"
#        PATH_VIDEOS = "D:\MINOR_PROJECT\casia b\\videos"
        id = ["{0:03}".format(i) for i in range(1, 25)]
        dist_sub, wid_sub, hgt_sub = [], [], []
        categories = ["bg-01", "bg-02", "cl-01", "cl-02",
                      "nm-01", "nm-02", "nm-03", "nm-04",
                      "nm-05", "nm-06"]
        angle_90 = ["090"]
        print("Starting to extract features of subject ...")
        #003-cl-01-036-001
        #image=G:\minor\casia b\silhouettes\silhouette\003\cl-01\036\003-cl-01-036-001
        for i in range(len(id)):
            print(id[i])
            for j in range(len(categories)):
                # print(categories[j])
                for l in os.listdir(os.path.join(PATH_SIHOUETTES, id[i], categories[j], angle_90[0])):
                    # print(l)
                    dst,wid,hgt = self.extractFeatures(os.path.join(PATH_SIHOUETTES,id[i],categories[j],angle_90[0],l))
                    dist_sub.append(dst)
                    wid_sub.append(wid)
                    hgt_sub.append(hgt)
            self.distance_list.append(dist_sub)
            self.width_list.append(wid_sub)
            self.height_list.append(hgt_sub)
            dist_sub, wid_sub, hgt_sub = [], [], []
        print("Extraction complete ...")

    def getCroppedImage(self, sample_image, width_list_max, height_list_max):
        thresh = cv2.threshold(sample_image, 45, 255, cv2.THRESH_BINARY)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)

        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])

        x = extLeft[0]
        y = extTop[1]

        mid_point = x + width_list_max // 2
        if (extTop[0] < mid_point):
            diff = mid_point - extTop[0]
            x = x - diff
        elif extTop[0] > mid_point:
            diff = extTop[0] - mid_point
            x += diff
        if x < 0:
            x = 0
        elif x > 240:
            x = 240
        cropped = sample_image[y:y + height_list_max, x:x + width_list_max]  # [y_min:y_max,x_min:x_max]
        return cropped

    def getGEI(self,cycles,w,h):
        PATH_SIHOUETTES = "D:\\MINOR_PROJECT\\casia b\\silhouettes"
        PATH_VIDEOS = "D:\MINOR_PROJECT\casia b\\videos"
        GEI_FOLDER = "D:\\MINOR_PROJECT\\Gait Recognition\\src\\gei"
        id = ["{0:03}".format(i) for i in range(1, 25)]
        dist_sub, wid_sub, hgt_sub = [], [], []
        categories = ["bg-01", "bg-02", "cl-01", "cl-02",
                      "nm-01", "nm-02", "nm-03", "nm-04",
                      "nm-05", "nm-06"]
        #image=G:\minor\casia b\silhouettes\silhouette\003\cl-01\036\003-cl-01-036-001
        angles = ["{0:03}".format(i) for i in range(0, 181, 18)] #0,18,36-----------180
        image_stack = []
        print("Starting to save GEI ...")
        for i in range(len(id)):
            gei_image_num = 0
            image_stack = []
            print(id[i])
            for j in range(len(categories)):
                print(categories[j])
                for k in range(len(angles)):
                    count = 1
                    print(angles[k])
                    for l in os.listdir(os.path.join(PATH_SIHOUETTES, id[i], categories[j], angles[k])):
                        image_og = cv2.imread(os.path.join(PATH_SIHOUETTES, id[i], categories[j], angles[k], l))
                        try:
                            image = self.getCroppedImage(cv2.cvtColor(image_og,cv2.COLOR_RGB2GRAY), max(w[i]), max(h[i]))
                        except:
                            continue
                        image = cv2.resize(image,(240,240))
                        if count % cycles[i] != 0:
                            image_stack.append(image)
                            count += 1
                        else:
                            gei_image = np.zeros(image.shape, dtype=np.int)
                            gei_image = np.mean(image_stack, axis=0)
                            gei_image = gei_image.astype(np.int)
                            image_name = "{0:03}".format(i) + "-" + categories[j] + "-" + angles[k] + "-" \
                                         + str(gei_image_num) + '.jpg'
                            cv2.imwrite(os.path.join(GEI_FOLDER, image_name),gei_image)
                            gei_image_num += 1
                            count += 1
                            image_stack = []
            print("Subject {} complete ...".format(i))
            print("Ongoing to next ...")


if __name__ == '__main__':
    f = Features()
    f.getSubjectPath()
    d,w,h = f.getFeatures()
    cycles = f.getcycleLength(d)
    f.getGEI(cycles,w,h)
