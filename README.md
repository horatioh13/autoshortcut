# Autoshortcut

Super simple python script to create shortcuts and .desktop files for exectuables generated with pyinstaller to run python programs easily from terminal or activities overview.

optional command line argument of -d to create desktop file

workflow is:
1. create python app
2. run pyinstaller 'nameofapp.py'
3. run autoshortcut

autoshort cut automatically finds the newsest build of the app in the build directory.

autoshortcut can be run on itself to generate a shortcut.