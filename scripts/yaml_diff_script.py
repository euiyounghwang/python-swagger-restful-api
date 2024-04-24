import yaml
from deepdiff import DeepDiff
import json
import argparse

def yaml_as_dict(my_file):
    my_dict = {}
    with open(my_file, 'r') as fp:
        docs = yaml.safe_load_all(fp)
        for doc in docs:
            for key, value in doc.items():
                my_dict[key] = value
    return my_dict

if __name__ == '__main__':
    '''
    python ./scripts/yaml_diff_script.py --source C://Users/euiyoung.hwang/test1.yml --target C://Users/euiyoung.hwang/test2.yml
    '''
    parser = argparse.ArgumentParser(description="Script that might allow us to confirm the diff with two files")
    parser.add_argument('-s', '--source', dest='source', default="test1.yml", help='source file')
    parser.add_argument('-t', '--target', dest='target', default="test2.yml", help='target file')
    args = parser.parse_args()

    if args.source:
        source = args.source

    if args.target:
        target = args.target

    a = yaml_as_dict(source)
    b = yaml_as_dict(target)
    ddiff = DeepDiff(a, b, view='tree', ignore_order=True)
    jsoned = ddiff.to_json()
    # print(jsoned)
    print(json.dumps(json.loads(jsoned), indent=2))
    