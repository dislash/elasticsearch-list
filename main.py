#-*- coding: utf-8 -*-

from flask import Flask, request, render_template
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q, query
import os

app = Flask(__name__)

# connect to the Elasticsearch cluster
elastic = Elasticsearch([{'host': '34.97.218.155', 'port': 9200}])

@app.route("/")
def index():
    s = Search(using=elastic, index="daily")
    category_1 = Q('term',category=1)
    s.aggs.bucket('by_date', 'date_histogram', field='date', interval='day', order={'_key': 'desc'})\
          .bucket('category_1', 'filter', query.Q('term', category=1))\
          .bucket('am', 'filter', query.Q('term', am_pm='am'))\
          .bucket('by_time', 'terms', field='time')
          #.bucket('pm', 'filter', query.Q('term', am_pm='pm'))\
          #.bucket('by_time', 'terms', field='time')
    response = s.execute()
    rows = []
    for tag1 in response.aggregations.by_date.buckets:
        items = []
        if( tag1.category_1.am.doc_count == 1 ) {
            entry = {'id':tag1.key_as_string, 'title':tag1.doc_count, 'category_1': tag1.category_1.doc_count, 'am': tag1.category_1.am.doc_count, 'time: tag1.category_1.am.by_time.buckets[0].key}
            rows.append(entry)
        }
        #for tag2 in tag1.category_1:
        #    item = {'1amtime':tag2.doc_count}
        #    items.append(item)
        #    entry[tag1.key_as_string]=items
    print(rows)
    return render_template('list.html', books=rows)

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
