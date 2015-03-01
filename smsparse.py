from xml.dom import minidom
import os
# i have bug in my HTC phone - it save some contacts with symbols as > <
common_escape_table = {
	"&": "and",
	'"': "",
	"'": "",
	">": "gt",
	"<": "lt",
	"?": "q",
	":": "ddot",
  }
def common_escape(text):
	return "".join(common_escape_table.get(c,c) for c in text)
def parse_sms():
	xmldoc = minidom.parse('sms.xml')
	itemlist = xmldoc.getElementsByTagName('sms')
	
	if(os.path.isdir("archive")):
		os.chdir('archive')
	else:
		os.mkdir('archive')
		os.chdir('archive')

	for position,s in enumerate(itemlist):
		try:
			filename = common_escape("%s (%s)" % (s.attributes['contact_name'].value,s.attributes['address'].value))
			f = open(filename, 'ab+')
			if s.attributes['type'].value == '1':
				message = "Incoming message(%s): |%s| \r\n" % (s.attributes['readable_date'].value,s.attributes['body'].value)
			else:
				message = "Outgoing message(%s): |%s| \r\n" % (s.attributes['readable_date'].value,s.attributes['body'].value)
			f.write(message.encode('utf_8'))
			f.close()
		except OSError as e :
			print('Error in %d sms' % position)


parse_sms()

