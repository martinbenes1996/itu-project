import xml.etree.ElementTree as ET
#from lxml import etree as ET
import os
import datetime
import re

# ------------------------------------------------------------------------
#         MODULE FOR STORING INFORMATION (XML) FOR ITU PROJECT
# ------------------------------------------------------------------------
'''
    This module uses folder named XML located in the same directory.

    Functions mostly do not return value.
    Exceptions can be raised:
        AlreadyExistsError         -> user or entity already exists
        DoesNotExistError          -> user or entity does not exist
        WrongTypeError             -> trying to put files into another file, incompatible file/directory types
        IncompatibleRowDataError   -> definition of a table incompatible with provided data
        TableNotFoundError         -> table was not found, nothing happened
        NameContainsWrongCharError -> name of files/directories must contain only [a-zA-Z0-9_.]+, empty strings are not allowed

    Other exceptions might occur too! (strings...)
'''
# FTP, DNS, email, database, user
# , pretty_print=True

class AlreadyExistsError(Exception):
    pass
class DoesNotExistError(Exception):
    pass
class WrongTypeError(Exception):
    pass
class IncompatibleRowDataError(Exception):
    pass
class TableNotFoundError(Exception):
    pass
class NameContainsWrongCharError(Exception):
    pass

def CreateProject(name, owner="unknown"):
    ''' Register a new project.
        name  -> name of the project
        owner -> user who created it (to set the 'owner' attribute), default value is "unknown"
    '''
    if os.path.exists("XML/"+str(name)+".xml"):
        raise AlreadyExistsError

    root = ET.Element("project", name=str(name))

    ftp = ET.SubElement(root, "FTP")
    ET.SubElement(ftp, "home", type='d', size='0', date=str(datetime.datetime.now().date()), owner=str(owner))
    ET.SubElement(root, "DNS")
    ET.SubElement(root, "database")
    ET.SubElement(root, "emails")
    ET.SubElement(root, "users")

    tree = ET.ElementTree(root)
    tree.write("XML/"+str(name)+".xml", encoding='UTF-8', xml_declaration=True)

def DeleteProject(name):
    ''' Delete project.
        name -> name of the project
    '''
    if os.path.exists("XML/"+str(name)+".xml"):
        os.remove("XML/"+str(name)+".xml")

def RenameProject(projName, newName):
    ''' Register a new project.
        projName   -> name of the project
        newName    -> new name of the project
    '''
    if os.path.exists("XML/"+str(newName)+".xml"):
        raise AlreadyExistsError

    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    root.attrib['name'] = str(newName)

    tree.write("XML/"+str(newName)+".xml", encoding='UTF-8', xml_declaration=True)
    DeleteProject(str(projName))

# --------------------------- FTP ------------------------------------------------
def FindInXML(root, path, what="FTP"):
    ''' Returns an element specified by path. INTERNAL FUNCTION, DO NOT USE IT.'''
    string = ''
    for x in path:
        string = string + "/" + str(x)
    #print(string)
    return root.find("./"+str(what)+string)

def AddToFiletree(projName, path, objName, type, owner="unknown", size=0):
    ''' Add a file or a directory to filetree. Files and directories in one dir must have a different name!
        projName -> name of the modified project (string!)
        path     -> LIST with path to target directory (without the added file/dir) INCLUDING HOME
            examples: ["home"], ["home", "dir1", "dir2"]
        objName  -> name of the added file/dir
        type     -> "d"/"f": dir/file
        owner    -> which user owns it (default value is "unknown")
        size     -> size (default is 0)
    '''
    m = re.match(r'^[a-zA-Z0-9_.]+$', str(objName))       # names of files/directories have limited set of characters
    if m == None:
        raise NameContainsWrongCharError

    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    #print(root.find("./FTP/home").attrib)
    elem = FindInXML(root, path, "FTP")
    if elem == None:                # path does not exist
        raise DoesNotExistError
    if elem.attrib['type'] != 'd':  # target object is not a directory
        raise WrongTypeError
    test = elem.findall("*")        # looks for files and directories with same name
    for x in test:
        if x.tag == objName:
            raise AlreadyExistsError

    ET.SubElement(elem, objName, type=str(type), size=str(size), date=str(datetime.datetime.now().date()), owner=str(owner))
    tree.write("XML/"+str(projName)+".xml", encoding='UTF-8', xml_declaration=True)

def DeleteFromFiletree(projName, path, objName):
    ''' Delete file or directory from filetree.
        projName -> name of the modified project (string!)
        path     -> LIST with path to target directory (without the removed file/dir) INCLUDING HOME
            examples: ["home"], ["home", "dir1", "dir2"]
        objName  -> name of the removed file/dir
    '''
    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    elem = FindInXML(root, path, "FTP")
    if elem == None:                # path does not exist
        raise DoesNotExistError

    victim = elem.find(str(objName))
    if victim == None:
        raise DoesNotExistError
    try:
        elem.remove(victim)
    except:
        raise DoesNotExistError     # should not get there

    tree.write("XML/"+str(projName)+".xml", encoding='UTF-8', xml_declaration=True)

def RenameInFiletree(projName, path, objName, newName):
    ''' Rename file or directory in filetree.
        projName -> name of the modified project (string!)
        path     -> LIST with path to target directory (without the removed file/dir) INCLUDING HOME
            examples: ["home"], ["home", "dir1", "dir2"]
        objName  -> name of the renamed file/dir
        newName  -> new name of the renamed file/dir
    '''
    m = re.match(r'^[a-zA-Z0-9_.]+$', str(newName))       # names of files/directories have limited set of characters
    if m == None:
        raise NameContainsWrongCharError

    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    elem = FindInXML(root, path, "FTP")
    if elem == None:                # path does not exist
        raise DoesNotExistError

    victim = elem.find(str(objName))
    if victim == None:
        raise DoesNotExistError
    victim.tag = str(newName)       # rename element tag

    tree.write("XML/"+str(projName)+".xml", encoding='UTF-8', xml_declaration=True)

def GetInfoFromFiletree(projName, path):
    ''' Get informations about the content of a single directory from filetree.
        projName -> name of the project (string!)
        path     -> LIST with path to target directory (without the removed file/dir) INCLUDING HOME
            examples: ["home"], ["home", "dir1", "dir2"]
    '''
    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    elem = FindInXML(root, path, "FTP")
    if elem == None:                    # path does not exist
        raise DoesNotExistError

    d = {}
    for child in elem.findall("*"):     # find all children
        d[child.tag] = child.attrib

    return {'path'   : path,
            'content': d}

# ----------------------------- FTP end -----------------------------------------------------

# ----------------------------- email,dns,users ---------------------------------------------
def AddDNS(projName, objName):
    ''' Add a new DNS to a project.
        projName -> name of the project (string!)
        objName  -> name of the added DNS (string!)
    '''
    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    elem = FindInXML(root, [], "DNS")
    if elem == None:                    # path does not exist - should not happen
        raise DoesNotExistError

    test = elem.findall("*")            # looks for DNSes with same name
    for x in test:
        if x.text == objName:
            raise AlreadyExistsError

    ET.SubElement(elem, "dns").text = str(objName)
    tree.write("XML/"+str(projName)+".xml", encoding='UTF-8', xml_declaration=True)

def DeleteDNS(projName, objName):
    ''' Delete DNS from a project. If it does not find an object to delete, it does nothing.
        projName -> name of the project (string!)
        objName  -> name of the removed DNS (string!)
    '''
    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    elem = FindInXML(root, [], "DNS")
    if elem == None:                        # path does not exist - should not happen
        raise DoesNotExistError

    test = elem.findall("*")                # find children
    for x in test:
        if x.text == objName:
            try:
                elem.remove(x)
            except:
                raise DoesNotExistError     # should not get there
            break

    tree.write("XML/"+str(projName)+".xml", encoding='UTF-8', xml_declaration=True)

def GetDNS(projName):
    ''' Get DNS from a project.
        projName -> name of the project (string!)
    '''
    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    elem = FindInXML(root, [], "DNS")
    if elem == None:                        # path does not exist - should not happen
        raise DoesNotExistError

    test = elem.findall("*")                # find children
    result = []
    for x in test:
        result.append(x.text)

    return result

def AddEmail(projName, objName):
    ''' Add a new email to a project.
        projName -> name of the project (string!)
        objName  -> name of the added email (string!)
    '''
    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    elem = FindInXML(root, [], "emails")
    if elem == None:                        # path does not exist - should not happen
        raise DoesNotExistError

    test = elem.findall("*")                # looks for emails with same name
    for x in test:
        if x.text == objName:
            raise AlreadyExistsError

    ET.SubElement(elem, "email").text = str(objName)
    tree.write("XML/"+str(projName)+".xml", encoding='UTF-8', xml_declaration=True)

def DeleteEmail(projName, objName):
    ''' Delete email from a project. If it does not find an object to delete, it does nothing.
        projName -> name of the project (string!)
        objName  -> name of the removed email (string!)
    '''
    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    elem = FindInXML(root, [], "emails")
    if elem == None:                        # path does not exist - should not happen
        raise DoesNotExistError

    test = elem.findall("*")                # find children
    for x in test:
        if x.text == objName:
            try:
                elem.remove(x)
            except:
                raise DoesNotExistError     # should not get there
            break

    tree.write("XML/"+str(projName)+".xml", encoding='UTF-8', xml_declaration=True)

def GetEmail(projName):
    ''' Get email from a project.
        projName -> name of the project (string!)
    '''
    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    elem = FindInXML(root, [], "emails")
    if elem == None:                        # path does not exist - should not happen
        raise DoesNotExistError

    test = elem.findall("*")                # find children
    result = []
    for x in test:
        result.append(x.text)

    return result

def AddUser(projName, objName):
    ''' Add a new user to a project.
        projName -> name of the project (string!)
        objName  -> name of the added user (string!)
    '''
    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    elem = FindInXML(root, [], "users")
    if elem == None:                        # path does not exist - should not happen
        raise DoesNotExistError

    test = elem.findall("*")                # looks for users with same name
    for x in test:
        if x.text == objName:
            raise AlreadyExistsError

    ET.SubElement(elem, "user").text = str(objName)
    tree.write("XML/"+str(projName)+".xml", encoding='UTF-8', xml_declaration=True)

def DeleteUser(projName, objName):
    ''' Delete user from a project. If it does not find an object to delete, it does nothing.
        projName -> name of the project (string!)
        objName  -> name of the removed user (string!)
    '''
    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    elem = FindInXML(root, [], "users")
    if elem == None:                        # path does not exist - should not happen
        raise DoesNotExistError

    test = elem.findall("*")                # find children
    for x in test:
        if x.text == objName:
            try:
                elem.remove(x)
            except:
                raise DoesNotExistError     # should not get there
            break

    tree.write("XML/"+str(projName)+".xml", encoding='UTF-8', xml_declaration=True)

def GetUser(projName):
    ''' Get user from a project.
        projName -> name of the project (string!)
    '''
    try:
        print("XML/"+str(projName)+".xml")
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    elem = FindInXML(root, [], "users")
    if elem == None:                        # path does not exist - should not happen
        raise DoesNotExistError

    test = elem.findall("*")                # find children
    result = []
    for x in test:
        result.append(x.text)

    return result

# ----------------------------- email,dns,users end -----------------------------------------

# ----------------------------- database ----------------------------------------------------
def CreateTable(projName, tableName, definition):
    ''' Create a new table in a database.
        projName   -> name of the project (string!)
        tableName  -> name of the added table (string!)
        definition -> list of lists: [[name of column,data type],...]
            example: [["id","i"],["jmeno","s"],["prijmeni","s"],["vek","i"]]
    '''
    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    elem = FindInXML(root, [], "database")
    if elem == None:                        # path does not exist - should not happen
        raise DoesNotExistError

    test = elem.findall("*")                # looks for tables with same name
    for x in test:
        if str(tableName) == x.attrib['tablename']:
            raise AlreadyExistsError

    table = ET.SubElement(elem, "table", tablename=str(tableName))
    #table.text = str(tableName)
    defin = ET.SubElement(table, "definition", length=str(len(definition)))
    for d in definition:
        ET.SubElement(defin, "def", datatype=str(d[1])).text = str(d[0])
    ET.SubElement(table, "rows")

    tree.write("XML/"+str(projName)+".xml", encoding='UTF-8', xml_declaration=True)

def DeleteTable(projName, tableName):
    ''' Delete table from a database. If it does not find an object to delete, it does nothing.
        projName  -> name of the project (string!)
        tableName -> name of the removed table (string!)
    '''
    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    elem = FindInXML(root, [], "database")
    if elem == None:                        # path does not exist - should not happen
        raise DoesNotExistError

    test = elem.findall("*")                # find children
    for x in test:
        if x.attrib['tablename'] == str(tableName):
            try:
                elem.remove(x)
            except:
                raise DoesNotExistError     # should not get there
            break

    tree.write("XML/"+str(projName)+".xml", encoding='UTF-8', xml_declaration=True)

def AddRow(projName, tableName, rowData):
    ''' Add a new row into a table.
        projName   -> name of the project (string!)
        tableName  -> name of the table (string!)
        rowData    -> list of records
            example: ["0","Frodo","Pytlik","50+"]
    '''
    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    elem = FindInXML(root, [], "database")
    if elem == None:                        # path does not exist - should not happen
        raise DoesNotExistError

    test = elem.findall("*")                # find children
    for x in test:
        if x.attrib['tablename'] == str(tableName):                                 # find the requested table
            columns = x.find("definition").attrib['length']     # get the number of columns
            if int(columns) != len(rowData):                    # check if there is enough data provided
                raise IncompatibleRowDataError
            rows = x.find("rows")                               # get rows element
            r = ET.SubElement(rows, "row")                      # add a subelement row
            for col in rowData:                                 # for each piece of data add a record
                ET.SubElement(r, "record").text = str(col)
            tree.write("XML/"+str(projName)+".xml", encoding='UTF-8', xml_declaration=True)
            return

    raise TableNotFoundError    # if it gets here, something is wrong

def DeleteRow(projName, tableName, rowid):
    ''' Delete row in a table. If it does not find record, it does nothing.
        projName   -> name of the project (string!)
        tableName  -> name of the table (string!)
        rowid      -> THE FIRST RECORD IN A ROW (STRING!)
            example: "0"        (most often it will be id)
    '''
    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    elem = FindInXML(root, [], "database")
    if elem == None:                        # path does not exist - should not happen
        raise DoesNotExistError

    test = elem.findall("*")                # find children
    for x in test:
        if x.attrib['tablename'] == str(tableName):                                 # find the requested table
            rows = x.find("rows")                               # get rows element
            row = rows.findall("row")                           # find all rows
            for r in row:                                       # find a row that has requested id
                if r.find("record").text == rowid:
                    rows.remove(r)                              # remove it
            tree.write("XML/"+str(projName)+".xml", encoding='UTF-8', xml_declaration=True)
            return

def GetDatabase(projName):
    ''' Get the whole database in just one list!!!
        projName   -> name of the project (string!)
        Returns:
            list of dictionaries(each table)
                each dictionary contains name of the table, list of column definitions and list of lists(rows)
            example:
                [{'name': 'hrusky', 'rows': [], 'definition': [['id','i'],['jmeno','s'],['odruda','s']]},
                 {'name': 'jabka',
                  'rows': [['0', 'Granny Smith', 'green'], ['1', 'Granny Smith', 'green'],['2', 'Granny Smith', 'green']],
                  'definition': [['id','i'],['jmeno','s'],['barva','s']]}]
    '''
    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    elem = FindInXML(root, [], "database")
    if elem == None:                        # path does not exist - should not happen
        raise DoesNotExistError

    return ET.tostring(elem, "UTF-8")       # trying new things

    result = []
    counter = 0
    test = elem.findall("*")                                    # find children
    for x in test:
        result.append({"name":x.attrib['tablename']})                          # get name of the table
        definition = x.find("definition")
        defin = definition.findall("*")                         # find all definitions
        result[counter]['definition'] = []
        for d in defin:                                         # add them to the list
            defunit = [d.text,d.attrib['datatype']]             # create a list of column name and data type
            result[counter]['definition'].append(defunit)
        rows = x.find("rows")
        rowlist = rows.findall("row")                           # find all rows of a table
        result[counter]['rows'] = []
        for row in rowlist:                                     # for every row find records
            recordlist = row.findall("record")
            rowdata = []
            for record in recordlist:                           # save every record of a row into a list
                rowdata.append(record.text)
            result[counter]['rows'].append(rowdata)             # append the list to a list of rows

        counter = counter + 1
    return result

def AddColumn(projName, tableName, column, defaultValue="NULL"):
    ''' Add column to a table. Adds column to the end of a column list.
        projName     -> name of the project (string!)
        tableName    -> name of the table (string!)
        column       -> name of the new column and its data type (string!)
            example: ["name","s"]
        defaultValue -> default value of new column in existing rows (string!)
    '''
    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    elem = FindInXML(root, [], "database")
    if elem == None:                                # path does not exist - should not happen
        raise DoesNotExistError

    test = elem.findall("*")                        # find children
    for x in test:
        if x.attrib['tablename'] == str(tableName):                     # find the right table
            definition = x.find("definition")       # add column name and type to definition
            definition.attrib['length'] = str(int(definition.attrib['length'])+1)
            ET.SubElement(definition, "def", datatype=str(column[1])).text = str(column[0])
            rows = x.find("rows")
            rowlist = rows.findall("row")
            for row in rowlist:                     # add a default value to the new column
                ET.SubElement(row, "record").text = str(defaultValue)

    tree.write("XML/"+str(projName)+".xml", encoding='UTF-8', xml_declaration=True)

def DeleteColumn(projName, tableName, column):
    ''' Delete column from a table.
        projName   -> name of the project (string!)
        tableName  -> name of the table (string!)
        column     -> name of the deleted column (string!)
            example: "name"
    '''
    try:
        tree = ET.parse("XML/"+str(projName)+".xml")
        root = tree.getroot()
    except:
        raise DoesNotExistError

    elem = FindInXML(root, [], "database")
    if elem == None:                    # path does not exist - should not happen
        raise DoesNotExistError

    test = elem.findall("*")                                    # find children
    for x in test:
        if x.attrib['tablename'] == str(tableName):                                 # find the right table
            definition = x.find("definition")
            deflist = definition.findall("def")                 # find all defs
            counter = 0                                         # count the position of a column in a list
            for d in deflist:
                if d.text == column:                            # remove the right column
                    definition.remove(d)
                    definition.attrib['length'] = str(int(definition.attrib['length'])-1)
                    break
                counter = counter + 1
            if counter == len(deflist):                         # if the column was not found, nothing happens
                return

            rows = x.find("rows")
            rowlist = rows.findall("row")                       # find all rows of a table
            for row in rowlist:                                 # for every row
                recordlist = row.findall("record")              # find records
                row.remove(recordlist[counter])                 # and remove the record on the right position

    tree.write("XML/"+str(projName)+".xml", encoding='UTF-8', xml_declaration=True)

# ----------------------------- database end ------------------------------------------------

# print(ET.VERSION)
# tests
'''
CreateProject("dat007", "Ondrej")
CreateTable("dat007", "hrusky", [["id","i"],["jmeno","s"],["odruda","s"]])
CreateTable("dat007", "jabka", [["id","i"],["jmeno","s"],["barva","s"]])
CreateTable("dat007", "balon", [["neco","s"]])
DeleteTable("dat007", "balon")

AddRow("dat007", "jabka", ["0","Granny Smith","green"])
AddRow("dat007", "jabka", ["1","Moje jabko","red"])
AddRow("dat007", "jabka", ["2","Taiwanska namka","orange"])
AddColumn("dat007", "jabka", ["kyselost","i"], "0")
AddColumn("dat007", "jabka", ["vune","s"])
DeleteColumn("dat007", "jabka", "vune")
#DeleteColumn("dat007", "jabka", "barva")
#DeleteColumn("dat007", "jabka", "id")

print(GetDatabase("dat007"))

#AddRow("dat007", "hruska", ["0","Granny Smith","green"])
#DeleteRow("dat007", "jabka", "1")
#DeleteRow("dat007", "jabka", "10")
'''
'''
#CreateProject("aaa")
#RenameProject("aaa", "renamed")
CreateProject("id101", "Ondrej")
CreateProject("xxx666", "Ondrej")
DeleteProject("xxx666")
AddToFiletree("id101", ["home"],"mydir","d", "&Ond ra_")
AddToFiletree("id101", ["home"],"my_file1.html","f", "Ondra")
AddToFiletree("id101", ["home","mydir"],"myfile2","f", "Ondra")
AddToFiletree("id101", ["home","mydir"],"kocicky","d", "Ondra")
AddToFiletree("id101", ["home","mydir"],"pejsanci","d", "Ondra")
AddToFiletree("id101", ["home","mydir","kocicky"],"micka","f", "Ondra")
#AddToFiletree("id101", ["home","mydir"],"myfile2","f", "Ondra")
#AddToFiletree("id101", ["home","myfile1"],"myfile2","f", "Ondra")

RenameInFiletree("id101",["home","mydir"],"myfile2","renamed_file.txt")
#RenameInFiletree("id101",["home"],"mydir","mymymyd")

x = GetInfoFromFiletree("id101", ["home"])
print(x)
print("\n")
x = GetInfoFromFiletree("id101", ["home","mydir"])
print(x)

#DeleteFromFiletree("id101", ["home","mydir"], "myfile2")
#DeleteFromFiletree("id101", ["home"], "mydir")
#DeleteFromFiletree("id101", ["home"], "mydir24")
#DeleteFromFiletree("id101", ["home","hehe"], "mydir")

#AddToUser("id101", "email", "soubor")
'''
'''
CreateProject("xxx666", "Ondrej")
AddDNS("xxx666", "mydns")
AddDNS("xxx666", "mydns2")
AddDNS("xxx666", "mydns3")
AddDNS("xxx666", "mydns4")
#AddDNS("xxx666", "mydns")

print(GetDNS("xxx666"))

DeleteDNS("xxx666", "mydns2")
DeleteDNS("xxx666", "mydns2")

AddEmail("xxx666", "ja@seznam.cz")
AddEmail("xxx666", "mne@seznam.cz")
print(GetEmail("xxx666"))
DeleteEmail("xxx666", "ja@seznam.cz")

AddUser("xxx666", "Ondra")
AddUser("xxx666", "Martin")
print(GetUser("xxx666"))
DeleteUser("xxx666", "Martin")
'''

