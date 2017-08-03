import redis
import os
import fuzzy_matching


def input_info(url_dic,n):
    r = redis.Redis(host='localhost',port=6379,db=n)     
    for dic in list(url_dic.keys()):
        url_key = dic
        url_value = url_dic[url_key]
        r.hmset(url_key,url_value)

'''
def add_info(url_dic):
    for dic in list(url_dic.keys()):
        for urls in list(dic.keys()):
            r.hset(dic,urls,dic[urls])
'''

def delete_info(n):
    for i in n:
        r = redis.Redis(host='localhost',port=6379,db=i) 
        for key in r.keys():
            for url in r.hgetall(key):
                url_temp = url.decode()
                url_temp = url_temp.split(' ')[0]
                if not os.path.isfile(url_temp):
                    r.hdel(key,url)


def fuzzy_match(strings ,n):
    choice = []
    for i in n:
        r = redis.Redis(host='localhost',port=6379,db=i)
        for keys in list(r.keys()):
            keys = keys.decode()
            choice.append(keys)
    str_list = strings.split(' ')
    #print(process.extractOne(str_list[0],choice))
    str_list = [fuzzy_matching.extract(strs, choice, 1) for strs in str_list]
    return search(str_list,n)
    

def search(strings,n):
    dic_count = {}
    dic_value = {}
    ret_urls = [] 
    #strings_list = strings.split(' ')
    for strs in strings:
        for i in n:
            r = redis.Redis(host='localhost',port=6379,db=i)
            dicts = r.hgetall(strs[0])
            print(r.keys(), strs)
            for url in list(dicts.keys()):
                if url in dic_count:
                    dic_count[url] += 1 
                    dic_value[url] *= float(dicts[url].decode())
                else:
                    dic_count[url] = 1
                    dic_value[url] = float(dicts[url].decode())
    for key in dic_value:
        dic_value[key] = dic_value[key]*(2**dic_count[key])
    ret_list = sorted(dic_value.items(), key=lambda d: d[1],reverse=True)
    for i in ret_list:
        ret_urls.append(i[0].decode())
    return [ret[0].decode() for ret in ret_list]