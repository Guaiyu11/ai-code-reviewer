#!/usr/bin/env python3
"""
cURL Converter - Convert cURL commands to Python, JavaScript, PHP, Go, Rust.
Usage: python curlconv.py "<curl_command>" [--lang python|js|php|go|rust]
"""

import sys
import re
import urllib.parse

def parse_curl(curl_cmd):
    """Parse a cURL command into components."""
    cmd = curl_cmd.strip()
    if cmd.startswith('curl '):
        cmd = cmd[5:]
    
    parts = {
        'method': 'GET',
        'url': '',
        'headers': [],
        'data': None,
        'user_agent': None,
    }
    
    tokens = []
    # Simple tokenization
    current = ''
    in_quote = False
    quote_char = None
    for c in cmd:
        if c in ("'", '"') and not in_quote:
            in_quote = True
            quote_char = c
            current += c
        elif c == quote_char and in_quote:
            in_quote = False
            quote_char = None
            current += c
        elif c == ' ' and not in_quote:
            if current:
                tokens.append(current)
            current = ''
        else:
            current += c
    if current:
        tokens.append(current)
    
    i = 0
    while i < len(tokens):
        t = tokens[i]
        
        if t in ('-X', '--request'):
            parts['method'] = tokens[i+1].upper()
            i += 2
        elif t in ('-H', '--header'):
            header = tokens[i+1].strip("'\"")
            if header.lower().startswith('content-type:'):
                pass
            parts['headers'].append(header)
            i += 2
        elif t in ('-d', '--data', '--data-raw', '--data-binary'):
            parts['data'] = tokens[i+1].strip("'\"")
            if not parts['method'] or parts['method'] == 'GET':
                parts['method'] = 'POST'
            i += 2
        elif t.startswith("'"):
            if not parts['url']:
                parts['url'] = t.strip("'")
            i += 1
        else:
            if not parts['url']:
                parts['url'] = t.strip("'\"")
            i += 1
    
    return parts

def to_python(parts):
    """Convert parsed cURL to Python requests code."""
    url = parts['url']
    method = parts['method']
    headers = parts['headers']
    data = parts['data']
    
    lines = ['import requests', '']
    
    lines.append(f"url = '{url}'")
    lines.append('')
    
    if headers:
        lines.append('headers = {')
        for h in headers:
            if ':' in h:
                k, v = h.split(':', 1)
                lines.append(f"    '{k.strip()}': '{v.strip()}',")
        lines.append('}')
        lines.append('')
    
    if data:
        if '{' in data:
            lines.append(f"data = {data}")
        else:
            lines.append(f"data = '{data}'")
        lines.append('')
    
    if method == 'GET':
        lines.append("response = requests.get(url, headers=headers)")
    elif method == 'POST':
        if data:
            lines.append("response = requests.post(url, headers=headers, data=data)")
        else:
            lines.append("response = requests.post(url, headers=headers)")
    else:
        lines.append(f"response = requests.{method.lower()}(url, headers=headers)")
    
    lines.append('')
    lines.append("print(response.status_code)")
    lines.append("print(response.text)")
    
    return '\n'.join(lines)

def to_js(parts):
    """Convert parsed cURL to JavaScript fetch code."""
    url = parts['url']
    method = parts['method']
    headers = parts['headers']
    data = parts['data']
    
    lines = ['async function request() {']
    
    if headers:
        lines.append('  const headers = {')
        for h in headers:
            if ':' in h:
                k, v = h.split(':', 1)
                lines.append(f"    '{k.strip()}': '{v.strip()}',")
        lines.append('  };')
        lines.append('')
    
    options = []
    options.append(f"    method: '{method}'")
    if headers:
        options.append('    headers,')
    if data:
        options.append(f"    body: JSON.stringify({data}),")
    
    lines.append('  const options = {')
    lines.extend(f'  {o}' for o in options)
    lines.append('  };')
    lines.append('')
    lines.append("  const response = await fetch(url, options);")
    lines.append("  const data = await response.json();")
    lines.append("  console.log(data);")
    lines.append('}')
    lines.append('')
    lines.append('request();')
    
    return '\n'.join(lines)

def to_php(parts):
    """Convert parsed cURL to PHP code."""
    url = parts['url']
    method = parts['method']
    headers = parts['headers']
    data = parts['data']
    
    lines = ['<?php', '']
    lines.append(f'$url = "{url}";')
    lines.append('')
    
    if headers:
        lines.append('$headers = [')
        for h in headers:
            lines.append(f'    "{h}",')
        lines.append('];')
        lines.append('')
    
    lines.append('$ch = curl_init($url);')
    
    opts = []
    opts.append(f'CURLOPT_RETURNTRANSFER, true')
    opts.append(f'CURLOPT_CUSTOMREQUEST, "{method}"')
    if data:
        opts.append(f'CURLOPT_POSTFIELDS, "{data}"')
    
    for opt in opts:
        lines.append(f'curl_setopt($ch, {opt});')
    
    if headers:
        lines.append('curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);')
    
    lines.append('')
    lines.append('$response = curl_exec($ch);')
    lines.append('curl_close($ch);')
    lines.append('var_dump($response);')
    lines.append('?>')
    
    return '\n'.join(lines)

def to_go(parts):
    """Convert parsed cURL to Go code."""
    url = parts['url']
    method = parts['method']
    headers = parts['headers']
    data = parts['data']
    
    lines = ['package main', '']
    lines.append('import "net/http"')
    lines.append('import "bytes"')
    lines.append('import "fmt"')
    lines.append('')
    lines.append('func main() {')
    
    if data:
        lines.append(f'    body := bytes.NewBuffer([]byte(`{data}`))')
        lines.append(f'    req, _ := http.NewRequest("{method}", "{url}", body)')
    else:
        lines.append(f'    req, _ := http.NewRequest("{method}", "{url}", nil)')
    
    if headers:
        for h in headers:
            if ':' in h:
                k, v = h.split(':', 1)
                lines.append(f'    req.Header.Set("{k.strip()}", "{v.strip()}")')
    
    lines.append('')
    lines.append('    client := &http.Client{}')
    lines.append('    resp, _ := client.Do(req)')
    lines.append('    defer resp.Body.Close()')
    lines.append('    fmt.Println(resp.Status)')
    lines.append('}')
    
    return '\n'.join(lines)

def to_rust(parts):
    """Convert parsed cURL to Rust code."""
    url = parts['url']
    method = parts['method']
    headers = parts['headers']
    data = parts['data']
    
    lines = ['use reqwest::Client;', 'use serde_json::json;', '']
    lines.append('#[tokio::main]')
    lines.append('async fn main() -> Result<(), reqwest::Error> {')
    lines.append('    let client = Client::new();')
    lines.append('')
    
    if data:
        lines.append(f'    let body = json!({data});')
        lines.append(f'    let res = client.{method.lower()}(r#"{url}"#).json(&body);')
    else:
        lines.append(f'    let res = client.{method.lower()}(r#"{url}"#);')
    
    if headers:
        for h in headers:
            if ':' in h:
                k, v = h.split(':', 1)
                lines.append(f'        .header("{k.strip()}", "{v.strip()}")')
    
    lines.append('        .send().await?;')
    lines.append('    println!("{}", res.status());')
    lines.append('    Ok(())')
    lines.append('}')
    
    return '\n'.join(lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python curlconv.py '<curl_command>' [--lang python|js|php|go|rust]")
        print("\nExample:")
        print("  python curlconv.py \"curl -X POST https://api.example.com -d '{\\\"key\\\":\\\"value\\\"}'\"")
        sys.exit(1)
    
    curl_cmd = sys.argv[1]
    lang = 'python'
    
    for i, arg in enumerate(sys.argv):
        if arg == '--lang' and i + 1 < len(sys.argv):
            lang = sys.argv[i + 1].lower()
    
    parts = parse_curl(curl_cmd)
    
    print("=== Parsed ===")
    print(f"URL:     {parts['url']}")
    print(f"Method:  {parts['method']}")
    print(f"Headers: {parts['headers']}")
    print(f"Data:    {parts['data']}")
    print()
    
    print(f"=== {lang.upper()} ===\n")
    
    if lang == 'python':
        print(to_python(parts))
    elif lang == 'js':
        print(to_js(parts))
    elif lang == 'php':
        print(to_php(parts))
    elif lang == 'go':
        print(to_go(parts))
    elif lang == 'rust':
        print(to_rust(parts))
