#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# $Id$
# Copyright © 2009 Sam Johnston <samj@samj.net> http://samj.net/
#                  Australian Online Solutions Pty Ltd http://www.aos.net.au/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Google App Engine implementation of Open Cloud Computing Interface (OCCI)

This is a simple implementation of OCCI for Google App Engine (GAE)
"""

import sys
sys.path.insert(0, './lib')

import os
import uuid
import wsgiref.handlers
from populate import PopulateHandler
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
template.register_template_library('common.template_tags')

from rfc3339 import rfc3339

_DEBUG=True

class BaseRequestHandler(webapp.RequestHandler):
  """Centralises template generation

  Combines supplied template_values with defaults and renders specified template.
  """
  def generate(self, template_file, values={}, mime_type='text/html'):
    defaults = {
      'request': self.request,
      'application_name': 'OCCI Test Harness',
      'mime_type': 'text/html'
    }
    values.update(defaults)
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, os.path.join('templates', template_file))
    self.response.headers['Content-Type'] = mime_type
    self.response.out.write(template.render(path, values, debug=_DEBUG))

  def head(self, *args):
    pass

  def get(self, *args):
    pass

  def post(self, *args):
    pass

class Resource (db.Model):
  id = db.StringProperty()
  title = db.StringProperty()
  summary = db.TextProperty()
  created = db.DateTimeProperty(auto_now_add=True)
  updated = db.DateTimeProperty(auto_now_add=True)
  rights = db.StringProperty()
  category = db.CategoryProperty()

  def rfc3339_updated(self):
	return rfc3339(self.updated, utc=True, use_system_timezone=False)

class Link (db.Expando):
  resource = db.ReferenceProperty(Resource, collection_name='links')
  target = db.ReferenceProperty(Resource, collection_name='linkers')
  rel = db.StringProperty(required=True)
  href = db.StringProperty(required=True)
#  title = db.StringProperty()

class Category (db.Model):
  resource = db.ReferenceProperty(Resource, collection_name='categories')
  scheme = db.StringProperty()
  term = db.StringProperty()
  label = db.StringProperty()

class MainHandler(webapp.RequestHandler):

  def get(self):
    self.response.out.write('<html><head><title>OCCI Test Harness</title></head><body><ol>')
    for resource in Resource.all().filter('category =', 'compute').order('updated').fetch(1000):
      self.response.out.write('  <li><a href="%s">%s</a><br /><ul>' % (resource.id.split(':')[-1:][0], resource.title))
      for link in resource.links:
        self.response.out.write('    <li><a href="%s">%s</a></li>' % (link.target.id.split(':')[-1:][0], link.title))
      self.response.out.write('</ul></li>')
    self.response.out.write('</ol></body></html>')

class CategoryHandler(webapp.RequestHandler):

  def get(self, cats):
    self.response.out.write('Looking at the following categories: ')
    for cat in cats.split('/'):
      self.response.out.write("%s " % cat)

class FeedHandler(BaseRequestHandler):
  def get(self):
    entries = db.Query(Resource). \
                order('-updated').fetch(limit=1000)

    updated = ''
    if entries: updated = entries[0].rfc3339_updated()

    self.generate('atom-feed.xml', { 'entries': entries, 'updated': updated }, 'application/atom+xml')

class ResourceHandler(BaseRequestHandler):
  def get(self, id):
    resource = Resource.get(db.Key.from_path('Resource', 'urn:uuid:' + id))
    self.generate('atom-entry.xml', { 'resource': resource }, 'application/atom+xml')

class ExtensionHandler(webapp.RequestHandler):

  def get(self, id, ext, args):
    self.response.out.write('Hello resource %s, extension %s is going to %s you!' % (id, ext, args))

def main():
  application = webapp.WSGIApplication([(r'/', FeedHandler),
                                        (r'/populate', PopulateHandler),
                                        (r'/-/(.*)', CategoryHandler),
                                        (r'/([0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})/([^\/]+)/(.*)', ExtensionHandler),
                                        (r'/([0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})', ResourceHandler)
                                       ],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
