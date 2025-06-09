# RPG Combat Engine

A Python-based turn-based RPG combat system featuring characters with stats, level progression, status effects (Poison, Burn, Stun), special abilities with cooldowns, and a dynamic turn queue based on character speed.

## 🛠️ Features

- Turn-based combat system
- Character leveling and XP gain
- Status effects with turn-based duration
- Special abilities with cooldown
- Enemy AI with special skills and conditions

## 🚀 Setup Instructions

1. **Clone the repository:**
   
   git clone https://github.com/abdulrahim860/rpg-combat-engine.git
   cd rpg-combat-engine
   
2. **Run the program:**

    python combat_system.py

## ▶️ How to play

- The game starts with your hero vs two enemies.
- On your turn, you'll choose a target or use your special ability (if available).
- Enemies attack and may use skills.
- Combat ends when either the player dies or all enemies are defeated.

## 📌 Additional Notes

- Status effects like Poison and Burn deal damage over time.
- Stun prevents the affected character from acting for 1 turn.
- Power Strike is the player’s special move that deals bonus damage and can stun.
- Enemies can occasionally use "Enrage" for increased damage and inflict Burn.

## 📁 File Structure

- rpg_combat.py – Main code file containing all classes and logic
- README.md – Project documentation