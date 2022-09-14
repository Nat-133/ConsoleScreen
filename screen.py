import os
import sys
import numpy as np
import time

import colourUtils
import utils
write = sys.stdout.write
"""subprocess.run(["powershell", "-Command", cmd], capture_output=True)"""
os.system("cls")
os.system("mode con:cols=100 lines=50")
# print("\x1b[48;2;0;150;0mHello\x1b[0m")
# write("test")

class Screen:
    def __init__(self, width=50, height=50):
        self._screenBuffer = np.array([[(0.0, 0.0, 0.0, 1.0) for _ in range(width)] for _ in range(height)])
        #os.system(f"mode con: cols={width*2} lines={height}")
        os.system(f"mode con: cols={width} lines={height}")
        os.system(f"Set-ConsoleFont 8")

    def clearBuffer(self):
        self._screenBuffer.fill(0)

    def displayScreenBuffer(self):
        # os.system("cls")
        r, g, b, a = -1, -1, -1, -1
        displayString = "\x1b[1;1H"
        for row in self._screenBuffer[:-1]:
            for colour in row:
                c = colour*255
                rp, gp, bp, ap = c.round().astype(int) 
                if (r, g, b, a) != (rp, gp, bp, ap):
                    r, g, b, a = rp, gp, bp, ap
                    displayString += f"\x1b[48;2;{r};{g};{b}m"
                displayString += " "
            displayString += "\n"
        displayString += "\r\x1b[0m"
        write(displayString)
    
    def renderPixel(self, pos, colour) -> bool:
        x, y = pos
        self._screenBuffer[y, x] = colour
        #self._screenBuffer[y, 2*x + 1] = colour
        return True

    def plotShallowLine(self, pos0, pos1, colour):
        x0, y0 = pos0
        x1, y1 = pos1
        dx = x1 - x0
        dy = y1 - y0

        yi = np.sign(dy)
        if yi < 0:
            dy = - dy

        D = 2*dy - dx
        y = y0

        for x in range(x0, x1+1):
            self.renderPixel((x,y), colour)
            if D > 0:
                y = y + yi
                D = D - 2*dx
            D = D + 2*dy
    
    def plotSteepLine(self, pos0, pos1, colour):
        x0, y0 = pos0
        x1, y1 = pos1
        dx = x1 - x0
        dy = y1 - y0

        xi = np.sign(dx)
        if xi < 0:
            dx = - dx

        D = 2*dx - dy
        x = x0

        for y in range(y0, y1+1):
            self.renderPixel((x,y), colour)
            if D > 0:
                x = x + xi
                D = D - 2*dy
            D = D + 2*dx

    def renderLine(self, start, end, colour):
        x0, y0 = start
        x1, y1 = end
        dx = x1 - x0
        dy = y1 - y0
        if np.abs(dy) > np.abs(dx):
            if y0 < y1:
                self.plotSteepLine(start, end, colour)
            else:
                self.plotSteepLine(end, start, colour)
        else:
            if x0 < x1:
                self.plotShallowLine(start, end, colour)
            else:
                self.plotShallowLine(end, start, colour)


try:
    utils.changeFontSize(2)
    screen = Screen(200,200)

    points = np.array([(0, 20), (15, 15), (20, 0), (15, -15), (0, -20), (-15, -15), (-20, 0), (-15, 15), (0, 20)])
    points = points*4
    points = points + np.array((25, 25))*4
    colours = colourUtils.spectrum(8)
    for i in range(8):
        p1, p2 = points[i:i+2]
        screen.renderLine(p1, p2, colours[i])


    screen.displayScreenBuffer()
    angle = 0

    while True:
        screen.clearBuffer()
        centre = np.array((100, 100))
        endPoint = (np.array((np.cos(angle), np.sin(angle))) * 75).round().astype(int) + centre
        screen.renderLine(centre, endPoint, (1,1,1,1))
        screen.displayScreenBuffer()
        angle += 0.01
        #time.sleep(0.1)

        
finally:
    os.system("mode con:cols=50 lines=50")
    utils.changeFontSize(16)
    print("finished")