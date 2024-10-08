# Project_Context_Graph
根据项目构建一个图
## 需求
对于给定的Java项目构建项目上下文图：

项目上下文图包括：项目实体和项目关系

项目实体是构成软件项目骨架的代码组件，

主要关注四类实体：文件、类、函数和全局变量。

其中：
+ 文件包含文件名和文件说明；
+ 类包含类名、类签名和类说明；
+ 函数包含函数名、函数签名和函数说明；
+ 全局变量包含变量名和值。

注意：文件名、类方法全局变量都包含locale,Locale表示实体在软件项目中的相对代码位置。

例如，类实体的Locale被定义为“文件夹.文件名.类名”。
实体关系表示项目实体之间的交互作用，考虑两类关系：文件内关系和文件间关系。

文件内关系描述了文件内的代码层次结构，由编程语
言的语法定义。例如，一个类位于层次结构的第一级，而其函数位于第二级。 文件间关系定义了文件间的依赖关系。

具体实体关系包括：  
1. 文件-文件(import);  
2. 文件-类：has_class;
3. 类-文件(has_class_reverse); 
4. 类-方法(has_method); 
5. 方法-类(has_method_reverse);
6. 类-全局变量(has_global_var); 
7. 全局变量-类(has_global_var_reverse)

## 关系形式
<初始节点，边类型，结束节点>

## 目标
根据项目构架一个图，相当于数据库

提供一个工具，功能是根据给定的一个文件的其中的一的方法从图中检索到他的上下文

## 使用
```python
from tree_sitter import Language, Parser
project_folder = "../project_data/"
JAVA_LANGUAGE = Language("build/my-languages.so", "java")
java_parser = Parser()
java_parser.set_language(JAVA_LANGUAGE)
```
project_folder中填入项目根目录所在位置即可
