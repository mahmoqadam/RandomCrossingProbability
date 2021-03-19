from numpy import *
import numpy as np
import numpy as num

########################################################################################
#####  INPUT  ##########################################################################

# number of Interfaces
num_interfcace= 20
# probability that crossing with first interface is in region A
pA= 0.00001
# probability that if you are in region A or B on interface i you reach interface i+1
pAjump= 0.5
pBjump= 0.4
# number of random numbers
ncycle= 100
# number of cycles
mcycle= 10

# save info
NAMES = ["number of intergace:               ", "initial probability in A region: ", "probability of jumping from A:   ", "probability of jumping from B:   ", "number of Random numbers:      ", "Cycle number :                  "]
FLOATS = [num_interfcace, pA, pAjump, pBjump, ncycle, mcycle]
DAT =  num.column_stack((NAMES, FLOATS))
num.savetxt('info.txt', DAT, delimiter=" ", fmt="%s")
#### END INPUT ##########################################################################
#########################################################################################

AvepCrossTotList=0
setBackToInitialpA=pA
pCrossTotList=np.zeros([mcycle])
count = 0

def RAND(ncycle,pA,interf,NA,NB,pInA,pInB,pCross):
    ListA=[]
    ListB=[]
    print "Target Probability:", pA
    # build two random sets
    randset=array([random.rand(ncycle),random.rand(ncycle)])
    for i in range(len(randset[0,:])):
        if randset[0,i]<pA:
            # add point
            NA[interf]=NA[interf]+1
            # build list of points
            ListA.append(randset[0,i])
        else:
            NB[interf]=NB[interf]+1
            ListB.append(randset[0,i])
    # convert List to Array
    ListInA = np.array(ListA)
    ListInB = np.array(ListB)
    pInA[interf]= np.array(NA[interf]/(NA[interf]+NB[interf]))
    pInB[interf]= np.array(NB[interf]/(NA[interf]+NB[interf]))
    pCross[interf] = (NA[interf]+NB[interf])/ncycle
    #print "Points in A:", ListInA
    #print "Points in B:", ListInB
    print "Number of Points in A:", NA[interf]
    print "Number of Points in B:", NB[interf]
    print "Total number of points:", NA[interf]+NB[interf]
    print "Probability of being in A: ", pInA
    print "Probability of being in B: ", pInB
    print "Crossing Probability: ", pCross
    print "**************************"

def RAND2(ncycle,pA,interf,NA,NB,pInA,pInB,pAjump,pBjump,pCross):
    ListA=[]
    ListB=[]
    print "Target Probability:", pA
    # build two random sets
    randset=array([random.rand(ncycle),random.rand(ncycle)])
    for i in range(len(randset[0,:])):
        if randset[0,i]<pA:
            if randset[1,i]<pAjump:
                NA[interf]=NA[interf]+1
                ListA.append(randset[0,i])
        else:
            if randset[1,i]<pBjump:
                NB[interf]=NB[interf]+1
                ListB.append(randset[0,i])
    # convert List to Array
    ListInA = np.array(ListA)
    ListInB = np.array(ListB)
    pInA[interf]= np.array(NA[interf]/(NA[interf]+NB[interf]))
    pInB[interf]= np.array(NB[interf]/(NA[interf]+NB[interf]))
    pCross[interf] = (NA[interf]+NB[interf])/ncycle
    #print "Points in A:", ListInA
    #print "Points in B:", ListInB
    print "Number of Points in A:", NA[interf]
    print "Number of Points in B:", NB[interf]
    print "Total number of points:", NA[interf]+NB[interf]
    print "Probability of being in A: ", pInA
    print "Probability of being in B: ", pInB
    print "Crossing Probability: ", pCross
    print "**************************"


while (count < mcycle):
    j=0
    # number for points in region A and B
    NA=np.zeros([num_interfcace])
    NB=np.zeros([num_interfcace])
    # build list for region A and B
    ListA=[]
    ListB=[]
    # probability of being in A and B
    pInA=np.zeros([num_interfcace])
    pInB=np.zeros([num_interfcace])
    # crossing probability
    pCross=np.zeros([num_interfcace])
    pCrossCons = 1
    # overall crossing probability
    pCrossTot =1
    pA=setBackToInitialpA
    print "********************************************************"
    print "************************ INPUT *************************"
    print "number of Interfaces: ", num_interfcace
    print "initial probability in A region: ", pA
    print "probability of jumping from A: ", pAjump
    print "probability of jumping from B: ", pBjump
    print "number of Random numbers: ", ncycle
    print "********************** END INPUT ***********************"
    print "********************************************************"
    # probability for each interface
    for interf in xrange (num_interfcace):
        # initial run to find probability in A and B
        if interf == 0:
            print "Interface number: ", interf
            print "Cycle Counter: ", count
            RAND(ncycle,pA,interf,NA,NB,pInA,pInB,pCross)
        # probability of jumping to next interface from region A or B
        if interf > 0:
            print "Interface number:", interf
            print "Cycle Counter: ", count
            # set A region target probability with last probability of region A
            pA=pInA[interf-1]
            RAND2(ncycle,pA,interf,NA,NB,pInA,pInB,pAjump,pBjump,pCross)

    # total crossing proability
    for n in xrange(num_interfcace):      
        pCrossTot= pCrossCons * pCross[n]
        pCrossCons = pCrossTot

    print "Overall Crossing Probability", pCrossTot
    pCrossTotList[count]=pCrossTot
    count = count + 1
print "*********************************************************"
print "************************ RESULT *************************"
print "List Of Overall Crossing Probability: ", pCrossTotList
for r in xrange(count):
    AvepCrossTotList+=(pCrossTotList[r]/count)
print "Average Of Overall Crossing Probability: ", AvepCrossTotList
savetxt("matrix.csv", pCrossTotList)
f = open('AvepCrossTotList.txt', 'w')
f.write("Average Of Overall Crossing Probability:: %s" % AvepCrossTotList)
f.close()
