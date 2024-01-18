from PeelApp import cmd
from PySide6 import QtWidgets, QtCore
import PCAGBOPlugin as ap

dialogs = {
    "MigrateDirectories": None,
    "ReferenceCleanup": None,
    "GenerateFileStruct": None
}

def openDialog(dialog_name):
    try:
        if dialogs[dialog_name] is None:
            DialogClass = getattr(ap, dialog_name)
            dialogs[dialog_name] = DialogClass(cmd.getMainWindow())

        dialogs[dialog_name].show()
    except Exception as e:
        QtWidgets.QMessageBox.warning(None, "Error", f"An error occurred while opening the window: {e}")

def startup():
    try:
        mw = cmd.getMainWindow()
        agbo_bar = mw.menuBar().addMenu("AGBO")

        settings = [
            ("Migrate", "MigrateDirectories"),
            ("Ref Cleanup", "ReferenceCleanup"),
            ("File Struct Generator", "GenerateFileStruct")
        ]

        for label, dialog_name in settings:
            action = agbo_bar.addAction(label)
            action.triggered.connect(lambda checked=False, name=dialog_name: openDialog(name))
    except Exception as e:
        QtWidgets.QMessageBox.warning(None, "Startup Error", f"An error occurred during startup: {e}")