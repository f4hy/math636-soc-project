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

def prisonsetup():
    global strats
    global payoff
    global N
    global M
    global nodes
    global c
    R = 3
    T = 3.1
    S = 0
    P = 1
    N = sliden.get()
    M = slidem.get()

    strats,payoff= initialsetup(N, M, slideratio.get(), R, S, T, P)

    c.delete(nodes)
    nodes = [ [c.create_rectangle(w/M*float(j),h/N*float(i),w/M*float(j+1),h/N*float(i+1),fill=colors[strats[i][j]]) for j in range(M)] for i in range(N)]

    run.config(state=NORMAL)

def next ():
    """Calculates the next thing in the sequence and udpates the canvas"""
    global strats
    global payoff

    strats = play(N,M,strats,payoff)
    [ [c.itemconfig(nodes[i][j],fill=colors[strats[i][j]]) for j in range(M)] for i in range(N)]



h = 600
w = 600

N = 5
M = 5

ratio = 0.5

strats = [ [0 for j in range(M)] for i in range(N)]
payoff = {}

colors = {'C':"blue",'D':"red"}

# A Windows window created by tk usually starts with this command:
window = Tk()
c = Canvas(window, bg='#FFFFFF', height=h, width=w)
#r1ID = c.create_rectangle(0,0,20,20,fill='#00ff00',width=0)
#r2ID = c.create_rectangle(0,20,20,40,fill='#ff0000',width=0)
#l1ID = c.create_line(0,0,0,25,fill='green',smooth='true')

nodes = [ [c.create_rectangle(w/M*float(j),h/N*float(i),w/M*float(j+1),h/N*float(i+1),fill=colors['D']) for j in range(M)] for i in range(N)]




# note that the grid method is strongly preferred by an authority.
c.grid(column=0,columnspan=5,row=2,rowspan=3)

labeln = Label(window,text="N:")
labeln.grid(column=0,row=0)
sliden = Scale(window,orient=HORIZONTAL,from_=4,to=100,resolution=1) 
sliden.grid(column=1,row=0)

labelm = Label(window,text="M:")
labelm.grid(column=0,row=1)
slidem = Scale(window,orient=HORIZONTAL,from_=4,to=100,resolution=1) 
slidem.grid(column=1,row=1)

slidem.set(50)
sliden.set(50)

labelratio = Label(window,text="Ratio of c to d")
labelratio.grid(column=3,row=0)
slideratio = Scale(window,variable=ratio,to=1.0,resolution=0.01,orient=HORIZONTAL)
slideratio.grid(column=4,row=0)

slideratio.set(0.5)

labelkey = Label(window,text="Defect:" +colors['D']+" Coop:"+colors['C'])
labelkey.grid(column=1,row=5)

run = Button(window,text="run",command=next,state=DISABLED,height=5,width=50)
run.grid(column=2,row=5)

setup = Button(window,text="setup",command=prisonsetup)
setup.grid(column=3,row=1)

quitbutton = Button(window,text="quit",command=window.quit)
quitbutton.grid(column=4,row=5)

# this is usually the last line pertaining to the Windows window.
window.mainloop()
