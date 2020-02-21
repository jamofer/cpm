import unittest

from cpm.domain import project_schema


class TestProjectSchema(unittest.TestCase):
    def test_project_descriptor_is_invalid_if_empty(self):
        project_description = {}

        assert not project_schema.is_valid(project_description)

    def test_validate_project_descriptor_with_just_the_name(self):
        project_description = {
            'project_name': 'project'
        }

        assert project_schema.is_valid(project_description)

    def test_project_descriptor_is_invalid_if_name_is_not_string(self):
        project_description = {
            'project_name': 12
        }

        assert not project_schema.is_valid(project_description)
