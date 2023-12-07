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


