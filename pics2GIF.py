import imageio
import os
images = []
objectName = str(os.getcwd().split('\\')[int(len(os.getcwd().split('\\'))) - 1])

def main():
    print "Running script..."
    for n in xrange(0,37,1):
        location = str(os.getcwd())
        fileName = location + '\phase_' + str(n * 10)+'.png'
        images.append(imageio.imread(fileName))
    imageio.mimsave(location+'\\'+objectName+'.gif', images)
    print objectName+'.gif was created successfully!'
    raw_input('To exit press ENTER')

if __name__ == "__main__":
    main()
