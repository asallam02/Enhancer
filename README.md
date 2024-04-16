# Enhancer
This repo is for a python graphical user interface (GUI). It uses the PyQt framework. If you are unfimiliar with PyQt I recommend familiarizing yourself with it first before trying to understand this app. There is a reference file [here](./pyqt-reference.md) that has some resources on PyQt and some starter information. 

The main purpose of this app is to offer a UI for gene activation machine learning models. More specifically this app uses [Enformer](https://www.biorxiv.org/content/10.1101/2023.08.30.555582v1). It was developed as our capstone project for UBC biomedical engineering for use in the De Boer lab.  

## Get Started
To get started with this app first make sure you have all the required packages installed. I recommend using a virtual environment (see below for more information on how to set that up), but in case you don't want to do that you can download all the needed packages using `py -m pip install -r requirements.txt`. 

Then to run the app run `py main.py`

## File Structure
The main file structure of this app is as follows:

- Enhancer
    - Models
        - Backend
        - Graphing
    - Templates
    - frontPage.py
    - variablePage.py
    - visualizationPage.py
    - main.py  


### Some points to note:
- The entry point for the app is through main.py, this is the file that will start up the GUI. 
- All the backend logic for the app is stored in the Models folder. The Graphing folder includes all the logic for graphing while the Backend folder includes all the logic for running the machine learning model, creating a query, and querying the USCS database. 
- The Templates file includes the .ui templates for the app generated using qt designer. Please note, the final py files were slightly modified compared to the output you would get from directly translating these files to .py, if you do regenerate the files do so at your own risk. 

## What does the app do?
The flow of the application goes as follows
- User opens the app
- App creates an instance of the Enformer model
- User inputs chromosome and desired location
- App creates a Query object and fetches the desired sequence from the UCSC database
- User edits the sequence, chooses a desired sequence, and clicks go
- App runs the original and modified sequences through enformer and saves the results
- App creates an Organizer object 
- User adds a box
- Organizer object creates a box and saves the parameters
- User clicks next
- App does background calculations, plots the graphs, and shows them 

## Installing packages and venv
To run this app through the terminal we recommend using a venv. A venv is a virtual environment that allows you to install all your needed pip packages without breaking any other program on your laptop due to version differences. 
- To setup a venv run `python -m venv venv`
- To start the venv on windows run `venv\Scripts\activate.bat` on a cmd terminal or `venv\Scripts\activate.ps1` on a powershell terminal and on mac run  `source myvenv/bin/activate`
- Then to install the dependencies run `python -m pip install -r requirements.txt` (this will install all the needed packages in one command)
- If you want to exit the venv run `deactivate`

If you're developing and want to add a new package to the requirements file you can use the command `pip freeze > requirements.txt` after you install the package you need. 

## Future work
Unfortunately we did not get a chance to incorporate everything we wanted to in the time we had. Below is a list of the future work this gui needs if anyone was to take it up in the future. 
- A memory system: If you open the main.py file, you will find several un-implemented functions for memory managements where users can save sessions, sequences, open, and delete them. 
- Multi-threading: This application currently all runs on the same thread. We had looked into multi-threading but did not have enough time to implement it. [Here](https://realpython.com/python-pyqt-qthread/) is a pointer on multithreading using PyQt, the main task that could use a new thread is the ML model predictions as this takes the longest time and could leave the application unresponsive in the mean time. 
- Track visualization: currently the app shows 5 preset tracks, this was done for demo purposes since there are 5000 tracks. The full list of tracks can be found in the tracks.txt file within the Backend folder. More work should be done here identifying which tracks researchers find important and how to dynamically display tracks. 
- Visible status: One important aspect to add is more visible status. This includes loading bars and error messages that could help give the user more context to what is happening in the backend. 