Phishing websites have several criteria that distinguish them from legitimate ones. To make an end to phishing,
 many solutions were proposed in the literature. 
 We were mostly motivated by the [survey suggested by Dr Rami M. Mohammad](http://eprints.hud.ac.uk/id/eprint/24236/), a software engineer graduated
  from the University of Huddersfield.

These features could be divided into 4 groups:

-   **URL based Features** : These are the features that analyze the URL of the website.

-   **Abnormal based features** : These features deal with servers and require the use of third parties such as WHOIS database.

-   **HTML and JavaScript based features** : For these features , we used the Web Scraping technique in order to extract data from the HTML and JavaScript code.

-   **Domain based features** : These features extracted from the WHOIS Database .

Currently, this project could extract 19 different features from each website.

Below, we give you the names of the features used by their group:


|Feature Group | Features' Names |
|--------------------------|------------------------------------------------------------------|
|URL based features | Having IP address <br/> URL length<br/> URL having "@" Symbol<br/> HTTPS token in the domain part of the url<br/> Shortening services<br/> double\_slash\_redirecting<br/> Prefic\_Suffix in the domain<br/> Having subdomains<br/> sum\_of\_symbole\_eq<br/> sum\_of\_symbole\_and<br/> exist\_of\_symbol\_ab<br/> exist\_of\_symbole\_anch |
|Abnormal based features | URL of Anchor <br/> SFH <br/> Port|
|HTML and JavaScript based features | Redirect <br/> IFrame <br/> Redirect\_html| 
|Domain based features | Age of Domain <br/> Domain registration duration|
 





Below, are the details of each feature ,and the rule behind its extraction:

|Feature Group | Feature’s Name & Details |
|--------------------------|----------------------------------------------------------------------------------|
|Having IP address | If the domain part has an IP address : return 1 otherwise : return -1 |
|URL length | If URL length < 54 : return -1 else if 54<=URL length <=75 : return 0 else : return 1|
|URL having "@" Symbol | If having « @ » symbol then : return 1 else : return -1|
|HTTPS token in the domain part of the URL | If using HTTP token in domain part of the URL: return 1 otherwise return -1|
|Shortening services |  If using shortening services : return 1 else : return -1|
|double\_slash\_redirecting | If the existing of « // » in the path part of the URL : return 1 else : return -1|
|Prefix\_Suffix in the domain | If the domain name part including « - » symbol : return 1 else : return -1|
|Domain registration duration | If Domain expires on ≤ year : return 1 else if domain expires on ≥ 1 year : return -1 else record in WHOIS not existing : return 0|
|Having subdomains | If number of subdomains >1 : return 1 else if number of subdomain <=1 : return -1 else if (TLD non-existing in Mozilla's TLD list) : return 0|
|Port | If the number of port used is of the preferred status(fig1) : return -1 else : return 1|
|sum\_of\_symbole\_eq | If the number of « = » symbol < 3 : return -1 else : return 1|
|sum\_of\_symbole\_and | If the number of « & » symbol < 3 : return -1 else : return 1|
|exist\_of\_symbol\_ab | If the URL has « ~ » symbol : return 1 else : return -1|
|exist\_of\_symbole\_anch | If URL has « \# » symbol : return 1 else return -1|
|URL of Anchor | If \% of URL anchor < 31\% : return -1 else if \% of 31\%≤ URL anchor ≤ 67\%: return 0 else : return 1|
|Redirect | If the website has been redirected less then 2 times : return -1 else if it has been redirected twice : return 0 else : return 1|
|Redirect\_html | If the number of redirections in the HTML DOM =0 : return -1 else  : return 1|
|IFrame | If using Iframe : return 1 else return 0|
|Age of Domain| If age ≥ 6 months : return -1 else if no WHOIS record : return 0 else : return 1 |
|SFH| If the SFH contains empty string or "about:blank" : return 1 else if SFH doesn't exist : return 0 else : return -1 |