import numpy
import os
import matplotlib.pyplot as plt
import py_compile

def convert(): # Finds the parameters in torder to calculate the whole MEMS Amplitude
# Runing the Minimum function and saving the output into 3 parameters
    location = str(os.getcwd()) + '\\Amplitudes.txt'
    rows = 480
    columns = 640
    figure = plt.figure()

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
    objectName = str(os.getcwd().split('\\')[int(len(os.getcwd().split('\\'))) - 1])
    figure.suptitle("Amplitude"+objectName)
    cbar = figure.colorbar(axes.imshow(image, cmap='hot'),  orientation='vertical')
    # cbar.ax.set_yticklabels(['Low', 'Medium', 'High'])  # vertical colorbar
    plt.savefig(str(os.getcwd()) + "Amplitude"+objectName + '.png')
    plt.clf()
    print "* * * Success! * * *\n"
    raw_input("To Exit Hit 'Enter'\n")

if __name__=='__main__':
    print "Hello\n"
    raw_input("To Start Hit 'Enter'\n")
    convert()
    py_compile.compile('txt2pic2.py')

