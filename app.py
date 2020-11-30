import numpy as np
import pandas as pd
import streamlit as st
import cv2
import streamlit.components.v1 as components

# embed streamlit docs in a streamlit app




st.title("ASL Translation Data Mining Project FALL2020")

st.header("By: Hanna Bowman, Mark Dobres, Matt Zenner ")

st.write()


components.iframe("https://docs.google.com/document/d/13GSd2RFZXFlBHFAm_6_8_XLbOHc8OB1JF41P7_0Z5go/edit?usp=sharing", height=900 )


st.subheader("Translation from live video to text: ")

if st.button("Click to Begin..."): 
	cap = cv2.VideoCapture(0)

	while(True):
	    # Capture frame-by-frame
	    ret, frame = cap.read()

	    # Our operations on the frame come here
	    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	    # Display the resulting frame
	    cv2.imshow('frame',gray)
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break

	# When everything done, release the capture
	cv2.destroyAllWindows()
	cap.release()

	st.success("press q to exit camera")