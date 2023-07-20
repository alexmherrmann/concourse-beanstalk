#!/usr/bin/env python3
# write "doing nothing" to stderr
import sys
import json


print("doing nothing", file=sys.stderr)

# load stdin as json
stdin = json.loads(sys.stdin.read())
print(json.dumps({"version": stdin["version"]}))