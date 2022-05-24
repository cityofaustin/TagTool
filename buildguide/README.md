### City of Austin Innovation Office

# TagTool Build Guide🏷️

---

## Python Release

If you want to just run the Python file directly, it is highly suggested you [set up a Virtual Environment](https://python.land/virtual-environments/virtualenv) and [use the requirements.txt](https://note.nkmk.me/en/python-pip-install-requirements/) to install the needed plugins. You can then simply run main.py to run the application. This results in a smaller file size and quicker startup time. This version is not user friendly and not as easy to distribute to end users. Use this version if you are experienced in Python as it should run on any OS that supports the QT framework (Windows, Mac, Linux, various Unix platforms). Also note that if you don't install the required libraries in requirements.txt the application may crash when trying to perform certain operations. For easy user friendly deployment, please look at downloading one of the OS builds in the releases section.

### Editing or creating new UI

TagTool uses the PyQT5 library for its user interface. [QT Designer](https://build-system.fman.io/qt-designer-download) was used to create the UI files in this project. They are in the **src folder** under **UI Files**. Once a UI file is saved you will have to run the following command (assuming you have **PYQT5** installed via PIP):

```
pyuic5 -x input.ui -o output.py
```

Replace input.ui with the .ui you created and change output.py to what you want to name the file. This new or updated .py file needs to go into the **ui** folder within the **src** directory. You can then import this new file at the start of the **main.py** script and create a class to create a new window, access UI elements, etc.

### Script changes

If modifying the **main.py** script, there are some things to note.

The **versionNumber** variable near the top of the script should be updated to reflect the latest version number. This is used on the about screen and is only for aesthetic purposes. 

Accessing **default.json** or **res.dat** differs on Windows/Linux/Mac. For Windows and Linux, they are the same, but since Mac has the files embedded within the .app file, some changes need to be made when accessing them. 

A typical block of code when accessing these files looks like this:

```python
if platName == 'Darwin':
    dfJson = pd.read_json(f'{appPath}/default.json')
else:
    dfJson = pd.read_json("default.json")
```

**platName** is assigned at runtime automatically. ***Darwin*** is the name of MacOS, so you will want to check for that and preface the filename with the **appPath** variable and a forward slash.

Another thing to note is that for some reason, a print statement inside of a loop was causing the MacOS version to crash after build. This did not happen when running the script directly from Python and only crashed after building with PyInstaller. Something to keep in mind if seeing strange crashes. 

### Virtual Environment

TagTool is converted to an executable using the **PyInstaller** library. It is highly recommended that you [create a virtual python environment](https://python.land/virtual-environments/virtualenv) and install only the required libraries. Building the application from within this virtual environment is required or else the resulting executable will include every python library you have installed on your local machine, resulting in *massive executable sizes*. A **requirements.txt** is provided in the root of this project and can be installed in your virtual environment by using the following command (from the virtual environment)

```For Mac
pip install -r requirements.txt
```

### Build instructions

Once the virtual environment is built and activated, you can navigate to the src folder. It is recommended that you delete the **dist** and **build** folders before continuing as the next part will generate them with the latest data. After that the following command can be run but will differ based on the OS it's being built for:

```
pyinstaller Windows.spec
pyinstaller Mac.spec
pyinstaller Linux.spec
```

Each OS has its own spec file that has special build instructions. Windows will output a .exe, Mac outputs a .app, and Linux puts out an executable file. The finished build will end up inside of the build folder.

### Version differences and packaging

The Windows and Linux versions need the **res.dat** and the **default.json** files included in the same folder as the executable. 

<img title="" src="img\directory.jpg" alt="IMAGE" width="435">

These can then be zipped up and distributed. On Windows and Linux these two files ***must*** always be in the same directory as the executable file.

For Mac, the build should produce a single **.app** file. The **res.dat** and **default.json** are stored inside the .app file and are managed within. All you need to do is zip up the .app and it should be good for distribution.
