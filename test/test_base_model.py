#!/usr/bin/python
"""Test file for the BaseModule module"""

import unittest

class TestBaseModel(unittest.TestCase):
    """
        Defines a class for test the BaseModel
        It inherits from TestCase Class
    """
    
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_save(self):
        """
        self.model.name = "New Name"
        self.model.save()
        self.assertGreater(self.model.updated_at, self.model.created_at)
        """
        pass


if __name__ == "__main__":
    unittest.main()
