#!/usr/bin/env python
import os
import json
import yaml
import argparse
import shutil
import sys
from subprocess import check_call, check_output

TESTS_PROJECT_PATH = 'Tests/project.yml'
TESTS_RESOLVED_PROJECT_PATH = 'Tests/project-resolved.yml'
UNIT_TESTS = 'UnitTests'
EMPTY_TESTS = 'EmptyTests'

def get_changed_projects(base_branch):
    current_branch = check_output('git rev-parse --abbrev-ref HEAD', shell=True).strip()
    changed_files = check_output('git diff {branch} origin/{base_branch} --name-status'.format(branch=current_branch, base_branch=base_branch), shell=True)

    changed_projects = set()
    for changed_file_description in changed_files.strip().split(os.linesep):
        if len(changed_file_description.split()) < 2:
            continue

        changed_file = changed_file_description.split()[1]
        path_elements = changed_file.split('/')
        changed_projects.add(path_elements[0])

    return changed_projects


def filter_targets(schemes, scheme_name, dependency_graph, changed_projects):
    scheme = schemes[scheme_name]
    build_targets = scheme['build']['targets']
    test_targets = scheme['test']['targets']
    keys = build_targets.keys()
    for target in keys:
        project_name = target.split('/')[0]
        full_target_name = target.split(':')[0]
        target_name = full_target_name.split('/')[1]

        project_dependency_set = set(dependency_graph[project_name])
        project_modified = project_name in changed_projects or\
                           len(project_dependency_set.intersection(changed_projects)) > 0

        test_target_dependency_set = set(dependency_graph[target_name])
        test_target_modified = len(test_target_dependency_set.intersection(changed_projects)) > 0

        if not (project_modified or test_target_modified):
            build_targets.pop(target, None)
            test_targets.remove(full_target_name)
        else:
            print('Enabled {target} as it could be affected by recent changes'
                  .format(target=full_target_name))

        if not build_targets:
            print('No build targets for {scheme_name}. Stubbing with empty tests'
                  .format(scheme_name=scheme_name))
            stub_target_name = EMPTY_TESTS
            build_targets[stub_target_name] = ['test', 'run']
            test_targets.append(stub_target_name)
            schemes[scheme_name] = empty_tests_scheme()


def parse_arguments():
    arg_parser = argparse.ArgumentParser(add_help=True)
    arg_parser.add_argument('-a',
                            '--all',
                            help='Run all tests',
                            required=False,
                            action="store_true")
    arg_parser.add_argument('-b',
                            '--base_branch',
                            help='Base branch to compare. By default `master`',
                            default='master')
    arguments = arg_parser.parse_args()
    args_dict = vars(arguments)
    return args_dict


def scheme_contains_empty_tests(scheme):
    return EMPTY_TESTS in scheme['test']['targets']


def empty_tests_scheme():
    return {
        'test': {
            'config': 'Debug',
            'targets': [EMPTY_TESTS]
        },
        'build': {
            'targets': {
                EMPTY_TESTS: ['test', 'run']
            }
        }
    }


def empty_tests_target():
    return {
        EMPTY_TESTS: {
            'type': 'bundle.unit-test',
            'platform': 'iOS',
            'sources': [EMPTY_TESTS]
        }
    }


def main():
    args = parse_arguments()
    if args['all']:
        print('Enabling all tests')
        shutil.copy(TESTS_PROJECT_PATH, TESTS_RESOLVED_PROJECT_PATH)
        check_call(['xcodegen', '-s', 'project-resolved.yml'], cwd=os.path.join(os.getcwd(), 'Tests'))
        sys.exit(0)

    changed_projects = get_changed_projects(args['base_branch'])
    if not changed_projects:
        print("No source code changed. Generating project with empty test.")
        check_call(['xcodegen', '-s', 'project-empty.yml'], cwd=os.path.join(os.getcwd(), 'Tests'))
        return

    with open("dependency_graph.json") as file:
        dependency_graph = json.load(file)

    with open(TESTS_PROJECT_PATH) as file:
        project = yaml.full_load(file)

    schemes = project['schemes']
    filter_targets(schemes, UNIT_TESTS, dependency_graph, changed_projects)

    if scheme_contains_empty_tests(schemes[UNIT_TESTS]):
        project['targets'] = empty_tests_target()

    with open(TESTS_RESOLVED_PROJECT_PATH, 'w') as file:
        yaml.dump(project, file)

    check_call(['xcodegen', '-s', 'project-resolved.yml'], cwd=os.path.join(os.getcwd(), 'Tests'))


if __name__ == '__main__':
    main()
