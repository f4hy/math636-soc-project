"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from Tkinter import *
from prison import *

#initialize some variables
h = 600
w = 600

N = 5
M = 5

ratio = 0.5

strats = []
payoff = {}

colors = {'C':"blue",'D':"red"}

def prisonsetup():
    """function to set up the prion. Called when the setup button is pushed """
    global strats, payoff
    global N,M
    global nodes, c
    N = sliden.get()
    M = slidem.get()
    dx = float(w)/float(M)
    dy = float(h)/float(N)

    #call the setup function in prison.py
    strats,payoff= initialsetup(N, M, slideratio.get(), slideR.get(), slideS.get(), slideT.get(), slideP.get())

    #remove the old nodes
    c.delete(nodes)
    #create the new ones, draw them to fill the space
    nodes = [ c.create_rectangle(dx*(j),dy*(i),dx*(j+1),dy*(i+1),fill=colors[strats[i][j]]) for j in range(M) for i in range(N)]
    #now the game can be played
    run.config(state=NORMAL)

def next ():
    """Calculates the next thing in the sequence and updates the canvas"""
    global strats, payoff

    oldstrats = strats[:]
    strats = play(N,M,strats,payoff)
    print "Done with play"
    [ [c.itemconfig(nodes[i][j],fill=colors[strats[i][j]]) for j in range(M)] for i in range(N)]
    print "Done with painting"

def analysis():
    """function to preform analysis on the setup"""
    pass

# A window created by tk usually starts with this command:
window = Tk()
#set up the thing to draw the rectangles
c = Canvas(window, bg='#FFFFFF', height=h, width=w)

nodes = [ c.create_rectangle(w/M*float(j),h/N*float(i),w/M*float(j+1),h/N*float(i+1),fill=colors['D']) for j in range(M) for i in range(N)]

c.grid(column=0,columnspan=20,row=2,rowspan=3)

labeln = Label(window,text="N:")
labeln.grid(column=0,row=0)
sliden = Scale(window,orient=HORIZONTAL,from_=4,to=200,resolution=1) 
sliden.grid(column=1,row=0)

labelm = Label(window,text="M:")
labelm.grid(column=0,row=1)
slidem = Scale(window,orient=HORIZONTAL,from_=4,to=200,resolution=1) 
slidem.grid(column=1,row=1)

slidem.set(50)
sliden.set(50)

def setslides(A):
    S = slideS.get()
    T = slideT.get()
    R = slideR.get()
    P = slideP.get()
    slideS.config(from_=0,to=P)
    slideP.config(from_=S,to=R)
    slideR.config(from_=P,to=T)
    slideT.config(from_=R,to=5)

labelR = Label(window,text="R:")
labelR.grid(column=2,row=0)
slideR = Scale(window,orient=HORIZONTAL,from_=0,to=5,resolution=0.1,command=setslides) 
slideR.grid(column=3,row=0)

labelS = Label(window,text="S:")
labelS.grid(column=2,row=1)
slideS = Scale(window,orient=HORIZONTAL,from_=0,to=5,resolution=0.1,command=setslides) 
slideS.grid(column=3,row=1)

labelT = Label(window,text="T:")
labelT.grid(column=4,row=0)
slideT = Scale(window,orient=HORIZONTAL,from_=0,to=5,resolution=0.1,command=setslides) 
slideT.grid(column=5,row=0)

labelP = Label(window,text="P:")
labelP.grid(column=4,row=1)
slideP = Scale(window,orient=HORIZONTAL,from_=0,to=5,resolution=0.1,command=setslides) 
slideP.grid(column=5,row=1)

slideR.set(3)
slideT.set(3.5)
slideS.set(0)
slideP.set(1)

labelratio = Label(window,text="Ratio of c to d")
labelratio.grid(column=6,row=0)
slideratio = Scale(window,variable=ratio,to=1.0,resolution=0.01,orient=HORIZONTAL)
slideratio.grid(column=7,row=0)

slideratio.set(0.5)

labelkey = Label(window,text="Defect:" +colors['D']+" Coop:"+colors['C'])
labelkey.grid(column=1,row=5)

#buttons
run = Button(window,text="run",command=next,state=DISABLED,height=5,width=50)
run.grid(column=2,columnspan=3,row=5)

setup = Button(window,text="setup",command=prisonsetup)
setup.grid(column=6,row=1)

analyze = Button(window,text="analyze",command=analysis)
analyze.grid(column=5,row=5)

quitbutton = Button(window,text="quit",command=window.quit)
quitbutton.grid(column=7,row=5)

# this is usually the last line pertaining to the window.
window.mainloop()

