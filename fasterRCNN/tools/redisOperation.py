#-*-coding:utf-8-*-
import redis
import pickle 
import datetime
 
class redisOperation(redis.Redis):

    def __init__(self, host='localhost', port=6379, db=3, station_name='station1'):
        self.database = redis.Redis(host=host, port=port, db=db)
        print("Successfully connect to Redis Server.")
        # 这里先进行一部分的初始化：
        key = datetime.datetime.now().strftime('%Y-%m-%d')+"_"+station_name
        
        if key in self.database.keys():
            pass
        else:
            value = pickle.dumps({
                'data':[],
                'last_index':0,
                'is_used': False # 是否正在使用，害怕视频生成检测程序与识别程序互相冲突。
            })
            self.database.set(key,value)
    
    def setData(self, key, value):
        value = pickle.dumps(value)
        self.database.set(key, value)
 
    def getData(self, key):
        data = self.database.get(key)
        if data is None:
            return None
        else:
            return pickle.loads(data)
 
    def getKeys(self):
        byteKeys = self.database.keys()
        rawKeys = []
        for key in byteKeys:
            # rawKeys.append(key.decode())
            rawKeys.append(key)
        return rawKeys

    def delKeys(self,key):
        self.database.delete(key)