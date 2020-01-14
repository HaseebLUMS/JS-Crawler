# JS-Crawler
A selenium-based tool which takes a list of URLs as input and outputs all the scripts used in the resulting webpages of input URLs. In the case of web JavaScript, there are generally two types of script objects: (1) inline scripts which are embedded in the HTML page itself e.g. <script> … </script> and, (2) external scripts fetched from some server for which link is given in the page as “src” attribute in the “script” tags e.g. <script src = “abc.com/xyz.js”></script>. For collecting inline scripts, JS Crawler parses the HTML webpage given by selenium and collects all the scripts. And, for collecting external scripts, JS Crawler generates requests for all those scripts for which “src” attribute is found in the HTML page. For generating the requests, JS Crawler uses Python’s "requests” library and it also stores all src attributes (e.g abc.com/xyz.js in above example) which are used for generating requests. 


To Run: python topMillion.py "totalMachines" "current machine number"

e.g for total 5 machines run 
on machine 1: python topMillion.py 5 1 

on machine 2: python topMillion.py 5 2

on machine 3: python topMillion.py 5 3

on machine 4: python topMillion.py 5 4

on machine 5: python topMillion.py 5 5


=> data will be stored in data/ folder (user should make an empty folder named "data" before starting crawler)
=> file to source URL log will be stored in logs/ folder  (user should make an empty folder named "logs"before starting crawler)
