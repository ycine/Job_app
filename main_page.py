import requests
# import urllib.request
from bs4 import BeautifulSoup
from lxml import etree
import re
# import pandas

class JobGetter:
    main_url = 'https://www.pracuj.pl/praca/'
    url_job = '/mechanik;kw'
    job_date_added = '/ostatnich 24h;p,1'
    # full_url = 'https://www.pracuj.pl/praca/python;kw/ostatnich%2024h;p,1'
    # full_url_page = 'https://www.pracuj.pl/praca/python;kw/ostatnich%2024h;p,1?pn=2'


    def connect_to_webpage(self):
        '''sprawdza czy jest polaczenie z sciezka http'''
        response = requests.get(self.main_url)
        
        return response


    def define_jobs(self, job, date_added):
        '''wprowadz nazwe oferty, przedzial czasowy, '''
        path = requests.get(self.main_url+str(job)+str(date_added))
        
        # print(path.url)
        return path
        

    def get_number_of_offers(self, path):
        '''pobierz liczbe ofert ze strony'''
        soup = BeautifulSoup(path.text, 'html.parser')
        dom = etree.HTML(str(soup))
        
        # soup = BeautifulSoup(path.text, 'lxml')
        # number_of_offers = soup.select_one('span.j1lr4pyy')
        # print(soup)
        
        # TA SCIEZKA PONIZEJ JEST SCIEZKA ABSOLUTNA
        # xpath1 = '''/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/span[1]/span[1]'''
        # print(dom.xpath('//*[contains(text(), "ofert pracy")]')[0].text)


        oferty_list = ['''//*[contains(text(), "oferty pracy") and not(self::script)]''', 
                       '''//*[contains(text(), "ofert pracy") and not(self::script)]''']

        for i in oferty_list:
                try:
                    number_of_offers = dom.xpath(i)
                    # number_of_offers = '{}[not(self::script)]'.format(number_of_offers[0])
                    if number_of_offers: 
                        offer_digit = re.findall('\d+', number_of_offers[0].text)
                        number_of_offers = int(offer_digit[0])
                        print(';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;')
                        print(number_of_offers)
                        print(';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;')
                        print('')
                        return number_of_offers

                    else:
                        print(f"No elements found for XPath '{i}'")
                except Exception as e:
                    print(f"Error while selecting XPath '{i}': {e}")

        
        
        # number_of_offers = dom.xpath(path_without_script)  
        
        # div_tag = soup.find('div', class_='hrb6ql3 t1c1o3wg')
      
# Find the span tag with class "j1lr4pyy" inside the div tag
        # number_of_offers = soup.find("span", {"class": re.compile("j1lr4pyy")})
        # print(number_of_offers.text)

        # span_tag = div_tag.find('span', class_='core_j1lr4pyy')

        # # Extract the text content of the span tag
        # text = span_tag.get_text()

        # # Extract the number from the text
        # number = int(text.split()[0])  # Split the text by space and get the first part as integer

        # print(number) 
        # number_of_offers = soup.find('span', class_='j1lr4pyy')
        # text = number_of_offers.get_text()

        return None
 

    def get_offers_from_page(self, path):
        '''pobiera oferty ze strony, (przechodzenie na nowe strony)'''

        soup = BeautifulSoup(path.text, 'html.parser')
        dom = etree.HTML(str(soup))
        # cz1 = soup.select("b1iadbg8")

        def find_xpaths(dom, path_list: list):
            '''sprawdza ktory xpath pobierze dane z listy xpathow'''
            for i in path_list:
                try:
                    elements = dom.xpath(i)
                    if elements:
                        # print(f"Found {len(elements)} elements matching XPath '{i}'")
                        return elements
                    else:
                        print(f"No elements found for XPath '{i}'")
                except Exception as e:
                    print(f"Error while selecting XPath '{i}': {e}")


        try:

            for i in range(1,51):
                                
                xpath_miasto = ['/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/h5[1]',
                # SUPEROFERTA
                    '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/h5[1]',
                # PIERWSZA OFERTA NA STRONIE
                    '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[2]/h5[1]']
                                    
                                
                xpath_stanowisko = ['/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/h2[1]/a[1]',
                # SUPEROFERTA
                '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/h2[1]/a[1]',
                # PIERWSZA OFERTA NA STRONIE
                '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/h2[1]/a[1]',
                # ELEMENT BEZ TAGU A
                '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/h2[1]']


                xpath_firma = ['/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/a[1]/h4[1]',
                            # SUPEROFERTA
                            '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/h5[1]',
                            # PIERWSZA OFERTA NA STRONIE
                            '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[2]/h5[1]']

                xpath_miasto = find_xpaths(dom,xpath_miasto)
                xpath_stanowisko = find_xpaths(dom, xpath_stanowisko)
                xpath_firma = find_xpaths(dom,xpath_firma)
                
                for count, (miasto, stanowisko, firma) in enumerate(zip(xpath_miasto, xpath_stanowisko, xpath_firma),1):
                    print('')
                    print('::'+str(i)+'::')
                    print('{}.. CITY:  {} \n JOB: {}  \n COMPANY: {} \n LINK: {}'.format(count, miasto.text, stanowisko.text, firma.text, stanowisko.get('href')))
                    print('')

            
        except IndexError:
            print("Index out of range")
            
        # MIASTO
        # SCIEZKA ABSOLUTNA 
        # cz1 = soup.find_all("span", {"class": re.compile("b1iadbg8")})
    
        # NAZWA STANOWISKA
        # SCIEZKA ABSOLUTNA

        # cz2 = soup.find_all("h2", {"class": re.compile("b1iadbg8")})
        # cz2 = dom.xpath(xpath_stanowisko)
        # print(cz2)

        # NAZWA FIRMY
        # SCIEZKA ABSOLUTNA

        # cz3 = soup.find_all("div", {"class": re.compile("c147p5yp")})
        # cz3 = dom.xpath(xpath_firma)

        # LINK
        # SCIEZKA ABSOLUTNA
        # xpath_link = '''/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[3]/div[1]/div[1]/div[1]/div[2]/h2[1]/a[1]'''
        # cz4 = soup.find_all("a", {"class": re.compile("o1o6obw3")})
        # cz4 = dom.xpath(xpath_link)

    def loop_over_the_pages(self, number_of_offers,path):
        '''przechodzi pomiedzy stronami z ofertami pracy'''  

        if number_of_offers > 50:
            number_of_pages = number_of_offers//50    
            for i in range(1, number_of_pages+1):
                path = requests.get(self.main_url+ self.url_job+self.job_date_added + str('?pn=') + str(i+1))
                print('')
                JobGetter.get_offers_from_page(self, path)
                print('------------------------------------------------------')
                print('END OF PAGE: {0}'.format(i))
        else:
            pass
         


    def add_offers_to_database(self):
        '''add data to database mongo ?'''
        pass



