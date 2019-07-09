import requests, Constants, random
from bs4 import BeautifulSoup


class Person:
    def __init__(self, pid, name, url):
        self.id = pid
        self.name = name
        self.url = url
        self.image_url = None
        self.options = None

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'image_url': self.image_url,
            'options': self.options,
        }


class QuizGenerator:
    def __init__(self, category):
        persons_dict = self.get_category_persons(category)
        persons_dict_len = len(persons_dict)
        self.chosen_persons = []
        for i in range(0, Constants.NumberOfRounds):
            pid = self.get_random_person(persons_dict_len)
            while not self.add_image(persons_dict[pid]):
                pid = self.get_random_person(persons_dict_len)
            self.chosen_persons.append(persons_dict[pid])

        for person in self.chosen_persons:
            success = False
            while not success:
                (success, options_ids) = self.get_different_options(person.id, persons_dict_len )
            options_ids = random.sample(range(1, persons_dict_len), 3)
            person.options = [persons_dict[pid].name for pid in options_ids]
            person.options.append(person.name)
            random.shuffle(person.options)

    def get_category_persons(self, category):
        url = Constants.BaseURL + Constants.Categories[category]

        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        a_tags = soup.find_all("a")
        persons_dict = {}
        counter = 1
        for atag in a_tags:
            if atag.name == 'a' and atag.parent.name == 'div':
                if 'title' in atag.attrs and 'href' in atag.attrs and 'קטגוריה' not in atag.attrs['title']\
                        and 'ביקור בעמוד הראשי' not in atag.attrs['title']:
                    person = Person(counter, atag.attrs['title'], atag.attrs['href'])
                    persons_dict[counter] = person
                    counter += 1

        return persons_dict

    def add_image(self, person):
        person_page = requests.get(Constants.BaseURL + person.url)
        soup = BeautifulSoup(person_page.text, 'html.parser')
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            if 'property' in tag.attrs and tag.attrs['property'] == 'og:image':
                person.image_url = tag.attrs['content']
                return True
        return False

    def get_random_person(self, max_range):
        return random.randint(1, max_range)

    def get_different_options(self, num, max_range):
        rand_list = random.sample(range(1, max_range), 3)
        if num in rand_list:
            return False, None
        else:
            return True, rand_list

    def get_questions(self):
        return self.chosen_persons
