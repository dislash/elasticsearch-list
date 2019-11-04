#-*- coding: utf-8 -*-

from flask import Flask, request, render_template
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q, Filter
import os

app = Flask(__name__)

# connect to the Elasticsearch cluster
elastic = Elasticsearch([{'host': '34.97.218.155', 'port': 9200}])

@app.route("/")
def index():
    s = Search(using=elastic, index="daily")
    category_1 = Filter(Q('term',category=1))
    s.aggs.bucket('by_date', 'date_histogram', field='date', interval='day', order={'_key': 'desc'})\
          .bucket('1', category_1)\
          .bucket('am', 'terms', field='am_pm')\
          .bucket('by_time', 'terms', field='time')
    response = s.execute()
    rows = []
    for tag1 in response.aggregations.by_date.buckets:
        items = []
        entry = {'id':tag1.key_as_string, 'title':tag1.doc_count}
        rows.append(entry)
        for tag2 in tag1.by_category.buckets:
            for tag3 in tag2.by_am_pm.buckets:
                for tag4 in tag3.by_time.buckets:
                    item = {'category_count':tag2.doc_count, 'category':'1', 'am_pm':tag3.key, 'time':str(tag4.key)}
                    items.append(item)
                    entry[tag1.key_as_string]=items
    print(rows)
    return render_template('list.html', books=rows)

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
