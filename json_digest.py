import json
import os
import argparse

SRC_PATH = '/srv/runme'

def get_json_strings(prefix='mv'):
    """
    mean to be run locally on the server
    this allows the use of the OS library for easy of 
    file access
    """
    files = os.listdir(SRC_PATH)
    target_files = [x for x in files if x.startswith(prefix) and x.endswith("json")]
    json_collection = []

    for fl in target_files:
        with open(os.path.join(SRC_PATH, fl), 'rb') as f:
            json_str = f.readlines()
        json_collection.extend(json_str)
    return json_collection


def json_digest(json_strs):
    """
    takes in an array of json strings and converts them to
    actual json. Some notes:
    
    - json keys must have " instead of single quotes, otherwise
    there are issues with importing
    - the text values should be encoded with ascii or utf8, not
    unicode, otherwise the python json library will also
    have a similiarly difficult time with it
    """
    return_stats = []
    for line in json_strs:
        if line != "":
            try:
                json_v = json.loads(line)
                props = json_v.get('prop')
                if props is not None:
                    age = props.get('age')
                    name = json_v.get('name')
                    if (type(age) == int) and (name is not None):
                        if age >= 0:
                            return_stats.append("%s\t%d" % (str(name), age))
                    
            except Exception as e:
                print(e)
    print "%d valid jsons found" % len(return_stats)
    return return_stats


def write_statsfile(stat_strs, prefix):
    print "writing to file..."
    with open(os.path.join(SRC_PATH, '%s.txt' % prefix),'wb') as f:
        f.write('\n'.join(stat_strs))


parser = argparse.ArgumentParser(description = 'json ingestion library')
parser.add_argument('--prefix', help = 'file prefix that we will be searching for ')
args = parser.parse_args()

if __name__ == '__main__':
    js_str = get_json_strings(args.prefix)
    js_stats = json_digest(js_str)
    write_statsfile(js_stats, args.prefix)