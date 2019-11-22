import unittest
import pandas as pd  # type: ignore
import sys
sys.path.append('../src')
import yaml_parsing as yp  # type: ignore
import checksuites as cs  # type: ignore


class TestYamlParsing(unittest.TestCase):

    def setUp(self):
        self.df_file1 = pd.read_csv('data/file1.csv')

    def test_load_raw_yaml(self):
        self.assertRaises(FileNotFoundError,
                          yp.load_yaml_file_to_dict, 'xxxx')
        self.assertRaises(yp.YamlParsingError,
                          yp.load_yaml_file_to_dict, 'yamls/file2.yaml')
        result = yp.load_yaml_file_to_dict('yamls/file1.yaml')
        self.assertTrue(isinstance(result, dict))

    def test_apply_yamldict_to_checksuite_keyerrors(self):
        checksuite = cs.PandasDatsetCheckSuite(self.df_file1)
        ymld = yp.load_yaml_file_to_dict('yamls/file3.yaml')
        self.assertTrue(isinstance(ymld, dict))
        self.assertRaises(yp.YamlParsingError,
                          yp.apply_yamldict_to_checksuite,
                          ymld,
                          checksuite)
        ymld = yp.load_yaml_file_to_dict('yamls/file4.yaml')
        self.assertRaises(yp.YamlParsingError,
                          yp.apply_yamldict_to_checksuite,
                          ymld,
                          checksuite)
        ymld = yp.load_yaml_file_to_dict('yamls/file5.yaml')
        self.assertRaises(yp.YamlParsingError,
                          yp.apply_yamldict_to_checksuite,
                          ymld,
                          checksuite)
        # The following should not raise an error - test will
        # fail if it does
        ymld = yp.load_yaml_file_to_dict('yamls/file1.yaml')
        yp.apply_yamldict_to_checksuite(ymld, checksuite)

    def test_apply_yamldict_to_checksuite_valuechecks(self):
        checksuite = cs.PandasDatsetCheckSuite(self.df_file1)
        ymld = yp.load_yaml_file_to_dict('yamls/file1.yaml')
        yp.apply_yamldict_to_checksuite(ymld, checksuite)
        # Dataset checks
        self.assertFalse(checksuite.allow_duplicate_rows)
        self.assertTrue(checksuite.stop_on_fail)
        self.assertEqual(checksuite.min_rows, 3)


if __name__ == '__main__':
    unittest.main()
