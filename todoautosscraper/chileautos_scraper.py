# -*- coding: utf-8 -*-

import re
import os
os.environ['http_proxy']=''

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
    u'A\xc3\xb1o:': 'year', 
    u'Tipo vehíc:': 'type_of_vehicle',
    u'Tipo veh\xc3\xadc:': 'type_of_vehicle',
    u'Carrocería:': 'vehicle_body',
    u'Carrocer\xc3\xada:': 'vehicle_body',
    u'Color:': 'color',
    u'Kilometraje:': 'kilometers',
    u'Cilindrada :': 'engine',
    u'Transmisión:': 'at_transmission',
    u'Transmisi\xc3\xb3n:': 'at_transmission',
    u'Dirección:': 'assisted_steering',
    u'Direcci\xc3\xb3n:': 'assisted_steering',
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
    u'Telefono:': 'contact_numbers',
    u'Vende:': 'contact_name'
    }
    publication = {}
    publication['title'] = soup.find('div', style='margin:18px 0 5px 0;float:left;padding-left:10px;padding-right:10px;width:704px;').find('h2').string.strip()
    publication['description'] = table.find('div', style='text-align: justify').strings.next()

    for item in items:
      # import ipdb; ipdb.set_trace()
      if item.find('td') and item.find('td').string in attributes_list.keys() and item.find('td').findNextSibling():
        publication[attributes_list.get(item.find('td').string)] = item.find('td').findNextSibling().text.strip()
        if item.find('td').string == 'Telefono:':
          publication['contact_numbers'] = item.find('td').findNextSibling()
        if item.find('td').string == 'Vende:':
          publication['contact_name'] = item.find('td').findNextSibling().string
      elif item.find('b') and item.find('b').string == u'Precio':
        publication['price'] = int(item.findNextSibling().find('b').string.replace('$', '').replace('.', '').strip())
    
    # Convert to number
    for parameter in ['year', 'kilometers', 'engine', 'doors']:
      if publication.get(parameter):
        publication[parameter] = ChileautosScrapper.process_int_parameter(publication.get(parameter))

    if publication.get('contact_numbers'):
      contents = publication.get('contact_numbers').strings
      contact_numbers = []
      for content in contents:
        phone = {'number': content.replace('cel.:', '').replace('fijo:', '').replace(' ', '').strip(), 'phone_type': None}
        if content.find("cel.:") != -1:
          phone['phone_type'] = "mobile"
        if content.find("fijo:") != -1:
          phone['phone_type'] = "landline"
        contact_numbers.append(phone)
      publication['contact_numbers'] = contact_numbers

    for parameter, chileautos_keys in [('assisted_steering', [u'Hidráulica', u'Asistida']), ('abs_break', ['ABS']), ('air_conditioner', ['Acondicionado']), ('airbag', ['SI']), ('alarm', ['SI']), ('centralized_locking', ['Centralizado']), ('at_transmission', [u'Autom\xe1tica',  u'Autom\xc3\xa1tica']), ('catalitic', [u'SI']), ('electric_mirrors', [u'El\xe9ctricos', u'El\xc3\xa9ctricos']), ('radio', [u'SI'])]:
      if publication.get(parameter):
        if publication.get(parameter) in chileautos_keys:
          publication[parameter] = True
        else:
          publication[parameter] = False
        

    date_container = soup.findAll('div', style='margin:18px 0 5px 0;float:left;padding-left:10px;padding-right:10px;width:704px;')[0].text
                                                
    date_regex =  re.compile('Publicado el \w+, (\d+) de (\w+) de (\d+).')
    date_tuple = ()
    if date_regex.findall(date_container):
      date_tuple = date_regex.findall(date_container)[0]
    months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    if date_tuple:
      publication['publication_date'] = '%s/%s/%s' % (date_tuple[0], months.index(date_tuple[1])+1, date_tuple[2])

    publication['source'] = 'chileautos'
    publication['chileautos_id'] = chileautos_id


    return publication


  @staticmethod
  def retrieve_publications_list():

    html =  urllib2.urlopen('http://www.chileautos.cl/cemagic.asp?disp=1&goo=0&sort=fa&dea=100&pag=1')
    soup = BeautifulSoup(html, from_encoding="iso-8859-1")
    last = soup.find(class_="navu").get('href')
    previous_url = 'http:' + last
    publication_ids = []
    while previous_url:
    # for x in range(0,3):
      html = urllib2.urlopen(previous_url)
      page_publications, previous_url = ChileautosScrapper.get_publication_ids_and_previous_url(html)
      publication_ids.extend(page_publications)
    return publication_ids

  @staticmethod
  def get_publication_ids_and_previous_url(html):
    soup = BeautifulSoup(html, from_encoding="iso-8859-1")
    tr_list = soup.findAll(class_="des")
    url_list = []
    for tr in tr_list:
      unprocessed_link = tr.get('onclick')
      id_regex = re.compile(r'codauto=(\d+)')
      if id_regex.search(unprocessed_link).groups():
        publication_id = id_regex.search(unprocessed_link).groups()[0]
        url_list.append(publication_id)
    previous_url = None
    if soup.find(id='ante'):
      previous_url = 'http:' + soup.find(id='ante').get('href')
    return url_list, previous_url


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

