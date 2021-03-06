# -*- coding: utf-8 -*-

import os
from nose.tools import *
from io import StringIO
from unittest.mock import patch

import elasticsearch
from elasticsearch import exceptions
import kibtool

from . import KibtoolTestCase

# suppress console err message from http connections
import logging
logging.getLogger("urllib3").setLevel(logging.ERROR)

host, port = os.environ.get('TEST_ES_SERVER', 'localhost:9200').split(':')
port = int(port) if port else 9200

class TestCopyDash(KibtoolTestCase):
  def test_copy_dashid(self):
    (l_srcName, l_dstName) = self.create_indices()

    with patch('sys.stdout', new=StringIO()) as fake_out, patch('sys.stderr', new=StringIO()) as fake_err:
      l_kibtool = kibtool.KibTool(["./test_kibtool", "--kibfrom", l_srcName, "--kibto", l_dstName,
                                   "--dashid", "dashboard-1",
                                   "--copy"])
      l_kibtool.execute()
      self.assertEquals(fake_out.getvalue().strip(), "")
      self.assertEquals(fake_err.getvalue().strip(), "")

    l_src = self.client.get(index=l_srcName, doc_type="dashboard", id="dashboard-1")
    l_srcIdx = l_src.pop("_index")
    l_dst = self.client.get(index=l_dstName, doc_type="dashboard", id="dashboard-1")
    l_dstIdx = l_dst.pop("_index")
    self.assertEquals(l_srcIdx, l_srcName)
    self.assertEquals(l_dstIdx, l_dstName)
    self.assertEquals(l_src, l_dst)

  def test_copy_dash(self):
    (l_srcName, l_dstName) = self.create_indices()

    with patch('sys.stdout', new=StringIO()) as fake_out, patch('sys.stderr', new=StringIO()) as fake_err:
      l_kibtool = kibtool.KibTool(["./test_kibtool", "--kibfrom", l_srcName, "--kibto", l_dstName,
                                   "--dash", "dashboard 1",
                                   "--copy"])
      l_kibtool.execute()
      self.assertEquals(fake_out.getvalue().strip(), "")
      self.assertEquals(fake_err.getvalue().strip(), "")

    l_src = self.client.get(index=l_srcName, doc_type="dashboard", id="dashboard-1")
    l_srcIdx = l_src.pop("_index")
    l_dst = self.client.get(index=l_dstName, doc_type="dashboard", id="dashboard-1")
    l_dstIdx = l_dst.pop("_index")
    self.assertEquals(l_srcIdx, l_srcName)
    self.assertEquals(l_dstIdx, l_dstName)
    self.assertEquals(l_src, l_dst)

  def test_copy_dashid_depend(self):
    (l_srcName, l_dstName) = self.create_indices()

    with patch('sys.stdout', new=StringIO()) as fake_out, patch('sys.stderr', new=StringIO()) as fake_err:
      l_kibtool = kibtool.KibTool(["./test_kibtool", "--kibfrom", l_srcName, "--kibto", l_dstName,
                                   "--dashid", "dashboard-1",
                                   "--depend", "--copy"])
      l_kibtool.execute()
      self.assertEquals(fake_out.getvalue().strip(), "")
      self.assertEquals(fake_err.getvalue().strip(), "")

    l_src = self.client.get(index=l_srcName, doc_type="dashboard", id="dashboard-1")
    l_srcIdx = l_src.pop("_index")
    l_dst = self.client.get(index=l_dstName, doc_type="dashboard", id="dashboard-1")
    l_dstIdx = l_dst.pop("_index")
    self.assertEquals(l_srcIdx, l_srcName)
    self.assertEquals(l_dstIdx, l_dstName)
    self.assertEquals(l_src, l_dst)

    l_src = self.client.get(index=l_srcName, doc_type="visualization", id="visualization-1")
    l_srcIdx = l_src.pop("_index")
    l_dst = self.client.get(index=l_dstName, doc_type="visualization", id="visualization-1")
    l_dstIdx = l_dst.pop("_index")
    self.assertEquals(l_srcIdx, l_srcName)
    self.assertEquals(l_dstIdx, l_dstName)
    self.assertEquals(l_src, l_dst)

    l_src = self.client.get(index=l_srcName, doc_type="search", id="search-1")
    l_srcIdx = l_src.pop("_index")
    l_dst = self.client.get(index=l_dstName, doc_type="search", id="search-1")
    l_dstIdx = l_dst.pop("_index")
    self.assertEquals(l_srcIdx, l_srcName)
    self.assertEquals(l_dstIdx, l_dstName)
    self.assertEquals(l_src, l_dst)

    l_src = self.client.get(index=l_srcName, doc_type="index-pattern", id="index-pattern-1")
    l_srcIdx = l_src.pop("_index")
    l_dst = self.client.get(index=l_dstName, doc_type="index-pattern", id="index-pattern-1")
    l_dstIdx = l_dst.pop("_index")
    self.assertEquals(l_srcIdx, l_srcName)
    self.assertEquals(l_dstIdx, l_dstName)
    self.assertEquals(l_src, l_dst)

  def test_copy_kibto_error(self):
    (l_srcName, l_dstName) = self.create_indices()

    with patch('sys.stdout', new=StringIO()) as fake_out, patch('sys.stderr', new=StringIO()) as fake_err:
      with self.assertRaises(SystemExit) as w_se:
        l_kibtool = kibtool.KibTool(["./test_kibtool", "--kibfrom", l_srcName,
                                     "--dashid", "dashboard-1",
                                     "--depend", "--copy"])
        l_kibtool.execute()
      self.assertEquals(fake_out.getvalue().strip(), "")
      l_err = fake_err.getvalue().strip()
      self.assertEquals(l_err[:7], "usage: ")
      self.assertRegex(l_err, "ok to copy, but where\? --kibto is missing!$")

# ./test_kibtool --kibfrom kibtool-src --kibto kibtool-dst --dashid dashboard-1 --depend --copy
