import smtplib
from flask import render_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Email configuration
def send_message_finally():
    smtp_server = ''
    smtp_port = 2525
    username = ''
    password = ''
    from_email = ''
    emails = ['tsmskb@outlook.com']
    subject = 'С днем рождения вас!'

    msg = MIMEMultipart('related')

    # Create a MIME multipart message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ""
    msg['Subject'] = subject

    with open("ura.html", encoding='utf-8') as file:
        template = file.read()

    

    msgText = MIMEText(template, "html")
    msg.attach(msgText)

    for i in range(1,6):
        path_to_images = f"im{i}.png"
        with open(path_to_images, 'rb') as image_file:
            image1 = MIMEImage(image_file.read())
            image1.add_header('Content-ID', f'<image{i}>')
            msg.attach(image1)

    #with open("img0.png", 'rb') as image_file:
    #    image1 = MIMEImage(image_file.read())
    #    image1.add_header('Content-ID', f'<image1>')
    #    msg.attach(image1)

    # Create an SMTP connection
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(username, password)

    # Send the email
    for i in range(len(emails)):
        server.sendmail(from_email, emails[i], msg.as_string())
        print(f'message sent to {emails[i]}')

    # Close the SMTP connection
    server.quit()