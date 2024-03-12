# PyQtGUI-BMEG457
This repo is for the pyqt (or if we decide on something else) version of the GUI. There is a readme file [here](./pyqt-reference.md) that has some resources on pyqt. I'll also add the backend files to this repo and setup the file structure for the pyqt app. 

## File Structure
The main idea is to have two main folder: Models and Views 
Under models we can have more folders for the seperate tasks if need be (ex: graphing has 3 python files can have a folder for graphing)

- Models: The models folder holds the backend files or the application logic
- Views: The views folder holds the frontend side of things. So this would be how users interact with the application and how it looks (clickable buttons, etc)


## Installing packages and venv
A venv is a virtual environment that allows you to install all your needed pip packages without breaking any other program on your laptop. 
- To setup a venv run `python -m venv venv`
- To start the venv on windows run `venv\Scripts\activate.bat` on a cmd terminal or `venv\Scripts\activate.ps1` on a powershell terminal and on mac run  `source myvenv/bin/activate`
- The to install the dependencies run `python -m pip install -r requirements.txt` (this will install all the needed packages in one command)
- If you want to exit the venv run `exit`

If you're developing and want to add a new package to the requirements file you can use the command `pip freeze > requirements.txt` after you install the package you need