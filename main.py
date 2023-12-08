from tree_sitter import Language, Parser
import os
from node import local, nodes, read_java_files

project_folder = "../project_data/"
JAVA_LANGUAGE = Language("build/my-languages.so", "java")
java_parser = Parser()
java_parser.set_language(JAVA_LANGUAGE)
class_query_text='''
(class_declaration) @class_declaration
'''
method_query_text='''
(method_declaration) @method_declaration
'''
field_query_text='''
(field_declaration) @field_declaration
'''
import_query_text='''
(import_declaration (scoped_identifier (identifier) @1))
'''

# 关系类型
EDGE=['import','has_class','has_class_reverse','has_method','has_method_reverse','has_global_var','has_global_var_reverse']

'''
项目图
'''
GRAPH=[]

def get_name(node):
    for child in node.children:
        if child.type=='identifier':
            vname=child.text.decode('utf-8', 'ignore')
            return vname

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

def get_has_reverse(has_relation,edge):
    has_reverse_relation = []
    for rel in has_relation:
        relation = []
        relation.append(rel[2])
        relation.append(edge)
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
    for class_node, alias in class_capture:
        class_name = get_name(class_node)
        loc = local(path_name, file_name, class_name, class_node.range)
        cnode = nodes(class_name, alias, loc, class_node)
        for sup_node in class_node.children:
            if sup_node.type == 'class_body':
                for f_node in sup_node.children:
                    if f_node.type == 'field_declaration':
                        relation = []
                        floc = local(path_name, file_name, class_name, f_node.range)
                        fnode = nodes(get_name(f_node), 'field_declaration', floc, f_node)
                        relation.append(cnode)
                        relation.append(EDGE[5])
                        relation.append(fnode)
                        has_global_var_relation.append(relation)
    return has_global_var_relation

java_files=read_java_files(project_folder)


import_relation=[]
import_list=[]
# 读取Java文件内容
for java_file in java_files:
    print(java_file)
    with open(java_file, 'r', encoding='gb18030',errors='ignore') as file:
        content = file.read()
        tree=java_parser.parse(bytes(content,"utf8",))
        root_node = tree.root_node
        # print(f"Content of {java_file}:\n{content}")
        # print(root_node)
        # print("=" * 50)

        # 构建query
        class_query = JAVA_LANGUAGE.query(class_query_text)
        method_query = JAVA_LANGUAGE.query(method_query_text)
        import_query=JAVA_LANGUAGE.query(import_query_text)
        # capture: list[Node, str]
        class_capture = class_query.captures(root_node)
        method_capture=method_query.captures(root_node)

        path_name, file_name = os.path.split(java_file)
        iloc=local(path_name,file_name,'NA','NA')
        import_node=nodes(file_name,'file',iloc,'NA')
        import_capture=import_query.captures(root_node)
        import_file=[import_node,import_capture]
        import_list.append(import_file)
        # has_class关系
        has_class_relation,inner_class=get_has_class(class_capture,java_file)
        # has_class_reverse关系
        has_class_reverse_relation=get_has_reverse(has_class_relation,EDGE[2])
        # has_method关系
        has_method_relation=get_has_method(class_capture,method_capture,inner_class,java_file)
        # has_method_reverse关系
        has_method_reverse_relation=get_has_reverse(has_method_relation,EDGE[4])
        # has_global_var关系
        has_global_var_relation=get_has_global_var(class_capture, java_file)
        # has_global_var_reverse关系
        has_global_var_reverse_relation=get_has_reverse(has_method_relation,EDGE[6])

        GRAPH.append(has_class_relation)
        GRAPH.append(has_class_reverse_relation)
        GRAPH.append(has_method_relation)
        GRAPH.append(has_method_reverse_relation)
        GRAPH.append(has_global_var_relation)
        GRAPH.append(has_global_var_reverse_relation)

for java_file in java_files:
    path_name, file_name = os.path.split(java_file)
    iloc=local(path_name,file_name,'NA','NA')
    inode = nodes(file_name, 'file', iloc, 'NA')
    for import_file in import_list:
        for node, alias in import_file[1]:
            if node.text.decode('utf-8', 'ignore')==file_name:
                relation = []
                relation.append(import_file[0])
                relation.append(EDGE[0])
                relation.append(inode)
                import_relation.append(relation)

GRAPH.append(import_relation)

print(GRAPH)