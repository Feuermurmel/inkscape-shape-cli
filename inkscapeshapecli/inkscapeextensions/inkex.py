"""
inkex.py
A helper module for creating Inkscape extensions

Copyright (C) 2005,2010 Aaron Spike <aaron@ekips.org> and contributors

Contributors:
  Aurélio A. Heckert <aurium(a)gmail.com>
  Bulia Byak <buliabyak@users.sf.net>
  Nicolas Dufour, nicoduf@yahoo.fr
  Peter J. R. Moulder <pjrm@users.sourceforge.net>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
import copy
import gettext
import os
import sys

from lxml import etree


# a dictionary of all of the xmlns prefixes in a standard inkscape doc
NSS = {
'sodipodi' :'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
'cc'       :'http://creativecommons.org/ns#',
'ccOLD'    :'http://web.resource.org/cc/',
'svg'      :'http://www.w3.org/2000/svg',
'dc'       :'http://purl.org/dc/elements/1.1/',
'rdf'      :'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
'inkscape' :'http://www.inkscape.org/namespaces/inkscape',
'xlink'    :'http://www.w3.org/1999/xlink',
'xml'      :'http://www.w3.org/XML/1998/namespace'
}


def localize():
    domain = 'inkscape'
    if sys.platform.startswith('win'):
        import locale
        current_locale, encoding = locale.getdefaultlocale()
        os.environ['LANG'] = current_locale
        try:
            localdir = os.environ['INKSCAPE_LOCALEDIR']
            trans = gettext.translation(domain, localdir, [current_locale], fallback=True)
        except KeyError:
            trans = gettext.translation(domain, fallback=True)
    elif sys.platform.startswith('darwin'):
        try:
            localdir = os.environ['INKSCAPE_LOCALEDIR']
            trans = gettext.translation(domain, localdir, fallback=True)
        except KeyError:
            try:
                localdir = os.environ['PACKAGE_LOCALE_DIR']
                trans = gettext.translation(domain, localdir, fallback=True)
            except KeyError:
                trans = gettext.translation(domain, fallback=True)
    else:
        try:
            localdir = os.environ['PACKAGE_LOCALE_DIR']
            trans = gettext.translation(domain, localdir, fallback=True)
        except KeyError:
            trans = gettext.translation(domain, fallback=True)
    #sys.stderr.write(str(localdir) + "\n")
    trans.install()


def errormsg(msg):
    """Intended for end-user-visible error messages.

       (Currently just writes to stderr with an appended newline, but could do
       something better in future: e.g. could add markup to distinguish error
       messages from status messages or debugging output.)

       Note that this should always be combined with translation:

         import inkex
         ...
         inkex.errormsg(_("This extension requires two selected paths."))
    """
    print(msg, file=sys.stderr)


def addNS(tag, ns=None):
    val = tag
    if ns is not None and len(ns) > 0 and ns in NSS and len(tag) > 0 and tag[0] != '{':
        val = "{%s}%s" % (NSS[ns], tag)
    return val


class Effect:
    """A class for creating Inkscape SVG Effects"""

    def __init__(self):
        self.document = None
        self.original_document = None
        self.svg_file = None

    def effect(self):
        """Apply some effects on the document. Extensions subclassing Effect
        must override this function and define the transformations
        in it."""
        pass

    def parse(self, filename=None):
        """Parse document in specified file or on stdin"""

        # First try to open the file from the function argument
        if filename is not None:
            try:
                stream = open(filename, 'r')
            except IOError:
                errormsg("Unable to open specified file: %s" % filename)
                sys.exit()

        # If it wasn't specified, try to open the file specified as
        # an object member
        elif self.svg_file is not None:
            try:
                stream = open(self.svg_file, 'r')
            except IOError:
                errormsg("Unable to open object member file: %s" % self.svg_file)
                sys.exit()

        # Finally, if the filename was not specified anywhere, use
        # standard input stream
        else:
            stream = sys.stdin

        p = etree.XMLParser(huge_tree=True)
        self.document = etree.parse(stream, parser=p)
        self.original_document = copy.deepcopy(self.document)
        stream.close()

    def affect(self, svg_file):
        """Affect an SVG document with a callback effect"""
        self.svg_file = svg_file
        localize()
        self.parse()
        self.effect()
