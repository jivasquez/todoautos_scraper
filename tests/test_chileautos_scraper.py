# -*- encoding: utf-8 -*-

import unittest
from todoautosscraper.chileautos_scraper import ChileautosScrapper

class TestChileautosScraper(unittest.TestCase):
  

  def test_retrieve_publication(self):

    expected_json = {
      "brand": u"Audi",
      "model": u"A4",
      "version":  u"2.0 multitronic dies",
      "year":  2007,
      "type_of_vehicle": u"Automóvil",
      "vehicle_body": u"Sedán",
      "color":  u"gris",
      "kilometers":  100000,
      "engine" :  2000,
      "at_transmission":  True,
      "assisted_steering":  True,
      "air_conditioner": True,
      "electric_mirrors": True,
      "abs_break": True,
      "airbag": True,
      "centralized_locking": True,
      "catalitic": True,
      "fuel": u"Diesel (Petroleo)",
      "doors": 4,
      "alarm": True,
      "source": "chileautos"
      }


    publication_json = ChileautosScrapper.retrieve_publication(4522651)
    self.maxDiff = None
    self.assertDictEqual(publication_json, expected_json)
    