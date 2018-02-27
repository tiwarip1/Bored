import bs4 as bs
import requests

def find_url(stock='TSLA'):
    
    url = 'https://www.marketwatch.com/investing/stock/'+str(stock)+'/charts'
    r = requests.get(url)
    data = r.text
    soup = bs.BeautifulSoup(data)
    print(soup)

def main():
    
    find_url()
    
main()