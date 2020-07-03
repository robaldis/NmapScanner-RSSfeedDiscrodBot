# insultgen.py


import requests 
from bs4 import BeautifulSoup 
import json
  
def news(): 
    # the target we want to open     
    url='https://insult.mattbas.org/api/insult'
      
    #open with GET method 
    resp=requests.get(url) 
      
    #http_respone 200 means OK status 
    if resp.status_code==200: 
        # we need a parser,Python built-in HTML parser is enough . 
        soup=BeautifulSoup(resp.text,'html.parser')     
        
        new_insult = {
            'insult':str(soup) 
        }
        with open('test.json', 'r+') as outfile:
            data = json.load(outfile)
        
            for insult in data:
                if insult == new_insult:
                    print(f'MATCHED\n {insult}\n {new_insult}')
                    break
                else:
                    data.append(new_insult)
                    break
            outfile.seek(0)
            outfile.write(json.dumps(data))  
            outfile.close()
        
    else: 
        print("Error") 


while True:     
    news()
