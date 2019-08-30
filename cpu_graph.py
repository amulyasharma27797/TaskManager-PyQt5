from imports import *

import psutil as p


class CPU(FigureCanvas):
    """Setting up the matplotlib for showing up the figure"""

    def __init__(self):

        # first image setup
        self.fig = Figure()
        self.fig.subplots_adjust(hspace=0.7, wspace=0.3, left=0.05)
        cpu_num = p.cpu_percent(percpu=True).__len__()
        self.core = dict()
        self.cpu = dict()
        self.var = dict()

        color = {1: 'r',
                 2: 'b',
                 3: 'c',
                 4: 'm',
                 5: 'k',
                 6: 'g',
                 7: 'y',
                 8: 'burlywood'}

        for i in range(1, cpu_num+1):
            if cpu_num == 4:
                self.ax = self.fig.add_subplot(2, 2, i)
            elif cpu_num == 6:
                self.ax = self.fig.add_subplot(3, 2, i)
            else:
                self.ax = self.fig.add_subplot(2, 4, i)

            self.ax.yaxis.tick_right()
            self.ax.set_xlabel("Seconds")
            self.ax.set_ylabel("%")
            self.ax.yaxis.set_label_position("right")  # setting y-ticks to the right
            self.ax.yaxis.set_label_coords(1.15, 0.5)
            self.ax.set_title("Core " + str(i))
            self.ax.grid(True)
            self.ax.set_xlim(60, 0)
            self.ax.set_ylim(0, 100)
            self.ax.set_autoscale_on(False)

            self.core[i] = []
            self.cpu[i], = self.ax.plot([], self.core[i], color=color[i])
            self.var[i] = 0

        # initialization of the canvas
        FigureCanvas.__init__(self, self.fig)

        # Redraw Figure
        self.fig.canvas.draw()

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

        for i in range(0, len(result)):
            self.var[i+1] = result[i]
            self.core[i+1].insert(0, result[i])
            self.cpu[i+1].set_data(range(len(self.core[i+1])), self.core[i+1])

        # force a redraw of the Figure
        self.fig.canvas.draw()


class Window(QWidget):
    """Window for running the CPU application"""

    def __init__(self):
        super().__init__()

        # Calling up the functions of this class
        self.label = dict()
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
        hbox_inner.setContentsMargins(40, 0, 0, 0)

        cpu_num = p.cpu_percent(percpu=True).__len__()
        color = {1: 'red',
                 2: 'blue',
                 3: 'cyan',
                 4: 'magenta',
                 5: 'black',
                 6: 'green',
                 7: 'yellow',
                 8: 'burlywood'}

        for i in range(1, cpu_num+1):
            self.label[i] = QLabel(self)
            self.label[i].setStyleSheet("background-color:"+color[i])
            self.label[i].setFixedSize(15, 15)
            hbox_inner.addWidget(self.label[i])

            self.label[i] = QLabel("Core " + str(i) + ":")
            self.label[i].setFont(QtGui.QFont("Sanserif", 12))
            self.label[i].setFixedSize(56, 20)
            hbox_inner.addWidget(self.label[i])

            val = str(self.a.var[i])
            self.label[i] = QLabel(val, self)
            self.label[i].setFont(QtGui.QFont("Sanserif", 12))
            hbox_inner.addWidget(self.label[i])

        hbox.addLayout(hbox_inner)
        vbox.addLayout(hbox)

        groupbox.setLayout(vbox)

    def update_cpu(self):
        """Updating the values of theC CPU cores"""

        cpu_num = p.cpu_percent(percpu=True).__len__()

        for i in range(1, cpu_num+1):
            self.label[i].setText(str(self.a.var[i]) + '%')

    def timerEvent(self, evt):
        """Calling the update function for updating the CPU % labels"""

        self.update_cpu()
