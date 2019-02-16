import pickle
from lxml import html
import requests
from tqdm import tqdm
positive_comments_file = "positive_comments.txt"


positive_comments = []
with open(positive_comments_file,"wb") as text_file:
    for i in tqdm(range(3000)):
        try: 

            j = 1
            number_of_pages = 1
            while(j<=number_of_pages):
                page = requests.get("https://allegro.pl/uzytkownik/"+str(i)+"/oceny?recommend=true"+"&page="+str(j))
        
                tree = html.fromstring(page.content)
                    
                try:
                    number_of_pages = int(tree.xpath('//div[@class="ratings-pagination__list"]/span/text()')[1])

            
                except:
                    pass
            
                comments = tree.xpath('//span[@class="long-word-wrap"]/text()')
                positive_comments += comments
                pickle.dump(comments, text_file)
                    
                j+=1


        except:
            pass
    print("finished downloading positive comments")
    print("number of positive commments : " + str(len(positive_comments)))



      

    print("saved positive comments to file: "+ positive_comments_file)

            



    negative_comments = []
    negative_comments_file ="negative_comments.txt"
    with open(negative_comments_file,"wb") as text_file:

        for i in tqdm(range(8000)):
            try:
                j = 1
                number_of_pages = 1
                while(j<=number_of_pages):
                    page = requests.get("https://allegro.pl/uzytkownik/"+str(i)+"/oceny?recommend=false"+"&page="+str(j))
                    
                    tree = html.fromstring(page.content)
                        
                    try:
                        number_of_pages = int(tree.xpath('//div[@class="ratings-pagination__list"]/span/text()')[1])

                
                    except:
                        pass
                
                    comments = tree.xpath('//span[@class="long-word-wrap"]/text()')
                    negative_comments += comments
                    pickle.dump(comments, text_file)
                        
                    j+=1
            except:
                pass


print("finished downloading negative comments")
print("number of negative commments : " + str(len(negative_comments)))



    

print("saved negative comments to file: "+ negative_comments_file)
