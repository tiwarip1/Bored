import bs4 as bs
import requests


def nasdaq_data(ticker = 'TSLA'):
    '''still need to add the additional data for csv's'''
    url = 'https://www.nasdaq.com/symbol/{}/real-time'.format(ticker)
          
    page = requests.get(url).text
    soup = bs.BeautifulSoup(page,'lxml')
    table = soup.find('div',{'class':'genTable'})
    
    row_l = []
    for row in table.findAll('span')[8:]:
        row=list(row)
        row_l.append(row)
        
    returned = []
    returned.append(float(row_l[0][0]))
    returned.append(int(row_l[4][0].replace(',','')))
    print(returned)
    
    return returned
        
nasdaq_data()