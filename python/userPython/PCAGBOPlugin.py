import os
import shutil
import re
from PeelApp import cmd
from PySide6 import QtWidgets, QtCore

class MigrateDirectories(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._src_directory = None
        self._dst_directory = None
        self._migrated_count = 0
        self.initUI()
        
    def initUI(self):
        layout = QtWidgets.QFormLayout()
        self.initDirectorySelectionUI(layout)
        self.initProgressBarUI(layout)
        self.setLayout(layout)
        
    def initDirectorySelectionUI(self, layout):
        self.title = QtWidgets.QLabel("-Migrate Settings-\n")
        layout.addRow("", self.title)

        # Source directory selection
        self.sourceButton = QtWidgets.QPushButton('Select Source Directory')
        self.sourceButton.clicked.connect(self.selectSourceDirectory)
        layout.addWidget(self.sourceButton)
        self._sourceLabel = QtWidgets.QLabel('Source Directory: None')
        layout.addWidget(self._sourceLabel)

        # Destination directory selection
        self.destButton = QtWidgets.QPushButton('Select Destination Directory')
        self.destButton.clicked.connect(self.selectDestinationDirectory)
        layout.addWidget(self.destButton)
        self._destLabel = QtWidgets.QLabel('Destination Directory: None\n')
        layout.addWidget(self._destLabel)

        # Migrate button
        self.migrateButton = QtWidgets.QPushButton("Migrate")
        self.migrateButton.released.connect(self.setupMigrate)
        layout.addRow("", self.migrateButton)
        
    def initProgressBarUI(self, layout):
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setVisible(False)
        self.progressBar.setStyleSheet("QProgressBar::chunk { background: #444; } "
                                       "QProgressBar{ text-align: center; color: #ccc; padding: 1px; height:10px; }")
        layout.addWidget(self.progressBar)
    
    def selectSourceDirectory(self):
        self._src_directory = QtWidgets.QFileDialog.getExistingDirectory()
        if self._src_directory:
            self._sourceLabel.setText(f'Source Directory: {self._src_directory}')

    def selectDestinationDirectory(self):
        self._dst_directory = QtWidgets.QFileDialog.getExistingDirectory()
        if self._dst_directory:
            self._destLabel.setText(f'Destination Directory: {self._dst_directory}\n')
    
    def setupMigrate(self):       
        try:
            self.progressBar.setVisible(True)
            self.progressBar.setMaximum(len(os.listdir(self._src_directory)))
            self.migrateFiles()
            self.progressBar.setValue(self.progressBar.maximum())
            self.progressBar.setFormat("Files copied successfully")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error:", f"An error occurred: {e}")
    
    def migrateFiles(self):
        if not os.path.exists(self._dst_directory):
            os.makedirs(self._dst_directory)

        for item in os.listdir(self._src_directory):
            self.progressBar.setValue(self._migrated_count)
            self.progressBar.setFormat("f{item}")
            
            src_path = os.path.join(self._src_directory, item)
            dst_path = os.path.join(self._dst_directory, item)

            if os.path.isdir(src_path):
                self.copyDirectory(src_path, dst_path)
            else:
                shutil.copy(src_path, dst_path)
                self._migrated_count += 1

    def copyDirectory(self, src, dst):
        if not os.path.exists(dst):
            shutil.copytree(src, dst)
        else:
            for item in os.listdir(src):
                src_path = os.path.join(src, item)
                dst_path = os.path.join(dst, item)
                if os.path.isdir(src_path):
                    self.copyDirectory(src_path, dst_path)
                else:
                    shutil.copy(src_path, dst_path)
                    self._migrated_count += 1


class GenerateFileStruct(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._session_directory = None
        self._session_date = None
        self.initUI()
        
    def initUI(self):
        layout = QtWidgets.QFormLayout()
        
        self.title = QtWidgets.QLabel("File Settings:\n")
        layout.addRow("", self.title)
        
        # Shoot Day
        self._session_date = QtWidgets.QLineEdit()
        layout.addRow("Shoot Day [yymmdd]:", self._session_date)
        
        # Session directory selection
        self.sourceButton = QtWidgets.QPushButton('Select Session Directory')
        self.sourceButton.clicked.connect(self.selectSessionDirectory)
        layout.addWidget(self.sourceButton)
        self.sessionLabel = QtWidgets.QLabel('Session Directory: None\n')
        layout.addWidget(self.sessionLabel)
        
        # Generate button
        self.cleanupButton = QtWidgets.QPushButton("Generate Structure")
        self.cleanupButton.released.connect(self.setupDirStructure)
        layout.addRow("", self.cleanupButton)
        
        self.setLayout(layout)
        
    def selectSessionDirectory(self):
        self._session_directory = QtWidgets.QFileDialog.getExistingDirectory()
        if self._session_directory:
            self.sessionLabel.setText(f'Source Directory: {self._session_directory}\n')
        
    def setupDirStructure(self):
        session_date = self._session_date.text()

        # Regex pattern for yymmdd format
        pattern = r'^\d{2}\d{2}\d{2}$'
    
        if not re.match(pattern, session_date):
            QtWidgets.QMessageBox.warning(self, "Invalid Date Format", "The date must be in yymmdd format.")
            return
        
        if self._session_directory == None:
            QtWidgets.QMessageBox.warning(self, "Invalid Session Direcroty", "Please choose a session directory")
            return

        base_path = os.path.join(self._session_directory, session_date)
        subdirs = [
            os.path.join(base_path, 'Mocap', 'Raw'),
            os.path.join(base_path, 'Mocap', 'Cleaned'),
            os.path.join(base_path, 'RefCams')
        ]

        for subdir in subdirs:
            self.makeDayDirStructure(subdir)
            
        cmd.setDataDirectory(f"{subdirs[2]}")
        
        QtWidgets.QMessageBox.information(self, "Success", "File struct generated.\nPeelCapture settings changed.")
            
    def makeDayDirStructure(self, path):
        try:
            os.makedirs(path, exist_ok=True)
        except OSError as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Could not create directory {path}: {e}")
        
        
class ReferenceCleanup(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ref_directory = None
        self.initUI()
        
    def initUI(self):
        QtWidgets.QMessageBox.warning(self, "WARNING", f"Only cleanup after shotgrid publish")
        
        layout = QtWidgets.QFormLayout()
        
        self.title = QtWidgets.QLabel("-Reference Cam Cleanup-\n")
        layout.addRow("", self.title)
        
        # Reference directory selection
        self.refButton = QtWidgets.QPushButton('Select Reference Directory')
        self.refButton.clicked.connect(self.selectSourceDirectory)
        layout.addWidget(self.refButton)
        self.refLabel = QtWidgets.QLabel('Reference Directory: None\n')
        layout.addWidget(self.refLabel)
        
        # Cleanup button
        self.cleanupButton = QtWidgets.QPushButton("Cleanup Ref Cams")
        self.cleanupButton.released.connect(self.takeCleanup)
        layout.addRow("", self.cleanupButton)
        
        self.setLayout(layout)
    
    def selectSourceDirectory(self):
        self._ref_directory = QtWidgets.QFileDialog.getExistingDirectory()
        if self._ref_directory:
            self.refLabel.setText(f'Source Directory: {self._ref_directory}\n')
    
    def takeCleanup(self):
        """
        Move files with the given name header to their respective folders.
        """
        all_files = [f for f in os.listdir(self._ref_directory) if os.path.isfile(os.path.join(self._ref_directory, f))]

        for filename in all_files:
            prefix = filename.split('_')[0]

            folder_path = os.path.join(self._ref_directory, prefix)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            os.rename(os.path.join(self._ref_directory, filename), os.path.join(folder_path, filename))
            
        QtWidgets.QMessageBox.information(self, "Cleanup Complete", f"All reference camera files moved to respective folders")