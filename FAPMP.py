from PIL import Image
import numpy as np
import os
import math
import matplotlib.pyplot as plt
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import timeit
from matplotlib.widgets import Slider, Button, RadioButtons, AxesWidget
import VertSlider
import Tkinter
import sys


def loadSettings(): # This function loads the setting text file that configures the area of calculation.
    global sets
    sets = {}
    location = str(os.getcwd()) + '\settings.txt'
    settings = open(location)
    settings = settings.read().split('\n')

    for line in settings:
        k, v = line.strip().split(' = ')
        sets[k] = int(v)
    print "[*] ",sets

def exclusionChecker():

    # Reload Settings.txt
    location = str(os.getcwd()) + '\settings.txt'
    settings = open(location)
    settings = settings.read().split('\n')
    for line in settings:
        k, v = line.strip().split(' = ')
        sets[k] = int(v)

    location = str(os.getcwd()) + '\\reference'
    referPic = np.loadtxt(location)
    for l in xrange(sets['height']):
        for m in xrange(sets['width']):
            if (isInRadius(l, m, sets['inRadius']) or (isInRadius(l, m, sets['outRadius']) == 0)
                or (l < sets['startRow']) or (l > sets['endRow']) or (m < sets['startClmn']) or (m > sets['endClmn'])):
                referPic[l][m] = 0
    figure = plt.figure()
    image = np.reshape(referPic, (sets['height'], sets['width']))
    axes = figure.add_subplot(1, 1, 1)
    axes.imshow(image, cmap='hot')
    plt.show(axes)


#This functions checks if a dot is in the ignorance radios which is the center of the membrane.
def isInRadius(row,clmn,r):
    a = math.pow(row-(sets['endRow'] + sets['startRow'])/2,2)+math.pow(clmn-(sets['endClmn'] + sets['startClmn'])/2,2)
    if (a <= math.pow(r,2)):
        return 1
    else:
        return 0

# This functions searches for the maximum pixel of all images and returns
# pixels location: Phase and row X colums
def Maximum3D():
    maxx = -30000
    I_row = 0
    I_col = 0
    I_count = 0
    def maxArea(n,l,m):
        for x in xrange(l - 5, l + 5):
            for y in xrange(m - 5, m + 5):
                if (a[n][x][y] <= 0):
                    return 0
        return 1

    for n in xrange(0,37,1):
        for l in xrange(sets['startRow'],sets['endRow']):
            for m in xrange(sets['startClmn'],sets['endClmn']):
                if (isInRadius(l,m,sets['inRadius']) or (isInRadius(l,m,sets['outRadius'])==0)):
                    continue
                elif maxArea(n,l,m) & (a[n][l][m]>maxx):
                    maxx = a[n][l][m]
                    I_row = l
                    I_col = m
                    count = (n)*10

    return I_row, I_col, count


def Reflection(d0,A,f,phase):

    # Everything is in nano meter.

    lambda0 = 660 # Lesser wave length.
    d2 = 3000 # Membrane thikness

    n1 = 1 # Air refractive index
    n2 = 3.8468 # Membrane refraction index (poly-silicon) - for lamda~630nm
    ns = 7 # Refraction index of the membrane's back (copper)
    d1 = d0 + A*math.cos(f+phase)
    k0 = 2*math.pi/lambda0
    k2 = n2*2*math.pi/lambda0
    delta1 = k0*d1
    delta2 = k2*d2

    M1 = np.matrix([[math.cos(delta1), math.sin(delta1) / n1 * 1j], [n1 * math.sin(delta1) * 1j, math.cos(delta1)]])
    M2 = np.matrix([[math.cos(delta2), math.sin(delta2) / n2 * 1j], [n2 * math.sin(delta2) * 1j, math.cos(delta2)]])
    M = np.dot(M2, M1)
    subVector = np.array([1, ns])
    sol = M.dot(subVector)
    r = (sol.item((0, 0)) - sol.item((0, 1))) / (sol.item((0, 0)) + sol.item((0, 1)))
    R = np.absolute(r) * np.absolute(r)
    return R


def R_phase(r):
    sum1 = 0.0
    avg1 = 0.0
    A = 0
    R = []
    f = np.linspace(0,2*math.pi,37)
    min = 10000000
    d0 = 500000   # The d0 of the current MEMS
    phase = 0 # The phase from 0 to 360
    for pp in np.arange(0,2*math.pi,0.1): # pp is the phase between the light and the elcteical/piezo excitation
        R0 = Reflection(d0,0,0,pp)
        for AA in xrange(1,501,1): # This one might have to be changed!
            sum1 = 0.0
            R = []
            for k in xrange(0,37,1):
                R.append(Reflection(d0,AA,f[k],pp))
                sum1 = sum1 + abs(abs((R[k]-R0)/ R0) - r[k])
            avg1 = sum1/37
            if (avg1 < min):
                min = avg1
                A = AA
                phase = pp
    # plt.plot(abs((R[k] - R0) / R0),r)
    # plt.draw()
    # plt.savefig('firsStep',format='png')
    # plt.show(block=False)
    return A, phase, avg1

def R_phase_2(r, pp, GoodAVG):
    sum = 0
    avg = 0
    A = 0
    R = range(0,37,1)
    f = np.linspace(0,2*math.pi,37)
    min = 10000000
    d0 = 500000
    R0 = Reflection(d0,0,0,pp)
    for AA in xrange(1,501,5):
        sum = 0
        for k in xrange(0,37,1):
            R[k] = Reflection(d0, AA,f[k],pp)
            sum = sum + abs(abs((R[k]-R0)/R0) - r[k])
        avg = sum/37
        if (avg<min):
            min = avg
            A = AA
    return int(A), avg

def plotEprox():

    location = str(os.getcwd()) + "\Amplitudes.txt"
    ampload = open(location, 'r')
    AMP = [map(float, line.split(' ')) for line in ampload]

    R = range(0, 37, 1)
    f = np.linspace(0, 2 * math.pi, 37)
    d0 = 500000
    R0 = Reflection(d0,0,0,values["Phase"])
    startColumn = sets['width']/2
    startRow = sets['height']/2
    for k in xrange(0, 37, 1):
        R[k] = Reflection(d0, AMP[startRow][startColumn], f[k], values["Phase"])

    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.25, bottom=0.25)
    l1, l2 = plt.plot(range(0,37),r ,'r--', range(0,37), abs((R-R0)/R0),'b--')
    plt.axis([0, 37, 0, 2])

    axcolor = 'lightgoldenrodyellow'
    column = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
    row = plt.axes([0.15, 0.25, 0.025, 0.65], axisbg=axcolor)

    scolumn = Slider(column, 'Column', 0, sets['width'], valinit=startColumn)
    srow = VertSlider.VertSlider(row, 'Row', 0, sets['height'], valinit=startRow)

    def update(val):
        row = srow.val
        column = scolumn.val
        for k in xrange(0, 37, 1):
            R[k] = Reflection(d0, AMP[int(row)][int(column)], f[k], values["Phase"])

        for i in range(0, 37, 1):
            norm = a[i][int(row)][int(column)] / ref[int(row)][int(column)]
            r[i] = abs(norm)
        l1.set_ydata(r)
        l2.set_ydata(R)
        fig.canvas.draw_idle()

    scolumn.on_changed(update)
    srow.on_changed(update)

    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

    def reset(event):
        scolumn.reset()
        srow.reset()
    button.on_clicked(reset)

    closebt = plt.axes([0.9, 0.95, 0.1, 0.04])
    button2 = Button(closebt, 'Exit', color=axcolor, hovercolor='0.975')
    def close(event):
        plt.close('all')
    button2.on_clicked(close)

    plt.show()


def loadFrames():
    global a
    a = []
# Loading all the image into a 37X480X640 size object
    print "[*]  Loading the frames..."
    for n in xrange(0,37,1):
        location = str(os.getcwd())+'\phase_'+str(n*10)
        a.append(np.loadtxt(location))
        # print "[*] ",str(os.getcwd()) + '\phase_' + str(n * 10)
    print "[*]  Loading colmplete."



def stepOne(): # Finds the parameters in torder to calculate the whole MEMS Amplitude
# Runing the Maximum function and saving the output into 3 parameters
    loadFrames()

    print "[*]   Calculating phase..."
    global values
    values = {}
    # Row of  maximum pixel,  Column of maximum pixel, Frame of the maximum pixel
    values["Row"], values["Column"], values["Frame"] = Maximum3D()
    print "[*] The Pixel is in Phase: "+str(values["Frame"])+\
          " at: "+str(values["Row"])+" X "+str(values["Column"])
    # Loading the reference picture
    location = str(os.getcwd())+'\\reference'
    global ref
    ref = np.loadtxt(location)

    # Create a normlized Sin() function of the extrimum pixel throught all the phases
    global r
    r = []
    for i in range(0,37,1):
        norm =a[i][values["Row"]][values["Column"]]/ref[values["Row"]][values["Column"]]
        r.append(abs(norm))

    global amp_temp, phase_temp, goodAVG
    amp_temp, phase_temp, goodAVG = R_phase(r)
    values["Amplitude"] = amp_temp # Amplitude of the maximum pixel
    values["Phase"] = phase_temp # Phase between the optics and the mechanical excitation


    location = str(os.getcwd()) + '\\calc.txt'
    calc = open(location,"w")
    calc.write("bestAmp = "+str(values["Amplitude"])+"\nphase = "+str(values["Phase"]))


    print "[*] Phase calculation is Complete!"
    print "[*] ",values


def findAmp():
    start = timeit.default_timer()
    print "[*]  Starting amplitude calculation..."
    A = [[0 for x in xrange(sets['width'])] for y in xrange(sets['height'])]
    Errors = [[0 for x in xrange(sets['width'])] for y in xrange(sets['height'])]
    r = range(0,37,1)
    for l in xrange(sets['startRow'],sets['endRow'],1):
        for m in xrange(sets['startClmn'],sets['endClmn'],1):
            if (isInRadius(l, m, sets['inRadius']) or (isInRadius(l, m, sets['outRadius']) == 0)):
                continue
            else:
                r = []
                for k in xrange(0,37,1):
                    norm = a[k][l][m] / ref[l][m]
                    r.append(abs(norm))
                A[l][m], Errors[l][m] = R_phase_2(r, values["Phase"],goodAVG)
        print "[***] Row #"+str(l+1)+" of",sets['startRow'],"to",sets['endRow'],"rows has been completed"
        print "[*] Code ran for ", (timeit.default_timer() - start) / 60, " minutes"
    location = str(os.getcwd())
    np.savetxt(location + '\\Amplitudes.txt',A)
    np.savetxt(location + '\\Errors.txt',Errors)
    figure = plt.figure()
    image = np.reshape(A, (sets['height'], sets['width']))
    axes = figure.add_subplot(1, 1, 1)
    axes.imshow(image, cmap='hot')
    figure.suptitle(objectName)
    cbar = figure.colorbar(axes.imshow(image, cmap='hot'), orientation='vertical')
    plt.savefig(str(os.getcwd()) + '\Amplitudes'+objectName+'.png')

    print "[*] Amplitude calculation is complete!\n"

    end = timeit.default_timer()
    print "[*] Code ran for ",(end-start)/3600," Hours\n"



    # Send me a mail
    fromaddr = "snipped"
    toaddr = "snipped"

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Analysis of "+objectName+" is complete!"

    body = "Hello,\nThis is the out put:"

    msg.attach(MIMEText(body, 'plain'))

    filename = "Amplitudes.png"
    attachment = open(str(os.getcwd()) + '\\Amplitudes'+objectName+'.png', "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "snipped")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)

    print "[*]   Email has been sent"

    server.quit()

# The Program interfane with the user starts here:
def main():
    global objectName
    objectName = str(os.getcwd().split('\\')[int(len(os.getcwd().split('\\'))) - 1])
    print "[*] Object name: "+objectName+'\n'
    global start, end
    loadSettings()
    stepOne()

    top = Tkinter.Tk()

    button1 = Tkinter.Button(top, text='Check\nExclusions', width=25, command=exclusionChecker)
    button1.grid(row=0, column=0)

    button2 = Tkinter.Button(top, text='Calculate\nAmplitude', width=25, command=findAmp)
    button2.grid(row=1, column=0)

    button3 = Tkinter.Button(top, text='Show Reflaction\nApproximation', width=25, command=plotEprox)
    button3.grid(row=2, column=0)

    button4 = Tkinter.Button(top, text='Exit', width=25, command=sys.exit)
    button4.grid(row=3, column=0)

    top.mainloop()

if __name__ == "__main__":
    main()
    print "Done!"
