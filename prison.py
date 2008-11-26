#!/usr/bin/python
"""
Program for prisoners delema calculations. 
Written for math363 by Brendan Fahy

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
import random

def initialsetup (N, M, ratio, R, S, T, P):
    """Initializes the a prison and returns the next state"""

    #set up they payoff matrix
    payoff = {}
    payoff[('C','C')] = R
    payoff[('C','D')] = S
    payoff[('D','C')] = T
    payoff[('D','D')] = P

    coop = int(100*ratio)
    defect = int(100*(1-ratio))
    #creates a list filled with 'C' and 'D' in the corect proportion
    distrobution = ['C']*coop+['D']*defect
    #randomly chooese from the list
    strats=[ [random.choice(distrobution) for j in range(M)] for i in range(N)]
    
    return (strats,payoff)
    
def play (N,M,strats,payoff):
    """Plays the spacial prison game"""

    value=[]
    #calculate the value each member gets
    for i in range(N):
        rowvalues = [] #first calc the rows.
        for j in range(M):
            mystrat = strats[i][j]  
            north    = strats[(i-1)%N][j]
            south    = strats[(i+1)%N][j]
            east     = strats[i][(j+1)%M]
            west     = strats[i][(j-1)%M]
            
            #sum the payoff with neighbors
            mypayoff  = payoff[(mystrat,north)]
            mypayoff += payoff[(mystrat,south)]
            mypayoff += payoff[(mystrat,east) ]
            mypayoff += payoff[(mystrat,west) ]
            
            


            rowvalues.append(mypayoff)
        value.append(rowvalues)

    print "done with payoffs"
    
    bestpayoff = max(payoff.values())*4
    print bestpayoff
    #calculate the new strategy
    nextstrats=strats[:]
    for i in range(N):
        for j in range(M):
            if value[i][j] < bestpayoff:
                
            #make a list of us and neighbors with values and their strat
                
                choices = [(value[i][j],strats[i][j])] #current
                bestneighbor = max([((value[(i+x)%N][(j+y)%M],strats[(i+x)%N][(j+y)%M])) for x in xrange(-1,2) for y in xrange(-1,2) if x**2!=y**2])
                if (value[i][j],strats[i][j]) < bestneighbor:
                    nextstrats[i][j] = bestneighbor[1]

   


    return nextstrats

    
