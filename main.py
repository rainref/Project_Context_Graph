from tree_sitter import Language, Parser

import os

def find_java_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                print(os.path.join(root, file))

# 替换成你的项目文件夹路径
project_folder = '/path/to/your/project/folder'
find_java_files(project_folder)


JAVA_LANGUAGE = Language("build/my-languages.so", "java")
parser = Parser()
parser.set_language(JAVA_LANGUAGE)

tree = parser.parse(
    bytes(
        """
""",
        "utf8",
    )
)

root_node = tree.root_node
print(root_node)