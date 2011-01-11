#!/usr/bin/python
# -*- coding: utf-8 -*-

# 
# Copyright (C) 2011 Platform Computing
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
# 

import httplib2
import urllib
import logging
import sys
import getopt
import re

try:
    from Tkinter import Frame, Label, StringVar, IntVar, Button, Entry, Checkbutton, \
    N, E, W, S, Tk, LEFT
except ImportError:
    logging.warn("TK GUI will not be available...")

#===============================================================================
# Convenience routines
#===============================================================================

def get_session_cookie(url, user, password):
    '''
    Returns a cookie with the session information.
    '''
    http = httplib2.Http()
    login_url = url + '/login'
    body = {'name': user, 'pass': password}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    response, content = http.request(login_url, 'POST', headers = headers,
                                     body = urllib.urlencode(body))

    if not response['status'] == '302':

        print response, content
        raise AttributeError('Something went wrong during login...')

    return response['set-cookie']

def get_version(url, heads):
    '''
    First called to check what service is running. Also very simple connection 
    test.
    '''
    http = httplib2.Http()
    try:
        response, content = http.request(url, 'GET', headers = heads)
    except:
        logging.warn('Could not do a simple GET! Maybe service requires login?')
        sys.exit(1)
    return response['server']

def get_categories(url, heads):
    url = url + '/-/'
    http = httplib2.Http()
    response, content = http.request(url, 'GET', headers = heads)
    result = []
    for line in content.split('\n'):
        result.append(line)
    return result

#===============================================================================
# The tests...
#===============================================================================

def test_version_information(url, heads):
    '''
    Verifies that OCCI/1.1 can be found in the Server header string.
    '''
    http = httplib2.Http()
    response, content = http.request(url, 'GET', headers = heads)
    if response['server'].find('OCCI/1.1') is - 1:
        raise AttributeError('OCCI implementation should include OCCI/1.1 - '
                     + 'Service did return: ' + response['server'])

def check_if_complete(rendering, rel, attributes, actions):
    '''
    Checks if a certain kind, mixin, action is complete...
    '''
    for item in rendering:
        item = item.strip().split('=')
        if item[0] == 'rel':
            if item[1].find(rel) == -1:
                raise AttributeError('Could not find the correct related. Should be "' + rel + '". Found: ' + item[1])
        elif item[0] == 'attributes':
            for attr in attributes:
                if item[1].find(attr) == -1:
                    raise AttributeError('Mandatory attribute "' + attr + '" was not found for: ' + rendering[0].strip() + '. Found: ' + item[1])
        elif item[0] == 'actions':
            for action in actions:
                if item[1].find(action) == -1:
                    raise AttributeError('Mandatory action "' + action + '" was not found for: ' + rendering[0].strip() + '. Found: ' + item[1])

def test_infrastructure_model_for_completness(url, heads):
    '''
    Verifies if the infrastructure model is implemented as specified.
    '''
    heads['Accept'] = 'text/plain'
    url = url + '/-/'
    http = httplib2.Http()
    response, content = http.request(url, 'GET', headers = heads)
    infra_model = []
    for line in content.split('\n'):
        cur = line.lstrip('Category:').split(';')
        # check if compute has all attributes & actions & rels
        #----------------------------------------------------------------- Kinds
        if cur[0].strip() == 'compute' and cur[1].strip() == 'scheme="http://schemas.ogf.org/occi/infrastructure#"':
            rel = 'http://schemas.ogf.org/occi/core#resource'
            attr = ['occi.compute.architecture', 'occi.compute.cores', 'occi.compute.hostname', 'occi.compute.speed', 'occi.compute.memory', 'occi.compute.state']
            actions = ['start', 'stop', 'suspend', 'restart']
            check_if_complete(cur, rel, attr, actions)
            infra_model.append('compute')
        elif cur[0].strip() == 'network' and cur[1].strip() == 'scheme="http://schemas.ogf.org/occi/infrastructure#"':
            rel = 'http://schemas.ogf.org/occi/core#resource'
            attr = ['occi.network.vlan', 'occi.network.label', 'occi.network.state']
            actions = ['up', 'down']
            check_if_complete(cur, rel, attr, actions)
            infra_model.append('network')
        elif cur[0].strip() == 'storage' and cur[1].strip() == 'scheme="http://schemas.ogf.org/occi/infrastructure#"':
            rel = 'http://schemas.ogf.org/occi/core#resource'
            attr = ['occi.storage.size', 'occi.storage.state']
            actions = ['online', 'offline', 'backup', 'snapshot', 'resize']
            check_if_complete(cur, rel, attr, actions)
            infra_model.append('storage')
        #----------------------------------------------------------------- Links
        elif cur[0].strip() == 'storagelink' and cur[1].strip() == 'scheme="http://schemas.ogf.org/occi/infrastructure#"':
            rel = 'http://schemas.ogf.org/occi/core#link'
            attr = ['occi.storagelink.deviceid', 'occi.storagelink.mountpoint', 'occi.storagelink.state']
            actions = []
            check_if_complete(cur, rel, attr, actions)
            infra_model.append('storagelink')
        elif cur[0].strip() == 'networkinterface' and cur[1].strip() == 'scheme="http://schemas.ogf.org/occi/infrastructure#"':
            rel = 'http://schemas.ogf.org/occi/core#link'
            attr = ['occi.networkinterface.state', 'occi.networkinterface.mac', 'occi.networkinterface.interface']
            actions = []
            check_if_complete(cur, rel, attr, actions)
            infra_model.append('networkinterface')
        #---------------------------------------------------------------- mixins
        elif cur[0].strip() == 'ipnetwork' and cur[1].strip() == 'scheme="http://schemas.ogf.org/occi/infrastructure/network#"':
            rel = 'http://schemas.ogf.org/occi/core#link'
            attr = ['occi.network.address', 'occi.network.gateway', 'occi.network.allocation']
            actions = []
            check_if_complete(cur, rel, attr, actions)
            infra_model.append('ipnetwork')
        #--------------------------------------------------------------- actions
        elif cur[0].strip() == 'start' and cur[1].strip() == 'scheme="http://schemas.ogf.org/occi/infrastructure/compute/action#"':
            rel = ''
            attr = ['graceful', 'acpioff', 'poweroff']
            actions = []
            check_if_complete(cur, rel, attr, actions)
            infra_model.append('start')
        elif cur[0].strip() == 'stop' and cur[1].strip() == 'scheme="http://schemas.ogf.org/occi/infrastructure/compute/action#"':
            rel = ''
            attr = []
            actions = []
            check_if_complete(cur, rel, attr, actions)
            infra_model.append('stop')
        elif cur[0].strip() == 'restart' and cur[1].strip() == 'scheme="http://schemas.ogf.org/occi/infrastructure/compute/action#"':
            rel = ''
            attr = ['graceful', 'warm', 'cold']
            actions = []
            check_if_complete(cur, rel, attr, actions)
            infra_model.append('restart')
        elif cur[0].strip() == 'suspend' and cur[1].strip() == 'scheme="http://schemas.ogf.org/occi/infrastructure/compute/action#"':
            rel = ''
            attr = ['hibernate', 'suspend']
            actions = []
            check_if_complete(cur, rel, attr, actions)
            infra_model.append('suspend')
        elif cur[0].strip() == 'up' and cur[1].strip() == 'scheme="http://schemas.ogf.org/occi/infrastructure/network/action#"':
            rel = ''
            attr = []
            actions = []
            check_if_complete(cur, rel, attr, actions)
            infra_model.append('up')
        elif cur[0].strip() == 'down' and cur[1].strip() == 'scheme="http://schemas.ogf.org/occi/infrastructure/network/action#"':
            rel = ''
            attr = []
            actions = []
            check_if_complete(cur, rel, attr, actions)
            infra_model.append('down')
        elif cur[0].strip() == 'online' and cur[1].strip() == 'scheme="http://schemas.ogf.org/occi/infrastructure/storage/action#"':
            rel = ''
            attr = []
            actions = []
            check_if_complete(cur, rel, attr, actions)
            infra_model.append('online')
        elif cur[0].strip() == 'offline' and cur[1].strip() == 'scheme="http://schemas.ogf.org/occi/infrastructure/storage/action#"':
            rel = ''
            attr = []
            actions = []
            check_if_complete(cur, rel, attr, actions)
            infra_model.append('offline')
        elif cur[0].strip() == 'resize' and cur[1].strip() == 'scheme="http://schemas.ogf.org/occi/infrastructure/storage/action#"':
            rel = ''
            attr = ['size']
            actions = []
            check_if_complete(cur, rel, attr, actions)
            infra_model.append('resize')
        elif cur[0].strip() == 'backup' and cur[1].strip() == 'scheme="http://schemas.ogf.org/occi/infrastructure/storage/action#"':
            rel = ''
            attr = []
            actions = []
            check_if_complete(cur, rel, attr, actions)
            infra_model.append('backup')
        elif cur[0].strip() == 'snapshot' and cur[1].strip() == 'scheme="http://schemas.ogf.org/occi/infrastructure/storage/action#"':
            rel = ''
            attr = []
            actions = []
            check_if_complete(cur, rel, attr, actions)
            infra_model.append('snapshot')

    if not 'compute' in infra_model:
        raise AttributeError('Missing compute kind.')
    elif not 'network' in infra_model:
        raise AttributeError('Missing network kind.')
    elif not 'storage' in infra_model:
        raise AttributeError('Missing storage kind.')
    elif not 'storagelink' in infra_model:
        raise AttributeError('Missing storagelink link.')
    elif not 'networkinterface' in infra_model:
        raise AttributeError('Missing networkinterface link.')
    elif not 'ipnetwork' in infra_model:
        raise AttributeError('Missing ipnetwork mixin.')
    elif not 'start' in infra_model:
        raise AttributeError('Missing start action definition.')
    elif not 'stop' in infra_model:
        raise AttributeError('Missing stop action definition.')
    elif not 'restart' in infra_model:
        raise AttributeError('Missing restart action definition.')
    elif not 'suspend' in infra_model:
        raise AttributeError('Missing suspend action definition.')
    elif not 'up' in infra_model:
        raise AttributeError('Missing up action definition.')
    elif not 'down' in infra_model:
        raise AttributeError('Missing down action definition.')
    elif not 'snapshot' in infra_model:
        raise AttributeError('Missing snapshot action definition.')
    elif not 'resize' in infra_model:
        raise AttributeError('Missing resize action definition.')
    elif not 'online' in infra_model:
        raise AttributeError('Missing online action definition.')
    elif not 'offline' in infra_model:
        raise AttributeError('Missing offline action definition.')
    elif not 'backup' in infra_model:
        raise AttributeError('Missing backup action definition.')

def test_accept_header(url, heads):
    '''
    Checks if correct content-types are returned for certain Accept headers.
    '''
    # GETs
    heads['Accept'] = 'text/plain'
    url = url + '/-/'
    http = httplib2.Http()
    response, content = http.request(url, 'GET', headers = heads)
    if not response['content-type'] == 'text/plain':
        raise AttributeError('When requesting text/plain - The Content-type text/plain should be exposed by the server.')

    heads['Accept'] = 'text/occi'
    http = httplib2.Http()
    response, content = http.request(url, 'GET', headers = heads)
    if not response['content-type'] == 'text/occi':
        raise AttributeError('When requesting text/occi - The Content-type text/occi should be exposed by the server.')
    if not response['status'] == '200':
        raise AttributeError('could not triggered action: ' + repr(response) + content)
    # POSTs
    #TODO...

def test_create_kinds(url, heads):
    '''
    tests the basic creation of kinds.
    '''
    loc = ''
    heads['Content-Type'] = 'text/occi'

    # POST
    post_heads = heads.copy()
    post_heads['Category'] = 'compute;scheme="http://schemas.ogf.org/occi/infrastructure#"'
    http = httplib2.Http()
    response, content = http.request(url, 'POST', headers = post_heads)
    if not response['status'] == '200' or response['status'] == '202':
        logging.warn('Creation failed - this might be okay - please examine output!' + repr(response) + content)
        raise AttributeError("Test did no run completly!")
    try:
        loc = response['location']
    except KeyError:
        raise AttributeError('OCCI implementation should expose the URI of the newly created resource.')

    # PUT
    put_heads = heads.copy()
    put_heads['X-OCCI-Attribute'] = 'occi.compute.hostname=foo'
    http = httplib2.Http()
    response, content = http.request(loc, 'PUT', headers = put_heads)
    if not response['status'] == '200' or response['status'] == '202':
        raise AttributeError('Unable to do an update on the resource: ' + loc)

    # GET
    http = httplib2.Http()
    response, content = http.request(loc, 'GET', headers = heads)
    if not response['status'] == '200' or response['status'] == '202':
        raise AttributeError('Unable to do retrieve the resource: ' + loc)

    # DELETE
    http = httplib2.Http()
    response, content = http.request(loc, 'DELETE', headers = heads)
    if not response['status'] == '200' or response['status'] == '202':
        raise AttributeError('Unable to do delete the resource: ' + loc)

def test_mixins(url, heads):
    '''
    Tests if a mixin can be created, retrieved and deleted.
    '''
    heads['Content-Type'] = 'text/occi'

    put_heads = heads.copy()
    put_heads['Category'] = 'my_stuff;scheme="http://example.com/occi#";location=/my_stuff/'
    http = httplib2.Http()
    response, content = http.request(url + '/-/', 'PUT', headers = put_heads)
    if not response['status'] == '200' or response['status'] == '202':
        raise AttributeError('Unable to create a user-defined mixin. Response: ' + repr(response) + content)

    http = httplib2.Http()
    response, content = http.request(url + '/-/', 'GET', headers = heads)
    if response['category'].find('my_stuff') == -1:
        raise AttributeError('Unable to find the previously defined mixin in the query interface!')

    put_heads = heads.copy()
    put_heads['Category'] = 'my_stuff;scheme="http://example.com/occi#"'
    http = httplib2.Http()
    response, content = http.request(url + '/-/', 'DELETE', headers = put_heads)
    if not response['status'] == '200' or response['status'] == '202':
        raise AttributeError('Unable to delete a user-defined mixin. Response: ' + repr(response) + content)

def test_links(url, heads):
    '''
    Tests if links are properly supported.
    '''
    heads['Content-Type'] = 'text/occi'

    # POST
    compute_heads = heads.copy()
    compute_heads['Category'] = 'compute;scheme="http://schemas.ogf.org/occi/infrastructure#"'
    http = httplib2.Http()
    response, content = http.request(url, 'POST', headers = compute_heads)
    if not response['status'] == '200' or response['status'] == '202':
        logging.warn('Creation failed - this might be okay - please examine output!' + repr(response) + content)
        raise AttributeError("Test did no run completly!")
    compute_loc = response['location']

    network = heads.copy()
    network['Category'] = 'network;scheme="http://schemas.ogf.org/occi/infrastructure#"'
    http = httplib2.Http()
    response, content = http.request(url, 'POST', headers = network)
    if not response['status'] == '200' or response['status'] == '202':
        logging.warn('Creation failed - this might be okay - please examine output!' + repr(response) + content)
        raise AttributeError("Test did no run completly!")
    network_loc = response['location']

    # now create a link...
    link = heads.copy()
    link['Category'] = 'networkinterface;scheme="http://schemas.ogf.org/occi/infrastructure#"'
    link['X-OCCI-Attribute'] = 'source=' + compute_loc + ',target=' + network_loc
    http = httplib2.Http()
    response, content = http.request(url, 'POST', headers = link)
    if not response['status'] == '200' or response['status'] == '202':
        logging.warn('Creation failed - this might be okay - please examine output!' + repr(response) + content)
        raise AttributeError("Test did no run completly!")
    link_loc = response['location']

    # cleanup...    
    http = httplib2.Http()
    response, content = http.request(link_loc, 'DELETE', headers = heads)
    http = httplib2.Http()
    response, content = http.request(compute_loc, 'DELETE', headers = heads)
    http = httplib2.Http()
    response, content = http.request(network_loc, 'DELETE', headers = heads)

def test_actions(url, heads):
    '''
    Tests if actions can be triggered.
    '''
    heads['Content-Type'] = 'text/occi'

    # POST
    compute_heads = heads.copy()
    compute_heads['Category'] = 'compute;scheme="http://schemas.ogf.org/occi/infrastructure#"'
    http = httplib2.Http()
    response, content = http.request(url, 'POST', headers = compute_heads)
    if not response['status'] == '200' or response['status'] == '202':
        logging.warn('Creation failed - this might be okay - please examine output!' + repr(response) + content)
        raise AttributeError("Test did no run completly!")
    compute_loc = response['location']

    http = httplib2.Http()
    response, content = http.request(compute_loc, 'GET', headers = heads)
    links = response['link'].split(',')
    for link in links:
        if link == '<' + compute_loc + '?action=start>':
            action_url = link.lstrip('<').rstrip('>')
            http = httplib2.Http()
            action_heads = heads.copy()
            action_heads['Category'] = 'start;scheme="http://schemas.ogf.org/occi/infrastructure/compute/action#"'
            response, content = http.request(action_url, 'POST', headers = action_heads)
            if not response['status'] == '200':
                raise AttributeError('could not triggered action: ' + repr(response) + content)

    http = httplib2.Http()
    response, content = http.request(compute_loc, 'DELETE', headers = heads)
    if not response['status'] == '200':
        raise AttributeError('could not delete resource: ' + repr(response) + content)

def test_filter(url, heads):
    '''
    Tests if the filtering mechanisms work.
    '''

    # POST
    compute_heads = heads.copy()
    compute_heads['Category'] = 'compute;scheme="http://schemas.ogf.org/occi/infrastructure#"'
    http = httplib2.Http()
    response, content = http.request(url, 'POST', headers = compute_heads)
    if not response['status'] == '200' or response['status'] == '202':
        logging.warn('Creation failed - this might be okay - please examine output!' + repr(response) + content)
        raise AttributeError("Test did no run completly!")
    compute_loc = response['location']

    network = heads.copy()
    network['Category'] = 'network;scheme="http://schemas.ogf.org/occi/infrastructure#"'
    http = httplib2.Http()
    response, content = http.request(url, 'POST', headers = network)
    if not response['status'] == '200' or response['status'] == '202':
        logging.warn('Creation failed - this might be okay - please examine output!' + repr(response) + content)
        raise AttributeError("Test did no run completly!")
    network_loc = response['location']

    # test if filtering works...
    filter_heads = heads.copy()
    filter_heads['Category'] = 'network;scheme="http://schemas.ogf.org/occi/infrastructure#"'
    http = httplib2.Http()
    response, content = http.request(url, 'GET', headers = filter_heads)
    if not response['x-occi-location'].find(compute_loc) is - 1:
        raise AttributeError('Filtering seems not have to be done reponse still include compute: ' + repr(response) + content)

    http = httplib2.Http()
    response, content = http.request(compute_loc, 'DELETE', headers = heads)
    if not response['status'] == '200':
        raise AttributeError('could not delete resource: ' + repr(response) + content)

    http = httplib2.Http()
    response, content = http.request(network_loc, 'DELETE', headers = heads)
    if not response['status'] == '200':
        raise AttributeError('could not delete resource: ' + repr(response) + content)

def test_location(url, heads):
    '''
    Do some ops on a location path.
    '''
    heads['Content-Type'] = 'text/occi'

    compute_heads = heads.copy()
    compute_heads['Category'] = 'compute;scheme="http://schemas.ogf.org/occi/infrastructure#"'
    http = httplib2.Http()
    response, content = http.request(url, 'POST', headers = compute_heads)
    if not response['status'] == '200' or response['status'] == '202':
        logging.warn('Creation failed - this might be okay - please examine output!' + repr(response) + content)
        raise AttributeError("Test did no run completly!")
    compute_loc = response['location']

    put_heads = heads.copy()
    put_heads['Category'] = 'my_stuff;scheme="http://example.com/occi#";location=/my_stuff/'
    http = httplib2.Http()
    response, content = http.request(url + '/-/', 'PUT', headers = put_heads)
    if not response['status'] == '200' or response['status'] == '202':
        raise AttributeError('Unable to create a user-defined mixin. Response: ' + repr(response) + content)

    put_heads = heads.copy()
    put_heads['X-OCCI-Location'] = compute_loc
    http = httplib2.Http()
    response, content = http.request(url + '/my_stuff/', 'PUT', headers = put_heads)
    if not response['status'] == '200' or response['status'] == '202':
        raise AttributeError('Unable to add a kind to a user-defined mixin. Response: ' + repr(response) + content)

    http = httplib2.Http()
    response, content = http.request(compute_loc, 'GET', headers = heads)
    if response['category'].find('my_stuff') is - 1:
        raise AttributeError('Mixin was not added to resource: ' + repr(response) + content)

    http = httplib2.Http()
    response, content = http.request(compute_loc, 'DELETE', headers = heads)
    if not response['status'] == '200':
        raise AttributeError('could not delete resource: ' + repr(response) + content)

    put_heads = heads.copy()
    put_heads['Category'] = 'my_stuff;scheme="http://example.com/occi#"'
    http = httplib2.Http()
    response, content = http.request(url + '/-/', 'DELETE', headers = put_heads)
    if not response['status'] == '200' or response['status'] == '202':
        raise AttributeError('Unable to delete a user-defined mixin. Response: ' + repr(response) + content)

def test_syntax(url, heads):
    '''
    Simple syntax checks - see if Category is setup correctly. 
    '''
    # TODO add checks for syntac of links, locations, attributes...

    regex = r'\w+;\bscheme=[a-z:./#"]*;\bclass="(?:action|kind|mixin)"'

    heads['Accept'] = 'text/plain'
    url = url + '/-/'
    http = httplib2.Http()
    response, content = http.request(url, 'GET', headers = heads)
    cat_rend = content.split('\n')[0].strip()

    cat_rend = cat_rend[10:]
    p = re.compile(regex)
    m = p.match(cat_rend)
    if m is None:
        raise AttributeError('There is an error in the syntax for rendering text/plain. Category should be setup like <term>;scheme="<url>";class=[kind,action,mixin]')

    heads['Accept'] = 'text/occi'
    http = httplib2.Http()
    response, content = http.request(url, 'GET', headers = heads)
    cat_rend = response['category'].strip()
    p = re.compile(regex)
    m = p.match(cat_rend)
    if m is None:
        raise AttributeError('There is an error in the syntax for rendering text/occi. Category should be setup like <term>;scheme="<url>";class=[kind,action,mixin]')

#===============================================================================
# Test runners...
#===============================================================================

class TextRunner(object):

    def __init__(self, url, username = None, password = None):
        if username is not None and password is not None:
            heads = cookie = get_session_cookie(url, username, password)
            heads = {'Cookie': cookie}
        else:
            heads = []

        print('Examining OCCI service at URL: ' + url)
        print('\n')
        print('NOTE: Passing all tests only indicates that the service')
        print('you are testing is OCCI compliant - IT DOES NOT GUARANTE IT!')
        print('\n')
        print('Version string the service reported: ' + get_version(url, heads))
        print('Number of registered categories: ' + str(len(get_categories(url, heads))))
        print('\n')

        self.run_tests(url, heads)

    def run_tests(self, url, heads):
        '''
        Run all the tests.
        '''
        self.run_single_test(test_version_information, url, heads, 'Verifing version information of the service')
        self.run_single_test(test_infrastructure_model_for_completness, url, heads, 'Verifing infrastructure model for completeness')
        self.run_single_test(test_accept_header, url, heads, 'Verifing correct handling of Accept headers')
        self.run_single_test(test_create_kinds, url, heads, 'Verifing creation of kinds in infra model')
        self.run_single_test(test_mixins, url, heads, 'Testing behaviour of used defined mixins')
        self.run_single_test(test_links, url, heads, 'Testing behaviour links between resources')
        self.run_single_test(test_actions, url, heads, 'Verifing that actions can be triggered  ')
        self.run_single_test(test_filter, url, heads, 'Testing filtering mechanisms on paths   ')
        self.run_single_test(test_location, url, heads, 'Verifing the behaviour on location paths')
        self.run_single_test(test_syntax, url, heads, 'Simple syntax checks for several renderings')

    def run_single_test(self, test, url, heads, label):
        '''
        run a single test.
        '''
        try:
            test(url, heads)
        except Exception as e:
            logging.warning(str(e))
            print label + '\t\t\tFailed'
        else:
            print label + '\t\t\tOK'

class GUIRunner(object):

    #===========================================================================
    # fields to set in the GUI
    #===========================================================================

    info_text = None

    def __init__(self, parent):
        '''
        Constructor.
        '''
        self.url = StringVar()
        self.login = IntVar()
        self.user = StringVar()
        self.password = StringVar()

        self.master = parent
        self.init_gui()

    def init_gui(self):
        '''
        Initialize a simple gui.
        '''
        top = Frame(self.master)
        top.grid(padx = 5, pady = 5)

        frame = Frame(top)
        frame.grid(column = 0, row = 0, columnspan = 2)

        text = Label(frame, text = 'OCCI service URL:')
        text.grid(column = 0, row = 0)

        self.url.set('http://localhost:8888')
        entry = Entry(frame, width = 25, textvariable = self.url)
        entry.grid(column = 1, row = 0)

        go = Button(frame, text = 'Go', command = self.run_tests)
        go.grid(column = 2, row = 0)

        reset = Button(frame, text = 'Reset', command = self.reset)
        reset.grid(column = 3, row = 0)

        login_frame = Frame(top, borderwidth = 2, relief = 'groove')
        login_frame.grid(column = 0, row = 1, sticky = W + E + N + S,
                         padx = 2, pady = 2)

        self.login.set(1)

        login_switch = Checkbutton(login_frame, text = 'Login required?',
                                   variable = self.login)
        login_switch.grid(column = 0, row = 0, columnspan = 2)

        self.user.set('foo')
        self.password.set('bar')

        user_text = Label(login_frame, text = 'Username:')
        user_text.grid(column = 0, row = 1, sticky = W)
        user_entry = Entry(login_frame, textvariable = self.user, width = 15)
        user_entry.grid(column = 1, row = 1)

        text = Label(login_frame, text = 'Password:')
        text.grid(column = 0, row = 2, sticky = W)
        entry = Entry(login_frame, textvariable = self.password, width = 15,
                      show = "*")
        entry.grid(column = 1, row = 2)

        info_frame = Frame(top, borderwidth = 2, relief = 'groove')
        info_frame.grid(column = 1, row = 1, sticky = W + E + N + S, padx = 2,
                        pady = 2)

        self.info_text = Label(info_frame, text = 'Please press "GO"')
        self.info_text.pack(side = 'top')

        test_frame = Frame(top, borderwidth = 2, relief = 'groove')
        test_frame.grid(column = 0, row = 2, columnspan = 2, padx = 2,
                        pady = 2)

        label = Label(test_frame, text = 'Checking for correct version information:')
        label.grid(column = 0, row = 0, sticky = W)

        self.version_test_label = Label(test_frame, text = '...')
        self.version_test_label.grid(column = 1, row = 0, sticky = W, padx = 3, pady = 3)

        label = Label(test_frame, text = 'Checking completeness of infrastructure model:')
        label.grid(column = 0, row = 1, sticky = W)

        self.infra_model_test_label = Label(test_frame, text = '...')
        self.infra_model_test_label.grid(column = 1, row = 1, sticky = W, padx = 3, pady = 3)

        label = Label(test_frame, text = 'Checking correct handling of Content-type/Accept headers:')
        label.grid(column = 0, row = 2, sticky = W)

        self.accept_header_test_label = Label(test_frame, text = '...')
        self.accept_header_test_label.grid(column = 1, row = 2, sticky = W, padx = 3, pady = 3)

        label = Label(test_frame, text = 'Testing instanciation of compute/storage/network kinds:')
        label.grid(column = 0, row = 3, sticky = W)

        self.creational_test_label = Label(test_frame, text = '...')
        self.creational_test_label.grid(column = 1, row = 3, sticky = W, padx = 3, pady = 3)

        label = Label(test_frame, text = 'Testing correct handling of user-defined mixins (tagging/grouping):')
        label.grid(column = 0, row = 4, sticky = W)

        self.mixin_test_label = Label(test_frame, text = '...')
        self.mixin_test_label.grid(column = 1, row = 4, sticky = W, padx = 3, pady = 3)

        label = Label(test_frame, text = 'Testing links between compute/storage compute/network:')
        label.grid(column = 0, row = 5, sticky = W)

        self.link_test_label = Label(test_frame, text = '...')
        self.link_test_label.grid(column = 1, row = 5, sticky = W, padx = 3, pady = 3)

        label = Label(test_frame, text = 'Triggering actions on compute/network/storage kinds:')
        label.grid(column = 0, row = 6, sticky = W)

        self.action_test_label = Label(test_frame, text = '...')
        self.action_test_label.grid(column = 1, row = 6, sticky = W, padx = 3, pady = 3)

        label = Label(test_frame, text = 'Testing filter mechanisms using Categories:')
        label.grid(column = 0, row = 7, sticky = W)

        self.filter_test_label = Label(test_frame, text = '...')
        self.filter_test_label.grid(column = 1, row = 7, sticky = W, padx = 3, pady = 3)

        label = Label(test_frame, text = 'Testing correct behaviour on location and "normal" paths:')
        label.grid(column = 0, row = 8, sticky = W)

        self.location_path_label = Label(test_frame, text = '...')
        self.location_path_label.grid(column = 1, row = 8, sticky = W, padx = 3, pady = 3)

        label = Label(test_frame, text = 'Simple syntax checks:')
        label.grid(column = 0, row = 9, sticky = W)

        self.syntax_test_label = Label(test_frame, text = '...')
        self.syntax_test_label.grid(column = 1, row = 9, sticky = W, padx = 3, pady = 3)

        label = Label(top, text = 'NOTE: Passing all tests only indicates that the service\nyou are testing is OCCI compliant - IT DOES NOT GUARANTE IT!')
        label.grid(column = 0, row = 4, columnspan = 2, padx = 5, pady = 5)

        quit_button = Button(top, text = 'Quit', command = self.quit)
        quit_button.grid(column = 1, row = 5, sticky = E, padx = 2)

    def run_tests(self):
        '''
        run a set of tests.
        '''
        url = self.url.get()
        if self.login.get() is 1:
            cookie = get_session_cookie(self.url.get(), self.user.get(),
                                        self.password.get())
            heads = {'Cookie': cookie}
        else:
            heads = {}

        # display basic information
        self.info_text.configure(text = 'Server version:\n'
                                    + get_version(url, heads)
                                    + '\nNumber of registered categories:\n'
                                    + str(len(get_categories(url, heads))),
                                    anchor = W, justify = LEFT)

        # run the tests...
        self.run_single_test(test_version_information, url, heads, self.version_test_label)
        self.run_single_test(test_infrastructure_model_for_completness, url, heads, self.infra_model_test_label)
        self.run_single_test(test_accept_header, url, heads, self.accept_header_test_label)
        self.run_single_test(test_create_kinds, url, heads, self.creational_test_label)
        self.run_single_test(test_mixins, url, heads, self.mixin_test_label)
        self.run_single_test(test_links, url, heads, self.link_test_label)
        self.run_single_test(test_actions, url, heads, self.action_test_label)
        self.run_single_test(test_filter, url, heads, self.filter_test_label)
        self.run_single_test(test_location, url, heads, self.location_path_label)
        self.run_single_test(test_syntax, url, heads, self.syntax_test_label)

    def run_single_test(self, test, url, heads, label):
        '''
        Run a single test and display the outcome.
        '''
        try:
            test(url, heads)
        except Exception as ae:
            logging.warn(str(ae))
            label.configure(text = 'Failed', background = 'red')
        else:
            label.configure(text = 'OK')

    def reset(self):
        '''
        Reset the gui...
        '''
        self.info_text.configure(text = 'Please press "GO"')
        self.version_test_label.configure(text = '...')
        self.infra_model_test_label.configure(text = '...')
        self.accept_header_test_label.configure(text = '...')
        self.creational_test_label.configure(text = '...')
        self.mixin_test_label.configure(text = '...')
        self.link_test_label.configure(text = '...')
        self.action_test_label.configure(text = '...')
        self.filter_test_label.configure(text = '...')
        self.location_path_label.configure(text = '...')
        self.syntax_test_label.configure(text = '...')

    def quit(self):
        '''
        Quit the master loop.
        '''
        self.master.quit()

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "url=", "username=", "password=", "gui"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)
    username = None
    password = None
    use_gui = False
    url = 'http://localhost:8888'
    for o, a in opts:
        if o in ("-h", "--help"):
            print ('Usage: test_occi.py url=<URL> [<--username=foo>, <--password=bar>] or test_occi.py --gui')
            sys.exit()
        elif o in ("-u", "--url"):
            url = a
        elif o in ("--username"):
            username = a
        elif o in ("--password"):
            password = a
        elif o in ("--gui"):
            use_gui = True
        else:
            assert False, "unhandled option"

    if use_gui is True:
        root = Tk()
        root.title('OCCI compliance test')
        gui = GUIRunner(root)
        root.mainloop()
    else:
        TextRunner(url, username, password)
