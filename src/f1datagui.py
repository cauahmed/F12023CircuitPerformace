#All the data imported and processed here belong to the Ergast API
#API documentation: http://ergast.com/mrd/
#The GUI has been made using flet which a python and flutter library made to create desktop and mobile apps.
#Library documentation: https://flet.dev/docs/

#Relevant packages are imported here
import requests
import apiprocessor
import flet as ft

#The main function of the api file is run to import and process the data for the GUI
apiprocessor.main()
maindict = (apiprocessor.maindict)
#The maxpoints variable is reintroduced 
maxpoints = 0.0

def main(page: ft.Page):
    #Hardcoded window properties for ease of use
    page.title = "2023 F1 constructor stats"
    page.window_width = 1000       
    page.window_height = 1000
    page.scroll = "Auto"

    #The following variables are used to set the heading information
    primarytitle = ft.Text("2023 F1 Championship", size=40)
    subtitle = ft.Text("Constructor Performance Stats", size=35)
    statinfo = ft.Text("Throughout History of Competition", size=30)
    tableheader = ft.Text("Points record", size=20)
    
    #The GUI table columns are initialized by assigning them to a DataTable variable
    Dt = ft.DataTable()
    Dt.columns = [
                ft.DataColumn(ft.Text("Constructor")),
                ft.DataColumn(ft.Text("Best Circuit")),
                ft.DataColumn(ft.Text("Circuit country")),
                ft.DataColumn(ft.Text("Total points"), numeric=True),
                ft.DataColumn(ft.Text("Total Races"), numeric=True),
                ft.DataColumn(ft.Text("Points Per Race"), numeric=True)
            ]
    #Each data item for each dictionary is extracted and put into the cell of the datatable
    global maxpoints
    for constructor in maindict:
        maxpoints = 0.0
        for circuit in maindict[constructor]:
            #The average points/points per race is saved for each circuit for each constructor
            averagepoints = maindict[constructor][circuit]['pointsperrace']
            if(averagepoints > maxpoints):
                    totalpoints = maindict[constructor][circuit]['points']
                    totalraces = maindict[constructor][circuit]['races']
                    #The highest average value is saved in maxpoints
                    maxpoints = averagepoints
                    #The circuitname is also stored in circuitid format
                    circuitname = circuit
        #Detailed constructor and circuit data imported to include name and other details if needed
        constructordata = (requests.get(f'http://ergast.com/api/f1/constructors/{constructor}.json')).json()
        circuitdata = (requests.get(f'http://ergast.com/api/f1/circuits/{circuitname}.json')).json()
        #Row is created for the best circuit result for each constructor 
        Dt.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(constructordata['MRData']['ConstructorTable']['Constructors'][0]['name'])),
                                         ft.DataCell(ft.Text(circuitdata['MRData']['CircuitTable']['Circuits'][0]['circuitName'])),
                                         ft.DataCell(ft.Text(circuitdata['MRData']['CircuitTable']['Circuits'][0]['Location']['country'])),
                                         ft.DataCell(ft.Text(totalpoints)),
                                         ft.DataCell(ft.Text(totalraces)),
                                         ft.DataCell(ft.Text(maxpoints))]))
    
    #All the page items are added to the page
    page.add(
        primarytitle,
        subtitle,
        statinfo,
        tableheader,
        Dt
    )
    
    

ft.app(target=main)