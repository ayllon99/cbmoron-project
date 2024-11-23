from pymongo import MongoClient


def uploadtomongo(ti):
    data=ti.xcom_pull(task_ids='scraping_info',key='data_mongo')
    match_id=ti.xcom_pull(task_ids='scraping_info',key='match_id')
    print(data)
    try:
        print(f'match_id={match_id}')
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
