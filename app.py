from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.imdb.com/search/title/?release_date=2021-01-01,2021-12-31')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('div', attrs={'class':'lister-list'})

nama_film = table.find_all('h3', attrs={'class':'lister-item-header'})
imdb_rating = table.find_all('div', attrs={'class':'ratings-bar'})
metascore_rating = table.find_all('div', attrs={'class':'ratings-bar'})
votes_counts = table.find_all('p', attrs={'class':'sort-num_votes-visible'})


row_length = len(nama_film)

Film_list=[]
imdb_rating_list=[]
metascore_rating_list =[]
votes_counts_list =[]


for i in range(row_length):
    Film_list.append(nama_film[i].find('a').text)
    imdb_rating_list.append(imdb_rating[i].find('strong').text)
    votes_counts_list.append(votes_counts[i].find('span',attrs={'name':'nv'}).text.replace(',',''))
    try:
        metascore_rating_list.append(metascore_rating[i].find('div', attrs={'class':'inline-block ratings-metascore'}).find('span').text.strip())
    except:
        metascore_rating_list.append('0')
    


#change into dataframe
data = pd.DataFrame({'JUDUL':Film_list,'RATING IMDB':imdb_rating_list,'RATING METASCORE':metascore_rating_list,'VOTING':votes_counts_list})

#insert data wrangling here
data['VOTING']=data['VOTING'].astype('int64')
data['RATING METASCORE']=data['RATING METASCORE'].astype('int64')
data['RATING IMDB']=data['RATING IMDB'].astype('float64')
data7=data.head(7).copy()

#end of data wranggling 

@app.route("/")
def index(): 
    
    card_data = f'{round(data7["RATING IMDB"].mean(),2)}' #be careful with the " and ' 

    # generate plot
    ax = data7[['JUDUL','RATING IMDB']].sort_values(by='RATING IMDB',ascending=False).plot(x='JUDUL',kind='bar',rot=0,figsize = (20,9)) 
    
    # Rendering plot
    # Do not change this
    figfile = BytesIO()
    plt.savefig(figfile, format='png', transparent=True)
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    plot_result = str(figdata_png)[2:-1]

    # render to html
    return render_template('index.html',
        card_data = card_data, 
        plot_result=plot_result
        )


if __name__ == "__main__": 
    app.run(debug=True)