import time
from pymongo import MongoClient
import datetime
import platform
from monitor import CPUUsageMonitor, MemoryUsageMonitor

# MongoDB connection details
MONGO_URI = 'mongodb+srv://nitya:1234@remotewatch.e6zcabc.mongodb.net/?retryWrites=true&w=majority&appName=RemoteWatch'
DATABASE_NAME = 'RemoteWatch'
COLLECTION_NAME = 'usageStatistics'

def update_data():
    # Create a MongoDB client
    client = MongoClient(MONGO_URI)
        
    # Access the database and collection
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
        
    # Get system information
    cpuHistory = cpuMonitor.get_cpu_usage_history()
    avgCPUUsage = cpuMonitor.get_avg_cpu_usage()
    memHistory = memMonitor.get_memory_usage_history()
    avgMemUsage = memMonitor.get_avg_memory_usage()
    timeStamp = datetime.datetime.now().strftime('%H:%M:%S')

    name = platform.node()
    
    # Create the update document
    update_document = {
        'Name': name,
        'avgCPUUsage': avgCPUUsage,
        'cpuUsageHistory': cpuHistory,
        'avgMemUsage' : avgMemUsage,
        'memUsageHistory' : memHistory,
        'timestamp': timeStamp
    }
    
    # Upsert the document in MongoDB
    collection.update_one(
        {'Name': name},  # Filter document by 'Name'
        {'$set': update_document},  # Update document with new data
        upsert=True  # Insert document if it does not exist
    )
    
    print("Data uploaded, timestamp - " + timeStamp)
        
    # Close the MongoDB connection
    client.close()

if __name__ == "__main__":
    cpuMonitor = CPUUsageMonitor(max_samples=60, sample_interval=1)
    memMonitor = MemoryUsageMonitor(max_samples=60, sample_interval=1)
    try:
        while True:
            update_data()
            time.sleep(30)  # Sleep for 30 seconds before updating again
    except KeyboardInterrupt:
        memMonitor.stop()
        cpuMonitor.stop()
        print("Monitoring stopped due to keyboard interrupt.")
