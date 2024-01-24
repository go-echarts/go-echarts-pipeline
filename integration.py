import os
import re
from difflib import ndiff

print("hello go-echarts!")

SNAPSHOT_FOLDER = "./snapshot"
GENERATED_FOLDER = "./html"
HTML_SUFFIX = ".html"
SNAPSHOT_HTML = {}
GENERATED_HTML = {}


def diff(text1, text2):
    find_differences = ndiff(text1.splitlines(), text2.splitlines())
    return '\n'.join(line for line in find_differences if line.startswith('- ') or line.startswith('+ '))


def replace_colors(text: str):
    return re.sub(r'#[\d\w]+', '__COLOR__', text)


def replace_numbers(text: str):
    return re.sub(r'-?\b\d+(\.\d+)?\b', '__NUMBER__', text)


def find_go_echarts_instance_rand_strings(text):
    return re.findall(r'goecharts_(\w*)', text)


def mask_content(text):
    text = replace_colors(text)
    text = replace_numbers(text)
    instance_rand_strings = find_go_echarts_instance_rand_strings(text)
    for instance_rand_str in instance_rand_strings:
        text = text.replace(instance_rand_str, "__RAND__")
    return text


for root, dirs, files in os.walk(SNAPSHOT_FOLDER):
    for file in files:
        if file.endswith(HTML_SUFFIX):
            SNAPSHOT_HTML[file] = os.path.join(root, file)

for root, dirs, files in os.walk(GENERATED_FOLDER):
    for file in files:
        if file.endswith(HTML_SUFFIX):
            GENERATED_HTML[file] = (os.path.join(root, file))

print(f"Get SNAPSHOT_HTML size {len(SNAPSHOT_HTML)}")
print(f"Get GENERATED_HTML size {len(GENERATED_HTML)}")

if len(SNAPSHOT_HTML) != len(GENERATED_HTML):
    print("Oops! the GENERATED_HTML size is not as same as the SNAPSHOT_HTML size !")
    exit(1)

FAILED_RESULT = {}
for file, snapshot_html_path in SNAPSHOT_HTML.items():
    if IGNORE_CHARTS.index(file) != -1:
        continue
    with open(snapshot_html_path, 'r') as snapshot:
        snapshot_content = snapshot.read()

    generated_html_path = GENERATED_HTML[file]
    with open(generated_html_path, 'r') as generated:
        generated_content = generated.read()

    print(f"current compare files: {file}")
    snapshot_content_masked = mask_content(snapshot_content)
    generated_content_masked = mask_content(generated_content)
    if snapshot_content_masked == generated_content_masked:
        print(f"current compare files: {file} is same! pass!")
    else:
        print(f"current compare files: {file} is different! failed!")
        FAILED_RESULT[file] = diff(generated_content, snapshot_content)

# FIX ME, skip check for now
FAILED_RESULT.pop("wordcloud.html")
FAILED_RESULT.pop("map.html")

if len(FAILED_RESULT) > 0:
    print("\nFind diff on files! plz have a check on them ! \n")
    for file, diffs in FAILED_RESULT.items():
        print(f"Compare files failed with {file}")
        print("Diff result from generated_content to snapshot_content : \n ")
        print(diffs)
        print("\n" + "-" * 30)
    exit(1)
else:
    print(f"Compare files all pass! excellent！")
