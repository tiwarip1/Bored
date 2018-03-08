import bs4 as bs
import requests

def find_url(stock='TSLA'):
    
    url = 'https://www.marketwatch.com/investing/stock/'+str(stock)
    r = requests.get(url).text
    soup = bs.BeautifulSoup(r,'lxml')
    price = str(soup.find('meta',{'name':'price'}))
    
    position_start = int(price.find('"'))
    price = price[price.find('"')+1:price.find('"',position_start+2)]
    
    url = 'https://finance.yahoo.com/quote/{ticker}?p={ticker}'.format(ticker = stock)
    r = requests.get(url).text
    soup = bs.BeautifulSoup(r,'lxml')
    
    volume = str(soup.find('span',{'data-reactid':'73'}))
    print(volume)

def main():
    
    find_url()
    
main()