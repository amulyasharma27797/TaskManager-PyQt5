from imports import *
import psutil as p


class Memory(FigureCanvas):
    """Setting up the matplotlib for showing up the figure"""

    def __init__(self):

        # first image setup and setting y-ticks to the right
        self.fig = Figure()
        self.fig.subplots_adjust(left=0.05)

        self.ax1 = self.fig.add_subplot(111)
        self.ax1.yaxis.tick_right()
        self.ax1.set_xlabel("Seconds")
        self.ax1.set_ylabel("%")
        self.ax1.yaxis.set_label_position("right")
        self.ax1.grid(True)

        # initialization of the canvas
        FigureCanvas.__init__(self, self.fig)

        # set X and Y Axis limits
        self.ax1.set_xlim(60, 0)
        self.ax1.set_ylim(-0.1, 100)

        # Generating empty plots
        self.memory_percentage, self.swap_percentage = [], []
        self.memory_percentage_show, = self.ax1.plot([], self.memory_percentage, color='r')
        self.swap_percentage_show, = self.ax1.plot([], self.swap_percentage, color='c')

        # Disable auto scaling
        self.ax1.set_autoscale_on(False)

        # Redraw Figure
        self.fig.canvas.draw()

        # initializing empty variables for showing memory and swap percentage
        self.mem_per = "0 GiB (0%) of 0 GiB"
        self.swap_per = "0 GiB (0%) of 0 GiB"

        # start timer, trigger event every 1000 milliseconds (=1sec)
        self.timer = self.startTimer(1000)

    def memory(self):

        # getting values from virtual memory
        self.memory_data = p.virtual_memory()

        return self.memory_data

    def swap(self):

        # getting values from swap memory
        self.swap_data = p.swap_memory()

        return self.swap_data

    def timerEvent(self, evt):
        """This event gets triggered whenever startTimer() is called"""

        memory_result = self.memory()
        swap_result = self.swap()

        self.mem_per = memory_result.percent  # Getting memory percent
        self.swap_per = swap_result.percent  # Getting swap percent

        self.memory_percentage.insert(0, (self.mem_per))  # Inserting memory % values in a list on 0th position
        self.swap_percentage.insert(0, (self.swap_per))  # Inserting swap % values in a list on 0th position

        self.memory_percentage_show.set_data(range(len(self.memory_percentage)), self.memory_percentage)
        self.swap_percentage_show.set_data(range(len(self.swap_percentage)), self.swap_percentage)

        # Redraw Figure
        self.fig.canvas.draw()


class MemoryWindow(QWidget):
    """Main Class for showing the Graph"""

    def __init__(self):
        super().__init__()

        self.create_layout()
        self.timer = self.startTimer(1000)
        self.show()

    def create_layout(self):

        layout = QGridLayout()
        self.setLayout(layout)

        groupbox = QGroupBox("Memory and Swap History")
        layout.addWidget(groupbox)

        vbox = QVBoxLayout()

        self.a = Memory()

        vbox.addWidget(self.a)

        hbox1 = QHBoxLayout()
        hbox1.setContentsMargins(200, 0, 0, 0)

        # 1st label for Memory
        label = QLabel(self)  # Showing red color
        label.setStyleSheet("background-color:red")
        label.setFixedSize(20, 20)
        hbox1.addWidget(label)

        vbox_inner = QVBoxLayout()

        label = QLabel("Memory")
        label.setFont(QtGui.QFont("Sanserif", 10))

        vbox_inner.addWidget(label)

        self.c = str(self.a.mem_per)
        self.label1 = QLabel(self.c, self)  # Updating memory % values
        self.label1.setFont(QtGui.QFont("Courier", 10))

        vbox_inner.addWidget(self.label1)

        hbox1.addLayout(vbox_inner)

        # 2nd label for Swap History
        hbox2 = QHBoxLayout()

        label = QLabel(self)  # Showing cyan color
        label.setStyleSheet("background-color:cyan")
        label.setFixedSize(20, 20)
        hbox1.addWidget(label)

        vbox_inner = QVBoxLayout()

        label = QLabel("Swap")
        label.setFont(QtGui.QFont("Sanserif", 10))
        label.setFixedSize(100, 20)
        vbox_inner.addWidget(label)

        self.d = str(self.a.swap_per)
        self.label2 = QLabel(self.d, self)  # Updating swap % values
        self.label2.setFont(QtGui.QFont("Courier", 10))
        vbox_inner.addWidget(self.label2)

        hbox1.addLayout(vbox_inner)

        vbox.addLayout(hbox2)

        vbox.addLayout(hbox1)

        groupbox.setLayout(vbox)

    def show_memory(self):
        """Displaying updated memory data in label1"""

        used = str(self.a.memory().used / 1073741824)
        per = str(self.a.memory().percent)
        total = str(self.a.memory().total / 1073741824)

        show = (used[:4] + " GiB (" + per + "%) of " + total[:4] + " GiB")

        self.label1.setText(str(show))

    def show_swap(self):
        """Displaying updated swap data in label2"""

        used = str(self.a.swap().used / 1073741824)
        per = str(self.a.swap().percent)
        total = str(self.a.swap().total / 1073741824)

        show = (used[:4] + " GiB (" + per + "%) of " + total[:4] + " GiB")

        self.label2.setText(str(show))

    def timerEvent(self, evt):
        """Calling the update function for updating the CPU % labels"""

        self.show_memory()
        self.show_swap()
