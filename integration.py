import os

print("hello go-echarts!")

SNAPSHOT_FOLDER = "./snapshot"
GENERATED_FOLDER = "./html"
HTML_SUFFIX = ".html"
SNAPSHOT_HTML = {}
GENERATED_HTML = {}

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

FAILED_RESULT = []
for file, path in SNAPSHOT_HTML.items():
    # with open(path, 'r') as snapshot:
    #     snapshot_content = snapshot.read()

    generated_html_path = GENERATED_HTML[file]
    with open(generated_html_path, 'r') as generated:
        generated_content = generated.read()

    print(f"current compare files: ${file}")
    if len(generated_content) != 0:
        print(f"current compare files: ${file} is same! pass")
    else:
        print(f"current compare files: ${file} is different! failed")
        # print(f"snapshot file content: ${snapshot_content}")
        print("\n")
        print(f"generated file content: ${generated_content}")
        FAILED_RESULT.append(file)

if len(FAILED_RESULT) > 0:
    print(f"Compare files failed with ${FAILED_RESULT}")
    exit(1)
