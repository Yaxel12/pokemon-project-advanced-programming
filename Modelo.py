class Move:
    def __init__(self, url):
        req = requests.get(url)
        self.json = req.json()
        self.name = self.json['name']
        self.power = self.json['power']
        self.type = self.json['type']['name']


class Pokemon:
    def __init__(self, name, level):
        req = requests.get(f'{base_url}/pokemon/{name.lower()}')
        self.json = req.json()
        self.name = name
        self.level = level
        self.stats = self.json['stats']
        self.set_stats()
        self.types = [type['type']['name'] for type in self.json['types']]
        self.moves = self.set_moves()

    def set_stats(self):
        for stat in self.stats:
            if stat['stat']['name'] == 'hp':
                self.current_hp = stat['base_stat'] + self.level
                self.max_hp = stat['base_stat'] + self.level
            elif stat['stat']['name'] == 'attack':
                self.attack = stat['base_stat']
            elif stat['stat']['name'] == 'defense':
                self.defense = stat['base_stat']
            elif stat['stat']['name'] == 'speed':
                self.speed = stat['base_stat']

    def set_moves(self):
        moves = []
        for move_data in self.json['moves']:
            versions = move_data['version_group_details']
            for version in versions:
                if version['version_group']['name'] != 'red-blue':
                    continue
                if version['move_learn_method']['name'] != 'level-up':
                    continue
                if self.level >= version['level_learned_at']:
                    move = Move(move_data['move']['url'])
                    if move.power is not None:
                        moves.append(move)
        return random.sample(moves, min(4, len(moves)))

    def perform_attack(self, other, move):
        damage = (2 * self.level + 10) / 250 * self.attack / other.defense * move.power
        if move.type in self.types:
            damage *= 1.5
        if random.randint(1, 10000) <= 625:
            damage *= 1.5
        damage = math.floor(damage)
        other.take_damage(damage)

    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0
