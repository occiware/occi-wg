<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:atom="http://www.w3.org/2005/Atom"
    xmlns:occi="http://purl.org/occi"
    xmlns:compute="http://purl.org/occi/compute"
    xmlns:network="http://purl.org/occi/network"
    xmlns:storage="http://purl.org/occi/storage"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <!-- 
        Open Cloud Computing Interface (OCCI) XSLT Transformations
        Copyright (C) 2009 Sam Johnston
        
        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU Affero General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.
        
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU Affero General Public License for more details.
        
        You should have received a copy of the GNU Affero General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
    -->
    <xsl:output method="text"/>
    <xsl:strip-space elements="*"/> 
    <xsl:output method="text"/> 
    <xsl:template match="*"/> 
    
    <xsl:template match="atom:feed"> 
        <xsl:text>[</xsl:text> 
        <xsl:value-of select="tokenize(atom:id,':')[3]"/> 
        <xsl:text>]&#10;</xsl:text> 
        <xsl:apply-templates/> 
    </xsl:template> 
    
    <xsl:template match="atom:entry"> 
        <xsl:text>&#10;[</xsl:text> 
        <xsl:value-of select="tokenize(atom:id,':')[3]"/> 
        <xsl:text>]&#10;</xsl:text> 
        <xsl:text>title|</xsl:text><xsl:value-of select="atom:title"></xsl:value-of><xsl:text>&#10;</xsl:text> 
        <xsl:text>summary|</xsl:text><xsl:value-of select="atom:summary"></xsl:value-of><xsl:text>&#10;</xsl:text> 
        <xsl:apply-templates/> 
        <xsl:text>etag|</xsl:text><xsl:value-of select="@occi:etag"></xsl:value-of><xsl:text>&#10;</xsl:text> 
    </xsl:template> 
    
    <xsl:template match="atom:updated|occi:*|compute:*|network:*">
        <xsl:value-of select="local-name()"/>|<xsl:apply-templates/> 
        <xsl:text>&#10;</xsl:text> 
    </xsl:template>

    <xsl:template match="atom:link">
            <xsl:text>link|</xsl:text>
            <xsl:value-of select="@rel"/>
<!--            <xsl:if test="not(@rel)">alternate</xsl:if>
            <xsl:text>|</xsl:text>
            <xsl:value-of select="@type"/>-->
<!--            <xsl:if test="not(@type)"><xsl:text>text/html</xsl:text></xsl:if>-->
            <xsl:text>|</xsl:text>
            <xsl:value-of select="@title"/>
            <xsl:text>|</xsl:text>
            <xsl:value-of select="@href"/> 
            <xsl:text>&#10;</xsl:text>
    </xsl:template>

    <xsl:template match="atom:category"> 
        <xsl:text>category|</xsl:text><xsl:value-of select="@term"></xsl:value-of><xsl:text>&#10;</xsl:text> 
        <xsl:apply-templates/> 
    </xsl:template> 
    
</xsl:stylesheet>
