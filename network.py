from imports import *
import psutil as p


class Network(FigureCanvas):
    """Setting up the matplotlib for showing up the figure"""

    def __init__(self):

        self.fig = Figure()
        # self.fig.subplots_adjust()

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
        self.ax1.set_ylim(0, 20)

        # Generating empty plots
        self.sent_packets, self.recv_packets, self.bytes_sent, self.bytes_recv = [], [], [], []
        self.sent_network, = self.ax1.plot([], self.sent_packets, color='c')
        self.recv_network, = self.ax1.plot([], self.recv_packets, color='r')

        # Disable auto scaling
        self.ax1.set_autoscale_on(False)

        # Redraw Figure
        self.fig.canvas.draw()

        # initializing empty variables for bytes and packets
        self.packets_recv = ("Recieving\t" + "0" + "Mbps")
        self.packets_sent = ("Sending\t" + "0" + "Mbps")

        self.bytes_recv = ("Total Received\t" + "0" + "Gbps")
        self.bytes_sent = ("Total Sent\t" + "0" + "Gbps")

        # start timer, trigger event every 1000 milliseconds (=1sec)
        self.timer = self.startTimer(1000)

    def get_network_usage(self):
        """Getting the network usage of all NIC's"""

        self.net_io = p.net_io_counters()

        return self.net_io

    def timerEvent(self, evt):
        """This event gets triggered whenever startTimer() is called"""

        result_sent_packets = self.get_network_usage().packets_sent
        result_recv_packets = self.get_network_usage().packets_recv

        self.packets_recv = result_recv_packets / 1048576
        self.packets_sent = result_sent_packets / 1048576

        self.bytes_recv = self.get_network_usage().bytes_recv / 1073741824
        self.bytes_sent = self.get_network_usage().bytes_sent / 1073741824

        self.sent_packets.insert(0, (result_sent_packets/1048576))
        self.recv_packets.insert(0, (result_recv_packets/1048576))

        self.sent_network.set_data(range(len(self.sent_packets)), self.sent_packets)
        self.recv_network.set_data(range(len(self.recv_packets)), self.recv_packets)

        self.fig.canvas.draw()


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

        groupbox = QGroupBox("CPU History")
        layout.addWidget(groupbox)

        vbox = QVBoxLayout()

        self.a = Network()

        vbox.addWidget(self.a)

        hbox1 = QHBoxLayout()
        hbox1.setContentsMargins(100, 0, 0, 0)

        # 1st label
        label = QLabel(self)  # Showing red color
        label.setStyleSheet("background-color:red")
        label.setFixedSize(20, 20)
        hbox1.addWidget(label)

        vbox_inner = QVBoxLayout()

        self.c = str(self.a.packets_recv)
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

        label = QLabel(self)  # Showing cyan color
        label.setStyleSheet("background-color:cyan")
        label.setFixedSize(20, 20)
        hbox1.addWidget(label)

        vbox_inner = QVBoxLayout()

        self.e = str(self.a.packets_sent)
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

        pr = str(self.a.packets_recv)
        show_pr = ("Recieving\t" + pr[:4] + "Mbps")

        br = str(self.a.bytes_recv)
        show_br = ("Total Recieved\t" + br[:4] + "Gbps")

        self.label1.setText(show_pr)
        self.label2.setText(show_br)

    def sent(self):
        """Displaying updated sent data"""

        ps = str(self.a.packets_sent)
        show_ps = ("Sending\t\t" + ps[:4] + "Mbps")

        bs = str(self.a.bytes_sent)
        show_bs = ("Total Sent\t" + bs[:4] + "Gbps")

        self.label3.setText(show_ps)
        self.label4.setText(show_bs)

    def timerEvent(self, evt):
        """Calling the update function for updating the CPU % labels"""

        self.received()
        self.sent()
