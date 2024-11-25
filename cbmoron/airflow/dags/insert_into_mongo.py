from pymongo import MongoClient


def uploadtomongo(ti):
    match_ids=ti.xcom_pull(task_ids='scraping_info',key='match_ids') 
    for match_id in match_ids:
        data=ti.xcom_pull(task_ids='scraping_info',key=f'{match_id}_data_mongo')
        try:
            print(f'Uploading to mongo match_id={match_id}')
            client = MongoClient("mongodb://root:root@mongo-server:27017/")
            db = client["CBM"]
            collection = db["temp"]
            document={f'{match_id}':data}
            print(document)
            collection.insert_one(document)
            print(f"Document inserted into {collection}")
            return True
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            return False
