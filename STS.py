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

simInfo = SimInfo()



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

def appGL(deltaT):#-------------------------------- OpenGL UPDATE
    """
    This is where you redraw your openGL graphics
    if you need to use them .
    """
    # Update UI elements here (called regularly by AC)
    try:
        # Read speed from shared memory via sim_info (reliable and avoids missing constant)
        lastLapTime = simInfo.graphics.lastTime
        ac.setText(label, str(lastLapTime))
    except Exception:
        # Keep render stable if AC isn't providing state yet
        pass # -> Delete this line if you do something here !


def acUpdate(deltaT):#-------------------------------- AC UPDATE
    """
    This is where you update your app window ( != OpenGL graphics )
    such as : labels , listener , ect ...
    """
    # Not used: updates are handled in `appGL` (render callback)
    # If you prefer using an update callback, register it explicitly
    # and move the UI logic here.
    return
    pass # -> Delete this line if you do something here !
