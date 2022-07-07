
class Food_data():
    def __init__(self):
        self.options = []
        self.options.append({'Name':'Archon Burger',
                            'Stats':'DH/DET',
                            'CRT': 0,
                            'DET': 54,
                            'DH': 90,
                            'SKS': 0,
                            'SPS': 0,
                            'TEN': 0,
                            'PIE': 0,
                            'VIT': 93,
                            'Percent': 0.08})

        self.options.append({'Name':'Beef Stroganoff',
                            'Stats':'SKS/DH',
                            'CRT': 0,
                            'DET': 0,
                            'DH': 54,
                            'SKS': 90,
                            'SPS': 0,
                            'TEN': 0,
                            'PIE': 0,
                            'VIT': 93,
                            'Percent': 0.08})

        self.options.append({'Name':'Pumpkin Ratatouille',
                            'Stats':'CRT/SKS',
                            'CRT': 90,
                            'DET': 0,
                            'DH': 0,
                            'SKS': 54,
                            'SPS': 0,
                            'TEN': 0,
                            'PIE': 0,
                            'VIT': 93,
                            'Percent': 0.08})

        self.options.append({'Name':'Pumpkin Potage',
                            'Stats':'DET/CRT',
                            'CRT': 54,
                            'DET': 90,
                            'DH': 0,
                            'SKS': 0,
                            'SPS': 0,
                            'TEN': 0,
                            'PIE': 0,
                            'VIT': 93,
                            'Percent': 0.08})

        self.options.append({'Name':'Scallop Salad',
                            'Stats':'TEN/DET',
                            'CRT': 0,
                            'DET': 54,
                            'DH': 0,
                            'SKS': 0,
                            'SPS': 0,
                            'TEN': 90,
                            'PIE': 0,
                            'VIT': 93,
                            'Percent': 0.08})

        self.options.append({'Name':'Scallop Curry',
                            'Stats':'DET/TEN',
                            'CRT': 0,
                            'DET': 90,
                            'DH': 0,
                            'SKS': 0,
                            'SPS': 0,
                            'TEN': 54,
                            'PIE': 0,
                            'VIT': 93,
                            'Percent': 0.08})
        
    def __call__(self, Food_ID):
        self.__dict__.update(self.options[Food_ID - 1])

    def __repr__(self):
        output = self.__dict__.copy()
        output.pop('options')
        for key, val in output.items():
            print(f"{key} = {val}")
        return ''

    def list(self):
        print('Food options')
        for i, option in enumerate(self.options ,start = 1):
            print(f"{i}: {option['Name']}")



            