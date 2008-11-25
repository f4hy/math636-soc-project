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


import random

def initialsetup (N, M, ratio, R, S, T, P):
    """Initializes the a prison and returns the next state"""
    
    payoff = {}
    payoff[('C','C')] = R
    payoff[('C','D')] = S
    payoff[('D','C')] = T
    payoff[('D','D')] = P
    
    coop = int(100*ratio)
    defect = int(100*(1-ratio))
    distrobution = ['C']*coop+['D']*defect
    
    
    strats=[ [random.choice(distrobution) for j in range(M)] for i in range(N)]
    
    return (strats,payoff)
    
def play (N,M,strats,payoff):
    """Plays the spacial prison game"""

    
    value=[ [0 for j in range(M)] for i in range(N)]
    
    #calculate the value each member gets
    for i in range(N):
        for j in range(M):
            ourstrat = strats[i][j]
            north    = strats[(i-1)%N][j]
            south    = strats[(i+1)%N][j]
            east     = strats[i][(j+1)%M]
            west     = strats[i][(j-1)%M]
            
            value[i][j]  = payoff[(ourstrat,north)]
            value[i][j] += payoff[(ourstrat,south)]
            value[i][j] += payoff[(ourstrat,east) ]
            value[i][j] += payoff[(ourstrat,west) ]
            
    
    nextstrats=[ ['C' for j in range(M)] for i in range(N)]
    
    #calculate the new strategy
    for i in range(N):
        for j in range(M):
            
            #make a list of us and neighbors with values and their strat
            choices = [(value[i][j],strats[i][j])] #current
            choices.append((value[(i-1)%N][j],strats[(i-1)%N][j]))#north
            choices.append((value[(i+1)%N][j],strats[(i+1)%N][j]))#south
            choices.append((value[i][(j+1)%M],strats[i][(j+1)%M]))#east
            choices.append((value[i][(j-1)%M],strats[i][(j-1)%M]))#west
            
            #pick the strat that has the highest result
            nextstrats[i][j] = max(choices)[1]

            
    return nextstrats

    
