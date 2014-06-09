'''
Created on May 29, 2014

@author: gene
'''

import argparse
import json
import os
import yaml


def type_filename(filename, mode='r'):
    if not os.path.exists(filename):
        msg = "The file %s does not exist" % filename
        raise argparse.ArgumentTypeError(msg)
    else:
        return open(filename, mode)


def main():
    parser = argparse.ArgumentParser(description='Combine files')
    parser.add_argument('filenames', metavar="FILE", nargs="+",
                         type=type_filename, help='File to combine')
    parser.add_argument('-j', '--json', action='store_true',
                         help='Files contain JSON')
    parser.add_argument('-y', '--yaml', action='store_true',
                         help='Files contain YAML')
    args = parser.parse_args()

    if args.json or args.yaml:
        output = {}
    else:
        output = ''

    for file_handle in args.filenames:
        if args.json:
            output = dict(output.items() +
                          json.loads(file_handle.read()).items())
        elif args.yaml:
            output = dict(output.items() +
                          yaml.load(file_handle.read()).items())
        else:
            output += file_handle.read()
        file_handle.close()

    if args.json:
        output = json.dumps(output, indent=4)
    elif args.yaml:
        output = yaml.dump(output)

    return output

if __name__ == '__main__':
    print(main(),)
