import os
import ast
import pkg_resources

def find_py_files(directory):
    py_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files

def extract_imports(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=file_path)
    
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                if n.name:
                    imports.add(n.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
    return imports

def map_modules_to_packages(modules):
    distribution_map = {dist.key: dist for dist in pkg_resources.working_set}
    packages = set()
    for module in modules:
        for dist in distribution_map.values():
            if module in dist._get_metadata('top_level.txt'):
                packages.add(dist.key)
    return packages

def main():
    current_directory = os.getcwd()
    py_files = find_py_files(current_directory)
    
    all_imports = set()
    for py_file in py_files:
        file_imports = extract_imports(py_file)
        all_imports.update(file_imports)
    
    packages = map_modules_to_packages(all_imports)
    
    print("Dependencies found:")
    for package in sorted(packages):
        print(package)

if __name__ == "__main__":
    main()
