from getpass import getpass
import imaplib
import base64
import os
import email

email_user = input('email address: ')
email_pass = getpass('password: ')

mail = imaplib.IMAP4_SSL('imap.seznam.cz',993)
mail.login(email_user, email_pass)
mail.select('Fotopast')

t, data = mail.search(None, 'ALL')
mail_ids = data[0]
id_list = mail_ids.split()

for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)' )
    raw_email = data[0][1]
# converts byte literal to string removing b''
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
# downloading attachments
    for part in email_message.walk():
        # this part comes from the snipped I don't understand yet... 
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            filePath = os.path.join('C:\\Users\\admin\\Downloads\\', fileName)
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
            subject = str(email_message).split("Subject: ", 1)[1].split("\n", 1)[0]
            print(f'Downloaded "{fileName}" from email titled "{subject}"')