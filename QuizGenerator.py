import random


class QuizGenerator:
    def __init__(self, categories_list, config_obj, dbhandler):
        self.config = config_obj
        self.dbhandler = dbhandler
        self.chosen_persons = []
        num_of_rounds = self.config['NumberOfRounds']
        round_ = 0
        while round_ < num_of_rounds:
            rolled_category = random.choice(categories_list)
            rolled_person, rolled_category_persons_list = self.get_random_person(rolled_category)
            print(f'{round_}: rolled person is: {rolled_person.name}')
            if rolled_person.name not in [person.name for person in self.chosen_persons]:
                success = False
                options_names = None
                while not success:
                    (success, options_names) = self.get_options(rolled_person, rolled_category_persons_list)
                rolled_person.options = options_names
                rolled_person.options.append(rolled_person.name)
                random.shuffle(rolled_person.options)
                self.chosen_persons.append(rolled_person)
                round_ += 1

    @staticmethod
    def get_options(correct_person, persons_in_category_list):
        options = random.choices(persons_in_category_list, k=3)
        options_names = [opt_person.name for opt_person in options]
        if correct_person.name in options_names:
            return False, None
        else:
            return True, options_names

    def get_random_person(self, category):
        category_persons_list = self.dbhandler.get_category_persons(category)
        rolled_person = random.choice(category_persons_list)

        return rolled_person, category_persons_list

    def get_questions(self):
        return self.chosen_persons
