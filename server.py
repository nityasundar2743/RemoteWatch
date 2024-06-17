from pymongo import MongoClient
import systemInfo
import platform

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
        
    # Get system information
    data_to_insert = systemInfo.get_system_info()

    # Update the data in the collection without deleting it
    for data in data_to_insert:
        collection.update_one(
            {"Name": data["Name"]},  # Filter by Name
            {"$set": data},  # Set the data
            upsert=True  # Insert the document if it doesn't exist
        )
        
    print("data uploaded, Time : " + data_to_insert[0]['Timestamp'])
        
    # Close the MongoDB connection
    client.close()

if __name__ == "__main__":
    while True:
        update_data()

    # update_data()
