import requests
# import urllib.request
from bs4 import BeautifulSoup
from lxml import etree
import re
# import pandas

class JobGetter:
    main_url = 'https://www.pracuj.pl/praca/'
    url_job = '/fotowoltaika;kw'
    job_date_added = '/ostatnich 24h;p,1?sc=0'
    table_with_job_offers = []
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
                       '''//*[contains(text(), "ofert pracy") and not(self::script)]''',
                       '''//*[contains(text(), "oferta pracy") and not(self::script)]''']

        found_number_of_offers = False
        for i in oferty_list:
            try:
                number_of_offers = dom.xpath(i)
                if number_of_offers:
                    offer_digit = re.findall('\d+', number_of_offers[0].text)
                    number_of_offers = int(offer_digit[0])
                    print(';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;')
                    print(number_of_offers)
                    print(';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;')
                    print('')
                    found_number_of_offers = True
                    return number_of_offers
                else:
                    print(f"No elements found for XPath '{i}'")
            except Exception as e:
                print(f"Error while selecting XPath '{i}': {e}")
        if not found_number_of_offers:
            raise Exception("None of the elements in oferty_list met the condition.")
        return None
        # number_of_offers = dom.xpath(path_without_script)  
        
        # div_tag = soup.find('div', class_='hrb6ql3 t1c1o3wg')
      
    
    def get_offers_from_page(self, path, number_of_offers):
        '''pobiera oferty ze strony, (przechodzenie na nowe strony)'''

        soup = BeautifulSoup(path.text, 'html.parser')
        dom = etree.HTML(str(soup))

        def find_xpaths(dom, path_list: list):
            '''sprawdza ktory xpath pobierze dane z listy xpathow'''
            for i in path_list:
                try:
                    elements = dom.xpath(i)
                    if elements[0].text is not None:
                        return elements
                    else:
                        print(f"No elements found for XPath '{i}'")
                except Exception as e:
                    print(f"Error while selecting XPath '{i}': {e}")

        
        def find_xpaths_url(dom, path_list: list):
            '''sprawdza ktory xpath pobierze dane z listy xpathow dla url'''
            for i in path_list:
                try:
                    elements = dom.xpath(i)
                    if elements[0] is not None:
                        return elements
                    else:
                        # XPATH ZAGNIEZDZONY
                        # '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/a[1]'
                        print(f" ::URL:: No elements found for XPath '{i}'")
                except Exception as e:
                    print(f"::URL:: Error while selecting XPath '{i}': {e}")


        def search_in_path_list():
            
            xpath_offer_id =['/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]',
                             '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[1]/div[3]']
            
            xpath_miasto = ['/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/h5[1]',
                    # SUPEROFERTA
                    '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/h5[1]', 
                    # PIERWSZA OFERTA NA STRONIE
                    '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[2]/h5[1]']
                                         
            xpath_stanowisko = ['/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/h2[1]/a[1]',
                                '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[3]/div[1]/div[1]/div[2]/h2[1]',
                                '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/h2[1]/a[1]',
                                '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/a[1]',
                                # SUPEROFERTA
                                '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/h2[1]/a[1]',
                                '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/h2[1]',
                                # PIERWSZA OFERTA NA STRONIE
                                '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/h2[1]/a[1]',
                                '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[3]/div[1]/div[1]/div[2]/h2[1]/a[1]',
                                # ELEMENT BEZ TAGU A
                                '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/h2[1]',
                                '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[3]/div[1]/div[1]/div[2]/h2[1]/a[1]'            
                                ]

            xpath_firma = ['/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/a[1]/h4[1]',
                            # SUPEROFERTA
                        '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/a[1]',
                        '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/a[1]/h4[1]',
                            # PIERWSZA OFERTA NA STRONIE
                        '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[2]/h5[1]'  
                        ]
            
            xpath_url = ['/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[3]/div[1]/a[1]',
                         '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/a[1]',
                         '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[1]/div[3]/div[1]/a[1]'
                         ]

            xpath_salary = ['/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/span[1]',
                            '/html[1]/body[1]/div[1]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[' + str(i) + ']/div[1]/div[1]/div[1]/div[2]/span[2]']

            try:
                # print('sciezki bledu miasto=========')
                print('MIASTO <')
                xpath_miasto_search = find_xpaths(dom, xpath_miasto)[0].text
                print('MIASTO >')
                if not xpath_miasto_search:
                    print('Nie znaleziono miasta..--..')
                    xpath_miasto_search = 'brak'
            except TypeError:
                xpath_miasto_search = 'brak'

            try:
                # print('sciezki bledu stanowisko=========')
                print('STANOWISKO <')
                xpath_stanowisko_search = find_xpaths(dom, xpath_stanowisko)[0].text
                print('STANOWISKO >')
                if not xpath_stanowisko_search:
                    print('Nie znaleziono stanowiska..--..')
                    xpath_stanowisko_search = 'brak'   
            except TypeError:
                xpath_stanowisko_search = 'brak'

            try:
                # print('sciezki bledu firma=========')
                print('FIRMA <')
                xpath_firma_search = find_xpaths(dom, xpath_firma)[0].text
                print('FIRMA >')
                if not xpath_firma_search:
                    print('Nie znaleziono firmy..--..')
                    xpath_firma_search = 'brak'
            except TypeError:
                xpath_firma_search = 'brak'
    
            try:
                # print('sciezki bledu firma=========')
                print('STAWKA <')
                xpath_salary_search = find_xpaths(dom, xpath_salary)[0].text
                print('STAWKA >')
                if not xpath_salary_search:
                    print('Nie znaleziono stawki..--..')
                    xpath_salary_search = 'brak'
            except TypeError:
                xpath_salary_search = 'brak'


            if re.match("\d+\s+lokalizacje", xpath_miasto_search):
                print("The variable starts with 'lokalizac'.")
                xpath_url_search = 'brak'

            else:  
                try:
                    # print('sciezki bledu firma=========')
                    print('URL <')
                    xpath_url_search = find_xpaths_url(dom, xpath_url)[0].get('href')
                    print('URL >')
                    if not xpath_url_search:
                        print('Nie znaleziono url..--..')
                        xpath_url_search = 'brak'
                except TypeError:
                    xpath_url_search = 'brak'

            try:
                # print('sciezki bledu firma=========')
                print('ID <')
                xpath_offer_id_search = find_xpaths_url(dom, xpath_offer_id)[0].get('data-test-offerid')
                print('ID >')
                if not xpath_offer_id_search:
                    print('Nie znaleziono id..--..')
                    xpath_offer_id_search = 'brak'
            except TypeError:
                xpath_offer_id_search = 'brak'

            # print('')
            # print('::'+str(i)+'::')
            # print('--------------------------------------------------------------')
            # print(xpath_offer_id_search)
            # print(xpath_miasto_search)  
            # print(xpath_firma_search)
            # print(xpath_stanowisko_search)
            # print(xpath_salary_search)
            # print(xpath_url_search)
            # print('--------------------------------------------------------------')
            # print('')

            offer_full_data = {'offer_id': xpath_offer_id_search, 'offer_position': xpath_stanowisko_search,
                                'offer_city': xpath_miasto_search, 'offer_company': xpath_firma_search,
                                'offer_salary': xpath_salary_search, 'offer_url':xpath_url_search}
            
            
            JobGetter.table_with_job_offers.append(offer_full_data)
            


        if number_of_offers < 50:
            for i in range(1,number_of_offers):
                search_in_path_list()
        else:
            for i in range(1,51):
                search_in_path_list()


    def loop_over_the_pages(self, number_of_offers,path):
        '''przechodzi pomiedzy stronami z ofertami pracy'''  

        if number_of_offers > 50:
            number_of_pages = number_of_offers//50    
            for i in range(1, number_of_pages+1):
                path = requests.get(self.main_url+ self.url_job+self.job_date_added + str('?pn=') + str(i+1))
                print('')
                JobGetter.get_offers_from_page(self, path, number_of_offers)
                print('------------------------------------------------------')
                print('END OF PAGE: {0}'.format(i))
        else:
            path = requests.get(self.main_url+ self.url_job+self.job_date_added + str('?pn=1'))
            print('')
            JobGetter.get_offers_from_page(self, path, number_of_offers)
            print('------------------------------------------------------')
            print('END OF PAGE')


    def show_obtainded_offers(self):
        for i in JobGetter.table_with_job_offers:
            print(i)


    def add_offers_to_database(self):
        '''add data to database mongo ?'''
        pass

# BAZA DANYCH:
# ID STANOWISKO FIRMA LOKALIZACJA- BEDZIE ROZNIE DATA-DODANIA-DO-BAZY 

