Open Cloud Computing Interface (OCCI)
Editor Getting Started Guide

Overview
========

"DocBook is a semantic markup language for technical documentation. It was originally intended for writing technical documents related to computer hardware and software but it can be used for any other sort of documentation."

It was selected for OCCI in order to allow us to maintain a single source and publish to multiple formats:
 * HyperText Markup Language (HTML)
 * Portable Document Format (PDF)
 * Plain Text (TXT)

Getting Started
===============

You will need the following to get started editing OCCI:
 * Mercurial (http://mercurial.selenic.com/)
 * XML Editor (XMLmind: http://www.xmlmind.com/xmleditor/download.shtml)

1. Download and install Mercurial and your preferred XML editor.
2. Get a local copy of the occi repository with this command:
     hg clone https://occi.googlecode.com/hg/ occi
3. Edit the DocBook source (Hint: TDG5 is a great resource both for getting started and as a reference)

Checking In
===========

If you want to check in changes you'll likely need to create a ~/.hgrc file something like this:

[ui]
username = John Citizen <john@example.com>

[auth]
occi.prefix = occi.googlecode.com/hg/
occi.username = john@example.com
occi.password = LF3W8dKKJG5X7
occi.schemes = https

You can now commit your changes (with a useful changelog entry please!) using:
      hg ci
      hg push

Rendering
=========

You will need DocBook tools if you want to render the DocBook XML to other formats (which you should do each time you check in changes):
 * DocBook XSLT (http://sourceforge.net/projects/docbook/files/docbook-xsl-ns/)
 * Apache FOP Binaries (http://www.apache.org/dyn/closer.cgi/xmlgraphics/fop)

Under Mac OS X (using the default Makefile):
1. Extract docbook-xsl-ns into ~/Library/XML/XSL
2. Extract Apache FOP and copy build/fop.jar and lib/*.jar into /Library/Java/Extensions

Then whenever you make changes simply run "make" to generate new HTML and PDF versions.

Resources
=========
 * Official Site (http://www.docbook.org/)
 * Wikipedia - DocBook (http://en.wikipedia.org/wiki/DocBook)
 * DocBook 5.0 - The Definitive Guide (http://www.docbook.org/tdg5/en/html/docbook.html)
 * DocBook XSL: The Complete Guide (http://www.sagehill.net/docbookxsl/index.html)
