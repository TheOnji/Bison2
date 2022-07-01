


class Food():

    def __init__(self, Food_choice):

        self.CriticalHit = 0
        self.Determination = 0
        self.DirectHitRate = 0
        self.SkillSpeed = 0
        self.SpellSpeed = 0
        self.Tenacity = 0
        self.Piety = 0

        self.Vitality = 0

        self.Foodstats = ' '


        match Food_choice:
            case 1:
                self.Food = 'Archon Burger'
                self.DirectHitRate = 90
                self.Vitality = 93
                self.Determination = 54
                self.Foodstats = 'DH/DET'
                self.percent = 0.10

            case 2:
                self.Food = 'Beef Stroganoff'
                self.SkillSpeed = 90
                self.Vitality = 93
                self.DirectHitRate = 54
                self.Foodstats = 'SKS/DH'
                self.percent = 0.10

            case 3:
                self.Food = 'Pumpkin Ratatouille'
                self.CriticalHit = 90
                self.Vitality = 93
                self.SkillSpeed = 54
                self.Foodstats = 'CRT/SKS'
                self.percent = 0.10

            case 4:
                self.Food = 'Pumpkin Potage'
                self.Determination = 90
                self.Vitality = 93
                self.CriticalHit = 54
                self.Foodstats = 'DET/CRIT'
                self.percent = 0.10

            case 5:
                self.Food = 'Scallop Salad'
                self.Tenacity = 90
                self.Vitality = 93
                self.Determination = 54
                self.Foodstats = 'TEN/DET'
                self.percent = 0.10

            case 6:
                self.Food = 'Scallop Curry'
                self.Determination = 90
                self.Vitality = 93
                self.Tenacity = 54
                self.Foodstats = 'DET/TEN'
                self.percent = 0.10














