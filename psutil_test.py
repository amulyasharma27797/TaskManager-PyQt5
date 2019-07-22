import psutil

rows = 0
listOfProcObjects = []


def getListOfProcesses():

    global listOfProcObjects
    listOfProcObjects = []

    # Iterate over the list
    for proc in psutil.process_iter():
        try:
            # Fetch process details as dict
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            pinfo['vms'] = proc.memory_info().vms
            pinfo['res'] = proc.memory_info().rss
            pinfo['shared'] = proc.memory_info().shared
            pinfo['mem_per'] = proc.memory_percent()
            pinfo['cpu'] = proc.cpu_percent()
            pinfo['path'] = proc.cwd()
            pinfo['priority'] = proc.nice()
            pinfo['time'] = proc.create_time()

            # Append dict to list
            listOfProcObjects.append(pinfo)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'])

    # print(listOfProcObjects)
    global rows
    rows = len(listOfProcObjects)
    # print(rows)
    return listOfProcObjects

getListOfProcesses()
