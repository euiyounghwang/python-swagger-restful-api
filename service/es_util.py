
import json

def response_payload_transform(diff):
    response = {}
    if not diff:
        response.update({'diff' : 'Same mapping'})
    else:
        response.update({'diff' : 'Different mapping', 'result' : diff})

    return response


def source_hosts_with_http(source_hosts_list):
    ''' split string source host with "," to list'''
    transform_source_hosts = []
    for source_host in source_hosts_list: 
        if not str(source_host).strip().startswith("http://"):
            transform_source_hosts.append("http://" + str(source_host).replace(" ", ""))
        else:
            transform_source_hosts.append(str(source_host).replace(" ", ""))

    # print(json.dumps(transform_source_hosts, indent=2))
    return transform_source_hosts

