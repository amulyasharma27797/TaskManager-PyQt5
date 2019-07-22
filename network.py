from imports import *
import psutil as p


class Network(FigureCanvas):
    """Setting up the matplotlib for showing up the figure"""

    def __init__(self):
        self.arr = list()

        self.old_sent_bytes = self.get_network_usage().bytes_sent  # Getting the bytes sent when the program initiates
        self.old_recv_bytes = self.get_network_usage().bytes_recv  # Getting the bytes recv when the program initiates

        self.fig = Figure()
        self.fig.subplots_adjust(left=0.05)

        self.ax1 = self.fig.add_subplot(111)
        self.ax1.yaxis.tick_right()
        self.ax1.set_xlabel("Seconds")
        self.ax1.set_ylabel("KiB/s")
        self.ax1.yaxis.set_label_position("right")
        self.ax1.grid(True)

        self.ax1.set_xlim(60, 0)
        self.ax1.set_ylim(0, 60)

        # initialization of the canvas
        FigureCanvas.__init__(self, self.fig)

        # Generating empty plots
        self.sent_bytes_difference, self.recv_bytes_difference, self.bytes_sent, self.bytes_recv = [], [], [], []
        self.sent_network, = self.ax1.plot([], self.sent_bytes_difference, color='r')
        self.recv_network, = self.ax1.plot([], self.recv_bytes_difference, color='c')

        # Disable auto scaling
        self.ax1.set_autoscale_on(False)

        # Redraw Figure
        self.fig.canvas.draw()

        # initializing empty variables for bytes and packets
        self.diff_recv = ("Recieving\t" + "0" + " Kbps")
        self.diff_sent = ("Sending\t" + "0" + " bytes/s")

        self.bytes_recv = ("Total Received\t" + "0" + " GiB")
        self.bytes_sent = ("Total Sent\t" + "0" + " GiB")

        # start timer, trigger event every 1000 milliseconds (=1sec)
        self.timer = self.startTimer(1000)

    def get_network_usage(self):
        """Getting the network usage of all NIC's"""

        self.net_io = p.net_io_counters()

        return self.net_io

    def timerEvent(self, evt):
        """This event gets triggered whenever startTimer() is called"""

        self.new_sent_bytes = self.get_network_usage().bytes_sent  # Getting current sent bytes
        self.result_sent_bytes = self.new_sent_bytes - self.old_sent_bytes  # Obtaining the difference in sent bytes
        self.old_sent_bytes = self.new_sent_bytes  # Setting new bytes value to old bytes

        self.new_recv_bytes = self.get_network_usage().bytes_recv  # Getting current recv bytes
        self.result_recv_bytes = self.new_recv_bytes - self.old_recv_bytes  # Obtaining the difference in recv bytes
        self.old_recv_bytes = self.new_recv_bytes  # Setting new bytes value to old bytes

        self.diff_sent = self.result_sent_bytes
        self.diff_recv = self.result_recv_bytes / 1024

        self.bytes_sent = self.new_sent_bytes / 1048576
        self.bytes_recv = self.new_recv_bytes / 1073741824

        self.sent_bytes_difference.insert(0, (self.result_sent_bytes/1024))
        self.recv_bytes_difference.insert(0, (self.result_recv_bytes/1024))

        self.set_y_axes()  # Dynamic Axes

        self.sent_network.set_data(range(len(self.sent_bytes_difference)), self.sent_bytes_difference)
        self.recv_network.set_data(range(len(self.recv_bytes_difference)), self.recv_bytes_difference)

        self.fig.canvas.draw()

    def set_y_axes(self):
        """Dynamically setting up Y-Axis according to the speed"""

        self.arr.append(self.result_recv_bytes/1024)
        k = 60
        n = len(self.arr)

        if len(self.arr) > k:

            l = [self.arr[i] for i in range(k)]
            for i in range(n-k):
                l.pop(0)
                l.append(self.arr[i+k])
            self.ax1.set_ylim(0, max(l))


class NetworkWindow(QWidget):
    """Main Class for showing the Graph"""

    def __init__(self):
        super().__init__()

        self.create_layout()
        self.timer = self.startTimer(1000)  # starting the timer for showing the CPU % labels
        self.show()

    def create_layout(self):

        layout = QGridLayout()
        self.setLayout(layout)

        groupbox = QGroupBox("Network History")
        layout.addWidget(groupbox)

        vbox = QVBoxLayout()

        self.a = Network()

        vbox.addWidget(self.a)

        hbox1 = QHBoxLayout()
        hbox1.setContentsMargins(100, 0, 0, 0)

        # 1st label
        label = QLabel(self)  # Showing cyan color
        label.setStyleSheet("background-color:cyan")
        label.setFixedSize(20, 20)
        hbox1.addWidget(label)

        vbox_inner = QVBoxLayout()

        self.c = str(self.a.diff_recv)
        self.label1 = QLabel(self.c, self)  # Updating packets receiving values
        self.label1.setFont(QtGui.QFont("Courier", 10))
        vbox_inner.addWidget(self.label1)

        self.d = str(self.a.bytes_recv)
        self.label2 = QLabel(self.d, self)  # Updating bytes received values
        self.label2.setFont(QtGui.QFont("Courier", 10))
        vbox_inner.addWidget(self.label2)

        hbox1.addLayout(vbox_inner)

        # 2nd label
        hbox2 = QHBoxLayout()

        label = QLabel(self)  # Showing red color
        label.setStyleSheet("background-color:red")
        label.setFixedSize(20, 20)
        hbox1.addWidget(label)

        vbox_inner = QVBoxLayout()

        self.e = str(self.a.diff_sent)
        self.label3 = QLabel(self.e, self)  # Updating packets sent values
        self.label3.setFont(QtGui.QFont("Courier", 10))
        vbox_inner.addWidget(self.label3)

        self.f = str(self.a.bytes_sent)
        self.label4 = QLabel(self.f, self)  # Updating bytes sent values
        self.label4.setFont(QtGui.QFont("Courier", 10))
        vbox_inner.addWidget(self.label4)

        hbox1.addLayout(vbox_inner)

        vbox.addLayout(hbox2)

        vbox.addLayout(hbox1)

        groupbox.setLayout(vbox)

    def received(self):
        """Displaying updated received data"""

        pr = str(self.a.diff_recv)
        show_pr = ("Recieving\t" + pr[:4] + " KiB/s")

        br = str(self.a.bytes_recv)
        show_br = ("Total Recieved\t" + br[:4] + " GiB")

        self.label1.setText(show_pr)
        self.label2.setText(show_br)

    def sent(self):
        """Displaying updated sent data"""

        ps = str(self.a.diff_sent)
        show_ps = ("Sending\t\t" + ps[:4] + " bytes/s")

        bs = str(self.a.bytes_sent)
        show_bs = ("Total Sent\t" + bs[:5] + " MiB")

        self.label3.setText(show_ps)
        self.label4.setText(show_bs)

    def timerEvent(self, evt):
        """Calling the update function for updating the CPU % labels"""

        self.received()
        self.sent()
