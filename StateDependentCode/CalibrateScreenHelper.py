from SelectorState import ForceVolumePositions, ClickPoint
from pynput import mouse
from ScreenCoordinates import ROI, ClickPoint

def doCalibrationClick():
    def onClick(x,y,button,pressed):
        if pressed:
            ROI.calibrationPoint = ClickPoint(x,y)
        else:
            # Stop listener
            return False
    # capturing mouse for duration of one click
    with mouse.Listener(on_click=onClick) as listener:
            listener.join()