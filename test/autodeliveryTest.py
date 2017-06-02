import requests
mlcookie = {"_d2id":"8860766b-d95d-4db6-b3b4-b5514c3fc181", 'orgpms':'6510056', 'pmsword':'mercado.libre',\
    '__unam':'d23464-15c5a23b77a-7c78750d-45', '_ga':'GA1.2.1596026962.1496160910', '_gid':'GA1.2.1183062292.1496362250'}
r = requests.get(r"http://localhost:5000/login",cookies = mlcookie,allow_redirects=True)
requests.get(r"http://localhost:5000/test",cookies ={**r.cookies, **mlcookie})


