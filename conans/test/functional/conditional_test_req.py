import unittest
from conans.test.utils.tools import TestClient
from conans.util.files import load, save


class ConditionalReqsTest(unittest.TestCase):

    def conditional_requirements_test(self):
        conanfile = """from conans import ConanFile

class TestConanLib(ConanFile):
    name = "Hello"
    version = "0.1"
    settings = "os", "build_type", "product"
        """
        test_conanfile = '''
from conans import ConanFile

class TestConanLib(ConanFile):
    requires = "Hello/0.1@lasote/testing"
    settings = "os", "build_type", "product"
    def requirements(self):
        self.output.info("Conditional test requirement: %s, %s, %s"
                         % (self.settings.os, self.settings.build_type, self.settings.product))

    def test(self):
        pass
'''
        client = TestClient()
        settings_path = client.client_cache.settings_path
        client.client_cache.settings
        settings = load(settings_path)
        settings += "\nproduct: [onion, potato]"
        save(settings_path, settings)
        client.save({"conanfile.py": conanfile,
                     "test_package/conanfile.py": test_conanfile})
        client.run("test_package -s os=Windows -s product=onion")
        self.assertIn("PROJECT: Conditional test requirement: Windows, Release, onion",
                      client.user_io.out)
