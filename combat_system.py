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

    def special_ability(self, target):
        """
        Hero's Power Strike:
        Deals double attack damage, chance to stun target.
        Has cooldown to prevent consecutive use.
        """
        if self.special_cooldown > 0:
            print(f"{self.name}'s Power Strike is on cooldown for {self.special_cooldown} more turn(s).")
            return False  # Cannot use special

        damage = max(1, (self.attack * 2) - (target.defense // 2))
        print(f"{self.name} uses Power Strike!")
        target.take_damage(damage)
        print(f"{target.name} takes {damage} damage from Power Strike!")

        if random.random() < 0.3:
            target.add_status_effect({"type": "Stun", "turns": 1})
            print(f"{target.name} is stunned!")

        self.special_cooldown = 3  # Set cooldown for 3 turns
        return True  # Special used successfully

    def reduce_cooldowns(self):
        """Reduce cooldown counters by 1 if above zero."""
        if self.special_cooldown > 0:
            self.special_cooldown -= 1

class Combat:
    """
    Manages turn-based combat between player and enemies.
    """

    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies
        self.turn_queue = sorted([player] + enemies, key=lambda c: c.speed, reverse=True)
        self.current_turn_index = 0

        # Track enemy Enrage cooldowns (dict enemy -> cooldown int)
        self.enemy_enrage_cooldowns = {enemy: 0 for enemy in enemies}

    def is_combat_over(self):
        """Check if combat is over (player dead or all enemies dead)."""
        return not self.player.is_alive() or all(not e.is_alive() for e in self.enemies)

    def is_player_turn(self):
        """Check if it is currently the player's turn."""
        return self.turn_queue[self.current_turn_index] == self.player
    
    def player_turn(self, target_index, use_special=False):
        """
        Process player's turn:
        - Validate target
        - Check for stun
        - Handle attack or special ability
        """
        if target_index < 0 or target_index >= len(self.enemies):
            print("Invalid target.")
            return

        target = self.enemies[target_index]
        if not target.is_alive():
            print("Target is already defeated.")
            return

        if self.player.stunned:
            print(f"{self.player.name} is stunned and skips the turn!")
            self.player.stunned = False
            self.next_turn()
            return

        # Chance to dodge player attack
        dodge_chance = max(0.05, min(0.3, (target.speed - self.player.speed) * 0.02))
        if random.random() < dodge_chance:
            print(f"{target.name} dodged the attack!")
            self.next_turn()
            return

        # Player uses special ability if requested and not on cooldown
        if use_special:
            special_used = self.player.special_ability(target)
            if not special_used:
                print("Special ability not used; performing normal attack instead.")
                self.basic_attack(target)
        else:
            self.basic_attack(target)

        # Reduce player cooldowns at end of turn
        self.player.reduce_cooldowns()
        self.next_turn()

    def basic_attack(self, target):
        """Perform a normal attack on target, with chance for status effects."""
        damage = max(1, self.player.attack - (target.defense // 2))
        if random.random() < 0.1:
            damage = int(damage * 1.5)
            print("Critical hit!")
        target.take_damage(damage)
        print(f"{self.player.name} attacks {target.name} for {damage} damage!")

        # Chance to apply status effects on normal attack
        if random.random() < 0.2:
            target.add_status_effect({"type": "Poison", "damage": 2, "turns": 3})
            print(f"{target.name} is poisoned!")
        elif random.random() < 0.1:
            target.add_status_effect({"type": "Burn", "damage": 3, "turns": 2})
            print(f"{target.name} is burned!")

        if not target.is_alive():
            print(f"{target.name} has been defeated!")
            self.player.gain_xp(25)
    
    def process_enemy_turns(self):
        """
        Process enemy turns until it becomes the player's turn again or combat ends.
        Enemies may use Enrage if cooldown allows.
        """
        while not self.is_player_turn() and not self.is_combat_over():
            enemy = self.turn_queue[self.current_turn_index]

            if enemy.is_alive():
                enemy.apply_status_effects()

                if not enemy.is_alive():
                    print(f"{enemy.name} died from status effects.")
                    self.player.gain_xp(25)
                    self.next_turn()
                    continue

                if enemy.stunned:
                    print(f"{enemy.name} is stunned and skips the turn!")
                    enemy.stunned = False
                    self.next_turn()
                    continue

                # Enemy chance to dodge player's counterattack (conceptual)
                dodge_chance = max(0.05, min(0.3, (self.player.speed - enemy.speed) * 0.02))
                if random.random() < dodge_chance:
                    print(f"{self.player.name} dodged the attack from {enemy.name}!")
                    self.next_turn()
                    continue

                # Check if enemy can use Enrage (cooldown 3 turns)
                if self.enemy_enrage_cooldowns[enemy] > 0:
                    self.enemy_enrage_cooldowns[enemy] -= 1
                    use_enrage = False
                else:
                    use_enrage = random.random() < 0.2  # 20% chance

                damage = max(1, enemy.attack - (self.player.defense // 2))

                if use_enrage:
                    damage = int(damage * 1.5)
                    print(f"{enemy.name} uses Enrage! Increased damage!")
                    if random.random() < 0.3:
                        self.player.add_status_effect({"type": "Burn", "damage": 3, "turns": 2})
                        print(f"{self.player.name} is burned!")
                    self.enemy_enrage_cooldowns[enemy] = 3  # Set cooldown

                if random.random() < 0.1:
                    damage = int(damage * 1.5)
                    print("Enemy critical hit!")

                self.player.take_damage(damage)
                print(f"{enemy.name} attacks {self.player.name} for {damage} damage!")

            self.next_turn()

    def next_turn(self):
        """
        Advance to the next alive character in turn queue.
        Skips dead characters automatically.
        """
        self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_queue)
        while not self.turn_queue[self.current_turn_index].is_alive():
            self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_queue)

def main():
    """
    Main game loop to start combat and process player/enemy turns.
    """
    # Initialize characters
    player = Character("Hero", 100, 100, 15, 10, 12)
    enemy1 = Character("Goblin", 30, 30, 8, 5, 10)
    enemy2 = Character("Orc", 50, 50, 12, 8, 8)

    combat = Combat(player, [enemy1, enemy2])

    while not combat.is_combat_over():
        print(f"\nPlayer HP: {player.health}/{player.max_health}")
        for i, enemy in enumerate(combat.enemies, 1):
            print(f"Enemy {i} - {enemy.name}: {enemy.health}/{enemy.max_health}")

        if combat.is_player_turn():
            print("\nYour turn!")
            print("Choose a target:")
            for i, enemy in enumerate(combat.enemies, 1):
                print(f"{i}. {enemy.name} (HP: {enemy.health}/{enemy.max_health})")
            print("0. Use Special Ability")

            while True:
                try:
                    choice = int(input("Select target (or 0 for special): ")) - 1
                    if choice == -1:
                        if player.special_cooldown == 0:
                            # Use special on first alive enemy
                            for idx, e in enumerate(combat.enemies):
                                if e.is_alive():
                                    combat.player_turn(idx, use_special=True)
                                    break
                            break
                        else:
                            print(f"Power Strike is on cooldown for {player.special_cooldown} more turn(s).")
                            print("Please choose a normal attack target instead.")
                            continue
                    elif 0 <= choice < len(combat.enemies):
                        combat.player_turn(choice)
                        break
                    else:
                        print("Invalid choice. Try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        else:
            combat.process_enemy_turns()

    # Combat ended
    if player.health > 0:
        print("\nVictory! All enemies defeated!")
    else:
        print("\nDefeat! You were defeated in combat.")


if __name__ == "__main__":
    main()