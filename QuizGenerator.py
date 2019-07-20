import requests, random
from bs4 import BeautifulSoup


class Person:
    def __init__(self, pid, name, url, category):
        self.id = pid
        self.name = name
        self.url = url
        self.category = category
        self.image_url = None
        self.options = None

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'category': self.category,
            'image_url': self.image_url,
            'options': self.options,
        }


class QuizGenerator:
    def __init__(self, categories_list, config_obj):
        self.config = config_obj
        persons_dict = {}
        self.category_indices = {}
        for category_name in categories_list:
            id_counter = len(persons_dict)+1
            url = self.config['BaseURL'] + self.config['CategoryURL'] + self.config['Categories'][category_name]['url']
            persons_dict.update(self.get_category_persons(url, category_name, id_counter))
            self.category_indices[category_name] = (id_counter, len(persons_dict))
        persons_dict_len = len(persons_dict)
        self.chosen_persons = []
        for i in range(0, self.config['NumberOfRounds']):
            pid = self.get_random_person(persons_dict_len)
            while not self.add_image(persons_dict[pid]) or persons_dict[pid] in self.chosen_persons:
                pid = self.get_random_person(persons_dict_len)
            self.chosen_persons.append(persons_dict[pid])

        for person in self.chosen_persons:
            success = False
            while not success:
                (success, options_ids) = self.get_options(person.category, person.id)
            person.options = [persons_dict[pid].name for pid in options_ids]
            person.options.append(person.name)
            random.shuffle(person.options)

    def get_category_persons(self, url, category, counter):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        a_tags = soup.find_all("a")
        persons_dict = {}
        for atag in a_tags:
            if atag.name == 'a' and atag.parent.name == 'div':
                if 'title' in atag.attrs and 'href' in atag.attrs and 'קטגוריה' not in atag.attrs['title']\
                        and 'ביקור בעמוד הראשי' not in atag.attrs['title']:
                    person = Person(counter, atag.attrs['title'], atag.attrs['href'], category)
                    persons_dict[counter] = person
                    counter += 1

        return persons_dict

    def add_image(self, person):
        person_page = requests.get(self.config['BaseURL'] + person.url)
        soup = BeautifulSoup(person_page.text, 'html.parser')
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            if 'property' in tag.attrs and tag.attrs['property'] == 'og:image':
                person.image_url = tag.attrs['content']
                return True
        return False

    def get_random_person(self, max_range):
        return random.randint(1, max_range)

    def get_options(self, category, correct_id):
        start = self.category_indices[category][0]
        stop = self.category_indices[category][1]
        rand_ids = random.sample(range(start, stop+1), 3)
        if correct_id in rand_ids:
            return False, None
        else:
            return True, rand_ids


    def get_questions(self):
        return self.chosen_persons
