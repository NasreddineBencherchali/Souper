# Souper
A python script that extract information from a given web page and display that information in a generated **HTML** file.

Currently the script extract the follwing **Tags** and **Informations** : 

* HTTP Response Header.
* Robots.txt
* ```Hyperlink Tags <a> ```
* ```Image Tags <img> ```
* ```Comment Tags <!-- --> ```
* ```Meta Tags <meta>```
* ```Hidden Inputs <input type='hidden'> ```
* ```Title Tags <title> ```
* ```Hrefs in Hyperlink Tags <a href=''> ```
* ```E-mails ```
* ```Allowed HTTP Verbs ```

The script support :
* Connection via an (HTTP, HTTPS) **proxy** 
* **Cookies** values in case login is required.

To use the script, use the following command:

**python souper.py**
