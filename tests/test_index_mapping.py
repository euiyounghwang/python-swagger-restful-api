
import pytest
import jsondiff
from service.es_util import response_payload_transform
import json


def test_index_mapping():

    # - Case
    source_mapping = {
        "test_mapping": "test"
    }

    target_mapping = {
        "test_mapping": "test"
    }
    
    # Compare JSON objects using jsondiff
    # diff = jsondiff.diff(source_mapping, target_mapping, syntax='symmetric')
    diff = jsondiff.diff(source_mapping, target_mapping, marshal=True, syntax="symmetric")
    # print(json.dumps(response_payload_transform(diff), indent=2))
    assert response_payload_transform(diff) == {
        "diff": "Same mapping"
    }

    # - Case
    target_mapping = {
        "test_mapping": "test1"
    }
    
    # Compare JSON objects using jsondiff
    # diff = jsondiff.diff(source_mapping, target_mapping, syntax='symmetric')
    diff = jsondiff.diff(source_mapping, target_mapping, marshal=True, syntax="symmetric")
    assert response_payload_transform(diff) == {
        "diff": "Different mapping",
        "result": {
            "test_mapping": [
                "test",
                "test1"
            ]
        }
    }

    # - Case
    target_mapping = {
    }
    
    # Compare JSON objects using jsondiff
    # diff = jsondiff.diff(source_mapping, target_mapping, syntax='symmetric')
    diff = jsondiff.diff(source_mapping, target_mapping, marshal=True, syntax="symmetric")
    # print(json.dumps(response_payload_transform(diff), indent=2))
    assert response_payload_transform(diff) == {
        "diff": "Different mapping",
        "result": [
            {
                "test_mapping": "test"
            },
            {

            }
        ]     
    }


     # - Case
    target_mapping = {
         "a": "test"
    }
    
    # Compare JSON objects using jsondiff
    # diff = jsondiff.diff(source_mapping, target_mapping, syntax='symmetric')
    diff = jsondiff.diff(source_mapping, target_mapping, marshal=True, syntax="symmetric")
    # print(json.dumps(response_payload_transform(diff), indent=2))
    assert response_payload_transform(diff) == {
        "diff": "Different mapping",
        "result": [
            {
                "test_mapping": "test"
            },
            {
                "a": "test"
            }
        ]     
    }


    # - Case
    target_mapping = {
        "test_mapping": "test",
        "add_mapping": "test"
    }
    
    # Compare JSON objects using jsondiff
    # diff = jsondiff.diff(source_mapping, target_mapping, syntax='symmetric')
    diff = jsondiff.diff(source_mapping, target_mapping, marshal=True, syntax="symmetric")
    # print(json.dumps(response_payload_transform(diff), indent=2))
    assert response_payload_transform(diff) == {
        "diff": "Different mapping",
        "result": {
            "$insert": {
                "add_mapping": "test"
            }
        }
    }


    # - Case
    target_mapping = {
        "test_mapping": "test",
        "add_mapping": "test",
         "employee": {  
            "name": "sonoo",   
            "salary": 56000,   
            "married":  True
        }
    }
    
    # Compare JSON objects using jsondiff
    # diff = jsondiff.diff(source_mapping, target_mapping, syntax='symmetric')
    diff = jsondiff.diff(source_mapping, target_mapping, marshal=True, syntax="symmetric")
    # print(json.dumps(response_payload_transform(diff), indent=2))
    assert response_payload_transform(diff) == {
        "diff": "Different mapping",
        "result": {
            "$insert": {
                "add_mapping": "test",
                "employee": {  
                    "name":       "sonoo",   
                    "salary":      56000,   
                    "married":    True
                }  
            }
        }
    }


    # - Case
    target_mapping = {
        "employee": {  
            "name": "sonoo",   
            "salary": 56000,   
            "married": True
        }  
    }
    
    # Compare JSON objects using jsondiff
    # diff = jsondiff.diff(source_mapping, target_mapping, syntax='symmetric')
    diff = jsondiff.diff(source_mapping, target_mapping, marshal=True, syntax="symmetric")
    # print(json.dumps(response_payload_transform(diff), indent=2))
    assert response_payload_transform(diff) == {
        "diff": "Different mapping",
        "result": [
            {
                "test_mapping": "test"
            },
            {
                "employee": {
                    "name": "sonoo",
                    "salary": 56000,
                    "married": True
                }
            }
        ]
    }