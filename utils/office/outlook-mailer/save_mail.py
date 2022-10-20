import os
import re

from win32com.client import Dispatch

# [Saving email from Outlook into folder with Python - Stack Overflow](https://stackoverflow.com/questions/51621535/saving-email-from-outlook-into-folder-with-python)

outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)
print(inbox)
messages = inbox.items
message = messages.GetLast()
name = str(message.subject)
# to eliminate any special characters in the name
name = re.sub("[^A-Za-z0-9]+", "", name) + ".msg"
# to save in the current working directory
message.SaveAs(os.getcwd() + "//" + name)
