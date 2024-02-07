import cv2 
import os 
  
# Read the video from specified path with chord and guitar

chord ="A"
guitar ="g3"

route = "/Users/salvatorecoscab/Movies/AA.mov"
cam = cv2.VideoCapture(route) 

# each n frames
n = 3
#get fps
fps = cam.get(cv2.CAP_PROP_FPS)
print(fps)
try: 
      
    # creating a folder named data 
    if not os.path.exists('data'): 
        os.makedirs('data') 
  
# if not created then raise error 
except OSError: 
    print ('Error: Creating directory of data') 
  
# frame 
currentframe = 0

count = 0
while(True): 
      
    # reading from frame 
    ret,frame = cam.read() 
  
    if ret: 
        # if video is still left continue creating images 
        
        if (count%n==0):
            # writing the extracted images 
            name = './data/'+chord+"/"+guitar+str(currentframe) + '.jpg'
            print ('Creating...' + name) 
            cv2.imwrite(name, frame) 
            currentframe += 1
    else: 
        break
    count += 1
# Release all space and windows once done 
cam.release() 
cv2.destroyAllWindows() 