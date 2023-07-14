import unittest

if __name__ == "__main__":
    suite = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=3).run( suite )