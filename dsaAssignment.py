import random
import pickle
from collections import deque

startState =0
unvisited = -1
sccCounter =0
ids = []
lowVals = []
onStack = []
stack = []
newDFA =[]
next=0
scc = []
sccLengths = []

def dfaDepth(startState, adjacencyMatrix):
    # -----------Question 2 and 4-----------
    numberOfNodes = len(adjacencyMatrix)
    searchQueue = deque([])
    visited =[]
    visited.append(startState)  # append start state as visited

    # beginning from start state
    for i in range(len(adjacencyMatrix[startState])):  # loop through columns of the start state row
        if (adjacencyMatrix[startState][i] != 0):
        #if adjacencyMatrix[startState][i] == 'a' or adjacencyMatrix[startState][i] == 'b':  # if the column contains a or b it means that there is a transition
            if i not in visited: #do the following if the state hasn't already been visited
                visited.append(i)  # append the state number to the array of visited nodes
                searchQueue.append(i) #enqueue the state number

    #loop while the queue is not empty
    while (searchQueue):
        currentState=searchQueue.popleft()
        #currentState = searchQueue.get() #get the head of queue
        for i in range(len(adjacencyMatrix[currentState])):  # loop through columns of the start state row
           # if adjacencyMatrix[currentState][i] == 'a' or adjacencyMatrix[currentState][i] == 'b':  # if the column contains a or b it means that there is a transition
           if(adjacencyMatrix[currentState][i] != 0):
                if (i not in visited): #do the following if the state hasn't already been visited
                    visited.append(i)  # append the state number to the array of visited nodes
                    searchQueue.append(i) #enque state

    #print the path of visited states and the depth of the DFA
    print("Number of states in DFA: ",numberOfNodes)
    print("Visited Nodes: ")
    print(*visited)
    print("Depth of DFA: ",len(visited) - 1)



#computes intersaction of two arrays
def intersection(arr1, arr2):
    arr3 = [value for value in arr1 if value in arr2]
    return arr3

#computes the set difference of two arrays
def diff(first, second):
    difference =[value for value in first if value not in second]
    return  difference

#finds the position of a specific element in a 2D array
def index_2d(data, search):
    for i, e in enumerate(data):
        try:
            return i, e.index(search)
        except ValueError:
            pass
    raise ValueError("{} is not in list".format(repr(search)))


def Hopcroft(acceptingRejectingDict, dfa):
    setOfFinalStates = []
    setOfNonFinalStates = []
    alphabet = ['a', 'b']

    #Separating nodes into two sets which are the set of final states and set of non final states
    for key, value in acceptingRejectingDict.items():
        if value == 'Accepting':
            setOfFinalStates.append(key)
        else:
            setOfNonFinalStates.append(key)

    waitingSet=[]
    partition=[]

    partition.append(setOfFinalStates) #append final and non-final states to partition P
    partition.append(setOfNonFinalStates)
    waitingSet.append(setOfFinalStates)#append final states to waiting set W

    while(waitingSet): #loop while waiting set is not empty
        set = waitingSet.pop() #remove a set A from waiting set

        for letter in alphabet: #for each possible transition
            X=[] #set this back to an empty array just in case it was populated in the previous iteration
        #get the set of states that when processing the transition letter, end up in one of the states in the array set
            for column in set:#for all states in set
                for row in range(len(dfa)):#find the state that has a transition letter coming out of it
                    if(dfa[row][column] == letter):
                        if row not in X:
                    # append the row where the transition letter matched (because the row number is the same as the state number
                            X.append(row)

            count = 0 #keeps track of which position we are currently in, in the partition array
            for Y in partition:
                intersect = intersection(Y, X) #compute intersection between sets Y and X
                setDiff = diff(Y,X)#compute set difference Y\X
                if(len(intersect)>0 and len(setDiff)>0): #if both of the sets are populated with something
                    partition[count] = intersect #replace Y in partition with intersaction set
                    partition.append(setDiff) #append set difference to partition

                    if(Y in waitingSet):
                        waitingSet.remove(Y) #replace Y in waiting set by the set differenc and intersaction found above
                        waitingSet.append(intersect)
                        waitingSet.append(setDiff)
                    else: #else append the smallest of the two sets
                        if intersect <= setDiff:
                            waitingSet.append(intersect)
                        else:
                            waitingSet.append(setDiff)
                count+=1

    print("Final Partition: ")
    print(partition)
    return partition

def constructNewDfa(partition,dfa, dict):
    minimizedDFA = []
    alphabet = ['a', 'b']
    minDFAdict = {}

    minimizedDFAsize = len(partition)

    for i in range(minimizedDFAsize): # for n number of rows
        minimizedDFA.append([0 for x in range(minimizedDFAsize)])

    count = 0
    #construct the minimized dfa
    for equivalenceSet in partition: #for each partition
        state =equivalenceSet[0] #get the first element from the equivalence set
        if(dict[state] == "Accepting"):
            minDFAdict[count] = 'Accepting'
        else:
            minDFAdict[count] = 'Rejecting'

        for transition in alphabet: #for all the alphabet
            for x in range(len(dfa[state])): #loop through the original dfa at row indicated by state
                if(dfa[state][x]==transition): #if the element is equal to transition
                    position = index_2d(partition, x) #check where the number stored in x is found in the partition array
                    minimizedDFA[count][position[0]] = transition
        count+=1

    #print information of new minimized dfa
    print("New Minimized DFA:")
    for row in range(len(minimizedDFA)):
          print(minimizedDFA[row])
    print("\nAccepting and Rejecting states:")
    print(minDFAdict)

    pickle_prob = open("minDfaDict.pickle", "wb") #pickle dictionary
    pickle.dump(minDFAdict, pickle_prob)
    pickle_prob.close()

    return minimizedDFA

def getStartState(partitions, startState):
    position = index_2d(partitions, startState)  # check where the start state is found in array partitions
    print("Start state= ", position[0])
    return position[0]

def stringGeneration(dfa, startState):
    print(dfa)
    print(startState)

    alphabet = ['a', 'b']

    pickle_in1 = open("minDfaDict.pickle", "rb") #get the pickled dictionary
    dict = pickle.load(pickle_in1)
    print(dict) #

    for i in range(100): #for all 100 strings do the following
        string = [] #stores the string to be generated
        stringLength = random.randint(1, 128) #randomly choose the string size

        for j in range(stringLength):   #loop used to generate the whole string
            letter = random.choice(alphabet) #choose either letter 'a' or 'b'
            string.append(letter)

        nextState = startState
        stringCounter = 0  # keeps current position in string
        while stringCounter < len(string):  # loop through the string starting from the second letter
            for x in range(0, len(dfa[nextState])):  #loop through columns of the state we are analyzing
                if dfa[nextState][x] == string[stringCounter]: #if a transition is met
                    nextState = x #set the next state equal to the column number
                    break
            stringCounter += 1

        if dict[nextState] == 'Accepting': #if the last state it ends upon is accepting print that string is accepted
            print(*string, ": Accepted")
        else: #else string is rejected so tell user it is rejected.
            print(*string, ": Rejecting")


def dfsForTarjanAlgo(currentNodeId):

    global sccCounter, stack, next, scc, sccLengths
    stack.append(currentNodeId) #push the id of the current node on the stack
    onStack[currentNodeId] = True #mark current node as being on the stack

    ids[currentNodeId] = next #give the positions at currentNodeID an Id value
    lowVals[currentNodeId] = next
    next+=1

    for element in range(len(newDFA[currentNodeId])): #loop through columns of DFA at row indicated by element
        if(newDFA[currentNodeId][element] !=0): #if it is not equal to zero i.e if there is a transition
            if (ids[element] == unvisited): #check if the state we're going to is marked as unvisited
                dfsForTarjanAlgo(element) #call this enforcing recursion
            if onStack[element]: #this line executes after the recursive stage above is done
                #if the state we came from is on the stack
                lowVals[currentNodeId] = min(lowVals[currentNodeId],lowVals[element]) #get the minimum between the current low link value,
                #and the state we have been at.

    if(ids[currentNodeId]==lowVals[currentNodeId]): #check if we are at the beginning of a scc
        print("Strongly Connected components: ")
        while True:
            element = stack.pop() #pop off the scc from the stack
            print("Node:", element) #print popped element
            scc.append(element) #append it to an array of stringly connected components
            onStack[element] = False #mark the node as not being on the stack anymore
            lowVals[element] = ids[currentNodeId] #giving the popped values the same ID
            if element == currentNodeId:
                sccLengths.append(len(scc))
                scc=[]
                break

    sccCounter+=1



numberOfNodes = 0
def main():
    global newDFA, ids, lowVals, onStack, stack, sccCounter, sccLengths
    #-------------For Question 1----------
    acceptingRejectingDictionary = {} #dictionary that will store state number as key and 'Rejecting' or 'Accepting' as their corressponding value
    acceptOrReject = ['Accepting', 'Rejecting'] #will be used to randomly pick one of the two elements
    global numberOfNodes

    numberOfNodes= random.randint(16,64) # randomly choose number of states for DFA
        
    adjacencyMatrix = [] # 2D list
    for i in range(numberOfNodes): # for n number of rows
        adjacencyMatrix.append([0 for x in range(numberOfNodes)]) #create n number of columns containing 0

        #get a random number to indicate to which state the current state can transition to
        transitionA = random.randint(0, numberOfNodes-1)
        transitionB = random.randint(0, numberOfNodes-1)

        if transitionA == transitionB: #if same number is randomly picked up
            #keep trying to randomly find an integer that is not equal to the same as the one found for transition a
            while transitionB == transitionA:
                transitionB = random.randint(0, numberOfNodes-1)

        #change elements from 0 to 'a' or 'b', to show that there is a transition from node i to the nodes indicated by transitionA and transitionB
        adjacencyMatrix[i][transitionA] = 'a'
        adjacencyMatrix[i][transitionB] = 'b'

        label = random.choice(acceptOrReject) #randomly choosing if this state is accepting or rejecting
        acceptingRejectingDictionary[i] = label #add the state number as a key and add Rejecting or Accepting as its value

    startState = random.randint(0, numberOfNodes-1) #randomly choose a start state
    print("Start", startState)

    for row in range(len(adjacencyMatrix)):
          print(adjacencyMatrix[row])
    print(acceptingRejectingDictionary)
    '''
    #Used to test the depth of a DFA
    adjacencyMatrix= [
        [0,0,0,0,'a','b'],
        [0,'b','a',0,0,0],
        [0,0,'a',0,'b',0],
        ['a','b',0,0,0,0],
        ['b',0,0,0,'a',0],
        [0,0,'b',0,'a',0]
    ]
    startState = 4
    '''
    dfaDepth(startState, adjacencyMatrix) #call this function to compute the depth of the DFA

    '''
    #Used to test Hopcroft with a dfa found in a paper online : https://www3.nd.edu/~dthain/compilerbook/chapter3.pdf
    adjacencyMatrix = [
        [0,'a','b',0,0],
        [0,'a',0,'b',0],
        [0,'a','b',0,0],
        [0,'a',0,0,'b'],
        [0,'a','b',0,0]]

    acceptingRejectingDictionary[0] = 'Rejecting'
    acceptingRejectingDictionary[1] = 'Rejecting'
    acceptingRejectingDictionary[2] = 'Rejecting'
    acceptingRejectingDictionary[3] = 'Rejecting'
    acceptingRejectingDictionary[4] = 'Accepting'
    startState=0
    '''
    partitions = Hopcroft(acceptingRejectingDictionary, adjacencyMatrix) #call this function to apply hopcroft minimization
    newDFA = constructNewDfa(partitions, adjacencyMatrix, acceptingRejectingDictionary) #call this function to construct the dfa passing the partitions gotten from hopcroft, the original dfa and its dictionary
    newstartState = getStartState(partitions, startState) #call this function to find the start state of the minimised dfa
    dfaDepth(newstartState, newDFA) #compute the depth of the new dfa
    stringGeneration(newDFA, newstartState) #call this function to execute string generation and finding out if it is accepted or rejected.

    numberOfNodes
    numberOfNodes = len(newDFA)
    #initializing global variables which will be used for tarjans algorithm
    ids = [unvisited] * numberOfNodes #stores id of every node. Initialize all of them to being unvisited (-1)
    lowVals = [0] * numberOfNodes #stores low link values
    onStack = [False] * numberOfNodes #stores if state is on stack
    '''
    #Used to test Tarjan's algorithm using the graph found in this video: https://www.youtube.com/watch?v=TyWtx7q2D7Y
    numberOfNodes = 8
    newDFA=[
    [0, 'a', 0, 0, 0, 0, 0, 0],
    [0, 0, 'a', 0, 0, 0, 0, 0],
    ['b', 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 'a'],
    [0, 0, 0, 0, 0, 'a', 0, 0],
    [0, 0, 0, 0, 0, 0, 'b', 0],
    [0, 0, 0, 0, 'a', 0, 0, 0],
    [0, 0, 0, 'b', 0, 0, 0, 0],]'''

    for i in range(0,numberOfNodes): #loop through states
        if(ids[i] == unvisited): #if state has notbeen visited yet
            dfsForTarjanAlgo(i) #compute depth first search

    print("Number of strongly connected graphs: ", len(sccLengths))
    largest = max(sccLengths)
    print("Largest SCC: " ,largest)
    smallest = min(sccLengths)
    print("Smallest SCC: " , smallest)

    enter=input("Press enter to exit...")


main()