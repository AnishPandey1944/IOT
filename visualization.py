from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class VisualizationTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        
        self.plot_type = QComboBox()
        self.plot_type.addItems(["Line", "Bar", "Scatter", "Histogram"])
        
        btn_refresh = QPushButton("Refresh Plot")
        btn_refresh.clicked.connect(self.update_plot)
        
        layout.addWidget(self.plot_type)
        layout.addWidget(self.canvas)
        layout.addWidget(btn_refresh)
        self.setLayout(layout)
        
    def load_data(self, data):
        self.current_data = data
        self.update_plot()
     
    def update_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        if not hasattr(self, 'current_data'):
            return
        
        plot_type = self.plot_type.currentText()
        
        try:
            if plot_type == "Histogram":
                ax.hist(self.current_data.values(), bins=20)
            else:
                # Implement other plot types
                ax.plot(self.current_data.values())
            
            ax.set_title(f"{plot_type} Plot")
            self.canvas.draw()
        except Exception as e:
            print(f"Plotting error: {str(e)}")