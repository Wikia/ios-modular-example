import yaml
import json
from os import getcwd, path, listdir

PROJECT_YAML = 'project.yml'
PROJECT_YAML_RESOLVED = 'project-resolved.yml'

def resolve_dependencies(project, projects, dependency_graph):
    new_project = project.copy()
    targets_keys = ['targetTemplates', 'targets']
    for targets_key in targets_keys:
        if targets_key not in project.keys():
            continue
        new_targets = {}
        for target_name, target in project[targets_key].items():
            if 'dependencies' not in target:
                new_targets[target_name] = target
                continue

            new_target = target.copy()
            dependency_set = set()
            dependencies = target_dependencies(target, projects, dependency_set)
            dependencies = remove_duplicates(dependencies)
            new_target['dependencies'] = dependencies
            new_targets[target_name] = new_target

            dependency_list = list(dependency_set)
            dependency_list.sort()
            dependency_graph[target_name] = dependency_list

        new_project[targets_key] = new_targets
    return new_project


def target_dependencies(target, projects, dependency_set=None, force_embed=False,
                        include_carthage=True, include_framework=True,
                        include_sdk=True, include_static=True):

    if 'dependencies' not in target:
        return []

    new_dependencies = []
    recursive_carthage_dependencies = False or force_embed
    recursive_framework_dependencies = False or force_embed
    if target['type'] == 'framework':
        for direct_dependency in target['dependencies']:
            dep = dependency(direct_dependency, embed=(False or force_embed),
                             include_carthage=include_carthage, include_framework=include_framework,
                             include_sdk=include_sdk, include_static=include_static)
            new_dependencies.append(dep) if dep is not None else None
    elif target['type'] == 'bundle.unit-test':
        force_embed = True
        for direct_dependency in target['dependencies']:
            dep = dependency(direct_dependency, embed=True,
                             include_carthage=include_carthage, include_framework=include_framework,
                             include_sdk=include_sdk, include_static=include_static)
            new_dependencies.append(dep) if dep is not None else None
        recursive_carthage_dependencies = True
        recursive_framework_dependencies = True
    elif target['type'] == 'bundle.ui-testing':
        force_embed = True
        for direct_dependency in target['dependencies']:
            dep = dependency(direct_dependency, embed=True,
                             include_carthage=include_carthage, include_framework=include_framework,
                             include_sdk=include_sdk, include_static=include_static)
            new_dependencies.append(dep) if dep is not None else None
            recursive_carthage_dependencies = True
            recursive_framework_dependencies = True
    elif target['type'] == 'application':
        force_embed = True
        for direct_dependency in target['dependencies']:
            dep = dependency(direct_dependency, embed=True,
                             include_carthage=include_carthage, include_framework=include_framework,
                             include_sdk=include_sdk, include_static=include_static)
            new_dependencies.append(dep) if dep is not None else None
        recursive_carthage_dependencies = True
        recursive_framework_dependencies = True

    framework_dependencies = [d['framework'] for d in target['dependencies'] if 'framework' in d.keys()]
    framework_dependencies = [d.replace('.framework', '') for d in framework_dependencies]

    if dependency_set is not None:
        dependency_set.update(set(framework_dependencies))

    for framework_dependency in framework_dependencies:
        for project in projects.values():
            for dep_target_name, dep_target in project['targets'].items():
                if dep_target_name != framework_dependency:
                    continue

                extended_deps = target_dependencies(dep_target, projects,
                                                    force_embed=force_embed,
                                                    include_carthage=recursive_carthage_dependencies,
                                                    include_framework=recursive_framework_dependencies,
                                                    include_sdk=False, include_static=False)
                new_dependencies.extend(extended_deps)

    return new_dependencies


def remove_duplicates(dependencies):
    framework_dependencies = [d for d in dependencies if 'framework' in d.keys()]
    framework_dependencies = {v['framework']: v for v in framework_dependencies}.values()

    carthage_dependencies = [d for d in dependencies if 'carthage' in d.keys()]
    carthage_dependencies = {v['carthage']: v for v in carthage_dependencies}.values()

    sdk_dependencies = [d for d in dependencies if 'sdk' in d.keys()]
    sdk_dependencies = {v['sdk']: v for v in sdk_dependencies}.values()

    targ_dependencies = [d for d in dependencies if 'target' in d.keys()]
    targ_dependencies = {v['target']: v for v in targ_dependencies}.values()
    return list(framework_dependencies) + list(carthage_dependencies) + list(sdk_dependencies) + list(targ_dependencies)


def dependency(direct_dependency, embed,
               include_carthage=True, include_framework=True,
               include_sdk=True, include_static=True):
    key = list(direct_dependency.keys())[0]
    dependency_name = direct_dependency[key]
    if key == 'framework' and include_framework:
        return {'framework': dependency_name, 'implicit': True, 'embed': embed}
    elif key == 'carthage' and include_carthage:
        return {'carthage': dependency_name, 'embed': embed}
    elif key == 'sdk' and include_sdk:
        return {'sdk': dependency_name}
    elif key == 'staticFramework' and include_static:
        return {'framework': dependency_name, 'embed': False}
    elif key == 'target':
        return {'target': dependency_name}
    else:
        return None

def save_dependency_graph_to_json(dependency_graph):
    json_content = json.dumps(dependency_graph, sort_keys=True, indent=4, separators=(',', ': '))
    with open('dependency_graph.json', 'w') as file:
        file.write(json_content)
    print('Saved current dependency graph to dependency_graph.json')

def main():
    print('Resolving dependencies')
    root_dir = getcwd()

    project_directories = [path.join(root_dir, f)
        for f in listdir(root_dir) if path.isdir(path.join(root_dir, f))]

    print(project_directories)

    projects = {}
    project_dir_mapping = {}

    for directory in project_directories:
        project_path = path.join(directory, PROJECT_YAML)
        if not path.isfile(project_path):
            continue

        with open(project_path) as file:
            project = yaml.full_load(file)
            projects[project['name']] = project
            project_dir_mapping[project['name']] = directory

    dependency_graph = {}
    for project_name, project in projects.items():
        new_project = resolve_dependencies(project, projects, dependency_graph)
        project_path = path.join(project_dir_mapping[project_name], PROJECT_YAML_RESOLVED)
        with open(project_path, 'w') as file:
            yaml.dump(new_project, file)

    print('Finished resolving dependencies')
    save_dependency_graph_to_json(dependency_graph)

if __name__ == '__main__':
    main()
