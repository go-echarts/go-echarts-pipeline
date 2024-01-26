import json
import os
import re
from difflib import ndiff

print("hello go-echarts!")

SNAPSHOT_FOLDER = "./snapshot"
GENERATED_FOLDER = "./html"
HTML_SUFFIX = ".html"
SNAPSHOT_HTML = {}
GENERATED_HTML = {}
FUNCTION_PATTERN = r'function\s*\([^)]*\)\s*\{.*?\}'

COLOR_MASK = '__COLOR__'
NUMBER_MASK = '123456789'
CHART_ID_MASK = '__RAND__'
FUNCTION_MASK = '9999999999'

MASK_LIST = [COLOR_MASK, NUMBER_MASK, CHART_ID_MASK, FUNCTION_MASK]

# FIXME: need find a way to mask treemap function contents
IGNORE_CHARTS = ["treemap.html"]


def compare(snapshot_opt: any, generated_opt: any) -> bool:
    """
    Return where current snapshot_opt and generated_opt is same or not.
    Skip replace numbers, simply check mask contents
    Allow to have same keys in dict without same sort
    :param snapshot_opt:
    :param generated_opt:
    :return: same or not
    """
    if snapshot_opt is None and generated_opt is None:
        return True

    if isinstance(snapshot_opt, int):
        return isinstance(generated_opt, int)

    if isinstance(snapshot_opt, str):
        if is_masked_content(snapshot_opt):
            return is_masked_content(generated_opt)
        else:
            return snapshot_opt == generated_opt

    if isinstance(snapshot_opt, list):
        if not isinstance(generated_opt, list):
            return False
        if len(snapshot_opt) != len(generated_opt):
            return False
        if all(x == snapshot_opt[0] for x in snapshot_opt) and all(x == generated_opt[0] for x in generated_opt):
            return compare(snapshot_opt[0], generated_opt[0])
        for i, value in enumerate(snapshot_opt):
            same = compare(value, generated_opt[i])
            if not same:
                return False
        return True

    if isinstance(snapshot_opt, dict):
        if not isinstance(generated_opt, dict):
            return False
        if len(snapshot_opt.keys()) != len(generated_opt.keys()):
            return False
        for key, val in snapshot_opt.items():
            if not generated_opt.__contains__(key):
                return False
            same = compare(val, generated_opt.get(key))
            if not same:
                return False
        return True


def diff(text1: str, text2: str) -> str:
    """
    Show diff contents like git diff between options
    :param text1:
    :param text2:
    :return: diff contents
    """
    find_differences = ndiff(text1.splitlines(), text2.splitlines())
    return '\n'.join(line for line in find_differences if line.startswith('- ') or line.startswith('+ '))


def is_masked_content(text: str) -> bool:
    return text in MASK_LIST


def mask_functions(text: str) -> str:
    return re.sub(FUNCTION_PATTERN, FUNCTION_MASK, text)


def mask_colors(text: str) -> str:
    return re.sub(r'#[\d\w]+', COLOR_MASK, text)


def mask_numbers(text: str) -> str:
    content = re.sub(r'-?\b\d+(\.\d+)?\b', NUMBER_MASK, text)
    # replace inf
    return re.sub(r'\binf\b', NUMBER_MASK, content)


def find_go_echarts_instance_rand_strings(text) -> list:
    return re.findall(r'goecharts_(\w*)', text)


def find_all_go_echarts_instance_options(text: str) -> list:
    return re.findall(r'option_' + CHART_ID_MASK + '\s*=\s*(.*)', text)


def mask_content(text: str) -> str:
    text = mask_colors(text)
    text = mask_numbers(text)
    instance_rand_strings = find_go_echarts_instance_rand_strings(text)
    # mask rand chartID
    for instance_rand_str in instance_rand_strings:
        text = text.replace(instance_rand_str, CHART_ID_MASK)
    return mask_functions(text)


# solve float and inf on json
def parse_float(value):
    try:
        return NUMBER_MASK
    except ValueError:
        return NUMBER_MASK


def show_result(result: dict):
    if len(result) > 0:
        print("\nFind diff on files! plz have a check on them ! \n")
        for f, diffs in result.items():
            print(f"Compare files failed with {f}")
            print("Find different options from generated_content to snapshot_content : \n ")
            for d in diffs:
                print(d)
                print("\n")
            print("-" * 30)
        exit(1)
    else:
        print(f"Compare files all pass! excellent！")


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

"""
FAILED_RESULT = {"file": [ diff1, diff2]}
i.e.
FAILED_RESULT = {
   "bar.html": [
       " + color123 ...
         - color ...
       "
       
   ]
}
"""
FAILED_RESULT = {}

for file, snapshot_html_path in SNAPSHOT_HTML.items():
    if file in IGNORE_CHARTS:
        continue
    with open(snapshot_html_path, 'r') as snapshot:
        snapshot_content = snapshot.read()

    generated_html_path = GENERATED_HTML[file]
    with open(generated_html_path, 'r') as generated:
        generated_content = generated.read()

    print(f"current compare files: {file}")

    snapshot_content_masked = mask_content(snapshot_content)
    generated_content_masked = mask_content(generated_content)
    snapshot_charts_options = find_all_go_echarts_instance_options(snapshot_content_masked)
    generated_charts_options = find_all_go_echarts_instance_options(generated_content_masked)

    diff_list = []
    if len(snapshot_charts_options) != len(generated_charts_options):
        print(f"current compare files: {file} is different! failed!")
        FAILED_RESULT[file] = "The instances size in each html is not same"
    else:
        for index, snapshot_charts_option in enumerate(snapshot_charts_options):
            generated_charts_option = generated_charts_options[index]
            snapshot_charts_option_json = json.loads(snapshot_charts_option, parse_float=parse_float)
            generated_charts_option_json = json.loads(generated_charts_option, parse_float=parse_float)
            match = compare(snapshot_charts_option_json, generated_charts_option_json)
            if not match:
                diff_list.append(diff(snapshot_charts_option, generated_charts_option))
    if not diff_list:
        print(f"current compare files: {file} is same! pass!")
    else:
        FAILED_RESULT[file] = diff_list
        print(f"current compare files: {file} is different! failed!")

show_result(FAILED_RESULT)
