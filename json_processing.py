import json
import os


def valid_json(json_str):
    """
    json validation function. This function takes in json strings
    and checks the following:

    - If the string is blank
    - if the string is empty
    - if the string can be converted (missing {})
    """
    try:
        # nothing passed
        if json_str is None:
            return False, "No string found"

        # blank strings
        if json_str == "":
            return False, "Empty string"

        # convert to json
        json_v = json.loads(json_str)
        return True, json_v

    except Exception as e:
        return False, e


def valid_json_format(json_v):
    """
    Takes in valid jsons (not strings)
    - Check to make sure that the 'Prop' value in data
    - check to make sure 'age' exists and
        - age >= 0
        - age is an int
    - check to make sure that the name exists
    """

    # checks for name fields
    err_msg = []

    name = json_v.get('name')
    if name is None:
        err_msg.append('name not available')
        return False

    # check 'prop field'
    props = json_v.get('prop')
    if props is None:
        err_msg.append('prop key not available')
        return False

    # check age field
    age = props.get('age')
    if age is None:
        err_msg.append('age is missing')
        return False

    # check proper age formatting
    if type(age) not in [int, float]:
        err_msg.append('non numeric age')
        return False

    if age < 0:
        err_msg.append('age too small')
        return False

    if len(err_msg) > 0:
        print ','.join(err_msg)
    # if all conditions are passed
    return True


def extract_fields(json_str):
    """
    takes in an array of json strings and converts them to
    actual json. Some notes:
    - json keys must have " instead of single quotes, otherwise
    there are issues with importing
    - the text values should be encoded with ascii or utf8, not
    unicode, otherwise the python json library will also
    have a similiarly difficult time with it
    """

    # checks if valid
    json_check, data = valid_json(json_str)
    if not json_check:
        print 'Not valid json format'
        return None

    # checks json data format
    if not valid_json_format(data):
        print 'missing name or age fields'
        return None

    name = data['name'].decode('utf-8', 'ignore')
    age = data['prop']['age']
    return name + '\t' + str(age)


def batch_extract(json_strs):
    """
    Pulls out valid names and ages from a list of json strs
    """
    names_and_ages = []

    # goes through input strings
    for json_item in json_strs:

        # pull fields out
        row = extract_fields(json_item)

        # if populated then store
        if row:
            names_and_ages.append(row)

    print "%d valid jsons found" % len(names_and_ages)
    return names_and_ages
