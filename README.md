# F12023CircuitPerformace

The repository consists of two script files written in Python.

The main file is the apiprocessor.py file, which contains all the app logic.

The f1datagui.py file is the application frontend file powered by the apiprocessor.py file.

The pseudocode behind the program is as follows:
For each constructor
	Find out the results for each constructor
		For each result, add a circuit to the list of circuits for the constructor
			Add points and calculate average if circuit exits
			Create new circuit data if circuit doesnot exist

The circuit with most points per race for each constructor is the one where they performed best at throughout history. For this program, I have not added any season, round or position modifiers to the api call. 
The relevant circuit data is displayed using a DataTable in the GUI. The GUI can support more functionalities in the future and the apiprocessor.py file can be changed likewise to support the said functionalities.

Final dict structure in JSON upon completion of the data processing stage: {ConstructorID: CircuitID : points: , races: , pointsperrace}

Testing methodology:
I initially imported small datasets and manually calculated the points, races and points per race values for each circuit for each constructor. The program returned the same values for that given dataset. 
Most used debugging tool: Print statements

I am open to criticism and would happily accept suggestions to improve the code.
