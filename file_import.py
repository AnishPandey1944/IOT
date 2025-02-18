from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, 
    QPushButton, QFileDialog, QLabel
)
from ..widgets.file_processor import FileProcessor

class FileImportTab(QWidget):
    files_loaded = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.file_processor = FileProcessor()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        self.file_list = QListWidget()
        self.file_list.setAlternatingRowColors(True)
        
        btn_layout = QVBoxLayout()
        btn_load = QPushButton("Load Files")
        btn_clear = QPushButton("Clear All")
        btn_load.clicked.connect(self.load_files)
        btn_clear.clicked.connect(self.clear_files)
        
        btn_layout.addWidget(btn_load)
        btn_layout.addWidget(btn_clear)
        
        layout.addLayout(btn_layout)
        layout.addWidget(QLabel("Selected Files:"))
        layout.addWidget(self.file_list)
        self.setLayout(layout)

    def load_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Data Files", "",
            "All Supported Files (*.pdf *.txt *.log *.csv *.xlsx);;"
            "PDF Files (*.pdf);;Text Files (*.txt *.log);;"
            "CSV Files (*.csv);;Excel Files (*.xlsx)"
        )
        if files:
            self.file_list.addItems(files)
            self.files_loaded.emit(files)
            
    def clear_files(self):
        self.file_list.clear()
        self.files_loaded.emit([])