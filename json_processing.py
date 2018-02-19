import json
import os

def valid_json(json_str):
	"""
	json validation function. This function takes in json strings
	and checks the following:

	- If the string is blank
	- if the string is empty
	- if the string can be converted (missing {})
	- Check to make sure that the 'Prop' value in data
	- check to make sure 'age' exists and
		- age >= 0
		- age is an int
	- check to make sure that the name exists
	"""
	try:

		# nothing passed
		if json_str is None:
			return False

		# blank strings
		if json_str == "":
			return False

		# convert to json
		json_v = json.loads(line)

		# check 'prop field'
		props = json_v.get('prop')
		if props  is None:
			return False

		# check age field
		age = props.get('age')
		if age is None:
			return False

		# check proper age formatting
		if type(age) != int:
			return False

		if age < 0:
			return False

		# checks for name fields
		name = props.get('name')
		if name is None:
			return False

		# if all conditions are passed
		return True

	except Exception as e:
		return False
		print(e)


def extract_fields(json_strs):
    """
    takes in an array of json strings and converts them to
    actual json. Some notes:
    
    - json keys must have " instead of single quotes, otherwise
    there are issues with importing
    - the text values should be encoded with ascii or utf8, not
    unicode, otherwise the python json library will also
    have a similiarly difficult time with it
    """
    names_and_ages = []

    # goes through input strings
    for json_item in json_strs:

    	# checks if valid
    	if valid_json(json_item):
    		json_v = json.loads(line)

    		row = []
    		for field in ['age','prop']
    			row.append(json_v[field])

    		names_and_ages.append(row)

    print "%d valid jsons found" % len(names_and_ages)
    return names_and_ages
