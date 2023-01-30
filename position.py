import cv2 
import argparse
import os
   
def click_event(event, x, y, flags, params): 
    
    #hile True:
        
        #key = cv2.waitKey(5)
        #if key == ord('e'):
        #    break
        
        if event == cv2.EVENT_LBUTTONDOWN: 
        
            print(x, ' ', y) 
        
            fichier.write(str(x) + ' ' + str(y) + '\n')
        
            font = cv2.FONT_HERSHEY_SIMPLEX 
            cv2.putText(img, '+', (x-13,y+9), font, 
                        1, (255, 0, 0), 2) 
            cv2.imshow('image', img) 
  
    
        if event==cv2.EVENT_RBUTTONDOWN: 
  
        
        
            print(x, ' ', y) 
  
        
        
            font = cv2.FONT_HERSHEY_SIMPLEX 
            b = img[y, x, 0] 
            g = img[y, x, 1] 
            r = img[y, x, 2] 
            cv2.putText(img, str(b) + ',' +
                        str(g) + ',' + str(r), 
                        (x,y), font, 1, 
                        (255, 255, 0), 2) 
            cv2.imshow('image', img) 

  
if __name__=="__main__": 
    fichier = open("coordonnees_eau.txt", "w")

    parser = argparse.ArgumentParser(description='Read video file')
    parser.add_argument('video', help='input video filename')
    args = parser.parse_args()

    img = cv2.imread(args.video, 1) 
  
    
    cv2.imshow('image', img) 
  
    
    
    cv2.setMouseCallback('image', click_event) 
  
    
    cv2.waitKey(0) 
  
    
    cv2.destroyAllWindows() 
    
    fichier.close()