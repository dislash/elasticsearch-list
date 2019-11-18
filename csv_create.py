{
    "aggs": {
        "range": {
            "date_range": {
                "field": "date",
                "format": "yyyy-MM-dd",
                "ranges": [
                    { "to": "2019-11-17" , "from": "2019-11-01" } 
                ]
            },
            "aggs": {
                "histogram": {                  
                    "date_histogram": {
                        "field": "date",
                        "interval": "1d"
                    },
                    "aggs": {
                        "by_category": {
                            "terms": {
                                "field": "category"
                            },
                            "aggs": {
                                "count_sum": {
                                    "sum": {
                                        "field": "time"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
