import os
import json
from PyQt5.QtCore import pyqtSignal, Qt, QThread
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, 
    QGroupBox, QGridLayout, QCheckBox,
    QPushButton, QProgressBar, QLabel,
    QTextEdit
)
from ..widgets.file_processor import FileProcessor
from ..widgets.gpt_handler import GPTHandler 

class AnalysisWorker(QThread):
    analysis_complete = pyqtSignal(dict, int)
    progress_updated = pyqtSignal(int)

    def __init__(self, files, file_processor, gpt_handler):
        super().__init__()
        self.files = files
        self.file_processor = file_processor
        self.gpt_handler = gpt_handler
        self.analysis_prompt = """Analyze this IoT data and provide:
1. Data type identification
2. Potential anomalies
3. Key patterns/trends
4. Suggested visualizations
5. Data quality issues

9Data: """

    def run(self):
        total_files = len(self.files)
        for idx, file in enumerate(self.files):
            content = self.file_processor.read_file(file)
            if content['status'] != 'success':
                self.analysis_complete.emit({
                    'error': f"Failed to read {os.path.basename(file)}: {content['message']}"
                }, idx)
                continue

            prompt = self.analysis_prompt + content['data'][:2000]  # Limit to first 2000 chars
            response = self.gpt_handler.generate_response(prompt)
            
            if response['status'] == 'success':
                try:
                    analysis = json.loads(response['data'])
                except json.JSONDecodeError:
                    analysis = {'error': 'Invalid JSON response from API'}
            else:
                analysis = {'error': response['message']}
            
            self.analysis_complete.emit(analysis, idx)
            self.progress_updated.emit(int((idx + 1) / total_files * 100))

class AIAnalysisTab(QWidget):
    code_generated = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.gpt = GPTHandler()
        self.file_processor = FileProcessor()
        self.current_files = []
        self.analyses = {}
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.progress = QProgressBar()
        self.status = QLabel("Ready for analysis")
        
        self.scroll = QScrollArea()
        self.selection_widget = QWidget()
        self.selection_layout = QVBoxLayout()
        self.selection_widget.setLayout(self.selection_layout)
        self.scroll.setWidget(self.selection_widget)
        self.scroll.setWidgetResizable(True)
        
        btn_analyze = QPushButton("Analyze Files with AI")
        btn_generate = QPushButton("Generate Code")
        btn_analyze.clicked.connect(self.start_analysis)
        btn_generate.clicked.connect(self.generate_code)
        
        layout.addWidget(self.scroll)
        layout.addWidget(self.progress)
        layout.addWidget(self.status)
        layout.addWidget(btn_analyze)
        layout.addWidget(btn_generate)
        self.setLayout(layout)
        
    def load_files(self, files):
        self.current_files = files
        self.analyses.clear()
        
    def start_analysis(self):
        if not self.current_files:
            self.status.setText("No files loaded for analysis")
            return
        
        # Clear previous analysis
        while self.selection_layout.count():
            child = self.selection_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.worker = AnalysisWorker(
            self.current_files,
            self.file_processor,
            self.gpt
        )
        self.worker.analysis_complete.connect(self.handle_analysis_result)
        self.worker.progress_updated.connect(self.progress.setValue)
        self.worker.start()
        
        self.status.setText("AI analysis in progress...")
        self.progress.setValue(0)
        
    def handle_analysis_result(self, analysis, file_idx):
        file = self.current_files[file_idx]
        self.analyses[file] = analysis
        
        group = QGroupBox(f"Analysis: {os.path.basename(file)}")
        grid = QGridLayout()
        
        # Analysis display
        analysis_text = QTextEdit()
        analysis_text.setReadOnly(True)
        
        if 'error' in analysis:
            analysis_text.setPlainText(f"Error: {analysis['error']}")
        else:
            formatted = "\n".join(
                f"{k}:\n{json.dumps(v, indent=2)}" 
                for k, v in analysis.items()
            )
            analysis_text.setPlainText(formatted)
        
        # Include checkbox
        cb_include = QCheckBox("Include in code generation")
        grid.addWidget(cb_include, 0, 0)
        grid.addWidget(analysis_text, 1, 0)
        
        group.setLayout(grid)
        self.selection_layout.addWidget(group)
        
    def generate_code(self):
        selected_analyses = []
        for i in range(self.selection_layout.count()):
            group = self.selection_layout.itemAt(i).widget()
            if isinstance(group, QGroupBox):
                checkbox = group.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    file = self.current_files[i]
                    selected_analyses.append(self.analyses.get(file, {}))
        
        if not selected_analyses:
            self.status.setText("No analyses selected for generation")
            return
        
        prompt = (
            "Generate Python code for IoT data analysis based on these insights:\n"
            f"{json.dumps(selected_analyses, indent=2)}\n\n"
            "Include data processing, anomaly detection, and visualization."
        )
        
        response = self.gpt.generate_response(prompt)
        
        if response['status'] == 'success':
            self.code_generated.emit(response['data'])
            self.status.setText("Code generated successfully!")
        else:
            self.status.setText(f"Generation error: {response['message']}")