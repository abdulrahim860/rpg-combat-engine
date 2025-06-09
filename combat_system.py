import random

class Character:
    """
    Represents a character in the game with stats, status effects, and abilities.
    """

    def __init__(self, name, health, max_health, attack, defense, speed, level=1, xp=0):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.level = level
        self.xp = xp
        self.xp_to_level = 50
        self.status_effects = []
        self.stunned = False  # Indicates if character is stunned this turn
        self.special_cooldown = 0  # Cooldown for special abilities

    def is_alive(self):
        """Check if character is alive."""
        return self.health > 0
    
    def apply_status_effects(self):
        """
        Apply ongoing status effects like Poison, Burn, or Stun,
        update turns left, and remove expired effects.
        """
        self.stunned = False  # Reset stun at start of effect processing

        for effect in self.status_effects[:]:
            if effect["type"] == "Poison":
                self.health -= effect["damage"]
                print(f"{self.name} takes {effect['damage']} poison damage!")
            elif effect["type"] == "Burn":
                self.health -= effect["damage"]
                print(f"{self.name} takes {effect['damage']} burn damage!")
            elif effect["type"] == "Stun":
                self.stunned = True
                print(f"{self.name} is stunned and might miss their turn!")

            effect["turns"] -= 1
            if effect["turns"] <= 0:
                self.status_effects.remove(effect)

    def take_damage(self, amount):
        """Reduce health by damage amount, minimum 0."""
        self.health = max(0, self.health - amount)

    def add_status_effect(self, effect):
        """
        Add a status effect; if effect exists, refresh duration.
        Effect format: {"type": str, "damage": int, "turns": int}
        """
        for e in self.status_effects:
            if e["type"] == effect["type"]:
                e["turns"] = max(e["turns"], effect["turns"])
                return
        self.status_effects.append(effect)

    def gain_xp(self, amount):
        """Increase XP and level up if XP threshold is reached."""
        self.xp += amount
        print(f"{self.name} gained {amount} XP!")
        while self.xp >= self.xp_to_level:
            self.level_up()

    def level_up(self):
        """Increase level and improve stats."""
        self.level += 1
        self.xp -= self.xp_to_level
        self.xp_to_level += 20
        self.max_health += 10
        self.health = self.max_health
        self.attack += 2
        self.defense += 2
        self.speed += 1
        print(f"{self.name} leveled up to Level {self.level}!")