import requests
import bs4 as bs
import matplotlib.pyplot as plt

class statistical_analysis():
    
    def __init__(self):
        
        #self.analyze_data('https://myanimelist.net/anime/34612/Saiki_Kusuo_no_%CE%A8-nan_2/stats')
        self.go_through_list('https://myanimelist.net/animelist/HerpitehDerpo')
        
    def go_through_list(self,site='https://myanimelist.net/anime/34612/Saiki_Kusuo_no_%CE%A8-nan_2/stats'):
        
        resp = requests.get(site)
        soup = bs.BeautifulSoup(resp.text,'lxml')
        sections = soup.find_all('span')
        anime_list=[]
        #print(soup.prettify())
        for items in sections:
            items=str(items)
            if items[5]=='>':
                if items[6:-7]==("Watching"or "Completed"or"Dropped"or"Plan to Watch"or"On-Hold"):
                    continue
                else:
                    anime_list.append(items[6:-7])
            
        print(anime_list)
    
    def analyze_data(self,site='https://myanimelist.net/anime/32664/Bananya/stats'):
        
        resp = requests.get(site)
        soup = bs.BeautifulSoup(resp.text,'lxml')
        
        sections = soup.find_all('small')
        weights_d = dict()
        rating=10
        weighted_mean = 0
        
        for line in sections:
            line=str(line)
            if line.find('(')>0:
                start=line.find("(")+1
                end=line.find(" ")
                weights_d[rating]=int(line[start:end])
                rating-=1
        
        plt.bar(list(weights_d.keys()),weights_d.values(),edgecolor="none")
        plt.title("Number of People per Rating")
        plt.xlabel("Rating")
        plt.ylabel("Number of People")
        plt.show()
        
        sum_people = sum(weights_d.values())
        for i in weights_d:
            weighted_mean+=i*weights_d[i]
        weighted_mean=weighted_mean/sum_people
        
        print("The weighted average of all the rating is: ",round(weighted_mean,2))

statistical_analysis()