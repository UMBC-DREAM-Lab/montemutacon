from tqdm import tqdm
import pymongo

class EmberFeatures():
    
    def __init__(self, collection='train', num_instances=50):
        
        if collection == 'train':
            collection_name = 'train_ember2018_me'
        else:
            collection_name = 'test_ember2018_me'
        
        
        try:
            client = pymongo.MongoClient("127.0.0.1", 27017)
            print("Database names: ", client.database_names())
            db = client["ember_2018_me"]
            print("Collections:", db.collection_names())
            print("[+] Connected to MongoDB.")
        except Exception as e:
            print("[-] Connection to MongoDB failed!")
            
        avail_instances = db[collection_name].estimated_document_count()
        print('Available instances:', avail_instances)
        
        if num_instances > avail_instances:
            print('Too many instances requested. Reverting to available instances!')
            num_instances = avail_instances
            
        
        cursor = db[collection_name].find()
        self.instances = list()
        for ii, document in tqdm(enumerate(cursor)):
            self.instances.append(document)
            if ii >= num_instances-1:
                break
                
        client.close()
        print('Downloaded instances:', len(self.instances))
        
    def list_features(self):
        keys = self.instances[0].keys()
        return list(keys)
    
    def get_feature(self, name):
        
        if name not in self.list_features():
            print('Feature was not found. Evailable features are:')
            print(self.list_features())
        
        target = []

        for instance in self.instances:
            target.append(instance[str(name)])
        return target