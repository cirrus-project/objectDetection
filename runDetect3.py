
import cv2
import numpy as np
import sys
import os
import Tkinter as tk
from PIL import Image, ImageTk


def show_frame():
    # read a frame from the movie
    _, frame = cap.read()
    if (np.size(frame)<=1):
        # loop if we hit the end
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        _, frame = cap.read()
    # scale the image to be half the screen height
    sf = float(height/frame.shape[0])
    frame = cv2.resize(frame,(0,0), fx=sf, fy=sf)
    # convert to grayscale and invert if needed
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if ents[0][1].get():
        cv2image = 255-cv2image
    # find all the blobs and draw circles round them
    blobs= blobdetector.detect(cv2image)
    for b in blobs:
        cv2.circle(cv2image, ((int(b.pt[0]), int(b.pt[1]))),4,255,1)
    # use PIL to draw the image in the gui
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

def update(entries):
    # update the blobdetector with the parameters and write to a txt file
    global blobdetector
    params = cv2.SimpleBlobDetector_Params()
    params.filterByColor = False;

    pFileName = FILENAME + '.txt'
    paramFile = open(pFileName, 'w') 
    for entry in entries:
        field = entry[0]
        text  = entry[1].get()
        if field=='Negative':
            continue
        
        if len(str(text)):
            exec("params." + field + "= " + str(text))
            paramFile.write("params." + field + "= " + str(text) + "\n")
    blobdetector = cv2.SimpleBlobDetector_create(params)



def makeform():
    ## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
    ## ~~~~~~~~~~CODE TO GENERATE~~~~~~~~~~~ ##
    ## ~~~~~~~~~~~~~ENTRY BOXES~~~~~~~~~~~~~ ##
    ## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
    entries = []
    row = tk.Frame(root)

    v = tk.IntVar()
    chk = tk.Checkbutton(row, text="Invert Image", variable=v).pack(anchor='w', side=tk.LEFT)
    entries.append(('Negative', v))
    row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    ## row for adaptive thresholding
    row = tk.Frame(root)
    lab = tk.Label(row, width=15, text='Thresholding', anchor='w').pack(side=tk.LEFT)
    lab = tk.Label(row, width=5, text='Max', anchor='w')
    lab.pack(side=tk.LEFT)
    ent = tk.Entry(row, width=5)
    entries.append(('maxThreshold', ent))
    ent.pack(side=tk.LEFT)
    lab = tk.Label(row, width=5, text='Min', anchor='w')
    lab.pack(side=tk.LEFT)
    ent = tk.Entry(row, width=5)
    ent.pack(side=tk.LEFT)
    entries.append(('minThreshold', ent))

    lab = tk.Label(row, width=5, text='Step', anchor='w')
    lab.pack(side=tk.LEFT)
    ent = tk.Entry(row, width=5)
    entries.append(('thresholdStep', ent))
    ent.pack(side=tk.LEFT)
    lab = tk.Label(row, width=8, text='Distance', anchor='w')
    lab.pack(side=tk.LEFT)
    ent = tk.Entry(row, width=5)
    entries.append(('minDistBetweenBlobs', ent))
    ent.pack(side=tk.LEFT)
    row.pack(side=tk.TOP, fill=tk.X, padx=15, pady=15)

    ## Area threshold
    row = tk.Frame(root)
    v = tk.IntVar()
    v.set(1)
    chk = tk.Checkbutton(row, text="Filter by Area        ", variable=v, width=15).pack(anchor='w', side=tk.LEFT)
    entries.append(('filterByArea', v))
    lab = tk.Label(row, width=5, text='Max', anchor='w')
    lab.pack(side=tk.LEFT)
    ent = tk.Entry(row, width=5)
    entries.append(('maxArea', ent))
    ent.pack(side=tk.LEFT)
    lab = tk.Label(row, width=5, text='Min', anchor='w')
    lab.pack(side=tk.LEFT)
    ent = tk.Entry(row, width=5)
    ent.pack(side=tk.LEFT)
    entries.append(('minArea', ent))
    row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
    ## Circularity threshold
    row = tk.Frame(root)
    v = tk.IntVar()
    v.set(0)
    chk = tk.Checkbutton(row, text="Filter by Circularity", variable=v, width=15, justify=tk.LEFT).pack(anchor='w', side=tk.LEFT)
    entries.append(('filterByCircularity', v))
    lab = tk.Label(row, width=5, text='Max', anchor='w')
    lab.pack(side=tk.LEFT)
    ent = tk.Entry(row, width=5)
    entries.append(('maxCircularity', ent))
    ent.pack(side=tk.LEFT)
    lab = tk.Label(row, width=5, text='Min', anchor='w')
    lab.pack(side=tk.LEFT)
    ent = tk.Entry(row, width=5)
    ent.pack(side=tk.LEFT)
    entries.append(('minCircularity', ent))
    row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
    ## Inertia threshold
    row = tk.Frame(root)
    v = tk.IntVar()
    chk = tk.Checkbutton(row, text="Filter by Inertia      ", variable=v, width=15, justify=tk.LEFT).pack(anchor='w', side=tk.LEFT)
    entries.append(('filterByInertia', v))
    lab = tk.Label(row, width=5, text='Max', anchor='w')
    lab.pack(side=tk.LEFT)
    ent = tk.Entry(row, width=5)
    entries.append(('maxInertiaRatio', ent))
    ent.pack(side=tk.LEFT)
    lab = tk.Label(row, width=5, text='Min', anchor='w')
    lab.pack(side=tk.LEFT)
    ent = tk.Entry(row, width=5)
    ent.pack(side=tk.LEFT)
    entries.append(('minInertiaRatio', ent))
    row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
    ## Convexity threshold
    row = tk.Frame(root)
    v = tk.IntVar()
    chk = tk.Checkbutton(row, text="Filter by Convexity ", variable=v, width=15, justify=tk.LEFT).pack(anchor='w', side=tk.LEFT)
    entries.append(('filterByConvexity', v))
    lab = tk.Label(row, width=5, text='Max', anchor='w')
    lab.pack(side=tk.LEFT)
    ent = tk.Entry(row, width=5)
    entries.append(('maxConvexity', ent))
    ent.pack(side=tk.LEFT)
    lab = tk.Label(row, width=5, text='Min', anchor='w')
    lab.pack(side=tk.LEFT)
    ent = tk.Entry(row, width=5)
    ent.pack(side=tk.LEFT)
    entries.append(('minConvexity', ent))
    row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
    return entries

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'please provide a filename'
        sys.exit(0)

    FULLPATH, FILENAME = os.path.split(sys.argv[1])

    # create a display window
    root = tk.Tk()
    root.wm_title("Blob Detection Viewer")
    root.bind('<Escape>', lambda e: root.quit())
    height = 0.5*root.winfo_screenheight() 

    # setup opencv to read the video
    cap = cv2.VideoCapture(sys.argv[1])

    lmain = tk.Label(root)
    lmain.pack()
    ents = makeform()
    b1 = tk.Button(root, text='Update Detector',command=(lambda e=ents: update(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)

    update(ents)
    show_frame()
    root.mainloop()
