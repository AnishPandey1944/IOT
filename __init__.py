from PyQt5.QtWidgets import QMainWindow, QTabWidget
from .tabs.file_import import (
    FileImportTab,)
from .tabs.ai_analysis import AIAnalysisTab
from .tabs.ai_chat import AIChatTab
from .tabs.code_gen import CodeGenerationTab
from .tabs.visualization import VisualizationTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced IoT Analyzer")
        self.setGeometry(100, 100, 1200, 800)
        
        self.tabs = QTabWidget()
        self.file_import = FileImportTab()
        self.ai_analysis = AIAnalysisTab()
        self.code_gen = CodeGenerationTab()
        self.visualization = VisualizationTab()
        self.ai_chat = AIChatTab()
        
        self.tabs.addTab(self.file_import, "📁 Import")
        self.tabs.addTab(self.ai_analysis, "🤖 AI Analysis")
        self.tabs.addTab(self.code_gen, "💻 Code Gen")
        self.tabs.addTab(self.visualization, "📊 Visualize")
        self.tabs.addTab(self.ai_chat, "💬 AI Chat")
        
        self.setCentralWidget(self.tabs)
        self._connect_tabs()

    def _connect_tabs(self):
        self.file_import.files_loaded.connect(self.ai_analysis.load_files)
        self.ai_analysis.code_generated.connect(self.code_gen.set_code)
        self.code_gen.data_processed.connect(self.visualization.load_data)