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
from math import log
import copy
import timeit
import time
#initialize some variables
h = 400
w = 400

N = 5
M = 5

generation = 0

ratio = 0.5
graphics = True

strats = []

paststrats = {}

payoff = {}


mutualinformationfile=open('mutualinformation%s%s.log' % (time.localtime()[4],time.localtime()[5]), 'a')

colors = {'C':"blue",'D':"red",'CD':"green",'DC':"yellow"}

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
        slidem.config(to=500)
        sliden.config(to=500)
        c.grid_remove()

def randomprisonsetup():
    """function to set up the prion. Called when the setup button is pushed """
    global strats, payoff
    global mutualinformationfile
    global N,M
    global nodes, c
    global generation
    N = sliden.get()
    M = slidem.get()
    dx = float(w)/float(M)
    dy = float(h)/float(N)

    generation = 0
    paststarts = {}
    mutualinformationfile=open('mutualinformation%s%s.log' % (time.localtime()[4],time.localtime()[5]), 'a')
    mutualinformationfile.write('#Running statistical analysis at %s\n' % time.ctime())

    setslides(1)
    #call the setup function in prison.py
    setstatus("Setting up")
    strats = initialrandomsetup(N, M, slideratio.get())
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
    setstatus("Ready to run. Generation = 0")

def centeredprisonsetup():
    """function to set up the prion. Called when the setup button is pushed """
    global strats, payoff
    global N,M
    global mutualinformationfile
    global nodes, c
    global generation
    N = sliden.get()
    M = slidem.get()
    dx = float(w)/float(M)
    dy = float(h)/float(N)

    setslides(1)
    generation = 0
    paststarts = {}
    mutualinformationfile=open('mutualinformation%s%s.log' % (time.localtime()[4],time.localtime()[5]), 'a')
    mutualinformationfile.write('#Running statistical analysis at %s\n' % time.ctime())


    #call the setup function in prison.py
    setstatus("Setting up")
    strats = initialcenterdefectsetup(N, M)
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
    setstatus("Ready to run. Generation = 0")


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
    global strats, payoff,generation,paststrats
    
    setstatus("playing the game")
    
    
    
    paststrats[generation] = copy.deepcopy(strats)
    generation += 1
    strats = play(N,M,strats,payoff)
    if graphics:
        changecolor = c.itemconfig
        lcolors = colors
#        [c.itemconfig(nodes[i][j],fill=lcolors[strats[i][j]]) for j in xrange(M) for i in xrange(N) if paststrats[generation-1][i][j] is not strats[i][j]]
        [c.itemconfig(nodes[i][j],fill=lcolors[strats[i][j]]) for j in xrange(M) for i in xrange(N)]
    #mutualinformation(strats,paststrats[generation-1])
    mutualinformationfile.write("mutual information after 1")
    mutualinformation(strats,paststrats[generation-1])
    if generation > 15:
	mutualinformationfile.write("mutual information after 15")
        mutualinformation(strats,paststrats[generation-15])
    setstatus("Turn Done, Generation:%d" % generation)
    

def multistep ():
    """Calculates the next few steps in the sequence and updates the canvas"""
    global strats, payoff,generation,graphics
    
    graphicssetting=graphics
    graphics = False
    for x in xrange(4):
	    nextstep()
    graphics = graphicssetting
    nextstep()
    

def analysis():
    """function to preform analysis on the setup"""
    global generation
    setstatus("Analyzing")

    sys.setrecursionlimit(5000)

    try:
        A,B = countclusters(strats,'C')
        f=open('clusters.log', 'a')
        f.write('\nRunning analysis at %s\n' % time.ctime())
        f.write('With M=%d, N=%d,R=%f,S=%f,T=%f,P=%f Generation:%d \n' % (M,N,slideR.get(), slideS.get(), slideT.get(), slideP.get(),generation) )
        f.write('Number of clusters: %d, Average Cluster size: %f \n' % (A,sum(B)/float(len(B)) ) ) 
        f.write('Cluster sizes: %s\n' % sorted(B))
        

        setstatus("Number of clusters %d, Ave cluster size %f, Wrote clusters to clusters.log" % (A,sum(B)/float(len(B)) ))

    except:
        print sys.exc_info()
        setstatus("Cluster too large to count")

def mutualinformation(x,y):
    pcc = 0.0
    pdd = 0.0
	
	#ratio of c's
    pc = float(len([j for i in x for j in i if j=='C']))/float(M*N)
	#ratio of d's
    pd = float(len([j for i in x for j in i if j=='D']))/float(M*N)
    
    pi = {'C':pc,'D':pd}
    
    
    pyc = float(len([j for i in y for j in i if j=='C']))/float(M*N)
    pyd = float(len([j for i in y for j in i if j=='D']))/float(M*N)
    
    py = {'C':pyc,'D':pyd}
	
	
    for j in xrange(M):
        for i in xrange(N):
            if x[i][j] == y[i][j]:
                if x[i][j] == 'C':
                    pcc += 1.0
                else:
                    pdd += 1.0
	#ratio of c's that change to c's
    pcc = pcc/(pc*float(M*N))
    pcd = 1-pcc
	#ratio of d's that change to d's
    pdd = pdd/(pd*float(M*N))
    pdc = 1-pdd
    
    cross = {('C','C'):pcc,('C','D'):pcd,('D','D'):pdd,('D','C'):pdc}
    
    I = []
    
    for j in xrange(M):
        for i in xrange(N):
            I.append(cross[(x[i][j],y[i][j])]*log( cross[(x[i][j],y[i][j])]/(pi[x[i][j]]*py[y[i][j]]),2))
            

    mutualinformationfile.write("%s" % (sum(I)/(N*M)))

def generatestatistics():
    """function to preform analysis on the setup"""
    setstatus("Analyzing")

    sys.setrecursionlimit(10000)

    f=open('statistics%s%s.log' % (time.localtime()[4],time.localtime()[5]), 'a')
    f.write('#Running statistical analysis at %s\n' % time.ctime())
    f.write('#With M=%d, N=%d,R=%f,S=%f,T=%f,P=%f starting generation:%d \n' % (M,N,slideR.get(), slideS.get(), slideT.get(), slideP.get(),generation) )

    f.write('#cluster sizes of the format "clustersize : how may of that size" ')
    f.write('\n#--generation---%coop----%defect----numberofclusters-----clustersizes--\n')

    histo = {}
    for i in xrange(slidertrials.get()):
        try:
            A,B = countclusters(strats,'C')
            coops = float(len([j for i in strats for j in i if j=='C']))/float(M*N)
            defects = float(len([j for i in strats for j in i if j=='D']))/float(M*N)
            for i in set(B):
                if i in histo:
                    histo[i] += B.count(i)
                else:
                    histo[i] = B.count(i)
            f.write('  %d         %f     %f     %d   \n' % (generation,coops,defects,A))
        except:
            print "clusters too large"
            print sys.exc_info()
            coops = float(len([j for i in strats for j in i if j=='C']))/float(M*N)
            defects = float(len([j for i in strats for j in i if j=='D']))/float(M*N)
            f.write('  %d         %f     %f     %s       \n' % (generation,coops,1-coops,"XXX") )
        nextstep()

    f=open('clusterdistrobution%s%s.log'  % (time.localtime()[4],time.localtime()[5]), 'a')
    f.write('#histogram created at %s\n' % time.ctime())
    f.write('#With M=%d, N=%d,R=%f,S=%f,T=%f,P=%f starting generation:%d \n' % (M,N,slideR.get(), slideS.get(), slideT.get(), slideP.get(),generation) )
    f.write('#cluster sizes----howmany ocurrances after %d trials\n' % slidertrials.get())
    for i in histo:
        f.write(' %d     %d \n' % (i,histo[i]))


def generateimage():
    """Write the canvas of nodes to an eps file"""
    c.postscript(file="prison%s.eps" % time.ctime(),colormode="color")
    setstatus("wrote file prison.eps")

# A window created by tk usually starts with this command:
window = Tk()
#set up the thing to draw the rectangles
c = Canvas(window, bg='#FFFFFF', height=h, width=w)

nodes = [ [c.create_rectangle(w/M*float(j),h/N*float(i),w/M*float(j+1),h/N*float(i+1),fill=colors['D']) for j in xrange(M)] for i in xrange(N)]

c.grid(column=0,columnspan=4,row=2,rowspan=3)

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
    global payoff
    S = slideS.get()
    T = slideT.get()
    R = slideR.get()
    P = slideP.get()
    slideS.config(from_=0,to=0)
    slideP.config(from_=0,to=-8)
    slideR.config(from_=1,to=1)
    slideT.config(from_=1,to=3)

    payoff = {}
    payoff[('C','C')] = slideR.get()
    payoff[('C','D')] = slideS.get()
    payoff[('D','C')] = slideT.get()
    payoff[('D','D')] = slideP.get()

    setstatus("New Payoffs Calulated")

labelR = Label(window,text="Reward:")
labelR.grid(column=2,row=0)
slideR = Scale(window,orient=HORIZONTAL,from_=0,to=5,resolution=0.01,command=setslides) 
slideR.grid(column=3,row=0)

labelS = Label(window,text="Suckers:")
labelS.grid(column=2,row=1)
slideS = Scale(window,orient=HORIZONTAL,from_=0,to=5,resolution=0.01,command=setslides) 
slideS.grid(column=3,row=1)

labelT = Label(window,text="Temptation:")
labelT.grid(column=4,row=0)
slideT = Scale(window,orient=HORIZONTAL,from_=0,to=5,resolution=0.01,command=setslides) 
slideT.grid(column=5,row=0)

labelP = Label(window,text="Punishment:")
labelP.grid(column=4,row=1)
slideP = Scale(window,orient=HORIZONTAL,from_=0,to=5,resolution=0.01,command=setslides) 
slideP.grid(column=5,row=1)

slideR.set(1)
slideT.set(1.4)
slideS.set(0)
slideP.set(0)

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


setup = Button(window,text="random setup",command=randomprisonsetup)
setup.grid(column=7,row=1)

centeredsetup = Button(window,text="centered setup",command=centeredprisonsetup)
centeredsetup.grid(column=6,row=1)


analyze = Button(window,text="analyze",command=analysis)
analyze.grid(column=5,row=5)

statistics = Button(window,text="generate statistics",command=generatestatistics)
statistics.grid(column=6,row=4)

labeltrials = Label(window,text="How many trials to run for statistics")
labeltrials.grid(column=6,row=2)
slidertrials = Scale(window,from_=10,to=70000,resolution=1,orient=HORIZONTAL)
slidertrials.grid(column=6,row=3)



generateoutput = Button(window,text="Write to file",command=generateimage)
generateoutput.grid(column=7,row=3)


benchmark = Button(window,text="Benchmark",command=benchmark)
#benchmark.grid(column=7,row=4)

graphicsbutton = Button(window,text="Graphics are on",command=togglegraphics,width=17)
graphicsbutton.grid(column=7,row=2)


status = Label(window,text="Status: first set up the board",width=20,wraplength=100)
status.grid(column=6,row=5)

quitbutton = Button(window,text="quit",command=window.quit)
quitbutton.grid(column=7,row=5)

# this is usually the last line pertaining to the window.
window.mainloop()

