from collections import defaultdict
import datetime
import platform
import psutil
import socket
import cpuinfo

def get_disk_info():
    # Get all disk partitions
    partitions = psutil.disk_partitions()
    
    # Create a dictionary to store aggregated disk usage info for each device
    disk_info = defaultdict(lambda: {'total': 0, 'used': 0, 'free': 0, 'percent': 0, 'partitions': 0})
    
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        device = partition.device
        
        # Aggregate the data for each device
        disk_info[device]['total'] += usage.total
        disk_info[device]['used'] += usage.used
        disk_info[device]['free'] += usage.free
        disk_info[device]['partitions'] += 1
    
    # Calculate the usage percent for each device
    for device, info in disk_info.items():
        info['percent'] = round((info['used'] / info['total']) * 100, 2)
    
    return disk_info

def get_system_info():
    info = {}

    # Basic system information
    info['Name'] = platform.node()
    info['OS'] = platform.uname().system + " " + platform.release()
    info['Version'] = platform.version()
    try:
        processor_info = cpuinfo.get_cpu_info()['brand_raw']
    except KeyError:
        try:
            processor_info = cpuinfo.get_cpu_info()['brand']
        except KeyError:
            processor_info = "Unknown Processor"
    info['Processor'] = processor_info
    info['Architecture'] = platform.architecture()[0]

    # Network information
    info['Hostname'] = socket.gethostname()
    info['IP Address'] = socket.gethostbyname(socket.gethostname())

    # CPU information
    info['Physical cores'] = psutil.cpu_count(logical=False)
    info['Logical cores'] = psutil.cpu_count(logical=True)
    info['Max Frequency'] = psutil.cpu_freq().max/1000
    info['Current Frequency'] = psutil.cpu_freq().current/1000
    info['CPU Usage'] = psutil.cpu_percent(interval=1)

    # Memory information
    svmem = psutil.virtual_memory()
    info['Total Memory'] = round(svmem.total/(1024*1024*1024),2)
    info['Available Memory'] = round(svmem.available/(1024*1024*1024),2)
    info['Used Memory'] = round(svmem.used/(1024*1024*1024),2)
    info['Memory Usage'] = svmem.percent

    # Get aggregated disk info
    disk_info = get_disk_info()

    # Format the disk info into the info dictionary
    for device, data in disk_info.items():
        info[f'Disk Total Space ({device})'] = round(data['total'] / (1024 * 1024 * 1024), 2)
        info[f'Disk Used Space ({device})'] = round(data['used'] / (1024 * 1024 * 1024), 2)
        info[f'Disk Free Space ({device})'] = round(data['free'] / (1024 * 1024 * 1024), 2)
        info[f'Disk Usage ({device})'] = data['percent']

    # Network details
    net_io = psutil.net_io_counters()
    info['Total Bytes Sent'] = net_io.bytes_sent
    info['Total Bytes Received'] = net_io.bytes_rec

    # Time
    info['Time'] = datetime.datetime.now().time().strftime('%H:%M:%S')

    # Wrapping the info dictionary in a list
    return [info]


if __name__ == "__main__":
    system_info = get_system_info()
    for info in system_info:
        for key, value in info.items():
            print(f"{key}: {value}")
