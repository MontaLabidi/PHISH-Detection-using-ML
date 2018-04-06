import re
import sys
import csv
import json
import whois
import socket
import requests
import threading
import multiprocessing
from queue import Queue
from tld import get_tld
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime,timedelta
from multiprocessing.pool import ThreadPool

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

def having_IP_Address(url,result,index):
	print(threading.current_thread().name,index)
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
			url = str(int(ip[0],0))+'.'+ str(int(ip[1],0)) +'.'+ str(int(ip[2],0)) +'.'+ str(int(a[3],0))
		except:
			pass
	
	try:
		socket.inet_aton(url)
		result[index] =1
		return 1
	except socket.error:
		result[index] =-1
		return -1
def URL_Length (url,result,index):
	print(threading.current_thread().name,index)
	s=len(url)
	if s<54 :
		result[index] =-1
		return (-1)
	elif 54<=s<=75 :
		result[index] =0
		return(0)
	else :
		result[index] =1
		return(1)
def Shortining_Service(url,result,index):
	print(threading.current_thread().name,index)
	parts = urlparse(url)
	if(parts.hostname.find('www.')==0):
		domain=parts.hostname.replace('www.','')
	else :
		domain=parts.hostname

	if bool(domain in services and parts.path):	
		result[index] =1
		return 1
	else :
		result[index] =-1
		return -1
def having_At_Symbol (url,result,index):
	print(threading.current_thread().name,index)
	if (url.find("@") == -1):
		result[index] =-1
		return -1
	else:
		result[index] =1
		return 1
def double_slash_redirecting(url,result,index):
	print(threading.current_thread().name,index)
	if (url.rfind("//") > 7):
		result[index] =-1
		return -1
	else:
		result[index] =1
		return 1
def Prefix_Suffix(url,result,index):
	print(threading.current_thread().name,index)
	url = urlparse(url).netloc
	try:
		ind=url.index('-')
		result[index] =1
		return 1
	except ValueError :
		result[index] =-1
		return -1
def having_Sub_Domain (url,result,index):
	print(threading.current_thread().name,index)
	res = get_tld(url, as_object=True, fail_silently=True)
	if not res:
		result[index] =0
		return 0
	if res.subdomain.count('.')<2:
		result[index] =-1
		return -1
	else :
		result[index] =1
		return 1
def Domain_registeration_length(url,result,index):
	print(threading.current_thread().name,index)
	
	
	try :
		tld = get_tld(url, as_object=True, fail_silently=True).tld
		domain = whois.whois(tld)
		expr_date=domain['expiration_date']
		# print(expr_date)
	except :
		result[index] =0
		return 0
	if type(expr_date) is list:
		if expr_date[0]-datetime.now() > timedelta(days=365):
			result[index] =-1
			return -1
		else :
			result[index] =1
			return 1
	elif type(expr_date) is datetime:
		if expr_date-datetime.now() > timedelta(days=365):
			result[index] =-1
			return -1
		else :
			result[index] =1
			return 1
	else :
		result[index] =0
		return 0
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
def port(url,result,index):
	print(threading.current_thread().name,index)
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
		result[index] =1
		return 1
	else :
		result[index] =-1
		return -1	
def HTTPS_token(url,result,index):
	print(threading.current_thread().name,index)
	url=urlparse(url).hostname
	try:
		url.index('https')
		result[index] =1
		return 1
	except:
		result[index] =-1
		return -1
def URL_of_Anchor(url,result,index):
	print(threading.current_thread().name,index)
	try:
		host_name=str(urlparse(url).hostname)
		Response=requests.get(url, timeout=my_timeout)
	except :
		result[index] =0
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
		result[index] =0
		return 0
	if a/n < 0.31:
		result[index] =-1
		return -1
	elif 0.31<a/n<0.64:
		result[index] =0
		return 0
	else :
		result[index] =1
		return 1
def Redirect(url,result,index):
	print(threading.current_thread().name,index)

	Response=requests.get(url,headers=headers, timeout=my_timeout)
	if len(Response.history)<2:
		result[index] =-1
		return -1
	elif len(Response.history)<3:
		result[index] =0
		return 0
	else :
		result[index] =1
		return 1
def Redirect_html(url,result,index):
	print(threading.current_thread().name,index)
	list=['window.setTimeout','window.location.reload','setTimeout']

	site=requests.get(url,headers=headers, timeout=my_timeout)
	soup = BeautifulSoup(site.text, 'lxml')
	
	r=0
	for script in soup.find_all('meta'):
		# print(script)
		if script.has_attr('http-equiv'):
			li=str(script["http-equiv"])
			# print(li)
			if li=="refresh":
				r=r+1
				# print ('refreshhhhhhhhhhh')
	for script in soup.find_all('script'):
		if script.has_attr('src'):
			if url_validate(script.get('src')):
				try:
					Response=requests.get(script.get('src'), timeout=my_timeout)
				
					if any(x in Response.text for x in list):
						# print ('redirecttttttt')
						r=r+1
					else :
						continue
				except:
					continue
			else:
				url1=url.strip('/')+'/'+script.get('src').strip('/')
				
				try:
					Response=requests.get(url1, timeout=my_timeout)
					
					if any(x in Response.text for x in list):
						# print ('redirecttttttt22222222')
						r=r+1
					else :
						continue
						
				except:
					continue
		else:
		
			if any(x in script.get_text() for x in list):
				# print ('redirecttttttt333333333')
				r=r+1
			else :
				continue	
	if r==0:
		result[index] =-1
		return -1
	else:
		result[index] =1
		return 1
	
def Iframe(url,result,index):
	print(threading.current_thread().name,index)

	Response=requests.get(url,headers=headers, timeout=my_timeout)
	soup = BeautifulSoup(Response.text, 'lxml')
	
	if not soup.find('iframe') :
		result[index] =1
		return 1
	else:
		result[index] =-1
		return -1
def SFH(url,result,index):
	print(threading.current_thread().name,index)
	Response=requests.get(url, headers=headers)
	Response.raise_for_status()
	soup = BeautifulSoup(Response.text, 'lxml')
	form =soup.find('form')
	
	if form :
		if form.has_attr("action"):
			action=form["action"]
			if url_validate(action) or action.find('/')==0:
				result[index] =-1
				return -1
			else :
				result[index] =1
				return 1
		else :
			if urlparse(url).scheme=='https' :
				result[index] =-1
				return -1
			else :
				result[index] =1
				return 1
	else :
		result[index] =0
		return 0
def age_of_domain(url,result,index):
	print(threading.current_thread().name,index)
	
	# url=urlparse(url).netloc
	
	
	try :
		tld = get_tld(url, as_object=True, fail_silently=True).tld
		domain = whois.whois(tld)
		crt_date=domain.creation_date
		# print(crt_date)
	except :
		result[index] =0
		return 0
	if type(crt_date) is list:
		if crt_date[0]-datetime.now() > timedelta(days=180):
			result[index] =-1
			return -1
		else :
			result[index] =1
			return 1
	elif type(crt_date) is datetime:
		if crt_date-datetime.now() > timedelta(days=180):
			result[index] =-1
			return -1
		else :
			result[index] =1
			return 1
	else :
		result[index] =0
		return 0

def sum_of_symbole_eq(url,result,index):
	print(threading.current_thread().name,index)
	if url.count('=')<3:
		result[index] =-1
		return -1
	else :
		result[index] =1
		return 1
def sum_of_symbole_perc(url,result,index):
	print(threading.current_thread().name,index)
	if url.count('%')<3:
		result[index] =-1
		return -1
	else :
		result[index] =1
		return 1
def sum_of_symbole_and(url,result,index):
	print(threading.current_thread().name,index)
	if url.count('&')<3:
		result[index] =-1
		return -1
	else :
		result[index] =1
		return 1
def exist_of_symbole_ab(url,result,index):
	print(threading.current_thread().name,index)
	if url.count('~'):
		result[index] =1
		return 1
	else :
		result[index] =-1
		return -1
def exist_of_symbole_anch(url,result,index):
	print(threading.current_thread().name,index)
	if url.count('#'):
		result[index] =1
		return 1
	else :
		result[index] =-1
		return -1
	
functions = [having_IP_Address,
			Shortining_Service,
			having_At_Symbol,
			double_slash_redirecting,
			Prefix_Suffix,
			having_Sub_Domain,
			Domain_registeration_length,
			port,
			HTTPS_token,
			URL_of_Anchor,
			Redirect,
			Iframe,
			age_of_domain,
			SFH]
	
def run_thread(url):
	threads = [None] * 14
	results = [None] * 14
	ind=0
	print('-->'+str(range_)+'--'+url)
	for index,function in enumerate(functions):
		thread = threading.Thread(target=function,args=(url,results,index))
		thread.daemon = True
		thread.start()
		threads[index]=thread
		
	for thread in threads:
		thread.join()
	
	with lock:
			writer.writerow(results)

	global i
	i+=1
	print(str(i)+'  URLs done')
	
lock = threading.Lock()

def threader():
	while True:
		url = q.get()
		run_thread(url)
		q.task_done()
	
"""functions = [having_IP_Address,
			URL_Length,
			Shortining_Service,
			having_At_Symbol,
			double_slash_redirecting,
			Prefix_Suffix,
			having_Sub_Domain,
			Domain_registeration_length,
			port,
			HTTPS_token,
			URL_of_Anchor,
			Redirect,
			Iframe,
			age_of_domain,
			sum_of_symbole_eq,
			sum_of_symbole_perc,
			sum_of_symbole_and,
			exist_of_symbole_ab,
			exist_of_symbole_anch]"""
		
data_size=12000
i=0
range_=0

threads=[]
my_timeout=90
headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }

# Create the queue for holding the URLs ready to be processed 
q = Queue()

if __name__ == '__main__':
	t1= datetime.now()
	for x in range(50):
			t = threading.Thread(target=threader)
			t.daemon = True
			t.start()
	with open('data/extracted_Non_Phish.csv',"w",newline='') as result_file:
		writer = csv.writer(result_file, dialect='excel',delimiter=',')
		# json_data=open('verified_online12.json').read()
		# data = json.loads(json_data)
		#creating a number of threads 
		#these threads will be waiting for any url to be put in the queue so they process it
		with open('data/top-1m.csv', 'r') as f:
			data = csv.reader(f)
			for row in data:
				url='http://www.'+str(row[1])
				url = url.rstrip()
				try:
					Response=requests.get(url,headers=headers, timeout=my_timeout)
					Response.raise_for_status()
					q.put(url)
					range_+=1
				except KeyboardInterrupt:
					print ("You pressed Ctrl+C")
					result_file.close()
					t2 = datetime.now()
					total = t2 - t1
					print('Scanning Completed in: ', total)
					sys.exit()
				except requests.exceptions.RequestException as e:
					print('Exception :',e.__class__)
				except Exception as e:
					print('Exception :',e.__class__)
				except :
					print('OTHER Exception ')
				
				if(range_==data_size):
					q.join()
					result_file.close()
					t2 = datetime.now()
					total = t2 - t1
					print('Scanning Completed in: ', total)
					break
					print(i)