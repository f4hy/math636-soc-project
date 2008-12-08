#!/usr/bin/python
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
import copy
import timeit
import time
#initialize some variables
h = 400
w = 400

N = 5
M = 5

ratio = 0.5
graphics = True

strats = []
payoff = {}

colors = {'C':"blue",'D':"red"}

def setstatus(newstatus):
    status.config(text=newstatus)

def togglegraphics():
    global graphics
    graphics = not graphics
    if graphics:
        graphicsbutton.config(text="Graphics are on")
        slidem.config(to=50)
        sliden.config(to=50)
        run.config(state=DISABLED)
        multirun.config(state=DISABLED)
        c.grid()
    else:
        graphicsbutton.config(text="Graphics are off")
        slidem.config(to=1000)
        sliden.config(to=1000)
        c.grid_remove()

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
    setstatus("Setting up")
    strats,payoff= initialsetup(N, M, slideratio.get(), slideR.get(), slideS.get(), slideT.get(), slideP.get())
    #create the new ones, draw them to fill the space if graphics enabled
    if graphics:
        setstatus("Drawing board")
        
    #localize
        newrectangle = c.create_rectangle
        lstrats = strats
        lcolors = colors
        nodes = [[newrectangle(dx*(j),dy*(i),dx*(j+1),dy*(i+1),width=0,fill=lcolors[lstrats[i][j]]) for j in xrange(M)] for i in xrange(N)]
        
    #now the game can be played
    run.config(state=NORMAL)
    multirun.config(state=NORMAL)
    setstatus("Ready to run.")

def benchmark():
    global strats, payoff
    global N,M
    global nodes, c
    f=open('benchmark.log', 'a')
    f.write('\nRunning benchmark at %s\n' % time.ctime())
    
    runstatement = "prisonsetup()"
    setupstatement = "from __main__ import prisonsetup;"

    setuptimer = timeit.Timer(runstatement,setupstatement)
    elapsed = setuptimer.timeit(5)
    f.write("running %s 5 times with N*M: %s is: %s\n" % (runstatement, (N*M),elapsed) )

    runstatement = "nextstep()"
    setupstatement = "from __main__ import nextstep;"

    playtimer = timeit.Timer(runstatement,setupstatement)
    f.write("running %s 5 times with N*M: %s is: %s\n" % (runstatement, (N*M),playtimer.timeit(5)) )


def nextstep ():
    """Calculates the next step in the sequence and updates the canvas"""
    global strats, payoff
    setstatus("playing the game")
    oldstrats = copy.deepcopy(strats)
    strats = play(N,M,strats,payoff)
    if graphics:
        changecolor = c.itemconfig
        lcolors = colors
        [c.itemconfig(nodes[i][j],fill=lcolors[strats[i][j]]) for j in xrange(M) for i in xrange(N) if oldstrats[i][j] is not strats[i][j]]
    setstatus("Turn Done")

def multistep ():
    """Calculates the next few steps in the sequence and updates the canvas"""
    global strats, payoff
    setstatus("playing the game")
    oldstrats = copy.deepcopy(strats)
    for x in xrange(5):
        strats = play(N,M,strats,payoff)
    if graphics:
        changecolor = c.itemconfig
        lcolors = colors
        [c.itemconfig(nodes[i][j],fill=lcolors[strats[i][j]]) for j in xrange(M) for i in xrange(N) if oldstrats[i][j] is not strats[i][j]]
    setstatus("Trun Done")

def analysis():
    """function to preform analysis on the setup"""
    setstatus("Analyzing")
    A,B = countclusters(strats,'C')
    f=open('clusters.log', 'a')
    f.write('\nRunning analysis at %s\n' % time.ctime())
    f.write('With M=%d, N=%d,R=%d,S=%d,T=%d,P=%d \n' % (M,N,slideR.get(), slideS.get(), slideT.get(), slideP.get()) )
    f.write('Number of clusters: %d, Average Cluster size: %f \n' % (A,sum(B)/float(len(B)) ) ) 
    f.write('Cluster sizes: %s\n' % sorted(B))

    setstatus("Number of clusters %d, Ave cluster size %f, Wrote clusters to clusters.log" % (A,sum(B)/float(len(B)) ))


def generateimage():
    """Write the canvas of nodes to an eps file"""
    c.postscript(file="prison.eps",colormode="color")
    setstatus("wrote file prison.eps")

# A window created by tk usually starts with this command:
window = Tk()
#set up the thing to draw the rectangles
c = Canvas(window, bg='#FFFFFF', height=h, width=w)

nodes = [ [c.create_rectangle(w/M*float(j),h/N*float(i),w/M*float(j+1),h/N*float(i+1),fill=colors['D']) for j in xrange(M)] for i in xrange(N)]

c.grid(column=0,columnspan=20,row=2,rowspan=3)

labeln = Label(window,text="N:")
labeln.grid(column=0,row=0)
sliden = Scale(window,orient=HORIZONTAL,from_=4,to=50,resolution=1) 
sliden.grid(column=1,row=0)

labelm = Label(window,text="M:")
labelm.grid(column=0,row=1)
slidem = Scale(window,orient=HORIZONTAL,from_=4,to=50,resolution=1) 
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
    setstatus("You must setup agian to use the new values")

labelR = Label(window,text="Reward:")
labelR.grid(column=2,row=0)
slideR = Scale(window,orient=HORIZONTAL,from_=0,to=5,resolution=0.1,command=setslides) 
slideR.grid(column=3,row=0)

labelS = Label(window,text="Suckers:")
labelS.grid(column=2,row=1)
slideS = Scale(window,orient=HORIZONTAL,from_=0,to=5,resolution=0.1,command=setslides) 
slideS.grid(column=3,row=1)

labelT = Label(window,text="Temptation:")
labelT.grid(column=4,row=0)
slideT = Scale(window,orient=HORIZONTAL,from_=0,to=5,resolution=0.1,command=setslides) 
slideT.grid(column=5,row=0)

labelP = Label(window,text="Punishment:")
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
run = Button(window,text="Run one step",command=nextstep,state=DISABLED,height=5,width=50)
run.grid(column=2,columnspan=2,row=5)

multirun = Button(window,text="Run five steps",command=multistep,state=DISABLED,height=5)
multirun.grid(column=4,row=5)


setup = Button(window,text="setup",command=prisonsetup)
setup.grid(column=6,row=1)

analyze = Button(window,text="analyze",command=analysis)
analyze.grid(column=5,row=5)

generateoutput = Button(window,text="Write to file",command=generateimage)
generateoutput.grid(column=7,row=3)


benchmark = Button(window,text="Benchmark",command=benchmark)
#benchmark.grid(column=7,row=4)

graphicsbutton = Button(window,text="Graphics are on",command=togglegraphics,width=17)
graphicsbutton.grid(column=7,row=3)


status = Label(window,text="Status: first set up the board",width=20,wraplength=100)
status.grid(column=6,row=5)

quitbutton = Button(window,text="quit",command=window.quit)
quitbutton.grid(column=7,row=5)

# this is usually the last line pertaining to the window.
window.mainloop()

