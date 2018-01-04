"""Tests for typeshed.py."""

import os


from pytype import load_pytd
from pytype.pytd import typeshed
from pytype.pytd.parse import builtins
from pytype.pytd.parse import parser_test_base
from pytype.tests import test_base
import unittest


class TestTypeshedLoading(parser_test_base.ParserTest):
  """Test the code for loading files from typeshed."""

  def setUp(self):
    super(TestTypeshedLoading, self).setUp()
    self.ts = typeshed.Typeshed(typeshed_location="typeshed", use_pickled=False)

  def test_get_typeshed_file(self):
    filename, data = self.ts.get_module_file("stdlib", "errno", (2, 7))
    self.assertEqual("errno.pyi", os.path.basename(filename))
    self.assertIn("errorcode", data)

  def test_get_typeshed_dir(self):
    filename, data = self.ts.get_module_file(
        "stdlib", "logging", (2, 7))
    self.assertEqual("__init__.pyi", os.path.basename(filename))
    self.assertIn("LogRecord", data)

  def test_parse_type_definition(self):
    ast = typeshed.parse_type_definition(
        "stdlib", "_random", (2, 7), "typeshed", False)
    self.assertIn("_random.Random", [cls.name for cls in ast.classes])


  def test_get_all_stdlib_module_names_2(self):
    t = typeshed.Typeshed("typeshed", False)
    modules = t.get_all_stdlib_module_names([2, 7])
    self.assertIn("collections", modules)
    self.assertIn("csv", modules)
    self.assertIn("ctypes", modules)
    self.assertIn("email.MIMEBase", modules)
    self.assertIn("xml.etree.ElementTree", modules)

  def test_get_all_stdlib_module_names_3(self):
    t = typeshed.Typeshed("typeshed", False)
    modules = t.get_all_stdlib_module_names([3, 5])
    self.assertIn("asyncio", modules)
    self.assertIn("collections", modules)
    self.assertIn("configparser", modules)


class TestTypeshedParsing(test_base.BaseTest):
  """Tests a handful of typeshed modules.

  The list was generated using
      ls ../typeshed/stdlib/2/ | sort -R | sed s/.pyi$// | head -16
  """

  def setUp(self):
    super(TestTypeshedParsing, self).setUp()
    self.loader = load_pytd.Loader("base", self.PYTHON_VERSION)

  def test_quopri(self):
    self.assertTrue(self.loader.import_name("quopri"))

  def test_rfc822(self):
    self.assertTrue(self.loader.import_name("rfc822"))

  def test_email(self):
    self.assertTrue(self.loader.import_name("email"))

  def test_robotparser(self):
    self.assertTrue(self.loader.import_name("robotparser"))

  def test_md5(self):
    self.assertTrue(self.loader.import_name("md5"))

  def test_uuid(self):
    self.assertTrue(self.loader.import_name("uuid"))

  def test_decimal(self):
    self.assertTrue(self.loader.import_name("decimal"))

  def test_select(self):
    self.assertTrue(self.loader.import_name("select"))

  def test__ast(self):
    self.assertTrue(self.loader.import_name("_ast"))

  def test_importlib(self):
    self.assertTrue(self.loader.import_name("importlib"))

  def test_SocketServer(self):
    self.assertTrue(self.loader.import_name("SocketServer"))

  def test_thread(self):
    self.assertTrue(self.loader.import_name("thread"))

  def test_runpy(self):
    self.assertTrue(self.loader.import_name("runpy"))

  def test_hotshot(self):
    self.assertTrue(self.loader.import_name("_hotshot"))

  def test_imp(self):
    self.assertTrue(self.loader.import_name("imp"))


if __name__ == "__main__":
  unittest.main()
