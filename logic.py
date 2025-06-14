from random import randint
import requests

from datetime import datetime, timedelta

class Pokemon:
    pokemons = {}
    
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
        self.original_stats = self.pokemon_stats.copy()
        self.last_hp_recovery = datetime.now()
        self.buff_expiration = None
        Pokemon.pokemons[pokemon_trainer] = self

    def check_hp_recovery(self):
        now = datetime.now()
        if (now - self.last_hp_recovery) >= timedelta(minutes=10):
            recovery_count = (now - self.last_hp_recovery) // timedelta(minutes=10)
            hp_to_add = 10 * recovery_count
            self.pokemon_stats['hp'] = min(self.pokemon_stats['hp'] + hp_to_add, self.original_stats['hp'])
            self.last_hp_recovery = now
            return True
        return False

    def feed(self):
        now = datetime.now()
        full_hp = self.original_stats['hp']
        current_hp = self.pokemon_stats['hp']
        
        if current_hp < full_hp:
            missing_hp = full_hp - current_hp
            heal_amount = missing_hp * 0.3
            self.pokemon_stats['hp'] = min(current_hp + heal_amount, full_hp)
            return f"Покемон покормлен! Восстановлено {heal_amount:.1f} HP."
        else:
            self.pokemon_stats['attack'] = int(self.original_stats['attack'] * 1.15)
            self.pokemon_stats['defense'] = int(self.original_stats['defense'] * 1.10)
            self.buff_expiration = now + timedelta(minutes=15)
            return "Покемон сыт! +15% к атаке и +10% к защите на 15 минут."

    def check_buffs(self):
        if self.buff_expiration and datetime.now() >= self.buff_expiration:
            self.pokemon_stats['attack'] = self.original_stats['attack']
            self.pokemon_stats['defense'] = self.original_stats['defense']
            self.buff_expiration = None
            return "Баффы от кормления закончились."
        return None

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
            return {'hp': 100, 'attack': 50, 'defense': 50}

    # Метод класса для получения информации
    def info(self):
        stats = '\n'.join([f'\t{key}: {value}' for key, value in self.pokemon_stats.items()])
        return f"Имя твоего покеомона: {self.name}\nТип: {self.pokemon_type}\nCпособность: {self.pokemon_ability}\nВысота: {self.pokemon_height}\nВес: {self.pokemon_weight}\nСтатистика:\n{stats}"

    # Метод класса для битвы покемонов
    def fight(self, opponent):
        if self.pokemon_stats['defense'] > opponent.pokemon_stats['attack']:
            damage = opponent.pokemon_stats['attack'] * 0.4  # 60% защиты, 40% урона
        else:
            damage = opponent.pokemon_stats['attack'] * 0.7  # 30% защиты, 70% урона
        
        self.pokemon_stats['hp'] -= damage
        if self.pokemon_stats['hp'] <= 0:
            return f"{self.name} проиграл битву!"
        else:
            return f"{self.name} победил битву!"

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img
