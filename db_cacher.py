import requests, time, datetime
from bs4 import BeautifulSoup
from PersonClass import Person


class DB_Cacher:
    def __init__(self, config_obj, dbhandler):
        self.config = config_obj
        self.dbhandler = dbhandler
        self.persons_dict = {}
        self.category_indices = {}

    def start_caching(self):
        # Collect all data from Wikipedia
        for category_name in self.config['Categories']:
            id_counter = len(self.persons_dict)+1
            url = self.config['BaseURL'] + self.config['CategoryURL'] + self.config['Categories'][category_name]['url']
            self.persons_dict.update(self.get_category_persons(url, category_name, id_counter))
            self.category_indices[category_name] = (id_counter, len(self.persons_dict))

        for person in self.persons_dict.values():
            image_exists = self.add_image(person)
            if not image_exists:
                person.image_url = ""

        # Store collected data in DB
            if "'" in person.name:
                person.name = person.name.translate(str.maketrans({"'": r"''"}))
            current_time = datetime.datetime.now()
            self.dbhandler.add_person(person.id, person.name, person.category, person.url,
                                      person.image_url, current_time)

    def add_image(self, person):
        time.sleep(1)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0"}
        print(f'getting page: {person.name}')
        person_page = requests.get(self.config['BaseURL'] + person.url, headers=headers)
        soup = BeautifulSoup(person_page.text, 'html.parser')
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            if 'property' in tag.attrs and tag.attrs['property'] == 'og:image':
                person.image_url = tag.attrs['content']
                return True
        return False

    @staticmethod
    def get_category_persons(url, category, counter):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        a_tags = soup.find_all("a")
        persons_dict_in_category = {}
        for atag in a_tags:
            if atag.name == 'a' and atag.parent.name == 'div':
                if 'title' in atag.attrs and 'href' in atag.attrs and 'קטגוריה' not in atag.attrs['title']\
                        and 'ביקור בעמוד הראשי' not in atag.attrs['title']:
                    person = Person(counter, atag.attrs['title'], atag.attrs['href'], category)
                    persons_dict_in_category[counter] = person
                    counter += 1

        return persons_dict_in_category
