# PyQt
## Get Started with PyQT
PyQt is a library for building apps in c and python. [This](https://www.pythontutorial.net/pyqt/) is a pretty good starting point if you have never tried it out before. The tutorials that I think are a bit more useful to get started straight away are below though:
- [Hello world project](https://www.pythontutorial.net/pyqt/pyqt-hello-world/)
- [How the frontend and backend connect (signals and slots)](https://www.pythontutorial.net/pyqt/pyqt-signals-slots/)
- [Creating a button](https://www.pythontutorial.net/pyqt/pyqt-qpushbutton/)
- [Creating a line entry widget](https://www.pythontutorial.net/pyqt/pyqt-qlineedit/)
- [Creating a main window with a toolbar](https://www.pythontutorial.net/pyqt/pyqt-qmainwindow/)
- [Model/View app structure](https://www.pythontutorial.net/pyqt/pyqt-model-view/)

## The bare minimum to understand this app
If you are in a rush and don't want to go through the links above. Here is a quick TL;DR to get you up to speed and to a point where you can understand what's happening in this app. 

PyQt creates widgets that can then be used within other widgets. So for this app we have a mainwindow widget in main.py. This is where the app runs loads all the other pages. A main window has a single central widget that we use to show the different pages of this app. We do this through a stacked widget, basically a widget holding more than one widget and allows you to switch between them easily. 

We then have signals and slots. This is the way PyQt creates actions and listening events. So a button press emits a signal for example and then you can create slots (listeners) to do an action on that signal. This is how we add functionality to the UI. For example if you have a button called myButton and a function called myFunction, you can connect them using `myButton.clicked.connect(myFunction)`

Finally the app structure. This app uses a structure similar to the model/view structure where you have all the backend logic stored in the Models folder. All the frontend files are in the parent directory (tried adding it to a Views folder, but ran into import issues. This should be added to future work list). 

This is the most basic information that can get you started with the app, it will make more sense as you look at the files a bit more. I do however recommend checking out the tutorials if you still find yourself confused. 

## Other Useful Links:
- [More complicated example](https://realpython.com/python-pyqt-gui-calculator/)
- [PyQT6 Docs](https://www.riverbankcomputing.com/static/Docs/PyQt6/index.html)
- [QtDesigner Tutorial](https://realpython.com/qt-designer-python/)