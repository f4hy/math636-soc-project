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
    
    return (strats,payoff,bestpayoff)
    
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
            mypayoff  = payoff[(ourstrat,north)]
            mypayoff += payoff[(ourstrat,south)]
            mypayoff += payoff[(ourstrat,east) ]
            mypayoff += payoff[(ourstrat,west) ]
            
            rowvalue.append(mypayoff)
        value.append(rowvalue)
    
    bestpayoff = max(payoff.values())*4
    #calculate the new strategy
    nextstrats=[]
    for i in range(N):
        rowofstrats = []
        for j in range(M):
            if value[i][j] < bestpayoff:
                
            #make a list of us and neighbors with values and their strat
                choices = [(value[i][j],strats[i][j])] #current
                choices.append((value[(i-1)%N][j],strats[(i-1)%N][j]))#north
                choices.append((value[(i+1)%N][j],strats[(i+1)%N][j]))#south
                choices.append((value[i][(j+1)%M],strats[i][(j+1)%M]))#east
                choices.append((value[i][(j-1)%M],strats[i][(j-1)%M]))#west
                
            #pick the strat that has the highest result
                rowofstrats.append(max(choices)[1])
            else: rowofstrats.append(strats[i][j])
   
        nextstrats.append(rowofstrats)

    return nextstrats

    
