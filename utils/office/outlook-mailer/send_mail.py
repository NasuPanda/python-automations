import win32com.client
from credentials import setting

outlook = win32com.client.Dispatch("Outlook.Application")

mail = outlook.CreateItem(0)

mail.to = setting.TO
mail.cc = setting.CC
mail.subject = 'Python 送信テスト'
mail.bodyFormat = 1
mail.body = '''
Pythonから送信しています。
'''

mail.display(True)
