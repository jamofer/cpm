import argparse

from cpm.api.result import Result
from cpm.api.result import OK
from cpm.api.result import FAIL
from cpm.domain.project_loader import ProjectLoader
from cpm.domain.test_service import TestService
from cpm.domain.compilation_recipes.test_recipe import TestRecipe
from cpm.domain.compilation_recipes.test_recipe import TestsFailed
from cpm.domain.compilation_recipes import CompilationError
from cpm.domain.project_loader import NotAChromosProject
from cpm.domain.test_service import NoTestsFound
from cpm.infrastructure.filesystem import Filesystem
from cpm.infrastructure.yaml_handler import YamlHandler


def run_tests(test_service, recipe, patterns=[]):
    try:
        test_service.run_tests(recipe, patterns)
    except NotAChromosProject:
        return Result(FAIL, 'not a Chromos project')
    except CompilationError as e:
        return Result(FAIL, f'{str(e)}')
    except TestsFailed:
        return Result(FAIL, '✖ FAIL')
    except NoTestsFound:
        return Result(OK, 'no tests to run')

    return Result(OK, '✔ PASS')


def execute(argv):
    add_target_parser = argparse.ArgumentParser(prog='cpm test', description='Chromos Package Manager', add_help=False)
    add_target_parser.add_argument('patterns', nargs=argparse.REMAINDER)
    args = add_target_parser.parse_args(argv)

    filesystem = Filesystem()
    yaml_handler = YamlHandler(filesystem)
    loader = ProjectLoader(yaml_handler, filesystem)
    service = TestService(loader)
    recipe = TestRecipe(filesystem)

    result = run_tests(service, recipe, args.patterns)

    return result
