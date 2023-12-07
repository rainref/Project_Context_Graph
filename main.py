from tree_sitter import Language, Parser
import os
from node import local, nodes

project_folder = "../project_data/"

JAVA_LANGUAGE = Language("build/my-languages.so", "java")
java_parser = Parser()
java_parser.set_language(JAVA_LANGUAGE)
java_query_text = '''
(package_declaration) @package_declaration
(import_declaration) @import_declaration

'''
class_query_text='''
(class_declaration) @class_declaration
'''
method_query_text='''
(method_declaration) @method_declaration
'''
field_query_text='''
(field_declaration) @field_declaration
'''
# 关系类型
EDGE=['import','han_class','has_class_reverse','has_method','has_method_reverse','has_global_var','has_global_var_reverse']
'''
一个项目总的节点列表
'''
NODELIST=[]
'''
项目图
'''
GRAPH=[]
def read_java_files(folder_path):
    java_files = []
    # 遍历文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))
    return java_files
def get_name(node):
    for child in node.children:
        if child.type=='identifier':
            name=child.text.decode('utf-8', 'ignore')
    return name

def get_has_class(class_capture,java_file):
    has_class_relation=[]
    path_name, file_name = os.path.split(java_file)
    loc=local(path_name,file_name,'NA','NA')
    node_file = nodes(file_name,'file',loc,'NA')
    class_name=''
    inner_class=False
    if len(class_capture)!=1:
        inner_class=True
    for node, alias in class_capture:
        relation=[]
        for child in node.children:
            if child.type=='identifier':
                class_name=child.text.decode('utf-8', 'ignore')
        loca=local(path_name,file_name,class_name,node.range)
        node_class=nodes(class_name,alias,loca,node)
        relation.append(node_file)
        relation.append(EDGE[1])
        relation.append(node_class)
        has_class_relation.append(relation)
    return has_class_relation,inner_class

def get_has_reverse(has_relation):
    has_reverse_relation = []
    for rel in has_relation:
        relation = []
        relation.append(rel[2])
        relation.append(EDGE[2])
        relation.append(rel[0])
        has_reverse_relation.append(relation)
    return has_reverse_relation

def get_has_method(class_capture,method_capture,inner_class,java_file):
    has_method_relation = []
    path_name, file_name = os.path.split(java_file)
    if inner_class is False:
        class_node,alias=class_capture[0]
        class_name=get_name(class_node)
        loc = local(path_name, file_name, class_name,class_node.range)
        cnode = nodes(class_name, alias, loc, class_node)
        for method_node, aliasm in method_capture:
            relation = []
            mloc = local(path_name, file_name, class_name, method_node.range)
            mnode=nodes(get_name(method_node),aliasm,mloc,method_node)
            relation.append(cnode)
            relation.append(EDGE[3])
            relation.append(mnode)
            has_method_relation.append(relation)
        return has_method_relation
    else:
        for class_node, alias in class_capture:
            class_name = get_name(class_node)
            loc = local(path_name, file_name, class_name,class_node.range)
            cnode = nodes(class_name, alias, loc, class_node)
            for sup_node in class_node.children:
                if sup_node.type == 'class_body':
                    for m_node in sup_node.children:
                        if m_node.type == 'method_declaration':
                            relation = []
                            mloc = local(path_name, file_name, class_name, m_node.range)
                            mnode = nodes(get_name(m_node), 'method_declaration', mloc, m_node)
                            relation.append(cnode)
                            relation.append(EDGE[3])
                            relation.append(mnode)
                            has_method_relation.append(relation)
        return has_method_relation

def get_has_global_var(class_capture,java_file):
    has_global_var_relation = []
    path_name, file_name = os.path.split(java_file)


java_files=read_java_files(project_folder)

# 读取Java文件内容
for java_file in java_files:
    with open(java_file, 'r', encoding='utf-8') as file:
        content = file.read()
        tree=java_parser.parse(bytes(content,"utf8",))
        root_node = tree.root_node
        print(f"Content of {java_file}:\n{content}")
        # print(root_node)
        # print("=" * 50)

        # 构建query
        class_query = JAVA_LANGUAGE.query(class_query_text)
        method_query = JAVA_LANGUAGE.query(method_query_text)
        field_query=JAVA_LANGUAGE.query(field_query_text)
        # capture: list[Node, str]
        class_capture = class_query.captures(root_node)
        method_capture=method_query.captures(root_node)

        # has_class关系
        has_class_relation,inner_class=get_has_class(class_capture,java_file)
        # has_class_reverse关系
        has_class_reverse_relation=get_has_reverse(has_class_relation)
        # has_method关系
        has_method_relation=get_has_method(class_capture,method_capture,inner_class,java_file)
        # has_method_reverse关系
        has_method_reverse_relation=get_has_reverse(has_method_relation)


