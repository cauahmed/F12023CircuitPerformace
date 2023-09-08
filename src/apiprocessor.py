#All the data imported and processed here belong to the Ergast API
#API documentation: http://ergast.com/mrd/

#Importing library required to get the JSON Data from the API
import requests

#Global variable declaration
maindict ={ }
newcircuitdict = { }
circuitpointsdict = { }
pointsdict ={ }
constructor_list = []
totalcircuitpoints = 0
totalcircuitraces = 0
pointsperrace = 0
#Updated is a boolean switch used to ensure the updating and adding of data are in sync
updated = False
maxpoints = 0.0

#Initial import of constructors who are participating in the 2023 season
constructordata = (requests.get('http://ergast.com/api/f1/2023/constructors.json')).json()

#Function definition responsible for constructing new circuit data for a given constructor
def createcircuitdetails(constructor, circuitid, totalcircuitpoints, totalcircuitraces, pointsperrace): 
    maindict[constructor][circuitid] = {}
    maindict[constructor][circuitid]['points'] = totalcircuitpoints
    maindict[constructor][circuitid]['races'] = totalcircuitraces
    maindict[constructor][circuitid]['pointsperrace'] = pointsperrace
    
#Function responsible for calculating net points scored and races participated in for each circuit where the constructor has raced
def calculatecircuitstats(constructor, circuitid, Result):
    maindict[constructor][circuitid]['points'] = round((maindict[constructor][circuitid]['points'] + float(Result['points'])), 2)
    maindict[constructor][circuitid]['races'] = maindict[constructor][circuitid]['races'] + 1
    maindict[constructor][circuitid]['pointsperrace'] = round((maindict[constructor][circuitid]['points']/maindict[constructor][circuitid]['races']), 2)
    
#Function responsible for printing the processed data
#A similar structure has been used in the GUI   
def results():
    global maxpoints
    #All the keys and subkeys within maindict are iterated 
    for constructor in maindict:
        maxpoints = 0.0
        circuitname = ""
        for circuit in maindict[constructor]:
            averagepoints = maindict[constructor][circuit]['pointsperrace']
            if(averagepoints > maxpoints):
                    maxpoints = averagepoints
                    circuitname = circuit
        constructordata = (requests.get(f'http://ergast.com/api/f1/constructors/{constructor}.json')).json()
        circuitdata = (requests.get(f'http://ergast.com/api/f1/circuits/{circuitname}.json')).json() 
        print(constructordata['MRData']['ConstructorTable']['Constructors'][0]['name'],
              " performed best at ",
              circuitdata['MRData']['CircuitTable']['Circuits'][0]['circuitName'],
              " with average race points of ",
              maxpoints)  

#Function responsible for importing and processing API data
def main():
    #A loop that creates a list of constructors, based on their IDs, using API call for initial import of constructor data
    for constructor in constructordata['MRData']['ConstructorTable']['Constructors']:
        constructor_list.append(constructor['constructorId'])
        
    #The main loop that iterates all the constructors in the constructor list 
    for constructor in constructor_list:
        #Stores constructor ID to be included in the result API call
        resultkeyword = constructor
        #A dictionary is created for each constructor to store the processed data
        maindict[constructor] = {}
        #The API call is made to retrieve the results for each constructor(this call can be streamlined by including more arguments. Takes a limiter which is 30 by default. I have set it to 250 considering processing time.)
        resultsdata = (requests.get(f'http://ergast.com/api/f1/constructors/{resultkeyword}/results.json?limit=250')).json()
        #The updated switch is reset here
        updated = False
        #The result data is accessed here. All the races, for each constructor, present in the imported data are checked.
        for Races in resultsdata['MRData']['RaceTable']['Races']:
            circuitid = Races['Circuit']['circuitId']
            #If the constructor dict is not empty and there is an existing entry for the circuit, its data is updated by adding the points, incrementing the number of races and the average point scored
            if(bool(maindict[constructor])):
                #Given dict size cannot be changed during iteration, a list of keys is created and iterated instead to overcome this issue
                key_copy = list(maindict[constructor].keys())
                for circuit in key_copy:
                    if(circuitid == circuit):
                        for Result in Races['Results']:
                            calculatecircuitstats(constructor, circuitid, Result)
                            #The updated switch is set to true as the entry is successfully updated
                            updated = True
                #If the dict is not empty but the circuit hasnt been added, the updated switch status of false enables a new entry when required
                if(updated == False):         
                    createcircuitdetails(constructor, circuitid, totalcircuitpoints, totalcircuitraces, pointsperrace)
                    for Result in Races['Results']:
                        #This function enables the circuit net points to be updated using the results section of the race data
                        calculatecircuitstats(constructor, circuitid, Result)  
            
            #This code only runs in the first run of the circuit loop when the initial circuit dict is empty                
            else:    
                createcircuitdetails(constructor, circuitid, totalcircuitpoints, totalcircuitraces, pointsperrace)
                for Result in Races['Results']:
                    calculatecircuitstats(constructor, circuitid, Result) 
                
            
#main()   
#print(maindict)
#results()                   
                    
        
        
        
 
        

        
                   
                        
        
        
        
                
            
            

    