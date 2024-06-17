from pymongo import MongoClient
import systemInfo
import time

# MongoDB connection details
MONGO_URI = 'mongodb+srv://nitya:1234@remotewatch.e6zcabc.mongodb.net/?retryWrites=true&w=majority&appName=RemoteWatch'
DATABASE_NAME = 'RemoteWatch'
COLLECTION_NAME = 'devices'

def update_data():
    # Sample data to insert into MongoDB
    data_to_insert = systemInfo.get_system_info()

    # Create a MongoDB client
    client = MongoClient(MONGO_URI)
        
    # Access the database and collection
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
        
    # Clear the collection (optional, if you want to overwrite existing data)
    collection.delete_many({"Name" : systemInfo.getname()})
        
    # Get system information
    data_to_insert = systemInfo.get_system_info()
        
    # Insert the data into the collection
    collection.insert_many(data_to_insert)
        
    print("Updated details successfully into MongoDB\n")
        
    # Close the MongoDB connection
    client.close()

if __name__ == "__main__":
    while True:
        update_data()

    # update_data()
