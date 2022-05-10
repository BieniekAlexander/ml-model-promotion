import argparse
import json

def get_id_by_display_name(lst, display_name):
	""" Find the json object with the specified display name, and return the id field at the end of the object's name """
	items = list(filter(lambda x: x['displayName']==display_name, lst))
	
        if items:
            item = items[0]
	    return item['name'].rsplit('/', 1)[-1]
        else:
            return ""


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Get id of google api object from display name')
	parser.add_argument('--display-name', dest='display_name', required=True,
                    help='name of google object to find')
	parser.add_argument('--json-path', dest='json_path', required=True,
                    help='path to the json file to read')

	args = parser.parse_args()
	obj = json.load(open(args.json_path, 'r'))

	assert isinstance(obj, list)

	print(get_id_by_display_name(obj, args.display_name))
