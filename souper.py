from bs4 import BeautifulSoup, Comment
import requests, cgi, urlparse, re


def send_request_and_beautify_the_response(url, cookies_dict, proxies_dict):
	# send a GET request to the website without verifying SSL, and provide cookies value
	response = requests.get(url, verify=False, cookies=cookies_dict, proxies=proxies_dict)

	# get the response in text format
	response_text = response.text

	# Beautify the response
	beautiful_response = BeautifulSoup(response_text, 'html.parser')

	# Return the response of the request and beautify it
	return response,beautiful_response

def get_response_header(r):
	response_header = r.headers
	return response_header

def get_allowed_http_verbs(url):
	verbs = ['GET', 'HEAD' , 'POST', 'PUT', 'DELETE', 'OPTIONS', 'TRACE', 'PATCH']
	allowed_verbs = []
	for every_verb in verbs:
		r = requests.request(every_verb, url)
		if r.status_code == 200:
			allowed_verbs.append(every_verb)

	return allowed_verbs

def get_information(r):
	# Get the title of the page
	page_title = r.title.string.encode("utf-8")

	# Get a list of all the links
	list_of_links = []
	for link in r.find_all('a'):
		list_of_links.append(link.get('href'))

	# Get a list of all the emails
	email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
	list_of_emails = re.findall(email_regex,r.text)
	list_of_emails_decoded = []
	for every_email in list_of_emails:
		list_of_emails_decoded.append(every_email.encode('utf-8'))

	# Returns the list of all the links found in a page in case we want to crawl them for more information
	return list_of_links, page_title, list_of_emails_decoded

def get_all_tags(r):
	# Get all the </a> tags
	list_of_all_link_tags = []
	for link_tags in r.find_all('a'):
		list_of_all_link_tags.append(link_tags)

	# Get all the <!-- --> tags
	list_of_all_comments_tags = []
	for comment_tags in r.findAll(text=lambda text:isinstance(text, Comment)):
		list_of_all_comments_tags.append(comment_tags)
	
	# Get all the <img> tags
	list_of_all_img_tags = []
	for img_tags in r.findAll('img'):
		list_of_all_img_tags.append(img_tags)

	# Get all the <meta> tags
	list_of_all_meta_tags = []
	for meta_tags in r.findAll('meta'):
		list_of_all_meta_tags.append(meta_tags)

	# Get all the hidden fields
	list_of_all_hidden_fields = []
	for hidden_fields in r.find_all("input", type="hidden"):
		list_of_all_hidden_fields.append(hidden_fields)

	return list_of_all_link_tags, list_of_all_img_tags, list_of_all_comments_tags, list_of_all_meta_tags, list_of_all_hidden_fields
	
def get_robots_txt(url):
	parsed_url = urlparse.urlparse(url)
	base_url = parsed_url.scheme + '://' + parsed_url.netloc +'/robots.txt'
	response = requests.get(base_url)
	if response.status_code == 200:
		response_text = response.text
		beautiful_response = BeautifulSoup(response_text, 'html.parser').prettify().encode('utf-8').split('\n')[:-1]
		return beautiful_response, base_url
	else:
		return False, False

# Web page content fucntions
def creating_title_header_page(page_url):
	title_header = '<table><tr class="h"><td><h1 class="p">GETTING INFORMATION ABOUT  :  <a href=' + page_url + '>'+ page_url +'</a></h1></td></tr></table><hr><ul>'
	links_header = ''

	# Link to Response_Header
	links_header = links_header + '<li><a href="#Response_Header">' + cgi.escape("Response Header") + '</a> | </li>'
	# Link ro Allowed_HTTP_Verbs
	links_header = links_header + '<li><a href="#Allowed_HTTP_Verbs">' + cgi.escape("Allowed HTTP Verbs") + '</a> | </li>'
	# Link to Robots.txt
	links_header = links_header + '<li><a href="#Robots_txt">' + cgi.escape("Robots.txt ") + '</a>  |  </li>'
	# Link to link_tags
	links_header = links_header + '<li><a href="#link_tags">' + cgi.escape("<a>") + '</a>  |  </li>'
	# Link to img_tags
	links_header = links_header + '<li><a href="#img_tags">' + cgi.escape("<img>") + '</a>  |  </li>'
	# Link to comments_tags
	links_header = links_header + '<li><a href="#comments_tags">' + cgi.escape("<!-- -->") + '</a>  |  </li>'
	# Link to meta_tags
	links_header = links_header + '<li><a href="#meta_tags">' + cgi.escape("<meta>") + '</a>  |  </li>'
	# Link to hidden_inputs
	links_header = links_header + '<li><a href="#hidden_inputs">' + cgi.escape("<input type='hidden'>") + '</a>  |  </li>'
	# Link to title_of_page
	links_header = links_header + '<li><a href="#title_of_page">' + cgi.escape("<title>") + '</a>  |  </li>'
	# Link to emails
	links_header = links_header + '<li><a href="#emails">' + cgi.escape("E-mails") + '</a>  |  </li>'
	# Link to hrefs
	links_header = links_header + '<li><a href="#hrefs">' + cgi.escape("<a href='' >") + '</a></li>'

	title_header = title_header + links_header + '</ul>'
	return title_header

def creating_content(title, content):

	if title == 'Response Header':
		page_content = '<tr><td class="e" id="Response_Header">' + title  + '</td><td class="v">'

		for field_name, field_value in content[0].iteritems():
			page_content = page_content + field_name + " : " + field_value + '</br></br>'
	
		# Get the value of the cookies
		response_cookie = content[1].cookies.get_dict()
		for field_name, field_value in response_cookie.iteritems():
			page_content = page_content +  field_name + " : " + field_value + '</br></br>'
		
		page_content = page_content + '</td></tr>'

	elif title == 'Allowed HTTP Verbs':
		page_content = '<tr><td class="e" id="Allowed_HTTP_Verbs">' + title  + '</td><td class="v">'
		for every_verb in content:
			page_content = page_content + every_verb + '</br></br>'

		page_content = page_content + '</td></tr>'

	elif title == 'Robots.txt':
		if content[0] == False:
			page_content = '<tr><td class="e" id="Robots_txt">' + title.encode("utf-8") + '</td><td class="v">'
		if content[0] != False:
			page_content = '<tr><td class="e" id="Robots_txt">' + title.encode("utf-8") + ' (<a href=' + content[1] + '>' + content[1] + '</a>)</td><td class="v">'
			for every_element in content[0]:
				if type(every_element) != type(None):
					page_content = page_content + every_element + '</br></br>'
			page_content = page_content + '</td></tr>'

	elif title == "All Tags":
		# For All Link Tags
		page_content = '<tr><td class="e" id="link_tags">' + cgi.escape("<a>")  + '</td><td class="v">'
		for every_element in content[0]:
			if type(every_element) != type(None):
				page_content = page_content + cgi.escape(every_element.encode("utf-8")) + '</br></br>'
		page_content = page_content + '</td></tr>'

		# For All Img Tags
		page_content = page_content + '<tr><td class="e" id="img_tags">' + cgi.escape("<img>")  + '</td><td class="v">'
		for every_element in content[1]:
			if type(every_element) != type(None):
				page_content = page_content + cgi.escape(every_element.encode("utf-8")) + '</br></br>'
		page_content = page_content + '</td></tr>'

		# For All Comments Tags
		page_content = page_content + '<tr><td class="e" id="comments_tags">' + cgi.escape("<!-- -->")  + '</td><td class="v">'
		for every_element in content[2]:
			if type(every_element) != type(None):
				page_content = page_content + "&lt!-- " + cgi.escape(every_element.encode("utf-8")) + '--&gt </br></br>'
		page_content = page_content + '</td></tr>'

		# For All Meta Tags
		page_content = page_content + '<tr><td class="e" id="meta_tags">' + cgi.escape("<meta>")  + '</td><td class="v">'
		for every_element in content[3]:
			if type(every_element) != type(None):
				page_content = page_content + cgi.escape(every_element.encode("utf-8")) + '</br></br>'
		page_content = page_content + '</td></tr>'

		# For All Hidden Fields
		page_content = page_content + '<tr><td class="e" id="hidden_inputs">' + cgi.escape("<input type='hidden'>")  + '</td><td class="v">'
		for every_element in content[4]:
			if type(every_element) != type(None):
				page_content = page_content + cgi.escape(every_element.encode("utf-8")) + '</br></br>'
		page_content = page_content + '</td></tr>'

	elif title == "All Information":
		
		# For all the links
		page_content = '<tr><td class="e" id="hrefs">' + cgi.escape("<a href='' >")  + '</td><td class="v">'
		for every_element in content[0]:
			if type(every_element) != type(None):
				page_content = page_content + cgi.escape(every_element.encode('utf-8')) + '</br></br>'
		page_content = page_content + '</td></tr>'

		# For the title
		page_content = page_content + '<tr><td class="e" id="title_of_page">' + cgi.escape("<title>")  + '</td><td class="v">' + content[1] + '</td></tr>'
		
		# For All the emails
		page_content = page_content + '<tr><td class="e" id="emails">' + cgi.escape("E-mails")  + '</td><td class="v">'
		for every_element in content[2]:
			if type(every_element) != type(None):
				page_content = page_content + cgi.escape(every_element.encode('utf-8')) + '</br></br>'
		page_content = page_content + '</td></tr>'
		
	return page_content

def build_web_page(url, cookies_dict, proxies_dict):

	# Send a request to the url and return the response + a beautify version of it
	response,beautiful_response = send_request_and_beautify_the_response(url, cookies_dict, proxies_dict)

	web_page = """
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "DTD/xhtml1-transitional.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml"><head>
		<style type="text/css">
		body {background-color: #fff; color: #222; font-family: sans-serif;}
		pre {margin: 0; font-family: monospace;}
		a:link {color: #009; text-decoration: none; background-color: #fff;}
		a:hover {text-decoration: underline;}
		table {border-collapse: collapse; border: 0; width: 934px; box-shadow: 1px 2px 3px #ccc;}
		.center {text-align: center;}
		.center table {margin: 1em auto; text-align: left;}
		.center th {text-align: center !important;}
		td, th {border: 1px solid #6666; font-size: 75%; vertical-align: baseline; padding: 4px 5px;}
		h1 {font-size: 150%;}
		h2 {font-size: 125%;}
		.p {text-align: left;}
		.e {background-color: #ccf; width: 300px; font-weight: bold;}
		.h {background-color: #99c; font-weight: bold;}
		.v {background-color: #ddd; max-width: 300px; overflow-x: auto;}
		.v i {color: #999;}
		img {float: right; border: 0;}
		li { display: inline;}
		hr {width: 934px; background-color: #ccc; border: 0; height: 1px;}
		</style>
		<title>Souper.py Results</title>
		</head>
		<body>
		<div class="center">
	"""

	title_header = creating_title_header_page(url)
	web_page = web_page + title_header + "<table>"

	# Building Reponse Header Content
	response_header = get_response_header(response)
	page_content = creating_content('Response Header',(response_header, response))

	# Building Allowed HTTP Verbs Content
	allowed_verbs = get_allowed_http_verbs(url)
	page_content = page_content + creating_content('Allowed HTTP Verbs', allowed_verbs)

	# Building Robots.txt Content
	robots_txt_file, base_url_for_robots_txt = get_robots_txt(url)
	page_content = page_content + creating_content('Robots.txt', (robots_txt_file, base_url_for_robots_txt))

	# Building All Tags Content
	list_of_all_link_tags, list_of_all_img_tags, list_of_all_comments_tags, list_of_all_meta_tags, list_of_all_hidden_fields = get_all_tags(beautiful_response)
	page_content = page_content + creating_content('All Tags', (list_of_all_link_tags, list_of_all_img_tags, list_of_all_comments_tags, list_of_all_meta_tags, list_of_all_hidden_fields))

	# Building All Information Content
	list_of_links, page_title, list_of_emails = get_information(beautiful_response)
	page_content = page_content + creating_content('All Information', (list_of_links, page_title, list_of_emails))

	# Finishing the page 
	web_page = web_page + page_content + "</table></div></body></html>"

	return web_page

# Other usefull functions
def write_to_file(web_page,file_name):
	# Writing the page to a file for preview 
	with open(file_name, "w"):
		pass

	with open(file_name, 'w') as html_file:
		html_file.write(web_page)
        
	print "[*] Results written to results.html [*]"

def cookies_dcit_generator(cookie_bool):
	# We create the dict that'll contain the formated values
	cookies_dict = {}
	if cookie_bool == "yes":
		# We get the cookies from the user
		cookies_value = str(raw_input("Provide the cookies value (cookie_name:cookie_value)\nIn case of multiple cookies sperate the by a commas (cookie_name_1:cookie_value, cookie_name_2:cookie_value ....))\n"))
		
		# We split the cookies entered from the user to form the dict
		cookies_value = cookies_value.split(',')

		for every_cookie in cookies_value:
			every_cookie = every_cookie.strip()
			cookie = every_cookie.split(':')
			cookies_dict[cookie[0]] = cookie[1]

	return cookies_dict

def proxy_dict_generator(proxy_bool):
	# We create the dict that'll contain the formated values
	proxies_dict = {}
	if proxy_bool == "yes":
		http_proxy = str(raw_input("HTTP PROXY : "))
		https_proxy = str(raw_input("HTTPS PROXY : "))
		cookies_dict = {'http': http_proxy, 'https': https_proxy}
	
	return proxies_dict

# The main function
if __name__ == "__main__":

	print """
 __                                               
/ _\ ___  _   _ _ __   ___ _ __       _ __  _   _ 
\ \ / _ \| | | | '_ \ / _ \ '__|     | '_ \| | | |
_\ \ (_) | |_| | |_) |  __/ |     _  | |_) | |_| |
\__/\___/ \__,_| .__/ \___|_|    (_) | .__/ \__, |
               |_|                   |_|    |___/ 
	"""

	# Get the url of the website
	url = str(raw_input("Enter the url of the website you want \n"))

	# Check if the user wants to provide a proxy
	proxy_bool = str(raw_input("Do you want to connect through a proxy ? (yes/no) \n"))
	proxies_dict = proxy_dict_generator(proxy_bool)

	# Check if the user wants to provide cookies
	cookie_bool = str(raw_input("Do you want to provide cookies ? (yes/no) \n"))
	cookies_dict = cookies_dcit_generator(cookie_bool)

	web_page = build_web_page(url, cookies_dict, proxies_dict)

	write_to_file(web_page,'results.html')
	