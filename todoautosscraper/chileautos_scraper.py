# -*- coding: utf-8 -*-

import re

from bs4 import BeautifulSoup
import urllib2

class ChileautosScrapper(object):
  
  def __init__(self, arg):
    pass


  @staticmethod
  def retrieve_publication(chileautos_id):
    html = ChileautosScrapper.get_html(chileautos_id)
    soup = BeautifulSoup(html, from_encoding="iso-8859-1")
    table = soup.find(class_="tablaauto justificado")
    items = table.findAll('tr')
    attributes_list = {'Marca:': 'brand',
    u'Modelo:': 'model',
    u'Versión:': 'model_version',
    u'Año:': 'year',
    u'Tipo vehíc:': 'type_of_vehicle',
    u'Carrocería:': 'vehicle_body',
    u'Color:': 'color',
    u'Kilometraje:': 'kilometers',
    u'Cilindrada :': 'engine',
    u'Transmisión:': 'at_transmission',
    u'Dirección:': 'assisted_steering',
    u'Aire': 'air_conditioner',
    u'Espejos': 'electric_mirrors',
    u'Frenos': 'abs_break',
    u'Airbag': 'airbag',
    u'Cierre': 'centralized_locking',
    u'Catalítico': 'catalitic',
    u'Combustible': 'fuel',
    u'Puertas:': 'doors',
    u'Alarma': 'alarm',
    u'Ciudad:': 'city',
    u'Patente:': 'plate_number',
    u'Telefono:': 'contact_numbers'
    }
    publication = {}
    for item in items:
      if item.find('td') and item.find('td').string in attributes_list.keys() and item.find('td').findNextSibling():
        publication[attributes_list.get(item.find('td').string)] = item.find('td').findNextSibling().text.strip()
        if item.find('td').string == 'Telefono:':
          publication['contact_numbers'] = item.find('td').findNextSibling()
    
    # Convert to number
    for parameter in ['year', 'kilometers', 'engine', 'doors']:
      if publication.get(parameter):
        publication[parameter] = ChileautosScrapper.process_int_parameter(publication.get(parameter))

    if publication.get('contact_numbers'):
      contents = publication.get('contact_numbers').strings
      contact_numbers = []
      for content in contents:
        phone = {'number': content.replace('cel.:', '').replace('fijo:', '').replace(' ', '').strip(), 'phone_type': None}
        if content.find("cel.:"):
          phone['phone_type'] = "mobile"
        if content.find("fijo:"):
          phone['phone_type'] = "landline"
        contact_numbers.append(phone)
      publication['contact_numbers'] = contact_numbers

    for parameter, chileautos_key in [('assisted_steering', u'Hidráulica'), ('abs_break', 'ABS'), ('air_conditioner', 'Acondicionado'), ('airbag', 'SI'), ('alarm', 'SI'), ('centralized_locking', 'Centralizado'), ('at_transmission', u'Autom\xe1tica'), ('catalitic', u'SI'), ('electric_mirrors', u'El\xe9ctricos'), ('radio', u'SI')]:
      if publication.get(parameter) and publication.get(parameter) == chileautos_key:
        publication[parameter] = True
    


    publication['source'] = 'chileautos'
    publication['chileautos_id'] = chileautos_id
    publication['chileautos_id'] = 4522651


    return publication

  @staticmethod
  def get_html(chileautos_id):
    response = urllib2.urlopen('http://www.chileautos.cl/auto.asp?codauto=%s' % chileautos_id)
    # print 'http://www.chileautos.cl/auto.asp?codauto=%s' % chileautos_id
    return response.read()
    
  @staticmethod
  def process_int_parameter(parameter):
    number_regex = re.compile(r'[^\d]+')
    string_parameter = number_regex.sub('', parameter)
    try:
      returned_parameter = int(string_parameter)
      return returned_parameter
    except:
      return False
    return False
    

# ChileautosScrapper.retrieve_publication(4522651)

