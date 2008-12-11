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
    strats=[ [random.choice(distrobution) for j in xrange(M)] for i in xrange(N)]
    return (strats,payoff)
    
def play (N,M,strats,payoff):
    """Plays the spacial prison game"""

    value=[]
    print "calculating valus"
    #calculate the value each member gets
    for i in xrange(N):
        rowvalues = [] #first calc the rows.
        for j in xrange(M):
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

    print "calculating new strats"
    bestpayoff = max(payoff.values())*4
    #calculate the new strategy
    nextstrats=[]
    for i in xrange(N):
        rowofstrats = []
        for j in xrange(M):
            if value[i][j] < bestpayoff:

                mystrat = strats[i][j]
                def bestneighbor(x, y):
                    if x[0] > y[0]:
                        return x
                    if x[0] == y[0] and y[1] == mystrat:
                        return y
                    return y
                
                best = (value[i][j],mystrat) #current
                best = bestneighbor(best,(value[(i-1)%N][j],strats[(i-1)%N][j]))
                best = bestneighbor(best,(value[(i+1)%N][j],strats[(i+1)%N][j]))
                best = bestneighbor(best,(value[i][(j+1)%M],strats[i][(j+1)%M]))
                best = bestneighbor(best,(value[i][(j-1)%M],strats[i][(j-1)%M]))

            #pick the strat that has the highest result
                rowofstrats.append(best[1])
            else: rowofstrats.append(strats[i][j])
   
        nextstrats.append(rowofstrats)

    
    return nextstrats


    
def countclusters(matrix,typetocount):
    """Counts the clusters"""

    numberofclusters = 0

    N = len(matrix)
    M = len(matrix[0])

    counted=[ [0 for j in xrange(M)] for i in xrange(N)]
    
    def countme(i,j):
        counted[i][j] = 1
        size = 1
        if matrix[(i+1)%N][j] == typetocount and counted[(i+1)%N][j] == 0:
            size += countme((i+1)%N,j)
        if matrix[i][(j+1)%M] == typetocount and counted[i][(j+1)%M] == 0:
            size += countme(i,(j+1)%M)
        if matrix[(i-1)%N][j] == typetocount and counted[(i-1)%N][j] == 0:
            size += countme((i-1)%N,j)            
        if matrix[i][(j-1)%M] == typetocount and counted[i][(j-1)%M] == 0:
            size += countme(i,(j-1)%M)

        return size

    clustersizes = []
    for i in xrange(N):
        for j in xrange(M):
            if counted[i][j] == 0 and matrix[i][j] == typetocount:
                numberofclusters += 1
                clustersizes.append(countme(i,j))
    
               
    return (numberofclusters,clustersizes)
                

