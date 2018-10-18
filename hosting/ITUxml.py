import xml.etree.ElementTree as ET
import os

# ------------------------------------------------------------------------
#         MODULE FOR STORING INFORMATION (XML) FOR ITU PROJECT
# ------------------------------------------------------------------------
'''
    This module uses folder named userXML located in the same directory.

    List of return values:
        0 -> ok (function GetInfo returns dict!)
        1 -> user or entity already exists
        2 -> user does not exist yet
        3 -> function parameter is not convertable to string (name, value, what, ...)
        4 -> error while opening or writing the file or any other possible error
'''

def RegisterUser(name):
    ''' Register a new user. '''
    try:
        if os.path.exists("userXML/"+name+".xml"):
            return 1

        root = ET.Element(str(name))

        files = ET.SubElement(root, "files")
        ET.SubElement(root, "DNS")
        ET.SubElement(root, "emails")

        tree = ET.ElementTree(root)
        tree.write("userXML/"+name+".xml")
        return 0
    except UnicodeDecodeError:
        return 2
    except:
        return 3

def RemoveUser(name):
    ''' Remove user xml. Always returns 0 (compatibility with other functions). '''
    if os.path.exists("userXML/"+name+".xml"):
        os.remove("userXML/"+name+".xml")

    return 0

def AddToUser(name, what, value):
    ''' Add things to user. Everything must be convertable to string!
        name  -> username of an already existing user!
        what  -> type of added information.
            Possibilities:
                "file"
                "dns"
                "email"
        value -> text that will be saved. '''
    try:
        tree = ET.parse("userXML/"+name+".xml")
        root = tree.getroot()

        if what == "file":
            files = root[0]
            # checks if the new info is not saved already
            for child in files.iter():
                if child is not files:
                    if child.text == value:
                        return 1
            ET.SubElement(files, "file").text = str(value)
        if what == "dns":
            dns = root[1]
            # checks if the new info is not saved already
            for child in dns.iter():
                if child is not dns:
                    if child.text == value:
                        return 1
            ET.SubElement(dns, "dns").text = str(value)
        if what == "email":
            email = root[2]
            # checks if the new info is not saved already
            for child in email.iter():
                if child is not email:
                    if child.text == value:
                        return 1
            ET.SubElement(email, "email").text = str(value)

        tree.write("userXML/"+name+".xml")
        return 0
    except xml.etree.ElementTree.ParseError:
        return 2
    except:
        return 4

def RemoveFromUser(name, what, value):
    ''' Remove things from user. Everything must be convertable to string!
        name  -> username of an already existing user!
        what  -> type of removed information.
            Possibilities:
                "file"
                "dns"
                "email"
        value -> text that will be deleted. '''
    try:
        tree = ET.parse("userXML/"+name+".xml")
        root = tree.getroot()

        victim = None
        if what == "file":
            victim = root[0]    # file
        if what == "dns":
            victim = root[1]    # dns
        if what == "email":
            victim = root[2]    # email

        # goes through all saved entities in infogroup (files, dns, ...) and looks for text
        # that should be deleted
        for child in victim.iter():
            if child is not victim:
                if child.text == value:
                    victim.remove(child)

        tree.write("userXML/"+name+".xml")
        return 0
    except xml.etree.ElementTree.ParseError:
        return 2
    except:
        return 4

def GetInfo(name):
    ''' Get all information about user. Info is stored in a dictionary.
        Keys:
            dict["files"]  -> list of files
            dict["dns"]    -> list of dns
            dict["emails"] -> list of emails
    '''
    try:
        tree = ET.parse("userXML/"+name+".xml")
        root = tree.getroot()

        UserInfo = {}
        UserInfo["files"] = [file.text for file in root[0].iter() if file is not root[0]]
        UserInfo["dns"] = [dns.text for dns in root[1].iter() if dns is not root[1]]
        UserInfo["emails"] = [email.text for email in root[2].iter() if email is not root[2]]

        return UserInfo
    except xml.etree.ElementTree.ParseError:
        return 2
    except:
        return 4





# garbage
'''
ET.SubElement(files, "file").text = "some value1"
    ET.SubElement(files, "file").text = "some value2"

    print(files[0].tag, files[1].tag)
    for file in root.iter('file'):
        if file.text == "some value1":
            file.text = "newname"
'''

'''
root = ET.Element("root")
doc = ET.SubElement(root, "doc")

ET.SubElement(doc, "field1", name="blah").text = "some value1"
ET.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"

tree = ET.ElementTree(root)
tree.write("filename.xml")


XMLTree = None      # possibly a dict of active users: {username:XMLTree}

def CreateXML():
    Cretaes XML file in case it does not exist. Use for exception.
    root = ET.Element("users")
    tree = ET.ElementTree(root)
    tree.write("userXML/filename.xml")

def SignIn(name):
    Load XML file.
    tree = ET.parse("userXML/filename.xml")
    root = tree.getroot()

    files = root[0]
    print(files.tag)

    # root.remove(files)
    # tree.write("userXML/filename.xml")

'''
# tests
'''
print("Register: "+str(RegisterUser("xpolan")))
print("Register: "+str(RegisterUser("xxx666")))
print("Remove: "+str(RemoveUser("xxx666")))
print(AddToUser("xpolan", "file", "soubor"))
print(AddToUser("xpolan", "file", "soubor"))
print(AddToUser("xpolan", "dns", "soubor"))
print(AddToUser("xpolan", "file", "kotatka"))
print(AddToUser("xpolan", "email", "email@email.cz"))
print(GetInfo("xpolan"))
print(RemoveFromUser("xpolan", "email", "email@email.cz"))
print(GetInfo("xpolan"))
print(RemoveFromUser("xpolan", "file", "soubor"))
print(GetInfo("xpolan"))
print("Remove: "+str(RemoveUser("xpolan")))
'''
