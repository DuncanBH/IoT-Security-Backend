daily_average_pipeline = [
    {
        '$project': {
            '_id': 0,
            'date': {
                '$dateToParts': {
                    'date': '$timestamp'
                }
            },
            'value': 1
        }
    }, {
        '$group': {
            '_id': {
                'date': {
                    'year': '$date.year',
                    'month': '$date.month',
                    'day': '$date.day'
                }
            },
            'average': {
                '$avg': '$value'
            }
        }
    }
]
