from random import randint
import requests

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer   

        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.pokemon_type = self.get_type()
        self.pokemon_ability = self.get_ability()
        self.pokemon_height = self.get_height()
        self.pokemon_weight = self.get_weight()
        self.pokemon_stats = self.get_stats()

        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']['front_default'])
        else:
            return "картинка"
        
    def get_type(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['types'][0]['type']['name'])
        else:
            return "normal"

    # Метод для получения способности покемона через API
    def get_ability(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['abilities'][0]['ability']['name'])
        else:
            return "no ability"

    # Метод для получения высоты покемона через API
    def get_height(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['height'])
        else:
            return "0"

    # Метод для получения веса покемона через API
    def get_weight(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['weight'])
        else:
            return "0"
        
    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"

    def get_stats(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        else:
            return {}

    # Метод класса для получения информации
    def info(self):
        return f"Имя твоего покеомона: {self.name}\nТип: {self.pokemon_type}\nСпособность: {self.pokemon_ability}\nВысота: {self.pokemon_height}\nВес: {self.pokemon_weight}\nСтатистика: {self.pokemon_stats}"

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img 



