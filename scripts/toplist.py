# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import argparse
import json
import os
import plistlib


THIS_DIR = os.path.abspath(os.path.dirname(__file__))


parser = argparse.ArgumentParser(
                    description="Builds .tmLanguage files out of .JSON-tmLanguage files.")
parser.add_argument('-s', dest='source',
                    help="source .JSON-tmLanguage file")

def build(source):
    with open(source, 'r') as f:
        json_data = json.load(f)
        plistlib.writePlist(json_data, os.path.splitext(source)[0] + '.tmLanguage')


if __name__ == '__main__':
    args = parser.parse_args()
    if args.source:
        build(args.source)
