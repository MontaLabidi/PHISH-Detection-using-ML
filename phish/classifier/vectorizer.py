import whois
import socket
import requests
import threading
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime,timedelta

services = [
	"full.sc",
	"adf.ly",
	"adfoc.us",
	"bit.ly",
	"bit.do",
	"bc.vc",
	"goo.gl",
	"go.co",
	"gomo.be",
	"budurl.com",
	"cli.gs",
	"cur.lv",
	"fa.by",
	"is.gd",
	"ow.ly",
	"fur.ly",
	"lurl.no",
	"qr.net",
	"moourl.com",
	"mcaf.ee",
	"safe.mn",
	"smallr.com",
	"snipr.com",
	"shorte.st",
	"s2r.co",
	"clicky.me",
	"idek.net",
	"snipurl.com",
	"snurl.com",
	"soo.gd",
	"su.pr",
	"po.st",
	"t.co",
	"youtu.be",
	"yep.it",
	"yourls.org",
	"viralurl.com",
	"tiny.cc",
	"tinyurl.com",
	"tr.im"]


def url_validate(x):
	try:
		result = urlparse(x)
		return result.scheme and result.netloc and result.path
	except:
		return False


def Favicon(url, result, index):
	print(threading.current_thread().name, index)
	li = ''
	try:
		site = requests.get(url, headers=headers, timeout=my_timeout, verify=False)
		soup = BeautifulSoup(site.text, 'lxml')
	except:
		result[index] = 0
		return 0

	p = ""
	if soup.find('link', rel="shortcut icon") == -1:
		result[index] = 0
		return 0
	else:
		for pb in soup.find_all('link', rel="shortcut icon"):
			p = p + str(pb)
			li = pb["href"]
		# print(li)
		li = ' '.join(li.strip().split())
		li = li.rstrip('\r\n\t')

		parsed_uri = urlparse(li)
		domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
		# print (domain)
		parsed_uri1 = urlparse(url)
		domain1 = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri1)
		# print (domain1)
		# print(parsed_uri.netloc)
		if domain == domain1:
			result[index] = 1
			return 1
		else:
			result[index] = -1
			return -1


def Iframe(url, result, index):
	print(threading.current_thread().name, index)
	try:
		site = requests.get(url, headers=headers, timeout=my_timeout, verify=False)
		soup = BeautifulSoup(site.text, 'lxml')
	except:
		result[index] = 0
		return 0
	i = soup.find('iframe')
	if i is None:
		result[index] = 1
		return 1
	else:
		result[index] = -1
		return -1


def age_of_domain(url, result, index):
	print(threading.current_thread().name, index)
	age = 0
	try:
		domain = urlparse(url).netloc
		w = whois.whois(domain)

		d1 = datetime.now()
		d2 = w.creation_date
		if type(d2) is datetime:
			age = ((d1.year - d2.year) * 12)
		elif isinstance(d2, (list, tuple)):
			age = ((d1.year - d2[0].year) * 12)
		else:
			age = 0

		if isinstance(age, int):
			if age > 24:
				result[index] = 1
				return 1
			else:
				if 12 < age < 24:
					result[index] = 0
					return 0
				else:
					result[index] = -1
					return -1
		else:
			result[index] = 0
			return 0
	except:
		result[index] = 0
		return 0


def having_At_Symbol(url, result, index):
	print(threading.current_thread().name, index)
	if (url.find("@") == -1):
		result[index] = -1
		return -1
	else:
		result[index] = 1
		return 1


def having_Sub_Domain(url, result, index):
	print(threading.current_thread().name, index)
	a = 0
	b = 0
	domain = urlparse(url).hostname
	while a < len(domain):
		if domain[a] == '.':
			b = b + 1
		a = a + 1

	if (b == 2):
		result[index] = 1
		return 1
	elif (b == 3):
		result[index] = 0
		return 0
	else:
		result[index] = -1
		return -1


def Redirect(url, result, index):
	print(threading.current_thread().name, index)
	list = ['window.setTimeout', 'window.location.reload', 'setTimeout']
	try:
		site = requests.get(url, headers=headers, timeout=my_timeout, verify=False)
		soup = BeautifulSoup(site.text, 'lxml')
	except:
		result[index] = 0
		return 0
	r = 0
	for pb in soup.find_all('meta'):
		# print(pb)
		try:
			li = str(pb["http-equiv"])
			if li == "refresh":
				r = r + 1
		# print(li)
		except KeyError:
			pass

	for pb in soup.find_all('script'):
		if pb.has_attr('src'):

			if url_validate(pb.get('src')):
				try:
					Response = requests.get(pb.get('src'), timeout=my_timeout, verify=False)

					if any(x in Response.text for x in list):
						r = r + 1
					else:
						continue
				except:
					continue
			else:
				url1 = url.strip('/') + '/' + pb.get('src').strip('/')

				try:
					Response = requests.get(url1, timeout=my_timeout, verify=False)

					if any(x in Response.text for x in list):
						r = r + 1
					else:
						continue

				except:
					continue
		else:

			if any(x in pb.get_text() for x in list):
				r = r + 1
			else:
				continue
	if r == 0:
		result[index] = 1
		return 1
	else:
		result[index] = -1
		return -1


def double_slash_redirecting(url, result, index):
	print(threading.current_thread().name, index)
	if (url.rfind("//") > 7):
		result[index] = -1
		return (-1)
	else:
		result[index] = 1
		return (1)


def HTTPS_token(url, result, index):
	print(threading.current_thread().name, index)
	url = urlparse(url).hostname
	try:
		url.index('https')
		result[index] = 1
		return (1)
	except:
		result[index] = -1
		return (-1)


def having_IP_Address(url, result, index):
	print(threading.current_thread().name, index)
	url = urlparse(url)
	url = str(url.netloc)
	try:
		ind = url.index(':')
	except ValueError:
		ind = len(url)

	url = url[:ind]

	ip = url.split('.')

	if len(ip) == 4:
		# test if its ip into hexadecimal code
		try:
			url = str(int(a[0], 0)) + '.' + str(int(a[1], 0)) + '.' + str(int(a[2], 0)) + '.' + str(int(a[3], 0))
		except:
			pass

	try:
		socket.inet_aton(url)
		result[index] = 1
		return 1
	except socket.error:
		result[index] = -1
		return -1


def URL_Length(url, result, index):
	print(threading.current_thread().name, index)
	s = len(url)
	if s < 54:
		result[index] = -1
		return (-1)
	elif 54 <= s <= 75:
		result[index] = 0
		return (0)
	else:
		result[index] = 1
		return (1)


def Prefix_Suffix(url, result, index):
	print(threading.current_thread().name, index)
	url = urlparse(url).netloc
	try:
		ind = url.index('-')
		result[index] = 1
		return (1)
	except ValueError:
		result[index] = -1
		return (-1)


def Domain_registeration_length(url, result, index):
	print(threading.current_thread().name, index)
	try:
		url = urlparse(url).netloc
		domain = whois.whois(url)
		expr_date = domain['expiration_date']
		if type(expr_date) is list:
			if expr_date[0] - datetime.now() > timedelta(days=365):
				result[index] = -1
				return -1
			else:
				result[index] = 1
				return 1
		elif type(expr_date) is datetime:
			if expr_date - datetime.now() > timedelta(days=365):
				result[index] = -1
				return -1
			else:
				result[index] = 1
				return 1
		else:
			result[index] = 0
			return 0
	except:
		result[index] = 0
		return 0


def Shortining_Service(url, result, index):
	print(threading.current_thread().name, index)
	parts = urlparse(url)
	if not parts.scheme and not parts.hostname:
		# couldn't parse anything sensible, try again with a scheme.
		parts = urlparse.urlsplit("http://" + url)

	if bool(parts.hostname in services and parts.path):
		result[index] = 1
		return 1
	else:
		result[index] = -1
		return -1


def URL_of_Anchor(url, result, index):
	print(threading.current_thread().name, index)
	try:
		host_name = str(urlparse(url).hostname)
		Response = requests.get(url, timeout=my_timeout, verify=False)
	except:
		result[index] = 0
		return 0
	n = 0
	a = 0
	soup = BeautifulSoup(Response.text, 'lxml')
	n = len(soup.find_all('a'))
	if n != 0:
		for link in soup.find_all('a'):
			if not (url_validate(link.get('href'))):
				a += 1
			elif urlparse(link.get('href')).hostname != host_name:
				a += 1
	else:
		result[index] = 0
		return 0
	if a / n < 0.31:
		result[index] = -1
		return -1
	elif 0.31 < a / n < 0.64:
		result[index] = 0
		return 0
	else:
		result[index] = 1
		return 1


def port_threader(url, port, verif):
	# print(threading.current_thread().name, port)
	sock = socket.socket()
	sock.settimeout(10)
	try:
		sock.connect((url, port))
		# print('port',port)
		if port != 80 and port != 443:
			verif[0] = True
		sock.close()
	except:
		if port == 80 or port == 443:
			verif[0] = True


def port(url, result, index):
	print(threading.current_thread().name, index)
	threads1 = []
	verif = [False]
	url = urlparse(url).netloc
	for port in [21, 22, 23, 80, 443, 445, 1433, 1521, 3306, 3389]:
		thread1 = threading.Thread(target=port_threader, args=(url, port, verif))
		thread1.daemon = True
		thread1.start()
		threads1.append(thread1)

	# wait until the thread terminates.
	for thread in threads1:
		thread.join()
	if verif[0]:
		result[index] = 1
		return 1
	else:
		result[index] = -1
		return -1


def vectorize(url):
	threads = [None] * 15
	results = [None] * 15

	for index, function in enumerate(functions):
		thread = threading.Thread(target=function, args=(url, results, index))
		thread.daemon = True
		thread.start()
		threads[index] = thread

	for thread in threads:
		thread.join()
	return results

functions= [having_IP_Address,
	URL_Length,
	Shortining_Service,
	having_At_Symbol,
	double_slash_redirecting,
	Prefix_Suffix,
	having_Sub_Domain,
	Domain_registeration_length,
	Favicon,
	port,
	HTTPS_token,
	URL_of_Anchor,
	Redirect,
	Iframe,
	age_of_domain]

my_timeout=60
headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }