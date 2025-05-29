#!/usr/bin/env python3
"""
Tiny Epic Pirates - Terminal Edition
A single-player pirate adventure game inspired by Tiny Epic Pirates
"""

import random
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

class IslandType(Enum):
    TRADING_POST = "Trading Post"
    TREASURE_ISLAND = "Treasure Island"
    PIRATE_HAVEN = "Pirate Haven"
    NAVAL_FORT = "Naval Fort"

class GoodType(Enum):
    RUM = "Rum"
    SPICES = "Spices"
    GOLD = "Gold"
    SILK = "Silk"
    SUGAR = "Sugar"

@dataclass
class Good:
    type: GoodType
    quantity: int = 0

@dataclass
class Island:
    name: str
    type: IslandType
    x: int
    y: int
    goods_prices: Dict[GoodType, int] = field(default_factory=dict)
    goods_available: Dict[GoodType, int] = field(default_factory=dict)
    treasure_difficulty: int = 0
    enemy_strength: int = 0

@dataclass
class Ship:
    name: str
    hull_points: int
    max_hull: int
    cargo_capacity: int
    crew_size: int
    max_crew: int
    cargo: Dict[GoodType, int] = field(default_factory=dict)
    
    def get_cargo_used(self) -> int:
        return sum(self.cargo.values())
    
    def get_cargo_space(self) -> int:
        return self.cargo_capacity - self.get_cargo_used()

@dataclass
class Player:
    name: str
    gold: int
    reputation: int
    x: int
    y: int
    ship: Ship
    turns_remaining: int = 20
    treasures_found: int = 0
    
class PirateGame:
    def __init__(self):
        self.player = None
        self.islands = []
        self.current_island = None
        self.game_over = False
        self.victory = False
        self.setup_game()
    
    def setup_game(self):
        """Initialize the game world"""
        # Create islands
        self.islands = [
            Island("Port Royal", IslandType.TRADING_POST, 0, 0, 
                  {GoodType.RUM: 15, GoodType.SPICES: 25, GoodType.SILK: 35},
                  {GoodType.RUM: 10, GoodType.SPICES: 8, GoodType.SILK: 5}),
            Island("Tortuga", IslandType.PIRATE_HAVEN, 3, 2,
                  {GoodType.RUM: 10, GoodType.GOLD: 50, GoodType.SUGAR: 20},
                  {GoodType.RUM: 15, GoodType.GOLD: 3, GoodType.SUGAR: 12}),
            Island("Dead Man's Cove", IslandType.TREASURE_ISLAND, 5, 5,
                  treasure_difficulty=3, enemy_strength=2),
            Island("Skull Island", IslandType.TREASURE_ISLAND, 1, 4,
                  treasure_difficulty=4, enemy_strength=3),
            Island("Nassau", IslandType.TRADING_POST, 4, 1,
                  {GoodType.SPICES: 20, GoodType.SILK: 30, GoodType.SUGAR: 18},
                  {GoodType.SPICES: 12, GoodType.SILK: 7, GoodType.SUGAR: 15}),
            Island("Fort Charles", IslandType.NAVAL_FORT, 2, 3,
                  enemy_strength=4),
        ]
        
        # Create player ship
        ship = Ship("The Black Pearl", 10, 10, 15, 5, 8)
        
        # Initialize player at Port Royal
        self.player = Player("Captain", 100, 0, 0, 0, ship)
        self.current_island = self.islands[0]  # Start at Port Royal
    
    def display_header(self):
        """Display game header with current status"""
        print("\n" + "="*60)
        print("🏴‍☠️  TINY EPIC PIRATES - TERMINAL EDITION  🏴‍☠️")
        print("="*60)
        print(f"Captain: {self.player.name} | Gold: {self.player.gold} | Reputation: {self.player.reputation}")
        print(f"Ship: {self.player.ship.name} | Hull: {self.player.ship.hull_points}/{self.player.ship.max_hull}")
        print(f"Crew: {self.player.ship.crew_size}/{self.player.ship.max_crew} | Turns Left: {self.player.turns_remaining}")
        print(f"Cargo: {self.player.ship.get_cargo_used()}/{self.player.ship.cargo_capacity}")
        print(f"Current Location: {self.current_island.name} ({self.current_island.type.value})")
        print("="*60)
    
    def display_cargo(self):
        """Display current cargo"""
        if not any(self.player.ship.cargo.values()):
            print("Cargo Hold: Empty")
        else:
            print("Cargo Hold:")
            for good_type, quantity in self.player.ship.cargo.items():
                if quantity > 0:
                    print(f"  {good_type.value}: {quantity}")
    
    def display_map(self):
        """Display a simple map of the world"""
        print("\n🗺️  CARIBBEAN MAP 🗺️")
        print("Current position marked with [X]")
        print()
        
        # Create a 6x6 grid
        for y in range(5, -1, -1):
            row = ""
            for x in range(6):
                if x == self.player.x and y == self.player.y:
                    row += "[X] "
                else:
                    island = next((i for i in self.islands if i.x == x and i.y == y), None)
                    if island:
                        if island.type == IslandType.TRADING_POST:
                            row += "🏪  "
                        elif island.type == IslandType.TREASURE_ISLAND:
                            row += "💰  "
                        elif island.type == IslandType.PIRATE_HAVEN:
                            row += "🏴‍☠️  "
                        elif island.type == IslandType.NAVAL_FORT:
                            row += "⚔️  "
                    else:
                        row += "🌊  "
            print(f"{y} {row}")
        print("  0  1  2  3  4  5")
        
        print("\nIslands:")
        for i, island in enumerate(self.islands, 1):
            marker = "[HERE]" if island == self.current_island else f"({island.x},{island.y})"
            print(f"{i}. {island.name} {marker} - {island.type.value}")
    
    def sail_to_island(self):
        """Handle sailing to a different island"""
        print("\n⛵ Where would you like to sail?")
        self.display_map()
        
        print(f"\n0. Stay at {self.current_island.name}")
        for i, island in enumerate(self.islands, 1):
            if island != self.current_island:
                distance = abs(island.x - self.player.x) + abs(island.y - self.player.y)
                print(f"{i}. {island.name} - Distance: {distance} turns")
        
        try:
            choice = int(input("\nEnter your choice (number): "))
            if choice == 0:
                return
            elif 1 <= choice <= len(self.islands):
                target_island = self.islands[choice - 1]
                if target_island == self.current_island:
                    print("You're already here!")
                    return
                
                distance = abs(target_island.x - self.player.x) + abs(target_island.y - self.player.y)
                if distance > self.player.turns_remaining:
                    print("Not enough turns to reach that island!")
                    return
                
                # Sail to the island
                self.player.x = target_island.x
                self.player.y = target_island.y
                self.current_island = target_island
                self.player.turns_remaining -= distance
                
                print(f"\n⛵ Sailed to {target_island.name}! ({distance} turns used)")
                
                # Random encounter chance while sailing
                if random.random() < 0.3:
                    self.random_encounter()
            else:
                print("Invalid choice!")
        except ValueError:
            print("Please enter a valid number!")
    
    def random_encounter(self):
        """Handle random encounters while sailing"""
        encounter_type = random.choice(["storm", "pirates", "merchant"])
        
        if encounter_type == "storm":
            damage = random.randint(1, 3)
            self.player.ship.hull_points = max(0, self.player.ship.hull_points - damage)
            print(f"\n⛈️  Storm! Your ship takes {damage} hull damage!")
            
        elif encounter_type == "pirates":
            print("\n🏴‍☠️ Pirate ship spotted!")
            self.combat_encounter(random.randint(2, 4))
            
        elif encounter_type == "merchant":
            print("\n🚢 Friendly merchant ship offers trade!")
            self.merchant_encounter()
    
    def combat_encounter(self, enemy_strength: int):
        """Handle combat encounters"""
        print(f"\n⚔️  COMBAT! Enemy strength: {enemy_strength}")
        print("1. Fight!")
        print("2. Try to flee")
        
        try:
            choice = int(input("Choose your action: "))
            if choice == 1:
                # Combat calculation
                player_strength = self.player.ship.crew_size + (self.player.reputation // 2)
                
                if player_strength >= enemy_strength:
                    gold_reward = random.randint(20, 50)
                    rep_reward = random.randint(1, 3)
                    self.player.gold += gold_reward
                    self.player.reputation += rep_reward
                    print(f"🎉 Victory! Gained {gold_reward} gold and {rep_reward} reputation!")
                else:
                    damage = random.randint(1, 4)
                    gold_lost = min(self.player.gold, random.randint(10, 30))
                    self.player.ship.hull_points = max(0, self.player.ship.hull_points - damage)
                    self.player.gold -= gold_lost
                    print(f"💥 Defeat! Lost {damage} hull points and {gold_lost} gold!")
                    
            elif choice == 2:
                if random.random() < 0.6:
                    print("🏃 Successfully fled!")
                else:
                    damage = random.randint(1, 2)
                    self.player.ship.hull_points = max(0, self.player.ship.hull_points - damage)
                    print(f"💥 Failed to flee! Took {damage} hull damage!")
        except ValueError:
            print("Invalid choice! Defaulting to flee...")
            self.combat_encounter(enemy_strength)
    
    def merchant_encounter(self):
        """Handle merchant ship encounters"""
        good_type = random.choice(list(GoodType))
        quantity = random.randint(1, 5)
        price = random.randint(10, 30)
        
        print(f"Merchant offers {quantity} {good_type.value} for {price} gold each")
        print("1. Buy")
        print("2. Decline")
        
        try:
            choice = int(input("Choose: "))
            if choice == 1:
                total_cost = price * quantity
                if self.player.gold >= total_cost and self.player.ship.get_cargo_space() >= quantity:
                    self.player.gold -= total_cost
                    self.player.ship.cargo[good_type] = self.player.ship.cargo.get(good_type, 0) + quantity
                    print(f"Purchased {quantity} {good_type.value} for {total_cost} gold!")
                else:
                    print("Not enough gold or cargo space!")
        except ValueError:
            print("Invalid choice!")
    
    def trade_at_port(self):
        """Handle trading at trading posts"""
        if self.current_island.type != IslandType.TRADING_POST:
            print("No trading available at this location!")
            return
        
        while True:
            print(f"\n🏪 Trading at {self.current_island.name}")
            print("1. Buy goods")
            print("2. Sell goods")
            print("3. View prices")
            print("4. Leave market")
            
            try:
                choice = int(input("Choose action: "))
                if choice == 1:
                    self.buy_goods()
                elif choice == 2:
                    self.sell_goods()
                elif choice == 3:
                    self.view_prices()
                elif choice == 4:
                    break
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Please enter a valid number!")
    
    def buy_goods(self):
        """Handle buying goods"""
        print("\n💰 Available goods to buy:")
        available_goods = []
        
        for good_type, price in self.current_island.goods_prices.items():
            available = self.current_island.goods_available.get(good_type, 0)
            if available > 0:
                available_goods.append((good_type, price, available))
                print(f"{len(available_goods)}. {good_type.value} - {price} gold each (Available: {available})")
        
        if not available_goods:
            print("No goods available for purchase!")
            return
        
        print("0. Cancel")
        
        try:
            choice = int(input("Choose good to buy: "))
            if choice == 0:
                return
            elif 1 <= choice <= len(available_goods):
                good_type, price, available = available_goods[choice - 1]
                
                max_affordable = self.player.gold // price
                max_space = self.player.ship.get_cargo_space()
                max_buyable = min(max_affordable, max_space, available)
                
                if max_buyable == 0:
                    print("Cannot buy any - insufficient gold, cargo space, or availability!")
                    return
                
                print(f"How many {good_type.value}? (Max: {max_buyable})")
                quantity = int(input("Quantity: "))
                
                if 1 <= quantity <= max_buyable:
                    total_cost = price * quantity
                    self.player.gold -= total_cost
                    self.player.ship.cargo[good_type] = self.player.ship.cargo.get(good_type, 0) + quantity
                    self.current_island.goods_available[good_type] -= quantity
                    print(f"Bought {quantity} {good_type.value} for {total_cost} gold!")
                else:
                    print("Invalid quantity!")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Please enter a valid number!")
    
    def sell_goods(self):
        """Handle selling goods"""
        print("\n💰 Your goods to sell:")
        sellable_goods = []
        
        for good_type, quantity in self.player.ship.cargo.items():
            if quantity > 0:
                price = self.current_island.goods_prices.get(good_type, 5)  # Default low price
                sellable_goods.append((good_type, price, quantity))
                print(f"{len(sellable_goods)}. {good_type.value} - {price} gold each (You have: {quantity})")
        
        if not sellable_goods:
            print("No goods to sell!")
            return
        
        print("0. Cancel")
        
        try:
            choice = int(input("Choose good to sell: "))
            if choice == 0:
                return
            elif 1 <= choice <= len(sellable_goods):
                good_type, price, available = sellable_goods[choice - 1]
                
                print(f"How many {good_type.value}? (Max: {available})")
                quantity = int(input("Quantity: "))
                
                if 1 <= quantity <= available:
                    total_earned = price * quantity
                    self.player.gold += total_earned
                    self.player.ship.cargo[good_type] -= quantity
                    print(f"Sold {quantity} {good_type.value} for {total_earned} gold!")
                else:
                    print("Invalid quantity!")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Please enter a valid number!")
    
    def view_prices(self):
        """Display current market prices"""
        print(f"\n📊 Market prices at {self.current_island.name}:")
        for good_type, price in self.current_island.goods_prices.items():
            available = self.current_island.goods_available.get(good_type, 0)
            print(f"{good_type.value}: {price} gold (Available: {available})")
    
    def search_for_treasure(self):
        """Handle treasure hunting"""
        if self.current_island.type != IslandType.TREASURE_ISLAND:
            print("No treasure to be found here!")
            return
        
        print(f"\n💰 Searching for treasure on {self.current_island.name}...")
        print(f"Difficulty: {self.current_island.treasure_difficulty}")
        print("1. Search for treasure (costs 1 turn)")
        print("2. Cancel")
        
        try:
            choice = int(input("Choose: "))
            if choice == 1:
                self.player.turns_remaining -= 1
                
                # Success based on crew size and difficulty
                success_chance = (self.player.ship.crew_size * 0.2) - (self.current_island.treasure_difficulty * 0.1)
                success_chance = max(0.1, min(0.8, success_chance))
                
                if random.random() < success_chance:
                    treasure_value = random.randint(50, 150)
                    self.player.gold += treasure_value
                    self.player.treasures_found += 1
                    self.player.reputation += 2
                    print(f"🎉 Found treasure worth {treasure_value} gold!")
                    print(f"Gained 2 reputation! Total treasures found: {self.player.treasures_found}")
                else:
                    print("💔 No treasure found this time...")
                    
                    # Chance of enemy encounter
                    if random.random() < 0.4:
                        print("🏴‍☠️ Disturbed some guardian pirates!")
                        self.combat_encounter(self.current_island.enemy_strength)
        except ValueError:
            print("Invalid choice!")
    
    def visit_pirate_haven(self):
        """Handle pirate haven activities"""
        if self.current_island.type != IslandType.PIRATE_HAVEN:
            print("This is not a pirate haven!")
            return
        
        while True:
            print(f"\n🏴‍☠️ Welcome to {self.current_island.name}!")
            print("1. Recruit crew members")
            print("2. Repair ship")
            print("3. Trade goods")
            print("4. Leave")
            
            try:
                choice = int(input("Choose action: "))
                if choice == 1:
                    self.recruit_crew()
                elif choice == 2:
                    self.repair_ship()
                elif choice == 3:
                    self.trade_at_port()
                elif choice == 4:
                    break
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Please enter a valid number!")
    
    def recruit_crew(self):
        """Handle crew recruitment"""
        if self.player.ship.crew_size >= self.player.ship.max_crew:
            print("Your crew is already at maximum capacity!")
            return
        
        available_crew = self.player.ship.max_crew - self.player.ship.crew_size
        cost_per_crew = 25
        
        print(f"\n👥 Recruit crew members ({cost_per_crew} gold each)")
        print(f"Current crew: {self.player.ship.crew_size}/{self.player.ship.max_crew}")
        print(f"Available positions: {available_crew}")
        
        max_affordable = self.player.gold // cost_per_crew
        max_recruitable = min(available_crew, max_affordable)
        
        if max_recruitable == 0:
            print("Cannot recruit any crew - insufficient gold or ship capacity!")
            return
        
        print(f"How many crew members to recruit? (Max: {max_recruitable})")
        print("0. Cancel")
        
        try:
            quantity = int(input("Quantity: "))
            if quantity == 0:
                return
            elif 1 <= quantity <= max_recruitable:
                total_cost = cost_per_crew * quantity
                self.player.gold -= total_cost
                self.player.ship.crew_size += quantity
                print(f"Recruited {quantity} crew members for {total_cost} gold!")
            else:
                print("Invalid quantity!")
        except ValueError:
            print("Please enter a valid number!")
    
    def repair_ship(self):
        """Handle ship repairs"""
        if self.player.ship.hull_points >= self.player.ship.max_hull:
            print("Your ship is already in perfect condition!")
            return
        
        damage = self.player.ship.max_hull - self.player.ship.hull_points
        cost_per_hull = 15
        total_cost = damage * cost_per_hull
        
        print(f"\n🔧 Ship repair needed")
        print(f"Hull damage: {damage} points")
        print(f"Repair cost: {total_cost} gold ({cost_per_hull} per hull point)")
        
        if self.player.gold < total_cost:
            max_affordable = self.player.gold // cost_per_hull
            print(f"You can only afford to repair {max_affordable} hull points")
            
            if max_affordable == 0:
                print("Insufficient gold for any repairs!")
                return
            
            print(f"1. Repair {max_affordable} hull points for {max_affordable * cost_per_hull} gold")
            print("2. Cancel")
            
            try:
                choice = int(input("Choose: "))
                if choice == 1:
                    self.player.gold -= max_affordable * cost_per_hull
                    self.player.ship.hull_points += max_affordable
                    print(f"Repaired {max_affordable} hull points!")
            except ValueError:
                print("Invalid choice!")
        else:
            print("1. Repair all damage")
            print("2. Cancel")
            
            try:
                choice = int(input("Choose: "))
                if choice == 1:
                    self.player.gold -= total_cost
                    self.player.ship.hull_points = self.player.ship.max_hull
                    print(f"Ship fully repaired for {total_cost} gold!")
            except ValueError:
                print("Invalid choice!")
    
    def check_game_over(self):
        """Check for game over conditions"""
        if self.player.turns_remaining <= 0:
            self.game_over = True
            print("\n⏰ Time's up! Your adventure has come to an end.")
            self.show_final_score()
        elif self.player.ship.hull_points <= 0:
            self.game_over = True
            print("\n💥 Your ship has been destroyed! You sink to the depths...")
            self.show_final_score()
        elif self.player.gold >= 1000 and self.player.treasures_found >= 3:
            self.victory = True
            self.game_over = True
            print("\n🎉 VICTORY! You've become a legendary pirate captain!")
            self.show_final_score()
    
    def show_final_score(self):
        """Display final game statistics"""
        print("\n" + "="*50)
        print("🏴‍☠️  FINAL SCORE  🏴‍☠️")
        print("="*50)
        print(f"Gold earned: {self.player.gold}")
        print(f"Reputation: {self.player.reputation}")
        print(f"Treasures found: {self.player.treasures_found}")
        print(f"Turns used: {20 - self.player.turns_remaining}")
        
        total_score = self.player.gold + (self.player.reputation * 10) + (self.player.treasures_found * 50)
        print(f"Total Score: {total_score}")
        
        if self.victory:
            print("🏆 LEGENDARY PIRATE CAPTAIN! 🏆")
        elif total_score >= 500:
            print("⭐ Renowned Pirate!")
        elif total_score >= 300:
            print("🗡️  Skilled Buccaneer!")
        elif total_score >= 150:
            print("⚓ Seasoned Sailor!")
        else:
            print("🌊 Landlubber...")
        
        print("="*50)
    
    def main_menu(self):
        """Display main action menu"""
        while not self.game_over:
            self.display_header()
            self.display_cargo()
            
            print(f"\n🏴‍☠️ What would you like to do at {self.current_island.name}?")
            print("1. Sail to another island")
            print("2. Trade goods" if self.current_island.type == IslandType.TRADING_POST else "2. [No trading available]")
            print("3. Search for treasure" if self.current_island.type == IslandType.TREASURE_ISLAND else "3. [No treasure here]")
            print("4. Visit pirate haven" if self.current_island.type == IslandType.PIRATE_HAVEN else "4. [Not a pirate haven]")
            print("5. View map")
            print("6. Rest (skip turn)")
            print("7. Quit game")
            
            try:
                choice = int(input("\nEnter your choice (1-7): "))
                
                if choice == 1:
                    self.sail_to_island()
                elif choice == 2:
                    self.trade_at_port()
                elif choice == 3:
                    self.search_for_treasure()
                elif choice == 4:
                    self.visit_pirate_haven()
                elif choice == 5:
                    self.display_map()
                    input("\nPress Enter to continue...")
                elif choice == 6:
                    self.player.turns_remaining -= 1
                    print("You rest and recover...")
                    # Small chance to recover hull
                    if random.random() < 0.3 and self.player.ship.hull_points < self.player.ship.max_hull:
                        self.player.ship.hull_points += 1
                        print("Your crew made some minor repairs!")
                elif choice == 7:
                    print("Thanks for playing!")
                    self.game_over = True
                    return
                else:
                    print("Invalid choice! Please enter a number between 1-7.")
                    
            except ValueError:
                print("Please enter a valid number!")
            
            self.check_game_over()
            
            if not self.game_over:
                input("\nPress Enter to continue...")
    
    def start_game(self):
        """Start the game"""
        print("🏴‍☠️" * 20)
        print("Welcome to TINY EPIC PIRATES!")
        print("🏴‍☠️" * 20)
        print("\nYou are a pirate captain seeking fortune and glory!")
        print("Goal: Earn 1000 gold and find 3 treasures to become legendary!")
        print("You have 20 turns to achieve greatness...")
        print("\nGood luck, Captain!")
        
        input("\nPress Enter to begin your adventure...")
        
        self.main_menu()

def main():
    """Main function to run the game"""
    game = PirateGame()
    game.start_game()

if __name__ == "__main__":
    main()