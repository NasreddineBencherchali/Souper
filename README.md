# Souper [![python](https://img.shields.io/badge/Python-2.7-green.svg?style=style=flat-square)](https://www.python.org/downloads/)  [![version](https://img.shields.io/badge/Version-Beta-blue.svg?style=style=flat-square)](https://twitter.com/nas_bench)

A python script that extract information from a given web page and display that information in a generated **HTML** file.

## Requirements

* **Requests**
* **Selenium**
* **BeautifulSoup**
* **ChromeDriver** - [Download Link](https://goo.gl/gtYUc1) (Copy downloaded file in the root of the python installation)

## Functionalities

Currently the script extract the follwing **Tags** and **Informations** :

* ```HTTP Response Header```
* ```Robots.txt```
* ```Hyperlink Tags <a>```
* ```Image Tags <img>```
* ```Comment Tags <!-- -->```
* ```Meta Tags <meta>```
* ```Hidden Inputs <input type='hidden'>```
* ```Title Tags <title>```
* ```Hrefs in Hyperlink Tags <a href=''>```
* ```E-mails```
* ```Allowed HTTP Verbs```

The script support :

* Connection via an (HTTP, HTTPS) **Proxy**
* Requesting the page via a headless browser via the **Selenium** Module using **ChromeDriver**
* **Cookies** : In case login is required (Not yet supported when using Selenium Module)

## Usage

```bash
python souper.py
```
