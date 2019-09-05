from collections import deque

import math

from imports import *
import psutil as p


class Node:
    """
    Setting up value and index for sliding window
    """
    def __init__(self, value, index=None):
        self.value = value
        self.index = index


class Network(FigureCanvas):
    """
    Setting up the matplotlib for showing up the figure
    """

    def __init__(self):
        self.recv_arr = list()  # Initialising an empty list
        self.send_arr = list()
        self.dq = deque()  # Initialising a deque
        self.window_limit = 60  # Setting up maximum window limit
        self.elapsed_seconds = 0  # Initialising elapsed seconds

        self.old_sent_bytes = self.get_network_usage().bytes_sent  # Getting the bytes sent when the program initiates
        self.old_recv_bytes = self.get_network_usage().bytes_recv  # Getting the bytes recv when the program initiates

        self.fig = Figure()
        self.fig.subplots_adjust(left=0.05)

        self.ax1 = self.fig.add_subplot(111)
        self.ax1.yaxis.tick_right()
        self.ax1.set_xlabel("Seconds")
        self.ax1.yaxis.set_label_position("right")
        self.ax1.grid(True)

        self.ax1.set_xlim(self.window_limit, 0)
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
        self.diff_recv = 0
        self.diff_sent = 0

        self.bytes_recv = ("Total Received\t" + "0" + " GB")
        self.bytes_sent = ("Total Sent\t" + "0" + " GB")

        # start timer, trigger event every 1000 milliseconds (=1sec)
        self.timer = self.startTimer(1000)

    def get_network_usage(self):
        """
        Getting the network usage of all NIC's
        :return:
        """

        self.net_io = p.net_io_counters()

        return self.net_io

    def timerEvent(self, evt):
        """
        This event gets triggered whenever startTimer() is called
        :param evt:
        :return:
        """

        self.new_sent_bytes = self.get_network_usage().bytes_sent  # Getting current sent bytes
        self.result_sent_bytes = self.new_sent_bytes - self.old_sent_bytes  # Obtaining the difference in sent bytes
        self.old_sent_bytes = self.new_sent_bytes  # Setting new bytes value to old bytes

        self.new_recv_bytes = self.get_network_usage().bytes_recv  # Getting current recv bytes
        self.result_recv_bytes = self.new_recv_bytes - self.old_recv_bytes  # Obtaining the difference in recv bytes
        self.old_recv_bytes = self.new_recv_bytes  # Setting new bytes value to old bytes

        self.diff_sent = self.result_sent_bytes
        self.diff_recv = self.result_recv_bytes

        self.bytes_sent = self.new_sent_bytes / (1024 * 1024)
        self.bytes_recv = self.new_recv_bytes / (1024 * 1024 * 1024)

        if len(self.recv_bytes_difference) > self.window_limit:  # Check that size of list shouldn't exceed window limit
            self.recv_bytes_difference.pop()
            self.sent_bytes_difference.pop()
        self.sent_bytes_difference.insert(0, self.result_sent_bytes)
        self.recv_bytes_difference.insert(0, self.result_recv_bytes)

        self.set_y_axes()  # Dynamic Axes

        self.fig.canvas.draw()

    def set_y_axes(self):
        """
        Dynamically setting up Y-Axis according to the speed
        :return:
        """

        self.elapsed_seconds += 1  # Increasing elapsed seconds per iteration

        if len(self.recv_arr) >= self.window_limit:
            self.recv_arr.pop(0)
        self.recv_arr.append(self.result_recv_bytes)  # Getting values of recv bytes per second in an array
        recv_iter_arr = len(self.recv_arr)-1
        recv_value = self.recv_arr[recv_iter_arr]

        if len(self.send_arr) >= self.window_limit:
            self.send_arr.pop(0)
        self.send_arr.append(self.result_sent_bytes)  # Getting values of recv bytes per second in an array
        send_iter_arr = len(self.send_arr)-1
        send_value = self.send_arr[send_iter_arr]

        self.maintain_max_queue(recv_value)
        self.maintain_max_queue(send_value)

        dq_value_speed = self.get_formatted_ylabel(self.dq[0].value)  # Speed of max value in window

        self.calculate_speed(dq_value_speed)

        self.ax1.set_ylim(0, math.ceil(float(self.get_formatted_speed(self.dq[0].value)) / 10) * 10)

        self.ax1.set_ylabel(dq_value_speed)

    def maintain_max_queue(self, value):
        """
        Maintaining the maximum value in the window
        :param value:
        :return:
        """

        while self.dq and self.dq[0].index <= self.elapsed_seconds - self.window_limit:
            self.dq.popleft()
        while self.dq and value >= self.dq[-1].value:
            self.dq.pop()
        self.dq.append(Node(value, self.elapsed_seconds))

    def calculate_speed(self, speed):
        """
        Getting the array of speed to be shown in the graph accordingly
        :param speed:
        :return:
        """

        temp_recv = list()
        temp_sent = list()
        if speed == "Bytes":
            self.recv_network.set_data(range(len(self.recv_bytes_difference)), self.recv_bytes_difference)
            self.sent_network.set_data(range(len(self.sent_bytes_difference)), self.sent_bytes_difference)
        elif speed == "KBps":
            for val in self.recv_bytes_difference:
                val = val / 1024
                temp_recv.append(val)
                self.recv_network.set_data(range(len(self.recv_bytes_difference)), temp_recv)
            for val in self.sent_bytes_difference:
                val = val / 1024
                temp_sent.append(val)
                self.sent_network.set_data(range(len(self.sent_bytes_difference)), temp_sent)
        elif speed == "MBps":
            for val in self.recv_bytes_difference:
                val = val / (1024 * 1024)
                temp_recv.append(val)
                self.recv_network.set_data(range(len(self.recv_bytes_difference)), temp_recv)
            for val in self.sent_bytes_difference:
                val = val / (1024 * 1024)
                temp_sent.append(val)
                self.sent_network.set_data(range(len(self.sent_bytes_difference)), temp_sent)
        else:
            for val in self.recv_bytes_difference:
                val = val / (1024 * 1024 * 1024)
                temp_recv.append(val)
                self.recv_network.set_data(range(len(self.recv_bytes_difference)), temp_recv)
            for val in self.sent_bytes_difference:
                val = val / (1024 * 1024 * 1024)
                temp_sent.append(val)
                self.sent_network.set_data(range(len(self.sent_bytes_difference)), temp_sent)

    def get_formatted_ylabel(self, speed_in_bytes):
        """
        Showing speed string accordingly
        :param speed_in_bytes:
        :return:
        """

        if speed_in_bytes > 1024 * 1024 * 1024:
            return "GBps"
        elif speed_in_bytes > 1024 * 1024:
            return "MBps"
        elif speed_in_bytes > 1024:
            return "KBps"
        else:
            return "Bytes"

    def get_formatted_speed(self, speed_in_bytes):
        """
        Showing speed accordingly
        :param speed_in_bytes:
        :return:
        """

        if speed_in_bytes > 1024 * 1024 * 1024:
            return speed_in_bytes / (1024 * 1024 * 1024)
        elif speed_in_bytes > 1024 * 1024:
            return speed_in_bytes / (1024 * 1024)
        elif speed_in_bytes > 1024:
            return speed_in_bytes / 1024
        else:
            return speed_in_bytes


class NetworkWindow(QWidget):
    """
    Main Class for showing the Graph
    """

    def __init__(self):
        super().__init__()

        self.create_layout()
        self.timer = self.startTimer(1000)  # starting the timer for showing the CPU % labels
        self.show()

    def create_layout(self):
        """
        Creating a layout for Network Window
        :return:
        """

        layout = QGridLayout()
        self.setLayout(layout)

        groupbox = QGroupBox("Network History")
        layout.addWidget(groupbox)

        vbox = QVBoxLayout()

        self.a = Network()

        vbox.addWidget(self.a)

        hbox1 = QHBoxLayout()
        hbox1.setContentsMargins(200, 0, 0, 0)

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
        """
        Displaying updated received data
        :return:
        """

        pr = str(self.get_formatted_speed_diff(self.a.diff_recv))
        show_pr = ("Recieving\t" + pr)

        br = str(self.a.bytes_recv)
        show_br = ("Total Recieved\t" + br[:4] + " GB")

        self.label1.setText(show_pr)
        self.label2.setText(show_br)

    def sent(self):
        """
        Displaying updated sent data
        :return:
        """

        ps = str(self.get_formatted_speed_diff(self.a.diff_sent))
        show_ps = ("Sending\t\t" + ps)

        bs = str(self.a.bytes_sent)
        show_bs = ("Total Sent\t" + bs[:5] + " MB")

        self.label3.setText(show_ps)
        self.label4.setText(show_bs)

    def timerEvent(self, evt):
        """
        Calling the update function for updating the CPU % labels
        :param evt:
        :return:
        """

        self.received()
        self.sent()

    def get_formatted_speed_diff(self, speed_in_bytes):
        """
        Returning speed accordingly
        :param speed_in_bytes:
        :return:
        """

        if speed_in_bytes > 1024 * 1024 * 1024:
            return "%.2f GBps" % (speed_in_bytes / (1024 * 1024 * 1024))
        elif speed_in_bytes > 1024 * 1024:
            return "%.2f MBps" % (speed_in_bytes / (1024 * 1024))
        elif speed_in_bytes > 1024:
            return "%.2f KBps" % (speed_in_bytes / 1024)
        else:
            return str(speed_in_bytes) + ' Bps'
