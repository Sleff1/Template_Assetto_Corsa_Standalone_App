# AC App Template by Hunter Vaners
# ------------------------------
#
# Don't forget to rename assettocorsa\apps\python\Template_Assetto_Corsa_App
#           by assettocorsa\apps\python\[Your_App_Name_Without_Spaces]
#  and
# the file Template_Assetto_Corsa_App.py
#           by Your_App_Name_Without_Spaces.py
#
# ------------------------------

import ac
import acsys
from third_party.sim_info import *



appName = "STS"
width, height = 200 , 200 # width and height of the app's window

simInfo = None

# Initialize lastLapCount globally so it's available before appGL runs
lastLapCount = 0



def acMain(ac_version):#----------------------------- App window Init

    # Don't forget to put anything you'll need to update later as a global variables
    global appWindow # <- you'll need to update your window in other functions.
    global testButton
    global label
    global speed

    appWindow = ac.newApp(appName)
    ac.setTitle(appWindow, appName)
    ac.setSize(appWindow, width, height)
    ac.addRenderCallback(appWindow, appGL) # -> links this app's window to an OpenGL render function

    global simInfo
    try:
        simInfo = SimInfo()
    except Exception:
        simInfo = None
    
    # testButton = ac.addButton(appWindow, "Test button")
    # ac.setSize(testButton, 200, 100)
    # def on_test_button_clicked(*args):
    #     log("button pressed")
    # ac.addOnClickedListener(testButton, on_test_button_clicked)

    label = ac.addLabel(appWindow, "label")
    ac.setPosition(label, 0, 100)
    ac.setSize(label, 200, 100)
    return appName

def log(message):
    ac.console(message)

def write_session_info():
    try:
        if simInfo is None:
            log("SimInfo not available, cannot write session info")
            return
        car_name = simInfo.static.carModel
        track_name = simInfo.static.track
        last_lap_time = simInfo.graphics.lastTime
        content = "Car: %s\nTrack: %s\nLast Lap Time: %s\n" % (car_name, track_name, last_lap_time)
        try:
            import os
            app_dir = os.path.dirname(os.path.realpath(__file__))
            out_path = os.path.join(app_dir, "session_info.txt")
        except Exception:
            out_path = "session_info.txt"

        try:
            # Append one CSV-style line per lap: car,time,track
            line = "%s,%s,%s\n" % (car_name, last_lap_time, track_name)
            with open(out_path, "ab") as f:
                f.write(line.encode('utf-8'))
            log("Appended session info to: %s" % out_path)
        except Exception as e:
            log("Failed to append session info to %s: %s" % (out_path, e))
    except Exception as e:
        log("Error writing session info: %s" % e)

def appGL(deltaT):#-------------------------------- OpenGL UPDATE

    try:
        global lastLapCount
        if simInfo is None:
            # Shared memory not ready yet; show placeholder
            try:
                ac.setText(label, "Waiting for sim...")
            except Exception:
                pass
            return

        # `completedLaps` is provided in the graphics pagefile
        currentLapCount = simInfo.graphics.completedLaps

        # Read speed from shared memory via sim_info (reliable and avoids missing constant)
        lastLapTime = simInfo.graphics.lastTime
        ac.setText(label, str(lastLapTime))

        if currentLapCount > lastLapCount:
            write_session_info()
        lastLapCount = currentLapCount
        
    except Exception:
        # Keep render stable if AC isn't providing state yet
        pass


def acUpdate(deltaT):#-------------------------------- AC UPDATE
    """
    This is where you update your app window ( != OpenGL graphics )
    such as : labels , listener , ect ...
    """
    return
    pass # -> Delete this line if you do something here !
