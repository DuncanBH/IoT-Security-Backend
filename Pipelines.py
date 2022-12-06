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


def average_for_period(year, month, day):
    pipeline = [
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
    match = {}

    if year is not None:
        match.update({'date.year': int(year)})

    if month is not None:
        match.update({'date.month': int(month)})

    if day is not None:
        match.update({'date.day': int(day)})

    pipeline[2]['$match'] = match

    print("Match", match)
    print("Pipeline", pipeline)
    return pipeline


def sound_for_period(year, month, day):
    pipeline = [
        {
            '$match': {
                'value': {
                    '$type': 'int'
                }
            }
        },
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
        },
        {
            '$match': {
            }
        }
    ]

    match = {}

    if year is not None:
        match.update({'date.year': int(year)})

    if month is not None:
        match.update({'date.month': int(month)})

    if day is not None:
        match.update({'date.day': int(day)})

    pipeline[2]['$match'] = match

    return pipeline


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
