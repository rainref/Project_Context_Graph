from tree_sitter import Language, Parser
import os

JAVA_LANGUAGE = Language("build/my-languages.so", "java")
parser = Parser()
parser.set_language(JAVA_LANGUAGE)


def read_java_files(folder_path):
    java_files = []
    # 遍历文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))
    return java_files



# 指定项目文件夹的路径
project_folder = "../EC-Myplch"
java_files=read_java_files(project_folder)

# 读取Java文件内容
for java_file in java_files:
    with open(java_file, 'r', encoding='utf-8') as file:
        content = file.read()
        tree=parser.parse(bytes(content,"utf8",))
        root_node = tree.root_node

        #print(f"Content of {java_file}:\n{content}")
        print(root_node)
        print("=" * 50)




