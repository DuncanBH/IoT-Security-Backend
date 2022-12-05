daily_average_pipeline = [
    {
        '$match': {
            'value': {
                '$type': 'int'
            }
        }
    }, {
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


def sound_for_a_day(year, month, day):
    return [
        {
            '$match': {
                'value': {
                    '$type': 'int'
                }
            }
        }, {
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
            '$match': {
                'date.year': year,
                'date.month': month,
                'date.day': day
            }
        }
    ]


daily_count_pipeline = [
    {
        '$match': {
            'motionSeen': {
                '$eq': True
            }
        }
    }, {
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
            'value': {
                '$count': {}
            }
        }
    }
]