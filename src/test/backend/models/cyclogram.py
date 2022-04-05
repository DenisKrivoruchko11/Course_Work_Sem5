import os
import unittest
from json import JSONDecodeError

import portion

from src.main.backend.models.cyclogram import Cyclogram, cyclogram_from_file


class TestCyclogram(unittest.TestCase):
    def test_constructor_with_equal_values_in_set_should_throws_attribute_error(self):
        self.assertRaises(AttributeError, lambda: Cyclogram('Name', ['a', 'a'], ['b'], -10, 1,
                                                            [[portion.empty()], [portion.empty()]]))

    def test_constructor_with_equal_start_time_and_end_time_should_throws_attribute_error(self):
        self.assertRaises(AttributeError, lambda: Cyclogram('Name', ['a', 'b'], ['a'], -1, -1,
                                                            [[portion.empty()], [portion.empty()]]))

    def test_constructor_with_incorrect_rows_number_should_throws_attribute_error(self):
        self.assertRaises(AttributeError, lambda: Cyclogram('Name', ['a', 'b'], ['a'], -1, 15,
                                                            [[portion.empty()]]))

    def test_constructor_with_incorrect_columns_number_should_throws_attribute_error(self):
        self.assertRaises(AttributeError, lambda: Cyclogram('Name', ['a', 'b'], ['a'], -1, 15,
                                                            [[portion.empty()], [portion.empty(), portion.empty()]]))

    def test_constructor_with_correct_data_should_works_correctly(self):
        cyclogram = Cyclogram('Name', ['A', 'B'], ['a', 'b'], 1, 10,
                              [[portion.open(1, 5), portion.closedopen(3, 7) | portion.closed(7, 7)],
                               [portion.empty(), portion.closedopen(1, 12)]])
        expected = {'name': 'Name', 'set1_elements': ['A', 'B'], 'set2_elements': ['a', 'b'], 'start_time': 1,
                    'end_time': 10, 'intervals': [[portion.open(1, 5), portion.closed(3, 7)],
                                                  [portion.empty(), portion.closed(1, 10)]]}
        self.assertDictEqual(expected, cyclogram.__dict__)

    def test_save_to_file_with_not_existing_file_should_create_file(self):
        path = 'data/test_save_to_file_with_not_existing_file.json'
        cyclogram = Cyclogram('Name1', ['A', 'B'], ['a', 'b'], 1, 10,
                              [[portion.closed(2, 9), portion.closedopen(3, 7)],
                               [portion.empty(), portion.closedopen(1, 12)]])

        cyclogram.save_to_file(path)

        self.assertDictEqual(cyclogram.__dict__, cyclogram_from_file(path).__dict__)

        os.remove(path)

    def test_save_to_file_with_existing_file_should_rewrite_file(self):
        path = 'data/test_save_to_file_with_existing_file.json'
        cyclogram = Cyclogram('Name1', ['A', 'B'], ['a', 'b'], 1, 10,
                              [[portion.closed(2, 9), portion.closedopen(3, 7)],
                               [portion.empty(), portion.closedopen(1, 12)]])

        cyclogram.save_to_file(path)

        self.assertDictEqual(cyclogram.__dict__, cyclogram_from_file(path).__dict__)

        open(path, 'w').close()

    def test_cyclogram_from_file_with_not_existing_file_should_throws_file_not_found_error(self):
        path = 'data/test_cyclogram_from_file_with_not_existing_file.json'

        self.assertRaises(FileNotFoundError, lambda: cyclogram_from_file(path))

    def test_cyclogram_from_file_with_not_json_file_should_throws_json_decode_error(self):
        path = 'data/test_cyclogram_from_file_with_not_json_file.txt'

        self.assertRaises(JSONDecodeError, lambda: cyclogram_from_file(path))

    def test_cyclogram_from_file_with_incorrect_json_file_should_throws_json_decode_error(self):
        path = 'data/test_cyclogram_from_file_with_incorrect_json_file.json'

        self.assertRaises(JSONDecodeError, lambda: cyclogram_from_file(path))

    def test_cyclogram_from_file_without_name_field_should_throws_key_error(self):
        path = 'data/test_cyclogram_from_file_without_name_field.json'

        self.assertRaises(KeyError, lambda: cyclogram_from_file(path))

    def test_cyclogram_from_file_with_incorrect_type_of_start_time_should_throws_type_error(self):
        path = 'data/test_cyclogram_from_file_with_incorrect_type_of_start_time.json'

        self.assertRaises(TypeError, lambda: cyclogram_from_file(path))

    def test_cyclogram_from_file_with_incorrect_type_of_set_should_throws_type_error(self):
        path = 'data/test_cyclogram_from_file_with_incorrect_type_of_set.json'

        self.assertRaises(TypeError, lambda: cyclogram_from_file(path))

    def test_cyclogram_from_file_with_incorrect_type_of_interval_bound_should_throws_value_error(self):
        path = 'data/test_cyclogram_from_file_with_incorrect_type_of_interval_bound.json'

        self.assertRaises(ValueError, lambda: cyclogram_from_file(path))

    def test_cyclogram_from_file_with_incorrect_type_of_interval_value_should_throws_type_error(self):
        path = 'data/test_cyclogram_from_file_with_incorrect_type_of_interval_value.json'

        self.assertRaises(TypeError, lambda: cyclogram_from_file(path))

    def test_cyclogram_from_file_with_file_without_extension_should_works_correctly(self):
        path = 'data/test_cyclogram_from_file_with_file_without_extension'
        cyclogram = Cyclogram('Name1', ['A', 'B'], ['a', 'b'], 1, 10,
                              [[portion.closed(2, 9), portion.closedopen(3, 7)],
                               [portion.empty(), portion.closedopen(1, 12)]])

        self.assertDictEqual(cyclogram.__dict__, cyclogram_from_file(path).__dict__)

    def test_cyclogram_from_file_with_correct_file_should_works_correctly(self):
        path = 'data/test_cyclogram_from_file_with_correct_file.json'
        cyclogram = Cyclogram('Name1', ['A', 'B'], ['a', 'b'], 1, 10,
                              [[portion.closed(2, 9), portion.closedopen(3, 7)],
                               [portion.empty(), portion.closedopen(1, 12)]])

        self.assertDictEqual(cyclogram.__dict__, cyclogram_from_file(path).__dict__)
