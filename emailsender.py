import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders
from email_templates import *
import csv

# CSV File path and Email Template path
csv_path = "./mail_lists_csv/maillist.csv"
email_template = './email_templates/template1.txt'

# Function to filter through Company and Email in the CSV File (List of receiver email_it to the mail)
csv_dict = {}
csv_list = []
def csv_importer(csv_path):
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for line in reader:
            if line["Email"] != '':
                csv_dict = {"name": line["Company"], "email": line["Email"], "cc": line["CC"], "file": line["File"]}
                csv_list.append(csv_dict)
                print(f"{line['Company']} added to csv_list" )
            else:
                print(f"{line['Company']} has no email")
        return csv_list
# Make it so that in the future the code differentiates between Company Name and Person Name 
# if line["Company"] then add "Dear {receiver_name} team,"
# if line["Contact"] then add "Dear {receiver_name},"

csv_file = csv_importer(csv_path)
print(csv_file)

# Function to grab title and content of email template
template_dict = {}
def email_template_importer(email_template): 
    with open(email_template, "r", encoding='utf-8') as template:
        title = template.readline()
        content = template.readlines()
        template_dict = {"title": title, "content": ''.join(content)}
        return template_dict

template_file = email_template_importer(email_template)

# The mail addresses and password
sender_address =''               
sender_pass = ''               

# Getting length of list 
length = len(csv_file) 
   
# Here we iterate the loop and send msg one by one to the reciver
for i in range(length): 
    
    X = csv_file[i]['email']
    Y = csv_file[i]['name']
    Z = csv_file[i]['cc']
    receiver_address = X
    receiver_name = Y
    cc_address = Z

    # print(f"To: {receiver_address}, CC: {cc_address}")
    
    message = MIMEMultipart()
    message['From'] = f"<{sender_address}>"
    message['To'] =  f"<{receiver_address}>"
    message['Cc'] = f"<{cc_address}>"
    message['Subject'] =  template_file["title"]
     

    mail_content = f'''
    Dear {receiver_name} team, <br><br>
    {template_file["content"]}
    '''

    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'html', 'utf-8'))
    # print("Message attached")
    
    # ATTACH FILES #
    file = ""
    # # Open the file to be sent  
    filename1 = f'./'                                                  
    filename2 = f'./' 

    # Open PDF file in binary mode
    # The file is in the directory same as where you run your Python script code from 
    with open(filename1, "rb") as attachment1, open(filename2, "rb") as attachment2:
        # MIME attachment is a binary file for that content type "application/octet-stream" is used
        part1 = MIMEBase("application", "octet-stream")
        part1.set_payload(attachment1.read())
        part2 = MIMEBase("application", "octet-stream")
        part2.set_payload(attachment2.read())
    # Encode into base64 
    encoders.encode_base64(part1) 
    encoders.encode_base64(part2) 

    part1.add_header('Content-Disposition', "attachment; filename= %s" % filename1)
    part2.add_header('Content-Disposition', "attachment; filename= %s" % filename2)  

    # Attach the instance 'part' to instance 'message' 
    message.attach(part1)
    print(f'File {filename1} attached') 
    message.attach(part2)
    print(f'File {filename2} attached') 


    # Create SMTP session for sending the mail

    s = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
    # s.set_debuglevel(1) 
    s.ehlo()
    s.starttls()
    s.login(sender_address, sender_pass)
    text = message.as_string()
    s.sendmail(sender_address, receiver_address, text) 
    s.quit() 

    print(f'Mail sent to {receiver_name}')

# It Send Separated Mail one by one each receiver mail 



# Iterating the index 
# same as 'for i in range(len(list))' 

# List of receiver email_id to the mail 
# li = [
#     {'name':'', 'email':''},
#     {'name':'', 'email':''},    
#     {'name':'', 'email':''},   
#     {'name':'', 'email':''},  
# ]                                               
#[item for item in input("Enter Receiver Mail Address :- ").split()] this is used to take user input of receiver mail id