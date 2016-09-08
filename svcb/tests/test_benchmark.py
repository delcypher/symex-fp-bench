# Copyright (c) 2016, Daniel Liew
# This file is covered by the license in LICENSE-SVCB.txt
import svcb
from svcb import schema
import svcb.benchmark
import unittest

class TestBenchmark(unittest.TestCase):
  def setUp(self):
    self.persistentSchema = schema.getSchema()

  def appendSchemaVersion(self, d):
    d['schema_version'] = self.persistentSchema['__version__']

  def testCreateSimple(self):
    s = {
      'architectures': ['x86_64'],
      'categories': ['xxx'],
      'language': 'c99',
      'name': 'foo',
      'sources': ['a_is_a_good_name.c', 'b-IS-also-A-good-name.c'],
      'verification_tasks': { 'no_assert_fail': {'correct': True} },
    }
    self.appendSchemaVersion(s)
    # Validate benchmark specification
    schema.validateBenchmarkSpecification(s, schema=self.persistentSchema)
    benchmarkObjs = svcb.benchmark.getBenchmarks(s)
    self.assertTrue(len(benchmarkObjs) == 1)
    # Test properties of the benchmark object
    b = benchmarkObjs[0]
    self.assertEqual(b.name, "foo")
    self.assertEqual(b.sources, ['a_is_a_good_name.c', 'b-IS-also-A-good-name.c'])
    self.assertEqual(b.architectures, ['x86_64'])
    self.assertEqual(b.defines, {}) # Implicitly empty
    self.assertEqual(b.language, 'c99')
    self.assertEqual(b.comments, '') # Implicity empty
    self.assertEqual(b.categories, ['xxx'])
    self.assertEqual(b.verificationTasks, { 'no_assert_fail': {'correct': True} })
    self.assertTrue(b.isLanguageC())
    self.assertFalse(b.isLanguageCXX())

  def testCreateTwoVariants(self):
    s = {
      'architectures': ['x86_64'],
      'categories': ['xxx'],
      'comments': 'global comment',
      'defines': { 'DUMMY':'1' },
      'dependencies': { 'klee_runtime': {}},
      'language': 'c99',
      'name': 'basename',
      'sources': ['a.c', 'b.c'],
      'variants': {
        'foo': {
          'verification_tasks':{ 'no_assert_fail': {'correct': True} },
          'defines': {'FAIL':'0'},
          'dependencies': { 'pthreads': {} },
        },
        'bar': {
          'verification_tasks':{ 'no_assert_fail': {'correct': False} },
          'defines': {'FAIL':'1'},
          'dependencies': { 'openmp': {} },
        }
      }
    }
    self.appendSchemaVersion(s)
    # Validate benchmark specification
    schema.validateBenchmarkSpecification(s, schema=self.persistentSchema)
    benchmarkObjs = svcb.benchmark.getBenchmarks(s)
    self.assertTrue(len(benchmarkObjs) == 2)

    # Extract the two benchmarks. The order is not defined so get based on name
    fooBenchmark = next(filter(lambda b: b.name == 'basename_foo', benchmarkObjs))
    barBenchmark = next(filter(lambda b: b.name == 'basename_bar', benchmarkObjs))

    # Check foo
    self.assertEqual(fooBenchmark.architectures, ['x86_64'])
    self.assertEqual(fooBenchmark.categories, ['xxx'])
    self.assertEqual(fooBenchmark.comments, 'global comment')
    self.assertEqual(fooBenchmark.defines, {'DUMMY':'1', 'FAIL':'0'})
    self.assertEqual(fooBenchmark.dependencies, {'klee_runtime':{}, 'pthreads':{}})
    self.assertEqual(fooBenchmark.language, 'c99')
    self.assertEqual(fooBenchmark.name, 'basename_foo')
    self.assertEqual(fooBenchmark.sources, ['a.c', 'b.c'])
    self.assertEqual(fooBenchmark.verificationTasks,{ 'no_assert_fail': {'correct': True} })
    self.assertTrue(fooBenchmark.isLanguageC())
    self.assertFalse(fooBenchmark.isLanguageCXX())

    # Check bar
    self.assertEqual(barBenchmark.architectures, ['x86_64'])
    self.assertEqual(barBenchmark.categories, ['xxx'])
    self.assertEqual(barBenchmark.comments, 'global comment')
    self.assertEqual(barBenchmark.defines, {'DUMMY':'1', 'FAIL':'1'})
    self.assertEqual(barBenchmark.dependencies, {'klee_runtime':{}, 'openmp':{}})
    self.assertEqual(barBenchmark.language, 'c99')
    self.assertEqual(barBenchmark.name, 'basename_bar')
    self.assertEqual(barBenchmark.sources, ['a.c', 'b.c'])
    self.assertEqual(barBenchmark.verificationTasks,{ 'no_assert_fail': {'correct': False} })
    self.assertTrue(barBenchmark.isLanguageC())
    self.assertFalse(barBenchmark.isLanguageCXX())


