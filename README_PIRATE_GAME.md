# 🏴‍☠️ Tiny Epic Pirates - Terminal Edition

A single-player pirate adventure game inspired by "Tiny Epic Pirates", designed for terminal play with simple number-based decisions.

## 🎯 Game Objective

Become a legendary pirate captain by:
- Earning **1000 gold**
- Finding **3 treasures**
- All within **20 turns**

## 🎮 How to Play

### Starting the Game
```bash
python pirate_game.py
```

### Game Controls
The game uses simple number inputs for all decisions:
- Enter the number corresponding to your choice
- Press Enter to confirm

### 🗺️ The World

Navigate a 6x6 Caribbean map with different types of islands:

- **🏪 Trading Posts** - Buy and sell goods for profit
- **💰 Treasure Islands** - Search for buried treasure (but beware of guardians!)
- **🏴‍☠️ Pirate Havens** - Recruit crew, repair ship, and trade
- **⚔️ Naval Forts** - Dangerous but potentially rewarding combat

### 🚢 Your Ship: "The Black Pearl"

- **Hull Points**: 10/10 (ship health)
- **Crew**: 5/8 (affects combat and treasure hunting)
- **Cargo**: 0/15 (space for goods)

### 💰 Trading System

Buy low, sell high! Each trading post has different:
- **Goods available**: Rum, Spices, Gold, Silk, Sugar
- **Prices**: Vary by location
- **Stock levels**: Limited quantities

### ⚔️ Combat

When you encounter enemies:
- **Your strength** = Crew size + (Reputation ÷ 2)
- **Win**: Gain gold and reputation
- **Lose**: Take hull damage and lose gold
- **Flee**: 60% chance to escape

### 🏴‍☠️ Random Encounters

While sailing, you might encounter:
- **⛈️ Storms** - Damage your ship
- **🏴‍☠️ Pirates** - Combat encounters
- **🚢 Merchants** - Trading opportunities

### 💎 Treasure Hunting

At treasure islands:
- **Success chance** = (Crew size × 0.2) - (Difficulty × 0.1)
- **Rewards**: 50-150 gold + 2 reputation
- **Risks**: Guardian pirates may attack

### 🏴‍☠️ Pirate Havens

Special services available:
- **Recruit crew**: 25 gold per crew member
- **Repair ship**: 15 gold per hull point
- **Trade goods**: Same as trading posts

## 📊 Scoring System

Your final score is calculated as:
- Gold earned
- Reputation × 10
- Treasures found × 50

### Score Rankings:
- **🏆 1000+ gold + 3 treasures**: Legendary Pirate Captain!
- **⭐ 500+**: Renowned Pirate
- **🗡️ 300+**: Skilled Buccaneer
- **⚓ 150+**: Seasoned Sailor
- **🌊 <150**: Landlubber...

## 🎯 Strategy Tips

1. **Start with trading** - Build up gold at Port Royal and Nassau
2. **Manage your crew** - More crew = better combat and treasure hunting
3. **Watch your hull** - Repair at pirate havens when damaged
4. **Plan your routes** - Sailing takes turns, plan efficiently
5. **Balance risk/reward** - Treasure islands are dangerous but profitable
6. **Use reputation** - Higher reputation improves combat effectiveness

## 🗺️ Island Locations

1. **Port Royal** (0,0) - Trading Post - Starting location
2. **Tortuga** (3,2) - Pirate Haven - Crew and repairs
3. **Dead Man's Cove** (5,5) - Treasure Island - Difficulty 3
4. **Skull Island** (1,4) - Treasure Island - Difficulty 4
5. **Nassau** (4,1) - Trading Post - Different goods/prices
6. **Fort Charles** (2,3) - Naval Fort - High-risk combat

## 🎲 Game Features

- **Turn-based gameplay** - 20 turns to achieve victory
- **Resource management** - Gold, cargo space, crew, hull points
- **Risk/reward decisions** - Combat, treasure hunting, trading
- **Random events** - Storms, encounters, market fluctuations
- **Multiple victory paths** - Trading, treasure hunting, or mixed strategies

## 🧪 Testing

Run the test suite to verify game functionality:
```bash
python test_pirate_game.py
```

## 🎮 Example Gameplay Session

```
Turn 1: Start at Port Royal, buy Rum (cheap here)
Turn 2-3: Sail to Nassau, sell Rum for profit
Turn 4-5: Sail to Tortuga, recruit crew
Turn 6-8: Sail to Dead Man's Cove, search for treasure
Turn 9-10: Return to trading posts to sell treasure goods
...continue until victory or 20 turns expire
```

## 🏴‍☠️ Have Fun!

May fair winds fill your sails and fortune favor your adventures, Captain!

---

*Inspired by "Tiny Epic Pirates" by Gamelyn Games*