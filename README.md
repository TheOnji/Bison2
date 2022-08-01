Bison2 - A FFXIV gear optimizer

Vision
The Bison2 program shall have a graphical interface where the user can specify what gear they want Bison to test for BIS. The interface shall have multiple pages where a user can choose to enter data for their job's rotation and view the results of Bison. The user input of rotation data should be saved in a database (JSON) to build up more knowledge of rotations as the tool is being used. 

Bison2 should not require extensive manual labor to be updated. It shall implement webscraping and automation to always stay up to date with minimal effort from the creator. 

When the software is complete it will be deployed to a host service for decentraliced use. 


---Developers memo---

To do list:
- Explore multiprocessing for speed gains
- Add multipage support for:
    1. Add new JSON file with job rotation
    2. Results page to display Bison2 results
- Add logic and system for storing and parsing rotation specs from JSON files
- Add webbscraping from Allagan studies to parse Job modifiers (MAIN and DIV)
- Add unit testing (as needed)
- Add login functionallity for deploying app to cloud
- Implement the old cursed Materia slotter to meld materia to bis if so desired
- Implement the allagan functions with an equip function to assemble stats from the item objects
    1. Equip() should be persistant in the loops to reduce memory usage (same as gear and food etc)
    2. DPS function needs to utilize JSON data instead of predefined functions.
- Streamlit interface needs to use session_state to manage data between pages (multipage)
- Select all button for main page in interface (via session state)

Implemented features:
- Single page streamlit interface
- Optimized Bison loop with GCD and materia fast checks before materia matrix tests
- Webscraping data for bis gear and food options and automatically store in JSON files
- Removed list unpack of iterable to optimize speed (was never needed anyway)
- Interfaced streamlit UI with main function and bison algorithm
- Implemented Food, Gear and Materia as callable objects to avoid rewriting memory in each Bison iteration