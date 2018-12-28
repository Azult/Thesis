import numpy
import os
import matplotlib.pyplot as plt

def convert(): # Finds the parameters in torder to calculate the whole MEMS Amplitude
# Runing the Minimum function and saving the output into 3 parameters
    location = str(os.getcwd())
    rows = 480
    columns = 640
    figure = plt.figure()
    for n in xrange(0,37,1):
        location = str(os.getcwd()) + '\phase_' + str(n * 10)
        print 'Loading' + str(os.getcwd()) + '\phase_' + str(n * 10)
        if (not os.path.isfile(location)):
            raw_input("File Does not exist, the program will be terminated.\n"
                      "To Exit Please Hit 'Enter'\n")
            return
        frame = numpy.loadtxt(location)
        if(not frame.size == rows * columns):
            raw_input("File pixel size mismatch, the program will be terminated.\n"
                     "To Exit Please Hit 'Enter'\n")
            return
        image = numpy.reshape(frame, (rows, columns))
        axes = figure.add_subplot(1, 1, 1)
        axes.imshow(image, cmap='hot')
        figure.suptitle('Phase = ' + str(n * 10))
        cbar = figure.colorbar(axes.imshow(image, cmap='hot'),  orientation='vertical')
        # cbar.ax.set_yticklabels(['Low', 'Medium', 'High'])  # vertical colorbar
        print 'Converting' + str(os.getcwd()) + '\phase_' + str(n * 10)
        plt.savefig(str(os.getcwd()) + '\phase_' + str(n * 10) + '.png')
        plt.clf()
    print "* * * Success! * * *\n"
    raw_input("To Exit Hit 'Enter'\n")


if __name__=='__main__':
    print "Hello\nThis script converts the txt data into a png images\n" \
          "In order it to work you have to put this file\nin the same folder " \
          "with the txt files.\nThe txt files must have the next criterions:\n" \
          "1. Name: 'pahse_##', for example: phase_10 or phase_230\n" \
          "2. Size: 640 X 480\n" \
          "3. 37 images in total - phase 0 to 360 in jumps of 10\n" \
          "Good Luck!\n"
    raw_input("To Start Hit 'Enter'\n")
    convert()
