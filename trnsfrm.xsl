<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
                xmlns:xs="http://www.w3.org/2001/XMLSchema"
                exclude-result-prefixes="xs">
<xsl:output method="html" indent="yes" encoding="UTF-8"/>

<xsl:variable name="lf">    <!-- print newline -->
<xsl:text>
</xsl:text>
</xsl:variable>

<xsl:variable name="ampersand"><![CDATA[&]]></xsl:variable> <!-- print ampersand -->

<xsl:template match="table">
    <!-- TABLE DETAILS -->
    <!--<xsl:comment> DETAIL OF TABLE <xsl:value-of select="@tableid"/> </xsl:comment>-->
    <xsl:value-of select="$lf"/>    <!-- newline -->
    <div>
        <xsl:attribute name="class">my-container-email dir-bar</xsl:attribute>
        <xsl:attribute name="id">current-table<xsl:value-of select="@tableid"/></xsl:attribute>
        <xsl:value-of select="$lf"/>    <!-- newline -->
		<div>
            <xsl:attribute name="class">container-fluid table-cell</xsl:attribute>
            <xsl:attribute name="id">table</xsl:attribute>
            <xsl:value-of select="$lf"/>    <!-- newline -->
            <xsl:value-of select="$lf"/>    <!-- newline -->
            <xsl:apply-templates select="definition"/>
            <xsl:apply-templates select="rows/row"/>
            <div class="create">
				<button>
                    <xsl:attribute name="class">btn btn-primary btn-align btn-text</xsl:attribute>
                    <xsl:attribute name="onclick">addNewRow();</xsl:attribute>
                    <i class="fas fa-plus-circle"></i><xsl:value-of select="$ampersand" disable-output-escaping="yes"/>nbsp;Add</button>
				<xsl:value-of select="$lf"/>    <!-- newline -->
				<button>
                    <xsl:attribute name="class">btn btn-primary btn-align btn-text</xsl:attribute>
                    <xsl:attribute name="onclick">requestTableNames();</xsl:attribute>
                    <i class="fas fa-arrow-left"></i><xsl:value-of select="$ampersand" disable-output-escaping="yes"/>nbsp;Back</button>
			</div>
        </div>
    </div>
</xsl:template>

<!-- Definitions -->
<xsl:template match="definition">
    <div>
        <xsl:attribute name="class">row dir-bar my-border-users no-margin</xsl:attribute>
        <xsl:value-of select="$lf"/>    <!-- newline -->
        <div>
            <xsl:attribute name="id">1</xsl:attribute>
            <xsl:attribute name="class">row dir-bar top no-margin center</xsl:attribute>
            <xsl:value-of select="$lf"/>    <!-- newline -->
            <xsl:apply-templates select="def"/>
        </div>
        <div class="col-lg-4"></div>
        <xsl:value-of select="$lf"/>    <!-- newline -->
    </div>
    <xsl:value-of select="$lf"/>    <!-- newline -->
    <xsl:value-of select="$lf"/>    <!-- newline -->
</xsl:template>

<xsl:template match="def">
    <xsl:choose>
        <xsl:when test=". = 'id'">
            <span><xsl:attribute name="class">enum-top-db</xsl:attribute>#</span>
            <xsl:value-of select="$lf"/>    <!-- newline -->
        </xsl:when>
        <xsl:otherwise>
            <span> <!-- 93/(column count + 1) -->
                <xsl:attribute name="class">column-top</xsl:attribute>
                <xsl:attribute name="style">width: <xsl:value-of select="93 div /table/definition/@length"/>%</xsl:attribute>
                <xsl:value-of select="."/>
            </span>
            <xsl:value-of select="$lf"/>    <!-- newline -->
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<!-- Rows -->
<xsl:template match="rows/row">
    <!--<xsl:comment> <xsl:value-of select="position()"/>. RECORD </xsl:comment>-->
    <xsl:value-of select="$lf"/>    <!-- newline -->
    <div class="row dir-bar my-border-db no-margin">
        <xsl:value-of select="$lf"/>    <!-- newline -->
        <div class="row dir-bar no-margin center">
            <xsl:value-of select="$lf"/>    <!-- newline -->
            <xsl:apply-templates select="record"/>
            <button>
                <xsl:attribute name="class">btn btn-align rename-align btn-secondary btn-text btn-table-edit</xsl:attribute>
                <xsl:attribute name="onclick">sendEditRow(<xsl:value-of select="position()-1"/>);</xsl:attribute>
                <i class="fas fa-edit"></i></button>
            <xsl:value-of select="$lf"/>    <!-- newline -->
            <button>
                <xsl:attribute name="class">btn btn-align btn-warning btn-text btn-table-del</xsl:attribute>
                <xsl:attribute name="onclick">sendDeleteRow(<xsl:value-of select="position()-1"/>);</xsl:attribute>
                <i class="fas fa-minus-circle"></i></button>
        </div>
        <div class="col-lg-4"></div>
    </div>
    <xsl:value-of select="$lf"/>    <!-- newline -->
    <xsl:value-of select="$lf"/>    <!-- newline -->
</xsl:template>

<xsl:template match="record">
    <xsl:choose>
        <xsl:when test="position() = 1">
            <span class="enum-db">#<xsl:value-of select="."/></span>
            <xsl:value-of select="$lf"/>    <!-- newline -->
        </xsl:when>
        <xsl:otherwise>
            <span> <!-- 93/(column count + 1) -->
                <xsl:attribute name="class">column</xsl:attribute>
                <xsl:attribute name="style">width: <xsl:value-of select="93 div /table/definition/@length"/>%</xsl:attribute>
                <xsl:value-of select="."/>
            </span>
            <xsl:value-of select="$lf"/>    <!-- newline -->
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

</xsl:stylesheet>



<!--
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

<xsl:template match="definition">
    <tr>
        <xsl:apply-templates select="def"/>
    </tr>
</xsl:template>

<xsl:template match="def">
    <th><xsl:value-of select="."/></th>
</xsl:template>


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
-->
