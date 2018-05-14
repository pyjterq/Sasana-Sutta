from django.test import TestCase

# Create your tests here.

from .parser_html import get_sutta_data_from_url


class TestSuttaDataFromUrl(TestCase):

    def test_sutta_number(self):
        results = get_sutta_data_from_url('/mn-123-var')
        self.assertEqual(results['sutta_nr'], 'mn123')

        results = get_sutta_data_from_url('/sn-54-19-vil')
        self.assertEqual(results['sutta_nr'], 'sn54.19')

        results = get_sutta_data_from_url('/dhp-agr')
        self.assertEqual(results['sutta_nr'], 'dhp')
        # /jat-159-vil

    def test_sutta_tittle(self):
        results = get_sutta_data_from_url('/mn-123-var')
        self.assertEqual(results['link'], 'http://sasana.pl/mn-123-var')

    def test_sutta_author(self):
        results = get_sutta_data_from_url('/mn-123-var')
        self.assertEqual(results['author'], 'Varapanyo Bhikkhu')

    def test_sutta_collection(self):
        results = get_sutta_data_from_url('/mn-123-var')
        self.assertEqual(results['collection'], 'Zbiór mów średniej długości')


# unittest.main()
