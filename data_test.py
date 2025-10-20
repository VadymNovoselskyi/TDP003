#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2011, IDA, LinkÃ¶ping University
# Copyright (C) 2011, TorbjÃ¶rn LÃ¶nnemark <tobbez@ryara.net>
# Copyright (C) 2014, Daniel Persson
import unittest
import data_helper as data  # import the file with your implemented functions
import hashlib
import sys
from operator import itemgetter

# ----------- HELPER FUNCTIONS -----------


def print_tech_dict(d):
    for k, v in d.items():
        print("{}: {}".format(k, v))
        for e in v:
            print(e)
        print()


def sort_dict(d, sort_key):
    for k in d.keys():
        d[k] = sorted(d[k], key=itemgetter(sort_key))
    return d


md5 = hashlib.md5


# ----------- TEST CLASS -----------


class DataTest(unittest.TestCase):
    """Subclass of the unittest.TestCase class

    Define all tests as a method of this class. Each test must start with the
    word test (ex test_load). Within each test method, various assertions
    can be made, e.g. checking that what you are testing gives the expected
    result.

    Use the method self.assertEqual() to compare an expected and observed result.

    Please refer to the unittest documentation for more information:
    https://docs.python.org/3.7/library/unittest.html

    To run the tests, have the files data_test.py, data.py and data.json in the
    same catalog. data.py is the file with your implemented API functions.
    Execute with:

    $ python3 data_test.py

    The test result is shown in the terminal.

    """

    def setUp(self):
        """The setUp() method is called before every test_*-method. Use it to
        prepare things that must always be done before a test is run, such as
        loading the data.
        """

        # The content in self.expected_data must match the content in data.json
        # for the testing to work. Do NOT change the content or the file!
        self.expected_data = [
            {
                "big_image": "XXX",
                "project_name": "python data-module test script",
                "course_name": "OK\xc4NT",
                "group_size": 2,
                "end_date": "2009-09-06",
                "techniques_used": ["python"],
                "academic_credits": "WUT?",
                "small_image": "X",
                "long_description": "no no no",
                "course_id": "TDP003",
                "project_id": 1,
                "external_link": "YY",
                "short_description": "no",
                "start_date": "2009-09-05",
                "lulz_had": "many",
            },
            {
                "big_image": "XXX",
                "project_name": "NEJ",
                "course_name": "OK\xc4NT",
                "group_size": 4,
                "end_date": "2009-09-08",
                "techniques_used": ["c++", "csv", "python"],
                "academic_credits": "WUT?",
                "small_image": "X",
                "long_description": "no no no",
                "course_id": "TDP003",
                "project_id": 3,
                "external_link": "YY",
                "short_description": "no",
                "start_date": "2009-09-07",
                "lulz_had": "few",
            },
            {
                "big_image": "XXX",
                "project_name": "2007",
                "course_name": "OK\xc4NT",
                "group_size": 6,
                "end_date": "2009-09-09",
                "techniques_used": ["ada", "python"],
                "academic_credits": "WUT?",
                "small_image": "X",
                "long_description": "no no no",
                "course_id": "TDP003",
                "project_id": 2,
                "external_link": "YY",
                "short_description": "no",
                "start_date": "2009-09-08",
                "lulz_had": "medium",
            },
            {
                "big_image": "XXX",
                "project_name": ",",
                "course_name": "HOHO",
                "group_size": 8,
                "end_date": "2009-09-07",
                "techniques_used": [],
                "academic_credits": "WUT?",
                "small_image": "X",
                "long_description": "no no no",
                "course_id": ' "',
                "project_id": 4,
                "external_link": "YY",
                "short_description": "no",
                "start_date": "2009-09-06",
                "lulz_had": "over 9000",
            },
        ]

        # Sort the expected data by project id
        self.expected_data = sorted(self.expected_data, key=itemgetter("project_id"))

        # Store the hardcoded expected results.
        # Do NOT change this part
        self.expected_technique_data = ["ada", "c++", "csv", "python"]
        self.expected_technique_stat_data = {
            "python": [
                {"id": 2, "name": "2007"},
                {"id": 3, "name": "NEJ"},
                {"id": 1, "name": "python data-module test script"},
            ],
            "csv": [{"id": 3, "name": "NEJ"}],
            "c++": [{"id": 3, "name": "NEJ"}],
            "ada": [{"id": 2, "name": "2007"}],
        }

        # Load the data using your implemented load function. The data is
        # stored as a member of the class instance, so that it can be accessed
        # in other methods of the class
        self.loaded_data = sorted(data.load("data_test.json"), key=itemgetter("project_id"))

    def test_load(self):
        """Test the implemented load function"""

        # Compare the loaded data with the expected data
        self.assertEqual(self.loaded_data[0], self.expected_data[0])

        # Test that loading a non-existing file returns None
        self.assertEqual(data.load("/dev/this_file_does_not_exist"), None)

    def test_get_project_count(self):
        """Test the implemented function get_project_count"""

        # Test that the correct number of projects are returned
        self.assertEqual(data.get_project_count(self.loaded_data), 4)

    def test_get_project(self):
        """Test the implemented function get_project"""

        # Try to get project 1, 2, 3 and 4 and check that a project with
        # the correct project_id is returned.
        self.assertEqual(data.get_project(self.loaded_data, 1)["project_id"], 1)
        self.assertEqual(data.get_project(self.loaded_data, 2)["project_id"], 2)
        self.assertEqual(data.get_project(self.loaded_data, 3)["project_id"], 3)
        self.assertEqual(data.get_project(self.loaded_data, 4)["project_id"], 4)

        # Try to get a non-existing project and check that None is returned
        self.assertEqual(data.get_project(self.loaded_data, 42), None)

    def test_search(self):
        """Test the implemented search function"""

        # Call search with no other parameters than the database.
        # All projects should be returned
        self.assertEqual(len(data.search(self.loaded_data)), 4)

        # Search for projects with csv as technique.
        # 1 project should be returned
        self.assertEqual(len(data.search(self.loaded_data, techniques=["csv"])), 1)

        # Search for projects including Python and sort them in ascending order.
        # Ensure that returned projects are sorted by ascending dates
        res = data.search(self.loaded_data, sort_order="asc", techniques=["python"])
        self.assertEqual(res[0]["start_date"], "2009-09-05")
        self.assertEqual(res[1]["start_date"], "2009-09-07")
        self.assertEqual(res[2]["start_date"], "2009-09-08")

        # Search for the term 'okÃ¤nt' in three specified search fields. Sort
        # results by end_date.
        # Ensure that projects are returned in the correct order.
        res = data.search(
            self.loaded_data,
            sort_by="end_date",
            search="okänt",
            search_fields=["project_id", "project_name", "course_name"],
        )
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0]["project_id"], 2)
        self.assertEqual(res[1]["project_id"], 3)
        self.assertEqual(res[2]["project_id"], 1)

        # Search for 'okÃ¤nt' in specified search fields.
        # Ensure correct number of results
        res = data.search(
            self.loaded_data,
            search="okänt",
            search_fields=["project_id", "project_name", "course_name"],
        )
        self.assertEqual(len(res), 3)

        # Search for 'okÃ¤nt' in specified search fields, provide empty technique list
        # Ensure correct number of results
        res = data.search(
            self.loaded_data,
            techniques=[],
            search="okänt",
            search_fields=["project_id", "project_name", "course_name"],
        )
        self.assertEqual(len(res), 3)

        # Search for 'okÃ¤nt', provide empty search fields list
        # Ensure 0 results
        res = data.search(self.loaded_data, search="okänt", search_fields=[])
        self.assertEqual(len(res), 0)

        # Search with results sorted by group size.
        # Ensure results are in descending order
        res = data.search(self.loaded_data, sort_by="group_size")
        self.assertEqual(res[0]["project_id"], 4)  # 1
        self.assertEqual(res[1]["project_id"], 2)  # 2
        self.assertEqual(res[2]["project_id"], 3)  # 3
        self.assertEqual(res[3]["project_id"], 1)  # 4

    def test_get_techniques(self):
        """Test the implemented get_techniques function"""

        res = data.get_techniques(self.loaded_data)
        self.assertEqual(res, self.expected_technique_data)

    def test_get_technique_stats(self):
        """Test the implemented get_technique_stats function"""

        res = data.get_technique_stats(self.loaded_data)
        res = sort_dict(res, "id")

        self.expected_technique_stat_data = sort_dict(
            self.expected_technique_stat_data, "id"
        )

        self.assertEqual(res, self.expected_technique_stat_data)


if __name__ == "__main__":
    print("Test:     ", md5(sys.argv[0].encode("UTF-8")).hexdigest())
    print("Test data:", md5(b"data.json").hexdigest())
    print()
    unittest.main()
