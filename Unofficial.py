import cv2
import numpy as np
import time
import simpleaudio as sa
from tkinter import *
from tkinter.ttk import *
import time
import mido

import threading
import sys

numbars = 1
current_color = 'red'


def setbar(value):
    for x in range(numbars):
        bar[x]['value'] = value


window = Tk()
frame = Frame(window)
s = Style()
s.theme_use('default')
s.configure("Custom.Horizontal.TProgressbar", background='yellow', troughcolor='black')
bar = []

for x in range(numbars):
    bar.append(Progressbar(window, orient=VERTICAL, length=900, style='Custom.Horizontal.TProgressbar'))
    bar[x].pack(side=RIGHT)

button = Button(window, text="download", command=setbar).pack()

# Set up MIDI output port
port = mido.open_output()

# Send a Control Change message to set the volume to 127
channel = 0  # MIDI channel 1
control_number = 7  # Control Change message for volume
value = 127  # Value for volume (0-127)
msg = mido.Message('control_change', channel=channel, control=control_number, value=value)
port.send(msg)
msg = mido.Message('control_change', channel=channel, control=64, value=127)

# List of all natural notes
naturalNotes = [21, 23, 25, 26, 28, 30, 32, 33, 35, 37, 39, 40, 42, 44, 46, 47, 49, 51, 53, 54, 56, 58, 60, 61, 63, 65, 67, 68, 70, 72, 73, 75, 77, 79, 80, 82, 84, 86, 87, 89, 91, 93, 94, 96, 98, 100, 101, 103, 105, 107, 108]

# To switch the color between red and yellow
def update_color():
    while True:
        # print('changing color')
        global current_color
        next_color = 'yellow' if current_color == 'red' else 'red'
        s.configure("Custom.Horizontal.TProgressbar", background=next_color, thickness=2000)
        current_color = next_color
        time.sleep(1)


def map_range(value, from_low, from_high, to_low, to_high):
    """
    Maps a value from one range of numbers to another range of numbers.

    Parameters:
    value (float): The value to map.
    from_low (float): The lower bound of the input range.
    from_high (float): The upper bound of the input range.
    to_low (float): The lower bound of the output range.
    to_high (float): The upper bound of the output range.

    Returns:
    float: The mapped value.
    """
    from_range = from_high - from_low
    to_range = to_high - to_low
    scale_factor = to_range / from_range
    mapped_value = (value - from_low) * scale_factor + to_low
    return mapped_value

centroid_y = 0

def main_part():
    global centroid_y
    # Set up video capture using laptop's camera
    cap = cv2.VideoCapture(0)

    # # Define the piano notes to be played
    # C3 = sa.WaveObject.from_wave_file("60.wav")
    # C4 = sa.WaveObject.from_wave_file("72.wav")
    # C5 = sa.WaveObject.from_wave_file("84.wav")
    # D3 = sa.WaveObject.from_wave_file("62.wav")
    # D4 = sa.WaveObject.from_wave_file("74.wav")
    # D5 = sa.WaveObject.from_wave_file("86.wav")
    # E3 = sa.WaveObject.from_wave_file("64.wav")
    # E4 = sa.WaveObject.from_wave_file("76.wav")
    # E5 = sa.WaveObject.from_wave_file("88.wav")
    # F3 = sa.WaveObject.from_wave_file("65.wav")
    # F4 = sa.WaveObject.from_wave_file("77.wav")
    # F5 = sa.WaveObject.from_wave_file("89.wav")
    # G3 = sa.WaveObject.from_wave_file("67.wav")
    # G4 = sa.WaveObject.from_wave_file("79.wav")
    # # G5 = sa.WaveObject.from_wave_file("91.wav")
    # A3 = sa.WaveObject.from_wave_file("69.wav")
    # A4 = sa.WaveObject.from_wave_file("81.wav")
    # # A5 = sa.WaveObject.from_wave_file("93.wav")
    # B3 = sa.WaveObject.from_wave_file("71.wav")
    # B4 = sa.WaveObject.from_wave_file("83.wav")
    # # B5 = sa.WaveObject.from_wave_file("95.wav")

    # Define the range of colors to be detected (in this case, red color)
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])

    # Initialize variables
    prev_y = 0
    playing_note = False

    # Adjust the minimum contour area and position threshold
    MIN_CONTOUR_AREA = 1000
    POSITION_THRESHOLD = 20

    while True:
        # Read frame from camera
        ret, frame = cap.read()

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only red colors
        mask = cv2.inRange(hsv, lower_red, upper_red)

        # Find contours in the thresholded image
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour (if any)
        max_area = 0
        max_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area and area > MIN_CONTOUR_AREA:
                max_area = area
                max_contour = contour

        # If a contour is found, find its centroid
        if max_contour is not None:
            moments = cv2.moments(max_contour)
            centroid_x = int(moments['m10'] / moments['m00'])
            centroid_y = int(moments['m01'] / moments['m00'])

            # # Check if the contour has moved upwards by a certain threshold
            # if centroid_y < prev_y - POSITION_THRESHOLD and not playing_note:
            #     playing_note = True
            #     if centroid_x < frame.shape[1] / 12:
            #         C3.play()
            #     elif centroid_x < frame.shape[1] * 2 / 12:
            #         D3.play()
            #     elif centroid_x < frame.shape[1] * 3 / 12:
            #         E3.play()
            #     elif centroid_x < frame.shape[1] * 4 / 12:
            #         F3.play()
            #     elif centroid_x < frame.shape[1] * 5 / 12:
            #         G3.play()
            #     elif centroid_x < frame.shape[1] * 6 / 12:
            #         A3.play()
            #     elif centroid_x < frame.shape[1] * 7 / 12:
            #         B3.play()
            #     elif centroid_x < frame.shape[1] * 8 / 12:
            #         C4.play()
            #     elif centroid_x < frame.shape[1] * 9 / 12:
            #         D4.play()
            #     elif centroid_x < frame.shape[1] * 10 / 12:
            #         E4.play()
            #     elif centroid_x < frame.shape[1] * 11 / 12:
            #         F4.play()
            #     else:
            #         G4.play()
            #
            # # Check if the contour has moved downwards by a certain threshold
            # elif centroid_y > prev_y + POSITION_THRESHOLD and not playing_note:
            #     playing_note = True
            #     # if centroid_x < frame.shape[1] / 12:
            #     #     B5.play()
            #     # elif centroid_x < frame.shape[1] * 2 / 12:
            #     #    A5.play()
            #     # elif centroid_x < frame.shape[1] * 3 / 12:
            #     #     G5.play()
            #
            #     centroid_x = 600 - centroid_x
            #
            #     if centroid_x < frame.shape[1] * 4 / 12:
            #         F5.play()
            #     elif centroid_x < frame.shape[1] * 5 / 12:
            #         E5.play()
            #     elif centroid_x < frame.shape[1] * 6 / 12:
            #         D5.play()
            #     elif centroid_x < frame.shape[1] * 7 / 12:
            #         C5.play()
            #     elif centroid_x < frame.shape[1] * 8 / 12:
            #         B4.play()
            #     elif centroid_x < frame.shape[1] * 9 / 12:
            #         A4.play()
            #     elif centroid_x < frame.shape[1] * 10 / 12:
            #         G4.play()
            #     elif centroid_x < frame.shape[1] * 11 / 12:
            #         F4.play()
            #     else:
            #         E4.play()
            #
            # # If the contour has not moved significantly, stop playing the note
            # elif abs(centroid_y - prev_y) <= POSITION_THRESHOLD:
            #     playing_note = False

            bar_value = map_range(centroid_y, 0, 300, 100, 0)
            setbar(bar_value)

            # note = int(map_range(centroid_y, 0, 600, 126, 0))
            # msg = mido.Message('note_on', note=note, velocity=127)
            # port.send(msg)

            # # Wait for half a second
            # time.sleep(0.05)

            # # Create a note off message and send it
            # msg = mido.Message('note_off', note=note, velocity=127)
            # port.send(msg)

            # Update the previous y position
            prev_y = centroid_y

        # Display the frame
        cv2.imshow('frame', frame)

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # print("centroid x ", centroid_x)
        # print("centroid y", centroid_y)
    # Release the capture and destroy all windows
    cap.release()
    cv2.destroyAllWindows()
    sys.exit()


def player():
    while True:
        value_in_List = int(map_range(centroid_y, 0, 600, 50, 0))
        note = naturalNotes[value_in_List]
        msg = mido.Message('note_on', note=note, velocity=127)
        port.send(msg)

        # Wait for half a second
        time.sleep(2)

        # Create a note off message and send it
        msg = mido.Message('note_off', note=note, velocity=127)
        port.send(msg)


mainThread = threading.Thread(target=main_part)
colorThread = threading.Thread(target=update_color)
numThreads = 10
threadList = []
for i in range(numThreads):
    threadList.append(threading.Thread(target=player))
    threadList[i].daemon = True
    threadList[i].start()
    time.sleep(.2)

mainThread.daemon = True
colorThread.daemon = True
colorThread.start()
mainThread.start()

window.mainloop()

sys.exit()
