# -*- encoding: utf-8 -*-

import unittest
from todoautosscraper.chileautos_scraper import ChileautosScrapper

class TestChileautosScraper(unittest.TestCase):
  

  def test_retrieve_publication(self):

    expected_json = {
      "brand": u"Audi",
      "plate_number": u"WT5355",
      "city": u"Santiago",
      "model": u"A4",
      "year":  2007,
      "publication_date": u"05/5/2015",
      "type_of_vehicle": u"Automóvil",
      "vehicle_body": u"Sedán",
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
      "contact_numbers": [{'number': u'42870825', 'phone_type': 'mobile'}]
      }


    publication_json = ChileautosScrapper.retrieve_publication(4534426)
    self.maxDiff = None
    self.assertDictEqual(publication_json, expected_json)
    

  def test_retrieve_list(self):
    publication_ids = ChileautosScrapper.retrieve_publications_list()
    import ipdb; ipdb.set_trace()
    self.assertEquals(publication_ids, 1)