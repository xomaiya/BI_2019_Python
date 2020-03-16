import unittest

from filter_fastq import calculate_gc_content, filter


class FilterTest(unittest.TestCase):
    def test_calculate_gc_content_empty_read(self):
        self.assertEqual(calculate_gc_content(''), 0)

    def test_calculate_gc_content_only_G(self):
        self.assertEqual(calculate_gc_content('ATTG'), 25)

    def test_calculate_gc_content_only_C(self):
        self.assertEqual(calculate_gc_content('ATCT'), 25)

    def test_calculate_gc_content_normal(self):
        self.assertEqual(calculate_gc_content('ATGGGCCTAA'), 50)

    def test_filter_less_min_length(self):
        self.assertEqual(filter('ATGC', 10, 0, 100), 'bad')

    def test_filter_normal_length(self):
        self.assertEqual(filter('ATGC', 4, 0, 100), 'good')

    def test_filter_less_min_gc(self):
        self.assertEqual(filter('ATGAACTTTAA', 0, 25, 75), 'bad')

    def test_filter_normal_gc(self):
        self.assertEqual(filter('ATGGCGACT', 0, 25, 75), 'good')

    def test_filter_more_max_gc(self):
        self.assertEqual(filter('GCGACGTGC', 0, 25, 75), 'bad')


if __name__ == '__main__':
    unittest.main()
