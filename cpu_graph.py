from imports import *

import psutil as p


class CPU(FigureCanvas):
    """Setting up the matplotlib for showing up the figure"""

    def __init__(self):

        # first image setup and setting y-ticks to the right
        self.fig = Figure()
        self.fig.subplots_adjust(hspace=0.5, left=0.05)

        self.ax1 = self.fig.add_subplot(221)
        self.ax1.yaxis.tick_right()
        self.ax1.set_xlabel("Seconds")
        self.ax1.set_ylabel("%")
        self.ax1.yaxis.set_label_position("right")
        self.ax1.grid(True)

        self.ax2 = self.fig.add_subplot(222)
        self.ax2.yaxis.tick_right()
        self.ax2.set_xlabel("Seconds")
        self.ax2.set_ylabel("%")
        self.ax2.yaxis.set_label_position("right")
        self.ax2.grid(True)

        self.ax3 = self.fig.add_subplot(223)
        self.ax3.yaxis.tick_right()
        self.ax3.set_xlabel("Seconds")
        self.ax3.set_ylabel("%")
        self.ax3.yaxis.set_label_position("right")
        self.ax3.grid(True)

        self.ax4 = self.fig.add_subplot(224)
        self.ax4.yaxis.tick_right()
        self.ax4.set_xlabel("Seconds")
        self.ax4.set_ylabel("%")
        self.ax4.yaxis.set_label_position("right")
        self.ax4.grid(True)

        # initialization of the canvas
        FigureCanvas.__init__(self, self.fig)

        # set X and Y Axis limits
        self.ax1.set_xlim(60, 0)
        self.ax1.set_ylim(0, 100)

        self.ax2.set_xlim(60, 0)
        self.ax2.set_ylim(0, 100)

        self.ax3.set_xlim(60, 0)
        self.ax3.set_ylim(0, 100)

        self.ax4.set_xlim(60, 0)
        self.ax4.set_ylim(0, 100)

        # Generating empty plots
        self.core1, self.core2, self.core3, self.core4 = [], [], [], []
        self.cpu1, = self.ax1.plot([], self.core1, color='r')
        self.cpu2, = self.ax2.plot([], self.core2, color='c')
        self.cpu3, = self.ax3.plot([], self.core3, color='m')
        self.cpu4, = self.ax4.plot([], self.core4, color='b')

        # Disable auto scaling
        self.ax1.set_autoscale_on(False)
        self.ax2.set_autoscale_on(False)
        self.ax3.set_autoscale_on(False)
        self.ax4.set_autoscale_on(False)

        # Redraw Figure
        self.fig.canvas.draw()

        # initializing empty variables for showing CPU percentages
        self.var1, self.var2, self.var3, self.var4 = 0, 0, 0, 0

        # start timer, trigger event every 1000 milliseconds (=1sec)
        self.timer = self.startTimer(1000)

    def get_cpu_percent(self):
        """Get the CPU percent of each core"""

        # Gives the list of CPU percent per CPU
        self.cpu_percent = p.cpu_percent(percpu=True)

        return self.cpu_percent

    def timerEvent(self, evt):

        # get the cpu percentage usage
        result = self.get_cpu_percent()

        self.var1 = result[0]
        self.var2 = result[1]
        self.var3 = result[2]
        self.var4 = result[3]

        # append new data to the data sets
        self.core1.insert(0, result[0])
        self.core2.insert(0, result[1])
        self.core3.insert(0, result[2])
        self.core4.insert(0, result[3])

        # update lines data using the lists with new data
        self.cpu1.set_data(range(len(self.core1)), self.core1)
        self.cpu2.set_data(range(len(self.core2)), self.core2)
        self.cpu3.set_data(range(len(self.core3)), self.core3)
        self.cpu4.set_data(range(len(self.core4)), self.core4)

        # mplcursors.cursor(self.cpu1, hover=True)

        # force a redraw of the Figure
        self.fig.canvas.draw()


class Window(QWidget):
    """Window for running the CPU application"""

    def __init__(self):
        super().__init__()

        # Calling up the functions of this class
        self.create_layout()
        self.timer = self.startTimer(1000)  # starting the timer for showing the CPU % labels
        self.show()

    def create_layout(self):
        """Setting up the layout of the window and calling
            the CPU class for plotting"""

        layout = QGridLayout()
        self.setLayout(layout)

        groupbox = QGroupBox("CPU History")
        layout.addWidget(groupbox)

        vbox = QVBoxLayout()

        self.a = CPU()

        vbox.addWidget(self.a)

        hbox = QHBoxLayout()
        hbox_inner = QHBoxLayout()
        hbox_inner.setContentsMargins(50, 0, 0, 0)

        # Core 1 Label
        label = QLabel(self)  # Showing red color
        label.setStyleSheet("background-color:red")
        label.setFixedSize(15, 15)
        hbox_inner.addWidget(label)

        label = QLabel("Core 1")  # Label (CPU 1)
        label.setFont(QtGui.QFont("Sanserif", 12))
        label.setFixedSize(55, 20)
        hbox_inner.addWidget(label)

        self.c = str(self.a.var1)
        self.label1 = QLabel(self.c, self)  # Updating core 1 value
        self.label1.setFont(QtGui.QFont("Sanserif", 12))
        hbox_inner.addWidget(self.label1)

        # Core 2 Label
        label = QLabel(self)
        label.setStyleSheet("background-color:cyan")
        label.setFixedSize(15, 15)
        hbox_inner.addWidget(label)

        label = QLabel("Core 2")
        label.setFont(QtGui.QFont("Sanserif", 12))
        label.setFixedSize(55, 20)
        hbox_inner.addWidget(label)

        self.c = str(self.a.var2)
        self.label2 = QLabel(self.c, self)  # Updating core 1 value
        self.label2.setFont(QtGui.QFont("Sanserif", 12))
        hbox_inner.addWidget(self.label2)

        # Core 3 Label
        label = QLabel(self)
        label.setStyleSheet("background-color:magenta")
        label.setFixedSize(15, 15)
        hbox_inner.addWidget(label)

        label = QLabel("Core 3")
        label.setFont(QtGui.QFont("Sanserif", 12))
        label.setFixedSize(55, 20)
        hbox_inner.addWidget(label)

        self.c = str(self.a.var3)
        self.label3 = QLabel(self.c, self)  # Updating core 1 value
        self.label3.setFont(QtGui.QFont("Sanserif", 12))
        hbox_inner.addWidget(self.label3)

        # Core 4 Label
        label = QLabel(self)
        label.setStyleSheet("background-color:blue")
        label.setFixedSize(15, 15)
        hbox_inner.addWidget(label)

        label = QLabel("Core 4")
        label.setFont(QtGui.QFont("Sanserif", 12))
        label.setFixedSize(55, 20)
        hbox_inner.addWidget(label)

        self.c = str(self.a.var4)
        self.label4 = QLabel(self.c, self)  # Updating core 1 value
        self.label4.setFont(QtGui.QFont("Sanserif", 12))
        # self.label4.setAlignment(QtCore.Qt.AlignRight)
        hbox_inner.addWidget(self.label4)

        hbox.addLayout(hbox_inner)
        vbox.addLayout(hbox)

        groupbox.setLayout(vbox)

    def update_cpu(self):
        """Updating the values of theC CPU cores"""

        self.label1.setText(str(self.a.var1) + '%')
        self.label2.setText(str(self.a.var2) + '%')
        self.label3.setText(str(self.a.var3) + '%')
        self.label4.setText(str(self.a.var4) + '%')

    def timerEvent(self, evt):
        """Calling the update function for updating the CPU % labels"""

        self.update_cpu()
