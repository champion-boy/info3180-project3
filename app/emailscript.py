import smtplib

def sendemail(toname,toemail,fromsubject,msg):
    fromname = 'Wishlist' 
    fromemail  = 'toni-annfitzgerald@hotmail.com'
    message = """From: {} <{}>\nTo: {} <{}>\nSubject: {}\n\n{}"""
    
    messagetosend = message.format(
                                 fromname,
                                 fromemail,
                                 toname,
                                 toemail,
                                 fromsubject,
                                 msg)
    
    # Credentials (if needed)
    username = 'toniannfitzgerald@gmail.com'
    password = 'xqgqdjeitwfxdlac'
    
    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromemail, toemail, messagetosend)
    server.quit()
    return