import numpy as np
import pandas as pd
import streamlit as st
import cv  
import streamlit.components.v1 as components
#https://github.com/madhav727/medium/blob/master/finger_counting_video.py
@st.cache()
def skinmask(img):
    hsvim = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower = np.array([0, 48, 80], dtype = "uint8")
    upper = np.array([20, 255, 255], dtype = "uint8")
    skinRegionHSV = cv.inRange(hsvim, lower, upper)
    blurred = cv.blur(skinRegionHSV, (2,2))
    ret, thresh = cv.threshold(blurred,0,255,cv.THRESH_BINARY)
    return thresh
@st.cache()
def getcnthull(mask_img):
    contours, hierarchy = cv.findContours(mask_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = max(contours, key=lambda x: cv.contourArea(x))
    hull = cv.convexHull(contours)
    return contours, hull
@st.cache()
def getdefects(contours):
    hull = cv.convexHull(contours, returnPoints=False)
    defects = cv.convexityDefects(contours, hull)
    return defects
st.title("ASL Translation Data Mining Project FALL2020")

st.header("By: Hanna Bowman, Mark Dobres, Matt Zenner ")

st.write()


components.iframe("https://docs.google.com/document/d/13GSd2RFZXFlBHFAm_6_8_XLbOHc8OB1JF41P7_0Z5go/edit?usp=sharing", height=900 )


st.subheader("Translation from live video to text: ")



if st.button("Begin..."):
    st.success("Press Q to exit camera")
    cap = cv.VideoCapture(0) # '0' for webcam
    while cap.isOpened():
        _, img = cap.read()
        try:
            mask_img = skinmask(img)
            contours, hull = getcnthull(mask_img)
            cv.drawContours(img, [contours], -1, (255,255,0), 2)
            cv.drawContours(img, [hull], -1, (0, 255, 255), 2)
            defects = getdefects(contours)
            if defects is not None:
                cnt = 0
                for i in range(defects.shape[0]):  # calculate the angle
                    s, e, f, d = defects[i][0]
                    start = tuple(contours[s][0])
                    end = tuple(contours[e][0])
                    far = tuple(contours[f][0])
                    a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                    b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                    c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                    angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  #      cosine theorem
                    if angle <= np.pi / 2:  # angle less than 90 degree, treat as fingers
                        cnt += 1
                        cv.circle(img, far, 4, [0, 0, 255], -1)
                if cnt > 0:
                    cnt = cnt+1
                cv.putText(img, str(cnt), (0, 50), cv.FONT_HERSHEY_SIMPLEX,1, (255, 0, 0) , 2, cv.LINE_AA)
            cv.imshow("img", img)
        except:
            pass
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()