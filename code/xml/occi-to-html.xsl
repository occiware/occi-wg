<?xml version="1.0" encoding="utf-8"?> 
<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:a="http://www.w3.org/2005/Atom" 
    xmlns:xhtml="http://www.w3.org/1999/xhtml" 
    xmlns="http://www.w3.org/1999/xhtml" 
    exclude-result-prefixes="a xhtml"> 
    <xsl:output method="xml" encoding="utf-8" 
        doctype-public="-//W3C//DTD XHTML 1.1//EN" 
        doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"/> 
    <xsl:template match="*"/><!-- Ignore unknown elements --> 
    <xsl:template match="*" mode="links"/> 
    <xsl:template match="*" mode="categories"/> 
    <xsl:template match="a:feed"> 
        <html xml:lang="en"> 
            <head> 
                <title><xsl:value-of select="a:title"/></title>
                <link href="http://occi.googlecode.com/svn/trunk/xml/occi.css" rel="stylesheet" type="text/css" />
            </head> 
            <body>
                <xsl:if test="a:logo"><img src="{a:logo}" height="100px" /></xsl:if>
                <h1><xsl:apply-templates select="a:title" mode="text-construct"/></h1> 
                <xsl:apply-templates/> 
                <p>Feed ID: <xsl:value-of select="a:id"/></p>
                <p>Author: <xsl:apply-templates select="a:author"/></p>
                <p>Feed updated: <xsl:value-of select="a:updated"/></p> 
                <xsl:apply-templates/> 
            </body> 
        </html> 
    </xsl:template>
    <xsl:template match="a:author"> 
		<div class="vcard">
		    <a class="fn org url" href="{child::a:uri}"><xsl:value-of select="child::a:name"/></a> &lt;<a class="email" href="mailto:{child::a:email}"><xsl:value-of select="child::a:email"/></a>&gt;
		</div> 
    </xsl:template>  
    <xsl:template match="a:summary"> 
        <div class="summary"> 
            <xsl:apply-templates select="." mode="text-construct"/> 
        </div> 
    </xsl:template> 
    <xsl:template match="a:content"> 
        <div class="content"> 
            <xsl:apply-templates select="." mode="text-construct"/> 
        </div> 
    </xsl:template> 
    <xsl:template match="a:entry"> 
        <div class="entry"> 
            <h2><xsl:apply-templates select="a:title" mode="text-construct"/></h2> 
            <div class="id">Entry ID: <xsl:value-of select="a:id"/></div> 
            <div class="updated">Entry updated: <xsl:value-of select="a:updated"/></div> 
            <div class="links"> 
                <xsl:text/>Links: <xsl:apply-templates select="a:link" mode="links"/> 
            </div> 
            <div class="categories"> 
                <xsl:text>Categories: </xsl:text> 
                <xsl:apply-templates select="a:category" mode="categories"/> 
            </div> 
            <xsl:apply-templates/> 
        </div> 
    </xsl:template> 
    <xsl:template match="a:link" mode="links"> 
        <xsl:if test="@rel='http://purl.org/occi/network#interface'"><img src="http://occitest.appspot.com/static/images/world.png" /></xsl:if> 
        <xsl:if test="@rel='http://purl.org/occi/storage#device'"><img src="http://occitest.appspot.com/static/images/drive.png" /></xsl:if> 
        <a href="{@href}"> 
            <!--<xsl:value-of select="@rel"/>-->
            <xsl:if test="not(@rel)">[generic link]</xsl:if> 
            <xsl:if test="@type"> 
                <xsl:text> (</xsl:text><xsl:value-of select="@type"/><xsl:text>): </xsl:text> 
            </xsl:if> 
            <xsl:value-of select="@title"/> 
        </a> 
        <xsl:if test="position() != last()"> 
            <xsl:text> | </xsl:text> 
        </xsl:if> 
    </xsl:template> 
    <xsl:template match="a:category" mode="categories"> 
        <xsl:value-of select="@term"/> 
        <xsl:if test="position() != last()"> 
            <xsl:text> | </xsl:text> 
        </xsl:if> 
    </xsl:template> 
    <xsl:template match="*[@type='text']|*[not(@type)]" mode="text-construct"> 
        <xsl:value-of select="node()"/> 
    </xsl:template> 
    <xsl:template match="*[@type='xhtml']" mode="text-construct"> 
        <xsl:copy-of select="node()"/> 
    </xsl:template> 
</xsl:stylesheet> 
