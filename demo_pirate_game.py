#!/usr/bin/env python3
"""
Demo script showing key features of the pirate game
"""

from pirate_game import PirateGame, GoodType
import time

def demo_game_features():
    """Demonstrate key game features"""
    print("🏴‍☠️" * 20)
    print("PIRATE GAME DEMO - Key Features")
    print("🏴‍☠️" * 20)
    
    game = PirateGame()
    
    # Show initial state
    print("\n1. INITIAL GAME STATE:")
    print("=" * 30)
    game.display_header()
    game.display_cargo()
    
    input("\nPress Enter to continue...")
    
    # Show map
    print("\n2. GAME MAP:")
    print("=" * 30)
    game.display_map()
    
    input("\nPress Enter to continue...")
    
    # Demonstrate trading
    print("\n3. TRADING SYSTEM:")
    print("=" * 30)
    print(f"At {game.current_island.name}:")
    game.view_prices()
    
    # Simulate buying some goods
    print("\n📦 Simulating purchase of 3 Rum...")
    if game.player.gold >= 45:  # 3 * 15 gold
        game.player.gold -= 45
        game.player.ship.cargo[GoodType.RUM] = 3
        print("✅ Purchased 3 Rum for 45 gold!")
    
    game.display_cargo()
    
    input("\nPress Enter to continue...")
    
    # Show cargo management
    print("\n4. CARGO MANAGEMENT:")
    print("=" * 30)
    print(f"Cargo space used: {game.player.ship.get_cargo_used()}/{game.player.ship.cargo_capacity}")
    print(f"Remaining space: {game.player.ship.get_cargo_space()}")
    
    input("\nPress Enter to continue...")
    
    # Demonstrate sailing
    print("\n5. SAILING SYSTEM:")
    print("=" * 30)
    print("Current position:", game.player.x, game.player.y)
    print("Simulating sail to Nassau (4,1)...")
    
    # Calculate distance
    target_x, target_y = 4, 1
    distance = abs(target_x - game.player.x) + abs(target_y - game.player.y)
    print(f"Distance: {distance} turns")
    
    # Simulate sailing
    game.player.x = target_x
    game.player.y = target_y
    game.player.turns_remaining -= distance
    game.current_island = next(i for i in game.islands if i.x == target_x and i.y == target_y)
    
    print(f"✅ Arrived at {game.current_island.name}!")
    print(f"Turns remaining: {game.player.turns_remaining}")
    
    input("\nPress Enter to continue...")
    
    # Show different island type
    print("\n6. DIFFERENT ISLAND TYPES:")
    print("=" * 30)
    print(f"Now at: {game.current_island.name} ({game.current_island.type.value})")
    if hasattr(game.current_island, 'goods_prices'):
        print("Available goods and prices:")
        for good, price in game.current_island.goods_prices.items():
            print(f"  {good.value}: {price} gold")
    
    input("\nPress Enter to continue...")
    
    # Demonstrate treasure island
    print("\n7. TREASURE HUNTING:")
    print("=" * 30)
    treasure_island = next(i for i in game.islands if i.type.name == "TREASURE_ISLAND")
    print(f"Example treasure island: {treasure_island.name}")
    print(f"Treasure difficulty: {treasure_island.treasure_difficulty}")
    print(f"Enemy strength: {treasure_island.enemy_strength}")
    
    # Simulate treasure hunting success
    print("\n🔍 Simulating treasure hunt...")
    time.sleep(1)
    treasure_value = 75
    game.player.gold += treasure_value
    game.player.treasures_found += 1
    game.player.reputation += 2
    print(f"🎉 Found treasure worth {treasure_value} gold!")
    print(f"Treasures found: {game.player.treasures_found}")
    print(f"Reputation gained: +2 (Total: {game.player.reputation})")
    
    input("\nPress Enter to continue...")
    
    # Show final state
    print("\n8. UPDATED GAME STATE:")
    print("=" * 30)
    game.display_header()
    game.display_cargo()
    
    print("\n9. VICTORY CONDITIONS:")
    print("=" * 30)
    print("To win, you need:")
    print("✅ 1000 gold (Current: {})".format(game.player.gold))
    print("✅ 3 treasures (Current: {})".format(game.player.treasures_found))
    print("✅ Within 20 turns (Used: {})".format(20 - game.player.turns_remaining))
    
    progress = (game.player.gold / 1000) * 100
    treasure_progress = (game.player.treasures_found / 3) * 100
    print(f"\nProgress: {progress:.1f}% gold, {treasure_progress:.1f}% treasures")
    
    print("\n🏴‍☠️ Demo complete! Ready to play the full game!")
    print("Run: python pirate_game.py")

if __name__ == "__main__":
    demo_game_features()