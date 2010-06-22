#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi, logging, sys

from google.appengine.ext.webapp import template

def entry_tags(entry):
  tags = ""
  # TODO: content, contributor, published, source
  # http://tools.ietf.org/html/rfc4287#section-4.1.2
#  for tag in ['id', 'title', 'summary', 'rights']:
  for tag in ['id', 'title', 'summary']:
    tags += ("    <%s>%s</%s>\n" %
      (tag, getattr(entry, tag), tag)).encode('utf-8')
  tags += "    <updated>%s</updated>\n" % entry.rfc3339_updated()
  tags += "    <link href=\"/%s\" />\n" % entry.id.split(':')[-1:][0]
  return tags

def category_tags(query):
  categories = ""
  # TODO: configurable category limits
  for row in query.fetch(101):
    categories += \
      ("    <category scheme=\"%s\" term=\"%s\" label=\"%s\" />\n" % \
      (row.scheme, row.term, row.label)).encode('utf-8')
  return categories

def link_tags(query):
  links = ""
  # TODO: configurable link limits
  for row in query.fetch(101):
#    if row.rel not in ('alternate', 'current', 'enclosure', 'edit',
#      'edit-meta', 'first', 'last', 'license', 'next', 'next-archive',
#      'previous', 'related', 'replies', 'self', 'via'):
#      row.rel = 'occi:' + row.rel
    links += ("    <link rel=\"%s\" href=\"%s\" " % \
      (row.rel, row.href)).encode('utf-8')
    for attribute in row.dynamic_properties():
      value = getattr(row,attribute)
      if attribute not in ('type', 'hreflang', 'title', 'length'):
        attribute = 'occi:' + attribute
      links += ("%s=\"%s\" " % (attribute, value)).encode('utf-8')
    links += "/>\n"
  return links

register = template.create_template_register();
register.simple_tag(entry_tags)
register.simple_tag(category_tags)
register.simple_tag(link_tags)
