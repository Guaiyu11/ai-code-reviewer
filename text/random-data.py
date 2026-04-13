#!/usr/bin/env python3
"""
Random Data Generator - Generate random test data.
Usage: python random-data.py <type> [count]
Types: name, email, phone, address, uuid, date, ip, mac, creditcard
"""

import sys
import random
import string
import uuid
from datetime import datetime, timedelta

def random_name():
    first = ['Alice', 'Bob', 'Carol', 'Dave', 'Eve', 'Frank', 'Grace', 'Hank', 'Iris', 'Jack', 'Kate', 'Leo', 'Mia', 'Noah', 'Olivia', 'Pete', 'Quinn', 'Rose', 'Sam', 'Tara', 'Uma', 'Victor', 'Wendy', 'Xander', 'Yuki', 'Zoe']
    last = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Anderson', 'Taylor', 'Thomas', 'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White', 'Harris']
    return random.choice(first) + ' ' + random.choice(last)

def random_email(name=None):
    if name is None:
        name = random_name()
    name_lower = name.lower().replace(' ', '.')
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'proton.me', 'icloud.com']
    return f"{name_lower}@{(random.choice(domains))}"

def random_phone():
    return f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"

def random_address():
    streets = ['Main', 'Oak', 'Cedar', 'Pine', 'Maple', 'Elm', 'Park', 'Lake', 'Hill', 'Forest']
    street_num = random.randint(1, 9999)
    street_name = random.choice(streets)
    street_type = ['St', 'Ave', 'Rd', ' Blvd', 'Dr', 'Ln'][random.randint(0, 5)]
    city = ['Springfield', 'Riverside', 'Georgetown', 'Fairview', 'Madison']
    state = ['CA', 'NY', 'TX', 'FL', 'WA', 'OR', 'CO', 'GA', 'VA', 'MA']
    zipcode = random.randint(10000, 99999)
    return f"{street_num} {street_name} {street_type}\n{random.choice(city)}, {random.choice(state)} {zipcode}"

def random_date(start_year=1990, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime('%Y-%m-%d')

def random_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"

def random_mac():
    return ':'.join(f'{random.randint(0,255):02x}' for _ in range(6))

def random_creditcard():
    """Generate a valid-format credit card number (Luhn invalid - just for testing)."""
    return f"{random.randint(4000,4999)}{random.randint(100000000,999999999)}{random.randint(1000,9999)}"

GENERATORS = {
    'name': random_name,
    'email': random_email,
    'phone': random_phone,
    'address': random_address,
    'uuid': lambda: str(uuid.uuid4()),
    'date': random_date,
    'ip': random_ip,
    'mac': random_mac,
    'creditcard': random_creditcard,
}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python random-data.py <type> [count]")
        print("Types:", ', '.join(GENERATORS.keys()))
        sys.exit(1)
    
    data_type = sys.argv[1].lower()
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    if data_type not in GENERATORS:
        print(f"Unknown type: {data_type}")
        print("Types:", ', '.join(GENERATORS.keys()))
        sys.exit(1)
    
    gen = GENERATORS[data_type]
    
    if data_type == 'email':
        for _ in range(count):
            name = random_name()
            print(gen(name))
    else:
        for _ in range(count):
            print(gen())
