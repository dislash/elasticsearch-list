#-*- coding: utf-8 -*-

from flask import Flask, request, render_template
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import os

app = Flask(__name__)

# connect to the Elasticsearch cluster
elastic = Elasticsearch([{'host': '34.97.218.155', 'port': 9200}])

@app.route("/")
def index():
    s = Search(using=elastic, index="daily")
    s.aggs.bucket('by_date', 'date_histogram', field='date', interval='day')\
          .bucket('by_am_pm', 'terms', field='am_pm')\
          .bucket('by_category', 'terms', field='category')\
          .bucket('by_time', 'terms', field='time')
    s= s.sort({"date" : {"order" : "desc"}})
    response = s.execute()
    rows = []
    for tag1 in response.aggregations.by_date.buckets:
        entry = {'id':tag1.key_as_string}
        rows.append(entry)
        for tag2 in tag1.by_am_pm.buckets:
            for tag3 in tag2.by_category.buckets:
                for tag4 in tag3.by_time.buckets:
                    print(tag1.key_as_string+tag2.key+str(tag3.key)+str(tag4.key))

    return render_template('list.html', books=rows)

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
