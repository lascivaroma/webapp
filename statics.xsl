<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:foo="http://foo.bar"
    exclude-result-prefixes="xs"
    version="1.0">
    <xsl:output encoding="UTF-8" method="html"/>
    <xsl:template match="div[@type='fragment']">
        <div class="fragment">
            <h2><xsl:apply-templates select="bibl[@type='source']"/></h2>
            <blockquote>
                <xsl:apply-templates select="quote/w"/>
            </blockquote>
            <dl>
                <dt>Bibliography</dt>
                <xsl:apply-templates select="bibl[not(@type='source')]"/>
                <dt>Tags</dt>
                <xsl:for-each select="foo:get_tags(@ana)">
                    <a href="{foo:url_for_tags(current())}" class="btn btn-sm btn-success"><xsl:value-of select="current()"/></a><xsl:text> </xsl:text>
                </xsl:for-each>
            </dl>
        </div>
    </xsl:template>
    <xsl:template match="@ana">
        <dd><xsl:value-of select="."/></dd>
    </xsl:template>
    <xsl:template match="w">
        <span class="word">
            <xsl:choose>
                <xsl:when test="@ana">
                    <xsl:attribute name="class">word analyzed</xsl:attribute>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:attribute name="class">word</xsl:attribute>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:apply-templates/>
        </span>
        <xsl:text> </xsl:text>
    </xsl:template>
    <xsl:template match="bibl">
        <xsl:apply-templates select="author"/>
        <xsl:apply-templates select="title"/>
        <xsl:apply-templates select="biblScope"/>
    </xsl:template>
    <xsl:template match="author">
        <xsl:apply-templates />,
    </xsl:template>
    <xsl:template match="persName[@xml:lang='eng']"/>
    <xsl:template match="idno[text() = 'nan']"/>
    <xsl:template match="idno[text() != 'nan']">
        <a href="{./text()}" title="{@type}">@</a><xsl:text> </xsl:text>
    </xsl:template>
    <xsl:template match="title">
        <i><xsl:apply-templates /></i>
    </xsl:template>
    <xsl:template match="biblScope">, <xsl:apply-templates />
    </xsl:template>
    <xsl:template match="bibl[not(@type='source')]">
        <dd>
            <xsl:apply-templates select="author"/>
            <xsl:apply-templates select="title"/>
            <xsl:apply-templates select="biblScope"/>
            <xsl:text> - </xsl:text><a href="{foo:url_for_bibl(@ref)}">Link</a>
        </dd>
    </xsl:template>
</xsl:stylesheet>