# -*- encoding: utf-8 -*-

import unittest
from mock import patch
from todoautosscraper.chileautos_scraper import ChileautosScrapper

class TestChileautosScraper(unittest.TestCase):
  
  @patch.object(ChileautosScrapper, 'get_html')
  def test_retrieve_publication(self, get_mocked_html):
    html = open('chileautos_publication.html')
    get_mocked_html.return_value = html.read().decode('ISO-8859-1')
    expected_json = {
      "title": u"Audi\xa0A4",
      "description": u"Full equipo, asientos de cuero completamente electrÃ³nicos, climatizador bi zona, triptronic al volante. Un lujo..",
      "brand": u"Audi",
      "plate_number": u"WT5355",
      "city": u"Santiago",
      "model": u"A4",
      "year":  2007,
      "publication_date": u"05/5/2015",
      "type_of_vehicle": u'Autom\xc3\xb3vil',
      "vehicle_body": u'Sed\xc3\xa1n',
      "color":  u"Azul",
      "kilometers":  100000,
      "engine" :  2000,
      "at_transmission":  True,
      "assisted_steering":  True,
      "air_conditioner": True,
      "electric_mirrors": True,
      "abs_break": True,
      "airbag": True,
      "centralized_locking": True,
      "fuel": u"Bencina",
      "doors": 4,
      "alarm": True,
      "source": "chileautos",
      "chileautos_id": 4534426,
      "contact_numbers": [{'number': u'42870825', 'phone_type': 'mobile'}],
      "contact_name": u'Marco  Miranda',
      "price": 7500000,
      "images": [
        'http://fotos.chileautos.cl/fotos/4534/g_4534426_1.jpg',
        'http://fotos.chileautos.cl/fotos/4534/g_4534426_2.jpg',
        'http://fotos.chileautos.cl/fotos/4534/g_4534426_3.jpg',
        'http://fotos.chileautos.cl/fotos/4534/g_4534426_4.jpg',
        'http://fotos.chileautos.cl/fotos/4534/g_4534426_5.jpg'
      ]
      }

    publication_json = ChileautosScrapper.retrieve_publication(4534426)
    self.maxDiff = None
    self.assertDictEqual(publication_json, expected_json)
    

  # def test_retrieve_list(self):
  #   publication_ids = ChileautosScrapper.retrieve_publications_list()
  #   import ipdb; ipdb.set_trace()
  #   self.assertEquals(publication_ids, 1)