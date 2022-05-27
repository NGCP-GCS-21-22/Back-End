import cv2
import numpy as np
from datetime import datetime
# https://www.asus.com/support/FAQ/1039488/
   
# Create a VideoCapture object and read from input file
# cap = cv2.VideoCapture('test.avi')
cap = cv2.VideoCapture(0)

# For recording the video 
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (1080, 720))

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video  file")
   
# Read until video is completed
while(cap.isOpened()):
      
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
   
    frame = cv2.resize(frame, (1080, 720))
    # Show the time
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, str(datetime.now()), (10,30), font, 1,(0,0,0),2,cv2.LINE_AA)
    
    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # For recording video  
    out.write(frame)

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
   
  # Break the loop
  else: 
    break

# When everything done, release 
# the video capture object
cap.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows() 