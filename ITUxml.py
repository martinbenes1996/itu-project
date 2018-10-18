import xml.etree.ElementTree as ET
import os

# ------------------------------------------------------------------------
#         MODULE FOR STORING INFORMATION (XML) FOR ITU PROJECT
# ------------------------------------------------------------------------
'''
    This module uses folder named userXML located in the same directory.

    Functions do not have return value except for GetInfo(name) which returns dictionary.
    Two exceptions can be raised:
        AlreadyExistsError -> user or entity already exists
        DoesNotExistError  -> user or entity does not exist

    Other exceptions (file cant be opened/closed) are ignored! Deal with them.
'''

class AlreadyExistsError(Exception):
    pass
class DoesNotExistError(Exception):
    pass

def RegisterUser(name):
    ''' Register a new user. '''
    if os.path.exists("userXML/"+name+".xml"):
        raise AlreadyExistsError

    root = ET.Element(str(name))

    files = ET.SubElement(root, "files")
    ET.SubElement(root, "DNS")
    ET.SubElement(root, "emails")

    tree = ET.ElementTree(root)
    tree.write("userXML/"+name+".xml")


def RemoveUser(name):
    ''' Remove user xml. '''
    if os.path.exists("userXML/"+name+".xml"):
        os.remove("userXML/"+name+".xml")


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
                        raise AlreadyExistsError
            ET.SubElement(files, "file").text = str(value)
        if what == "dns":
            dns = root[1]
            # checks if the new info is not saved already
            for child in dns.iter():
                if child is not dns:
                    if child.text == value:
                        raise AlreadyExistsError
            ET.SubElement(dns, "dns").text = str(value)
        if what == "email":
            emails = root[2]
            # checks if the new info is not saved already
            for child in emails.iter():
                if child is not emails:
                    if child.text == value:
                        raise AlreadyExistsError
            ET.SubElement(emails, "email").text = str(value)

        tree.write("userXML/"+name+".xml")

    except ET.ParseError:
        raise DoesNotExistError


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

    except ET.ParseError:
        raise DoesNotExistError


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
    except ET.ParseError:
        raise DoesNotExistError





# tests
'''
RegisterUser("xpolan")
RegisterUser("xxx666")
RemoveUser("xxx666")
AddToUser("xpolan", "file", "soubor")
# AddToUser("xpolan", "file", "soubor")
AddToUser("xpolan", "dns", "soubor")
AddToUser("xpolan", "file", "kotatka")
AddToUser("xpolan", "email", "email@email.cz")
print(GetInfo("xpolan"))
RemoveFromUser("xpolan", "email", "email@email.cz")
print(GetInfo("xpolan"))
RemoveFromUser("xpolan", "file", "soubor")
print(GetInfo("xpolan"))
RemoveUser("xpolan")
'''
