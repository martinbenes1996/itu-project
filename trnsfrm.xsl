<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
                xmlns:xs="http://www.w3.org/2001/XMLSchema"
                exclude-result-prefixes="xs">
<xsl:output method="html" ident="yes" encoding="UTF-8"/>

<xsl:template match="database">
    <html>
        <head></head>
        <body>
            <xsl:apply-templates select="table"/>
        </body>
    </html>
</xsl:template>

<xsl:template match="table">
    <p align="center"><xsl:value-of select="@tablename"/></p>
    <table align="center">
        <xsl:apply-templates select="definition"/>
        <xsl:apply-templates select="rows/row"/>
    </table>
</xsl:template>

<!-- Definitions -->
<xsl:template match="definition">
    <tr>
        <xsl:apply-templates select="def"/>
    </tr>
</xsl:template>

<xsl:template match="def">
    <th><xsl:value-of select="."/></th>
</xsl:template>

<!-- Rows -->
<xsl:template match="rows/row">
    <tr>
        <xsl:apply-templates select="record"/>
    </tr>
</xsl:template>

<xsl:template match="record">
    <td>
        <xsl:value-of select="."/>
    </td>
</xsl:template>

</xsl:stylesheet>
