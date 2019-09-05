from imports import *

import psutil
import psutil_test


class MyTable(QTableWidget):
    """This table provides basic grid layout for the main window."""
    def __init__(self, r, c):
        super().__init__(r, c)
        self.init_ui()

    def init_ui(self):
        self.show()

    def get_current_id(self):
        return self.item(self.currentRow(), 0).text()


def get_formatted_memory(memory_in_bytes):
    """
    This function formats the memory
    in preferred unit based on its size.
    :param memory_in_bytes:
    :return:
    """
    if memory_in_bytes > 1024 * 1024 * 1024:
        return "%.2f GB" % (memory_in_bytes / (1024 * 1024 * 1024))
    elif memory_in_bytes > 1024 * 1024:
        return "%.2f MB" % (memory_in_bytes / (1024 * 1024))
    elif memory_in_bytes > 1024:
        return "%.2f KB" % (memory_in_bytes / 1024)
    else:
        return str(memory_in_bytes) + 'B'


class TaskManager(QMainWindow):
    """
    This is the main window class.
    """
    def __init__(self):
        super().__init__()
        rows = psutil_test.rows
        if psutil_test.getListOfProcesses()[0].get('shared'):
            self.col_headers = ['P-ID', 'P-Name', 'User', 'Virt-Mem', 'Res-Mem', 'Shd-Mem', 'Mem %', 'CPU %', 'Path',
                                'Priority', 'Created']
        else:
            self.col_headers = ['P-ID', 'P-Name', 'User', 'Virt-Mem', 'Res-Mem', 'Mem %', 'CPU %', 'Path',
                                'Priority', 'Created']
        self.form_widget = MyTable(rows, len(self.col_headers))
        self.setCentralWidget(self.form_widget)
        self.key = 'pid'
        self.flag = False
        self.form_widget.setHorizontalHeaderLabels(self.col_headers)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self.change_values)
        self.form_widget.horizontalHeader().sectionClicked.connect(self.set_values)
        self.form_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.b1 = QPushButton()
        self.l1 = QLabel()
        self.s1 = QSlider(Qt.Horizontal)

        header = self.form_widget.horizontalHeader()
        for i in range(len(self.col_headers)):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        self.timer.start(1000)

    @QtCore.pyqtSlot()
    def change_values(self):
        """
        This method is used to change the values of processes dynamically.
        :return:
        """

        new_list = psutil_test.getListOfProcesses()
        final_list = self.sort_list(new_list, self.key, self.flag)  # set value function to be called by button trigger
        self.form_widget.setRowCount(len(final_list))

        for i, process in enumerate(final_list):
            self.form_widget.setItem(i, 0, QTableWidgetItem(str(process['pid'])))
            self.form_widget.setItem(i, 1, QTableWidgetItem(str(process['name'])))
            self.form_widget.setItem(i, 2, QTableWidgetItem(str(process['username'])))
            self.form_widget.setItem(i, 3, QTableWidgetItem(get_formatted_memory(process['vms'])))
            self.form_widget.setItem(i, 4, QTableWidgetItem(get_formatted_memory(process['res'])))
            if process.get('shared'):
                self.form_widget.setItem(i, 5, QTableWidgetItem(get_formatted_memory(process['shared'])))
                self.form_widget.setItem(i, 6, QTableWidgetItem("%.2f " % (process['mem_per'])))
                self.form_widget.setItem(i, 7, QTableWidgetItem(str(process['cpu'])))
                self.form_widget.setItem(i, 8, QTableWidgetItem(str(process['path'])))
                self.form_widget.setItem(i, 9, QTableWidgetItem(str(process['priority'])))
                self.form_widget.setItem(i, 10, QTableWidgetItem(str(datetime.datetime.fromtimestamp(process['time']))))
            else:
                self.form_widget.setItem(i, 5, QTableWidgetItem("%.2f " % (process['mem_per'])))
                self.form_widget.setItem(i, 6, QTableWidgetItem(str(process['cpu'])))
                self.form_widget.setItem(i, 7, QTableWidgetItem(str(process['path'])))
                self.form_widget.setItem(i, 8, QTableWidgetItem(str(process['priority'])))
                self.form_widget.setItem(i, 9, QTableWidgetItem(str(datetime.datetime.fromtimestamp(process['time']))))

    def contextMenuEvent(self, event):
        """
        Method for providing the right click context menu.
        :param event:
        :return:
        """
        context_menu = QMenu(self)
        id = self.form_widget.get_current_id()
        process = psutil.Process(pid=int(id))
        info = context_menu.addAction("More Info")
        kill_act = context_menu.addAction("Kill")
        change_priority = context_menu.addMenu("Change priority")
        if process.status() == 'stopped':
            status_change = context_menu.addAction("Resume")
        else:
            status_change = context_menu.addAction("Suspend")
        print_pdf = context_menu.addAction("Print PDF")
        quit_act = context_menu.addAction("Quit")

        highest_priority = change_priority.addAction("HIGHEST")
        high_priority = change_priority.addAction("HIGH")
        medium_priority = change_priority.addAction("MEDIUM")
        low_priority = change_priority.addAction("LOW")
        lowest_priority = change_priority.addAction("LOWEST")
        custom_priority = change_priority.addAction("CUSTOM")

        action = context_menu.exec_(self.mapToGlobal(event.pos()))
        if action == quit_act:
            self.close()

        if action == info:
            self.show_info(process)

        if action == kill_act:
            self.confirm_kill_process(process)

        if action == highest_priority:
            process.nice(-20)

        if action == high_priority:
            process.nice(-10)

        if action == medium_priority:
            process.nice(0)

        if action == low_priority:
            process.nice(10)

        if action == lowest_priority:
            process.nice(-20)

        if action == custom_priority:
            self.set_custom_priority(process)

        if action == print_pdf:
            self.handle_print()

        if action == status_change:
            if process.status() == 'stopped':
                self.resume_process(process)
            else:
                self.suspend_process(process)

    def sort_list(self, sort_list, key, flag):
        """
        This method is used to sort the values in the
        task manager according on their respective headers.
        :param sort_list:
        :param key:
        :param flag:
        :return:
        """
        return sorted(sort_list, key=lambda obj: obj[key], reverse=flag)

    def set_values(self, col):
        """Used to set the values of headers"""
        self.key = self.col_header_key_header_index.inverse.get(col)
        self.flag = not self.flag
        self.change_header_value(self.flag, self.key)

    def _get_widget_item(self, flag: bool, name: str):
        """Puts a sort icon next to the header."""
        if flag:
            return QTableWidgetItem(qta.icon('mdi.arrow-down-drop-circle'), name)
        else:
            return QTableWidgetItem(qta.icon('mdi.arrow-up-drop-circle'), name)

    col_header_key_header_name = {
        'pid': "P-ID",
        'name': "P-Name",
        'username': "User",
        'vms': "Virt-Mem",
        'res': "Res-Mem",
        'shared': "Shd-Mem",
        'mem_per': "Mem %",
        'cpu': "CPU %",
        'path': "Path",
        'priority': "Priority",
        'time': "Created"
    }

    keys_dict = ['pid', 'name', 'username', 'vms', 'res', 'mem_per', 'cpu', 'path', 'priority', 'time']
    if psutil_test.getListOfProcesses()[0].get('shared'):
        keys_dict.insert(5, 'shared')
    dicts = dict.fromkeys(keys_dict, None)

    for key, value in dicts.items():
        dicts[key] = keys_dict.index(key)

    col_header_key_header_index = bidict(dicts)

    def change_header_value(self, flag, key):
        """
        Puts a sort icon next to the header
        with the help of _get_widget_item().
        :param flag:
        :param key:
        :return:
        """
        for i, header in enumerate(self.col_headers):
            self.form_widget.setHorizontalHeaderItem(i, QTableWidgetItem(str(header)))
        self.form_widget.setHorizontalHeaderItem(self.col_header_key_header_index.get(key),
                                                 self._get_widget_item(flag, self.col_header_key_header_name.get(key)))
        self.form_widget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)

    def confirm_kill_process(self, process):
        """
        Dialog box for killing a process.
        :param process:
        :return:
        """
        message = QMessageBox.question(self, "Kill Process", "Are you sure you want to kill this process ?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            process.kill()
        else:
            pass

    def set_custom_priority(self, process):
        """
        Dialog box for setting custom priority to processes.
        :param process:
        :return:
        """
        d = QDialog()
        self.b1 = QPushButton("Set Priority", d)
        self.l1 = QLabel()
        self.l1.setText(str(process.nice()))
        self.s1 = QSlider(Qt.Horizontal)
        d.setWindowTitle("Change Priority")
        d.setGeometry(100, 100, 300, 100)
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        self.s1.setMinimum(-20)
        self.s1.setMaximum(19)
        self.s1.setValue(process.nice())
        self.s1.setTickInterval(1)
        self.s1.setTickPosition(QSlider.TicksBelow)
        self.s1.valueChanged.connect(self.slider_change)
        self.b1.clicked.connect(self.set_priority(process))
        hbox.addWidget(self.s1)
        hbox.addWidget(self.l1)
        vbox.addLayout(hbox)
        vbox.addWidget(self.b1)
        d.setLayout(vbox)
        d.setWindowModality(Qt.ApplicationModal)
        d.exec_()

    def slider_change(self):
        """
        Slider function for getting custom priority value.
        :return:
        """
        value = self.s1.value()
        self.l1.setText(str(value))

    def set_priority(self, process):
        """
        Used to provide a function object for the signal.
        :param process:
        :return:
        """
        def process_priority():
            """
            Actual function used to set process priority.
            :return:
            """
            value = self.s1.value()
            process.nice(value)
        return process_priority

    def handle_print(self):
        """
        Method for handling save as PDF functionality.
        :return:
        """
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.handle_paint_request(dialog.printer())

    def handle_paint_request(self, printer):
        """
        saves the information in task manager in a pdf.
        :param printer:
        :return:
        """
        document = QtGui.QTextDocument()
        info_cursor = QtGui.QTextCursor(document)
        info_table = info_cursor.insertTable(5, 1)

        info_cursor.insertText("Current date & time: {}".format(datetime.datetime.now()))
        info_cursor.movePosition(QtGui.QTextCursor.NextCell)
        info_cursor.insertText("System up time: {}".format(datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())))
        info_cursor.movePosition(QtGui.QTextCursor.NextCell)
        info_cursor.insertText("Memory Usage: {}%. ({} used out of {})".format(psutil.virtual_memory().percent,
                                                                               get_formatted_memory(
                                                                                   psutil.virtual_memory().used),
                                                                               get_formatted_memory(
                                                                                   psutil.virtual_memory().total)))
        info_cursor.movePosition(QtGui.QTextCursor.NextCell)
        info_cursor.insertText("CPU Usage: {}%".format(psutil.cpu_percent()))
        info_cursor.movePosition(QtGui.QTextCursor.NextCell)
        info_cursor.insertText("Disk Usage: {}%".format(psutil.disk_usage('/')[3]))

        cursor = QtGui.QTextCursor(document)
        table = cursor.insertTable(self.form_widget.rowCount() + 1, self.form_widget.columnCount())

        for count in range(len(self.col_headers)):
            cursor.insertText(self.form_widget.horizontalHeaderItem(count).text())
            cursor.movePosition(QtGui.QTextCursor.NextCell)

        for row in range(table.rows()):
            for col in range(table.columns()):
                item = self.form_widget.item(row, col)
                if item is not None:
                    cursor.insertText(item.text())
                cursor.movePosition(QtGui.QTextCursor.NextCell)
        document.print_(printer)

    def suspend_process(self, process):
        """
        Method used for suspension of processes.
        :param process:
        :return:
        """
        message = QMessageBox.question(self, "Suspend Process",
                                       "Are you sure you want to suspend this process for now?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            process.suspend()
        else:
            pass

    def resume_process(self, process):
        """
        Method used for resuming processes.
        :param process:
        :return:
        """
        message = QMessageBox.question(self, "Suspend Process",
                                       "Are you sure you want to resume this process now?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            process.resume()
        else:
            pass

    def show_info(self, process):
        """
        Method for showing all related information of the selected process.
        :param process:
        :return:
        """
        info_dialog = QDialog()
        l1, l2, l3, l4, l5, l6, l7, l8 = (QLabel() for i in range(8))

        info_dialog.setWindowTitle(process.name())
        l1.setText(str("Process ID: {}".format(process.pid)))
        l2.setText(str("User: {}".format(process.username())))
        l3.setText(str("Process Status: {}".format(process.status())))
        l4.setText(str("Memory Info: {}".format(process.memory_info())))
        l5.setText(str("CPU Usage: {}".format(process.cpu_percent())))
        l6.setText(str("Path: {}".format(process.cwd())))
        l7.setText(str("Priority: {}".format(process.nice())))
        l8.setText(str("Created Time: {}".format(datetime.datetime.fromtimestamp(process.create_time()))))

        vbox = QVBoxLayout()
        vbox.addWidget(l1)
        vbox.addWidget(l2)
        vbox.addWidget(l3)
        vbox.addWidget(l4)
        vbox.addWidget(l5)
        vbox.addWidget(l6)
        vbox.addWidget(l7)
        vbox.addWidget(l8)
        info_dialog.setLayout(vbox)
        info_dialog.setWindowModality(Qt.ApplicationModal)
        info_dialog.exec_()
