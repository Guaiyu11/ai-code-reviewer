#!/usr/bin/env python3
"""
Header Gen - Generate code headers/license banners.
Usage: python header-gen.py --name NAME [--type mit|apache|gpl|bsd]
"""

import sys

LICENSE_TEMPLATES = {
    'mit': """MIT License

Copyright (c) {year} {name}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""",
    'apache': """Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

Copyright {year} {name}

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.""",
    'gpl': """GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) {year} {name}

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation.""",
}

CODE_HEADER = """#!/usr/bin/env python3
\"\"\"
{name}
{description}

Author: {name}
Created: {date}
\"\"\"
"""

def generate_license(license_type, name):
    from datetime import datetime
    year = datetime.now().year
    template = LICENSE_TEMPLATES.get(license_type, LICENSE_TEMPLATES['mit'])
    return template.format(year=year, name=name)

def generate_code_header(name, description):
    from datetime import datetime
    return CODE_HEADER.format(
        name=name,
        description=description,
        date=datetime.now().strftime('%Y-%m-%d'),
        name=name
    )

if __name__ == '__main__':
    if '--help' in sys.argv or len(sys.argv) < 2:
        print("Usage: python header-gen.py --name NAME [--type mit|apache|gpl|bsd]")
        sys.exit(1)
    
    name = 'Unknown'
    license_type = 'mit'
    
    for i, arg in enumerate(sys.argv):
        if arg == '--name' and i + 1 < len(sys.argv):
            name = sys.argv[i + 1]
        elif arg == '--type' and i + 1 < len(sys.argv):
            license_type = sys.argv[i + 1].lower()
    
    print(generate_license(license_type, name))
