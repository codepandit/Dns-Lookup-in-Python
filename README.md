# Dns Lookup

This program will allow you to send dns query to your default server or you can choose the dns server to send your query

## Getting Started

To use dns.py user will require to enter atleast one parameter that is website or IP address of website. Other two parameters are optional you can enter the DNS's IP address of your choice and you also can choose the query type from ["MX", "CNAME", "PTR", "AA is default"]


To run the GUI program you have to run python dnsGui.py

## Dependecies 
```
pip install dnslib 
```

### Examples 


```
python dns.py microsoft.com
```

```
python dns.py microsoft.com --dns_ip 8.8.8.8
```

```
python dns.py microsoft.com --dns_ip 8.8.8.8 --rtype MX
```

```
python dnsGui.py
```



## Author

* **Nikhil Mehral** - [codepandit](https://github.com/codepandit)
The repository is private


