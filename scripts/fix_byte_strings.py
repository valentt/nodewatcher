#!/usr/bin/env python
"""Script to convert Python 2 byte strings to regular strings in migration files."""

import os
import re

# Find all migration files
migrations_dir = '/code/nodewatcher'
for root, dirs, files in os.walk(migrations_dir):
    if 'migrations' in root:
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()

                # Replace byte strings with regular strings
                # Handle b'string' patterns
                new_content = re.sub(r"\bb'([^']*)'", r"'\1'", content)
                # Handle b"string" patterns
                new_content = re.sub(r'\bb"([^"]*)"', r'"\1"', new_content)

                if content != new_content:
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    print(f'Fixed: {filepath}')

print('Done!')
