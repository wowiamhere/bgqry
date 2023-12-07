#!/home/user1/.venv/bgfb-env/bin/python

import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process, Queue
import time
import random

import bgfb_spider 

import smtplib, ssl
from email.message import EmailMessage
import requests

STORED_HASH = '.......'
counter = 1

def send_mail_txt():
	try:
		port = 465
		smtp_server = 'smtp.mail.yahoo.com'
		sender_em = ''
		receiver_em = ''
		psswrd = ''
		msg = "NEW POST!!!!NEW POST!!!"

		message = EmailMessage()
		message['Subject'] = 'alert'
		message['From'] = sender_em
		message['To'] = receiver_em
		message.set_content( msg )

		context = ssl.create_default_context()
		with smtplib.SMTP_SSL( smtp_server, port, context=context ) as server:
			server.login( sender_em, psswrd )
			server.send_message( message )
	
	except Exception as e:
		print('-----ERROR--------EMAIL----> ',e)


def send_telegram_alert(msg):
	token = ''
	url = f'https://api.telegram.org/bot{token}'
	params = { 'chat_id':'', 'text':msg}

	resp = requests.get( url + '/sendMessage', params=params )
	
	return resp


def run_spider(spider):
	def f(q):
		try:
			process = CrawlerProcess(get_project_settings())
			process.crawl( spider )
			process.start()
			new_hash = bgfb_spider.CURRENT_HASH
			new_post = bgfb_spider.CURRENT_POST
			process.join()
			q.put(new_hash)
			q.put(new_post)
		except Exception as e:
			q.put(e)
			send_telegram_alert(f'----run_spider------ERROR--->{e}')

	q = Queue()
	p = Process(target=f, args=(q,))
	p.start()
	result = [q.get(), q.get()]

	return result


while True:
	try:
		result = run_spider(bgfb_spider.bgfb)

		if (result[0] != STORED_HASH):
			send_telegram_alert(f'++++\n{result[1]}\n\n--\nnew:\n{result[0]}\n--\nold:\n{STORED_HASH}\n--{counter}--\n')			
			STORED_HASH = result[0]

		counter=counter+1
		time.sleep( random.randrange(61, 92, 1) )

	except Exception as e:
		print('!!!!!!----->###$$$#EEEEEE----->',e)
		send_telegram_alert(f'---main --------ERROR------>{e}')
