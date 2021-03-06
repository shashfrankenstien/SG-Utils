import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication 


class Message(object):
	'''Takes recipient, sender, subject and body to initiate'''
	def __init__(self, recipient='', sender='', subject='', body=''):
		self.message = MIMEMultipart()
		self.sender = sender
		self.recipient = recipient
		self.setHeader('From', sender)
		self.setHeader('To', recipient)
		self.setHeader('Subject', subject)
		self.setBody(body)

	def setHeader(self, key, value):
		self.message[key] = value

	def setBody(self, body):
		self.message.attach(MIMEText(body, 'plain'))

	def attachment(self, binary, filename):
		part = MIMEApplication(binary, Name=filename)
		part['Content-Disposition'] = 'attachment; filename="%s"' % filename
		self.message.attach(part)



class Mail(object):
	"""
	It takes MAIL_USERNAME, MAIL_PASSWORD and MAIL_SERVER_PORT to initiate.
	the 'send' method takes a Message object as an argument.
	"""
	_count = 0

	def __init__(self, username, password, mail_server_port, debug=False):
		self.username = username
		self.password = password
		self.host_port = mail_server_port
		self.server = smtplib.SMTP()
		self.server.set_debuglevel(debug)

	def send(self, msg):
		try:
			self.server.connect(self.host_port)
			self.server.ehlo()
			self.server.starttls()
			self.server.login(self.username,self.password)
			print('Emailer - logged in ')
			self.server.sendmail(msg.sender, msg.recipient, str(msg.message))
			print('Emailer - sent')
			self.server.quit()
			print('Emailer - closed')
		except Exception as e: 
			print ('\n\n' + str(e) + '\n\n')
		Mail._count += 1


