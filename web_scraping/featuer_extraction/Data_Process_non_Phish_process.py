import os
import re
import sys
import csv
import json
import whois
import socket
import ctypes
import schedule
import requests
import threading
import multiprocessing
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime,timedelta
from multiprocessing import Pool, JoinableQueue, Value

services = [
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
def Favicon(url):
	li=''
	try:
		site=requests.get(url,headers=headers, timeout=my_timeout)
		soup = BeautifulSoup(site.text,'lxml')
	except:
		return 0

	p=""
	if soup.find('link',rel="shortcut icon")==-1:
		return 0
	else:
		for pb in soup.find_all('link',rel="shortcut icon"):
			p=p+str(pb)
			li=pb["href"]
			#print(li)
		li= ' '.join(li.strip().split())
		li = li.rstrip('\r\n\t')

		parsed_uri = urlparse(li)
		domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
		#print (domain)
		parsed_uri1 = urlparse(url)
		domain1 = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri1)
		#print (domain1)
		#print(parsed_uri.netloc)
		if domain==domain1:
			return 1
		else:
			return -1
def Iframe(url):
	try:
		site=requests.get(url,headers=headers, timeout=my_timeout)
		soup = BeautifulSoup(site.text, 'lxml')
	except:
		return 0
	i=soup.find('iframe')
	if i is None :
		return 1
	else:
		return -1
def age_of_domain(url):
	age=0
	try:
		domain=urlparse(url).netloc
		w= whois.whois(domain)
		
		d1=datetime.now()
		d2=w.creation_date
		if type(d2) is datetime:
			age=((d1.year-d2.year)*12)
		elif isinstance(d2, (list, tuple)):
				age=((d1.year-d2[0].year)*12)
		else:
			age= 0
			
		if isinstance(age, int):
			if age>24:
				return 1
			else:
				if 12<age<24 :
					return 0
				else:
					return -1
		else:
			return 0	
	except:
		return 0
def having_At_Symbol (url):
	if (url.find("@") == -1):
		return -1
	else:
		return 1
def having_Sub_Domain (url):
	a=0
	b=0
	domain=urlparse(url).hostname
	while a < len(domain):
		if domain[a] == '.':
			b = b + 1
		a = a + 1

	if (b==2):
		return 1
	elif (b==3):
		return 0
	else:
		return(-1)
def Redirect(url):
	list=['window.setTimeout','window.location.reload','setTimeout']
	try:
		site=requests.get(url,headers=headers, timeout=my_timeout)
		soup = BeautifulSoup(site.text, 'lxml')
	except:
		return 0
	r=0
	for pb in soup.find_all('meta'):
		#print(pb)
		try:
			li=str(pb["http-equiv"])
			if li=="refresh":
				r=r+1
				#print(li)
		except KeyError:
				pass
	
	for pb in soup.find_all('script'):
		if pb.has_attr('src'):

			if url_validate(pb.get('src')):
				try:
					Response=requests.get(pb.get('src'), timeout=my_timeout)
				
					if any(x in Response.text for x in list):
						r=r+1
					else :
						continue
				except:
					continue
			else:
				url1=url.strip('/')+'/'+pb.get('src').strip('/')
				
				try:
					Response=requests.get(url1, timeout=my_timeout)
					
					if any(x in Response.text for x in list):
						r=r+1
					else :
						continue
						
				except:
					continue
		else:
		
			if any(x in pb.get_text() for x in list):
				r=r+1
			else :
				continue	
	if r==0:
		return 1
	else:
		return -1		
def double_slash_redirecting(url):
	if (url.rfind("//") > 7):
		return(-1)
	else:
		return("1")
def HTTPS_token(url):
	url=urlparse(url).hostname
	try:
		url.index('https')
		return(1)
	except:
		return(-1)
def having_IP_Address(url):
	url = urlparse(url)
	url=str(url.netloc)
	try:
		ind=url.index(':')
	except ValueError :
		ind=len(url) 

	url=url[:ind]	
	
	ip = url.split('.')
	
	if len(ip)==4 :
		#test if its ip into hexadecimal code
		try:
			url = str(int(a[0],0))+'.'+ str(int(a[1],0)) +'.'+ str(int(a[2],0)) +'.'+ str(int(a[3],0))
		except:
			pass
	
	try:
		socket.inet_aton(url)
		return 1
	except socket.error:
		return -1
def URL_Length (url):
	s=len(url)
	if s<54 :
		return (-1)
	elif 54<=s<=75 :
		return(0)
	else :
		return(1)
def Prefix_Suffix(url):
	url = urlparse(url).netloc
	try:
		ind=url.index('-')
		return(1)
	except ValueError :
		return(-1)
def Domain_registeration_length(url):
	try:
		url=urlparse(url).netloc
		domain = whois.whois(url)
		expr_date=domain['expiration_date']
		if type(expr_date) is list:
			if expr_date[0]-datetime.now() > timedelta(days=365):
				return -1
			else :
				return 1
		elif type(expr_date) is datetime:
			if expr_date-datetime.now() > timedelta(days=365):
				return -1
			else :
				return 1
		else :
			return 0
	except :
		return 0
def Shortining_Service(url):
	parts = urlparse(url)
	if not parts.scheme and not parts.hostname:
		# couldn't parse anything sensible, try again with a scheme.
		parts = urlparse.urlsplit("http://"+url)

	if bool(parts.hostname in services and parts.path):	
		return 1
	else :
		return -1
def URL_of_Anchor(url):
	try:
		host_name=str(urlparse(url).hostname)
		Response=requests.get(url, timeout=my_timeout)
	except :
		return 0	
	n=0
	a=0
	soup = BeautifulSoup(Response.text, 'lxml')
	n=len(soup.find_all('a'))
	if n!=0:
		for link in soup.find_all('a'):
				if not(url_validate(link.get('href'))):
					a+=1
				elif  urlparse(link.get('href')).hostname!=host_name :
					a+=1
	else:
		return 0
	if a/n < 0.31:
		return -1
	elif 0.31<a/n<0.64:
		return 0
	else :
		return 1
def port_threader(url,port,verif):
	#print(threading.current_thread().name, port)
	sock = socket.socket()
	sock.settimeout(10) 
	try:
		sock.connect((url,port))
		#print('port',port)
		if port !=80 and port!=443:
			verif[0]=True
		sock.close()
	except:
		if port ==80 or port==443:
			verif[0]=True
def port(url):
	threads1 = []
	verif=[False]
	url=urlparse(url).netloc
	for port in [21, 22, 23, 80, 443, 445, 1433, 1521, 3306, 3389]:
		thread1 = threading.Thread(target=port_threader,args=(url,port,verif))
		thread1.daemon = True
		thread1.start()
		threads1.append(thread1)
		
	# wait until the thread terminates.
	for thread in threads1:
		thread.join()
	if verif[0]:
		return 1
	else :
		return -1	

def run_thread(url,lock,writer,i,range_):
	print('-->'+str(range_.value)+'--'+url)
	pool = Pool(processes=15)
	try:
		return_functions=[pool.apply_async(function,[url]) for function in functions]
		results=[return_function.get(60) for return_function in return_functions]
		pool.close()
	except KeyboardInterrupt:
		print("You pressed Ctrl+C")
		pool.terminate()
	lock.acquire()
	writer.writerow(results)
	i.value+=1
	lock.release()
	print(str(i.value)+'  URLs done')
	

def threader(q,lock,i,range_,data_size,event=None):
	with open('data/result_p.csv',"a",newline='') as result_file:
		writer = csv.writer(result_file, dialect='excel',delimiter=',')
		
		# schedule.every(0.01).minutes.do()          
		while not event.is_set():
			url = q.get()
			run_thread(url,lock,writer,i,range_)
			# schedule.run_pending()
			q.task_done()
					
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
	

# Create the queue for holding the URLs ready to be processed 


if __name__ == '__main__':
	proc=[]
	t1 = datetime.now()
	my_timeout=90
	data_size=5000
	i=0
	range_=0
	headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
	lock = multiprocessing.Lock()
	q = JoinableQueue()
	
	with open('data/result_p.csv',"w",newline='') as result_file:
		writer = csv.writer(result_file, dialect='excel',delimiter=',')
		synch_i=Value(ctypes.c_int, 0)
		synch_range_=Value(ctypes.c_int, 0)
		event = multiprocessing.Event()
		for x in range(4):
			p = multiprocessing.Process(target=threader,args=(q,lock,synch_i,synch_range_,Value(ctypes.c_int, data_size)), kwargs={'event' : event})
			# p.daemon = True
			p.start()
			proc.append((p, event))
			
				
		with open('top-1m.csv', 'r') as f:
			data = csv.reader(f)
			for row in data:
				url='http://www.'+str(row[1])
				url = url.rstrip()
				try:
					Response=requests.get(url,headers=headers, timeout=my_timeout)
					Response.raise_for_status()
					q.put(url)
					
					synch_range_.value+=1
				except KeyboardInterrupt:
					print ("You pressed Ctrl+C")
					# Tell all processes to shut down
					for _, event in proc:
						event.set()

					# Now actually wait for them to shut down
					for p, _ in proc:
						p.join()
					result_file.close()
					t2 = datetime.now()
					total = t2 - t1
					print('Scanning Completed in: ', total)
					# sys.exit()
					q.join()
				except requests.exceptions.RequestException as e:
					print('Exception :',e.__class__)
				except Exception as e:
					print('Exception :',e.__class__)
				except :
					print('OTHER Exception ')
				
				if(synch_range_.value==data_size):
					q.join()
					for p in proc:
						p.join()
					print('work done')
					result_file.close()
					t2 = datetime.now()
					total = t2 - t1
					print('Scanning Completed in: ', total)
					break
					print(i)