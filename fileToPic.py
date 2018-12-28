from PIL import Image
import numpy as np
import os
import math
import matplotlib.pyplot as plt


def main():
    print "Hello!\n"
    height = 480
    width = 640
    while True:
        fileName = raw_input("Please enter the file name:\n")
        location = str(os.getcwd()) + '\\' + str(fileName)
        if(os.path.exists(location) == False):
            print "This file does not exist"
            continue
        A = np.loadtxt(location)
        figure = plt.figure()
        image = np.reshape(A, (height, width))
        axes = figure.add_subplot(1, 1, 1)
        axes.imshow(image, cmap='hot')
        cbar = figure.colorbar(axes.imshow(image, cmap='hot'), orientation='vertical')
        plt.savefig(str(os.getcwd()) + '\\'+str(fileName)+'.png')
        print "File saved successfully to the name: "+str(fileName)+'.png'
        Q = raw_input("Is there another file you want to convert? (y/n)\n")
        if (str(Q).lower()=='y'):
            continue
        else:
            print "Good bye!"
            break



if __name__ == "__main__":
    main()