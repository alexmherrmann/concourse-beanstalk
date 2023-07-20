#!/usr/bin/env python3
# write "doing nothing" to stderr
import sys
import json


print("doing nothing", file=sys.stderr)

# load stdin as json
stdin = json.loads(sys.stdin.read())

print(stdin, file=sys.stderr)

# Get stdin["version"] if it exists, otherwise use "1"
version = stdin.get("version", [{"ref": "1"}])
print(json.dumps({"version": version}))