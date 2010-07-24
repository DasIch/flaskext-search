#!/usr/bin/env python2
# coding: utf-8
"""
    flaskext-install
    ~~~~~~~~~~~~~~~~

    :copyright: 2010 by Daniel Neuhäuser
    :license: BSD, see LICENSE for details
"""
import re
import json
import sys
from optparse import OptionParser
from functools import partial
from httplib import HTTPConnection
from string import Template
from itertools import ifilter

from lxml.html import fromstring as parse_html

extension_desc_template = Template(u"""\
$name$approved by $author

$description

$links""")

fix_whitespace = partial(re.compile(ur'\s+').sub, u' ')

def render_extension_description(extension):
    links = ['docs', 'github', 'bitbucket']
    return extension_desc_template.substitute(dict(
        name=extension['name'],
        approved=u'*' if extension['approved'] else u'',
        author=extension['author'],
        website=extension['website'],
        description=extension['description'],
        links=u'\n'.join(
            u'{0}: {1}'.format(name, extension[name])
            for name in links if extension[name]
        )
    ))

class FlaskAPI(object):
    api_url = 'flask.pocoo.org'

    def __init__(self):
        self.connection = HTTPConnection(self.api_url)

    def make_request(self, path, method='GET'):
        self.connection.request(method, path, headers={
            'Accept': 'application/json'
        })
        return self.connection.getresponse()

    def get_extensions(self, with_plain_descriptions=True):
        extensions = json.loads(
            self.make_request('/extensions/').read()
        )['extensions']
        if with_plain_descriptions:
            for extension in extensions:
                extension['description'] = fix_whitespace(parse_html(
                    extension['description']
                ).text_content()).strip()
        return extensions

def main(argv=sys.argv[1:]):
    parser = OptionParser()
    parser.add_option(
        '-l', '--list',
        help='Lists every available extension.',
        dest='list',
        action='store_true'
    )
    parser.add_option(
        '-a', '--approved-only',
        help='List only approved extensions.',
        dest='approved',
        action='store_true'
    )
    parser.add_option(
        '-s', '--search',
        help='Search extension by name',
        dest='search',
    )
    parser.add_option(
        '--search-desc',
        help='Search extension by description',
        dest='search_desc'
    )
    if not argv:
        parser.print_help()
    options, args = parser.parse_args(argv)

    api = FlaskAPI()
    if options.list and options.search:
        parser.error('--search and --list are not compatible to each other')
    elif any([options.list, options.search, options.search_desc]):
        extensions = api.get_extensions()
        if options.search or options.search_desc:
            if options.search:
                key = 'name'
                phrase = options.search.lower()
            else:
                key = 'description'
                phrase = options.search_desc.lower()
            extensions = ifilter(
                lambda x: phrase in x[key].lower(),
                extensions
            )
        for extension in extensions:
            if not options.approved or options.approved and extension['approved']:
                print render_extension_description(extension) + '\n'

if __name__ == '__main__':
    main()
