

def Main():
    Onji = Character(Level = 90,
                     Strength=0,
                     Dexterity=0,
                     Vitality=0,
                     Intelligence=0,
                     Mind=0,
                     CriticalHit=0,
                     Determination=0,
                     DirectHitRate=0,
                     Defense=0,
                     MagicDefense=0,
                     AttackPower=0,
                     SkillSpeed=0,
                     AttackMagicPotency=0,
                     HealingMagicPotency=0,
                     SpellSpeed=0,
                     Tenacity=0,
                     Piety=0)

    print(Onji.Level)


class Character():
    def __init__(self, Name, Job, Level, HP, Strength, Dexterity, Vitality, Intelligence, Mind, CriticalHit,
                 Determination, DirectHitRate, Defense, MagicDefense, AttackPower, SkillSpeed,
                 AttackMagicPotency, HealingMagicPotency, SpellSpeed, Tenacity, Piety):
        self.Name = Name
        self.Level = Level
        self.HP = HP
        self.Strength = Strength
        self.Dexterity = Dexterity
        self.Vitality = Vitality
        self.Intelligence = Intelligence
        self.Mind = Mind
        self.CriticalHit = CriticalHit
        self.Determination = Determination
        self.DirectHitRate = DirectHitRate
        self.Defense = Defense
        self.MagicDefense = MagicDefense
        self.AttackPower = AttackPower
        self.SkillSpeed = SkillSpeed
        self.AttackMagicPotency = AttackMagicPotency
        self.HealingMagicPotency = HealingMagicPotency
        self.SpellSpeed = SpellSpeed
        self.Tenacity = Tenacity
        self.Piety = Piety
        self.Job = Job


if __name__ == "__main__":
    Main()
