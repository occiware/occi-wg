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

from occi import ext
from occi import fmt
from occi import res

class OCCI(object):
  __extensions = {}
  __formats = {}
  __resources = {}

  @staticmethod
  def RegisteredExtensions():
    """ Returns a list of registered extensions.
    """
    return dict(OCCI.__extensions)

  @staticmethod
  def RegisterExtension(extension):

    OCCI.__extensions[extension.name()] = extension
