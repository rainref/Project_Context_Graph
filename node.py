from tree_sitter import Language, Parser
import os

def read_java_files(folder_path):
    java_files = []
    # 遍历文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))
    return java_files


class nodes:
    def __init__(self,name,type,local,node):
        self.name = name
        self.type = type
        self.local = local
        self.node = node


class local:
    def __init__(self,folder,file_name,class_name,code_range):
        self.folder = folder
        self.file_name = file_name
        self.class_name = class_name
        self.code_range=code_range


if __name__ == '__main__':
    project_folder = "../project_data/"

    JAVA_LANGUAGE = Language("build/my-languages.so", "java")
    java_parser = Parser()
    java_parser.set_language(JAVA_LANGUAGE)
    import_query_text='''
    (import_declaration (scoped_identifier (identifier) @1))
    '''

    java_files=read_java_files(project_folder)
    for java_file in java_files:
        with open(java_file, 'r', encoding='utf-8') as file:
            content = file.read()
            tree=java_parser.parse(bytes(content,"utf8",))
            root_node = tree.root_node
            import_query = JAVA_LANGUAGE.query(import_query_text)
            import_capture = import_query.captures(root_node)
            print(import_capture)

