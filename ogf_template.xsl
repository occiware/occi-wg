<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" version="1.0">

  <!-- import org template... -->
  <xsl:import href="/usr/share/xml/docbook/stylesheet/nwalsh/fo/docbook.xsl" />

  <!-- some general parameters -->
  <xsl:param name="header.rule">
    0
  </xsl:param>
  <xsl:param name="footer.rule">
    0
  </xsl:param>
  <xsl:param name="generate.toc" select="'article toc'" />
  <xsl:param name="process.empty.source.toc" select="1"></xsl:param>
  <xsl:param name="section.autolabel">
    1
  </xsl:param>
  <xsl:param name="chapter.autolabel">
    1
  </xsl:param>
  <xsl:param name="section.autolabel.max.depth">
    4
  </xsl:param>
  <!--
	<xsl:param name="use.extensions" select="1"/>
	<xsl:param name="linenumbering.extension" select="0"></xsl:param>
-->
  <!--
	<xsl:param name="generate.toc"></xsl:param>
	<xsl:param name="process.empty.source.toc" select="1"></xsl:param>
	<xsl:param name="generate.section.toc.level" select="2"></xsl:param>
-->

  <!-- general use sans-serif font-->
  <xsl:attribute-set name="root.properties">
    <xsl:attribute name="font-family">sans-serif</xsl:attribute>
  </xsl:attribute-set>

  <!-- font adjust -->
  <xsl:attribute-set name="section.title.level1.properties">
    <xsl:attribute name="font-size">10pt</xsl:attribute>
  </xsl:attribute-set>

  <xsl:attribute-set name="section.title.level2.properties">
    <xsl:attribute name="font-size">10pt</xsl:attribute>
    <xsl:attribute name="font-weight">normal</xsl:attribute>
  </xsl:attribute-set>

  <xsl:attribute-set name="section.title.level3.properties">
    <xsl:attribute name="font-size">10pt</xsl:attribute>
    <xsl:attribute name="font-weight">normal</xsl:attribute>
  </xsl:attribute-set>

  <xsl:attribute-set name="section.title.level4.properties">
    <xsl:attribute name="font-size">10pt</xsl:attribute>
    <xsl:attribute name="font-weight">normal</xsl:attribute>
    <xsl:attribute name="text-decoration">underline</xsl:attribute>
  </xsl:attribute-set>

  <xsl:attribute-set name="header.content.properties">
    <xsl:attribute name="font-family">sans-serif</xsl:attribute>
    <xsl:attribute name="font-size">10pt</xsl:attribute>
  </xsl:attribute-set>

  <xsl:attribute-set name="footer.content.properties">
    <xsl:attribute name="font-family">sans-serif</xsl:attribute>
    <xsl:attribute name="font-size">10pt</xsl:attribute>
  </xsl:attribute-set>

  <xsl:attribute-set name="component.title.properties">
    <xsl:attribute name="font-size">10pt</xsl:attribute>
    <xsl:attribute name="text-align">left</xsl:attribute>
  </xsl:attribute-set>

  <xsl:attribute-set name="formal.title.properties" use-attribute-sets="normal.para.spacing">
    <xsl:attribute name="font-size">8pt</xsl:attribute>
    <xsl:attribute name="space-after.minimum">0.4em</xsl:attribute>
    <xsl:attribute name="space-after.optimum">0.6em</xsl:attribute>
    <xsl:attribute name="space-after.maximum">0.8em</xsl:attribute>
  </xsl:attribute-set>

  <!-- no author -->
  <xsl:template match="author" mode="titlepage.mode">
    <fo:block>
      <xsl:text></xsl:text>
    </fo:block>
  </xsl:template>

  <!--
    <xsl:template match="para/text()"> <xsl:call-template name="line.numbering"> <xsl:with-param name="content" select="."/> <xsl:with-param name="count" select="1"/> </xsl:call-template> </xsl:template> <xsl:template name="line.numbering"> <xsl:param name="content" select="."/> <xsl:param name="count" select="1"/> <xsl:number value="$count" format="01 "/> <xsl:choose> <xsl:when test="contains($content, '&#xA;')"> <xsl:value-of select="substring-before($content, '&#xA;')"/> <xsl:text>&#xA;</xsl:text> <xsl:variable name="rest" select="substring-after($content, '&#xA;')"/> <xsl:if test="string-length($rest)"> <xsl:call-template name="line.numbering"> <xsl:with-param name="content" select="$rest"/> <xsl:with-param name="count" select="$count + 1"/> </xsl:call-template> </xsl:if> </xsl:when> <xsl:otherwise> <xsl:value-of select="$content"/> </xsl:otherwise> </xsl:choose> </xsl:template>
  -->


  <!-- modified header -->
  <xsl:template name="header.content">
    <xsl:param name="position" select="''" />

    <fo:block>
      <xsl:choose>
        <xsl:when test="$position = 'left'">

          <fo:block>
            <xsl:text>GFD-C</xsl:text>
          </fo:block>
          <fo:block>
            Open Cloud Computing Interface
                </fo:block>
        </xsl:when>

        <xsl:when test="$position = 'center'">
        </xsl:when>

        <xsl:when test="$position = 'right'">
          <fo:block>
            <xsl:text>Open Cloud Computing Interface</xsl:text>
          </fo:block>
          <fo:block>
            <xsl:text>September 16, 2009</xsl:text>
          </fo:block>
        </xsl:when>
      </xsl:choose>
    </fo:block>
  </xsl:template>

  <!-- modified footer -->
  <xsl:template name="footer.content">
    <xsl:param name="position" select="''" />

    <fo:block>
      <xsl:choose>
        <xsl:when test="$position = 'left'">
          <xsl:text>occi-wg@ogf.org</xsl:text>
        </xsl:when>

        <xsl:when test="$position = 'center'">
        </xsl:when>

        <xsl:when test="$position = 'right'">
          <fo:page-number />
        </xsl:when>
      </xsl:choose>
    </fo:block>
  </xsl:template>

</xsl:stylesheet> 
