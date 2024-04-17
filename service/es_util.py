

def response_payload_transform(diff):
    response = {}
    if not diff:
        response.update({'diff' : 'Same mapping'})
    else:
        response.update({'diff' : 'Different mapping', 'result' : diff})

    return response


