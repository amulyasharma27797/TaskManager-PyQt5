import sys

from cpu_graph import *
from task_manager import *
from memory import *
from network import *


class Tab(QDialog):
    """Creating a main Tab for CPU Processes and CPU Graph to be displayed"""

    def __init__(self):
        super().__init__()

        # Setting up the window title and geometry
        self.setWindowTitle("System Monitor")
        self.setGeometry(100, 50, 1165, 600)
        self.setMinimumSize(1000, 600)
        self.setWindowFlags(self.windowFlags() & QtCore.Qt.WindowMinMaxButtonsHint)  # Displaying Max and Min Buttons

        vbox = QVBoxLayout()
        tab_widget = QTabWidget()

        tab_widget.addTab(TaskManager(), "Processes")
	tab_widget.addTab(Window(), "CPU Monitor")
        tab_widget.addTab(MemoryWindow(), "Memory")
        tab_widget.addTab(NetworkWindow(), "Network")

        vbox.addWidget(tab_widget)

        self.setLayout(vbox)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    tab_dialog = Tab()
    tab_dialog.show()
    App.exec_()
