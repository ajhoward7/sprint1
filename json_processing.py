import json
import os


def valid_json(json_str):
	if json_str == "":
		return False

	json_v = json.loads(line)

	if json_v.get('prop') is None:
		return 

def extract_ages(json_strs):
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
