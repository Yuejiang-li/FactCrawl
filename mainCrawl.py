import requests
import json
import time
import gc
import pandas as pd


def main():
    data = {'title':[], 'author':[], 'authordesc':[],
            'id':[], 'date':[], 'markstyle':[],
            'result':[], 'explain':[], 'abstract':[],
            'tag':[], 'type':[], 'videourl':[],
            'cover':[], 'section':[], 'iscolled':[],
            'arttype':[]}   # we shall use this dictionary to record data

    url_loaded = 'https://vp.fact.qq.com/loadmore'
    callback_head = 'jsonp'
    payload = {'artnum': 0, 'page': 0, 'callback': None}

    # loop over the pages
    for i in range(20):
        page_num = i+1
        print('currently parsing page {}'.format(page_num))
        payload['page'] = page_num
        payload['callback'] = callback_head + str(page_num)
        r = requests.get(url_loaded, params=payload)
        time.sleep(3)
        content = r.text.replace(payload['callback']+'(', '')
        content = content[:-1]
        contents = json.loads(content)['content']
        for content in contents:
            # go over each news
            for key, value in content.items():
                if key == 'tag':
                    value = ','.join(value)
                data[key].append(value)
        del contents, content
        gc.collect()
    df = pd.DataFrame(data)
    df.to_csv('Rumor_Fact.csv')




if __name__ == "__main__":
    main()
