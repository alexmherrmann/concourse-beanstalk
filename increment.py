#!/usr/bin/env python3

# Get the first argument from the command line
# and convert it to an integer
import sys


version = sys.argv[1]

# parse it as a version X.Y.Z
[major, minor, patch] = version.split(".")

# increment the patch
patch = int(patch.split("-")[0]) + 1

# Print the new version to stdout
print(f"{major}.{minor}.{patch}")