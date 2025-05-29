#!/usr/bin/env python3
"""
Quick non-interactive demo of the pirate game
"""

from pirate_game import PirateGame, GoodType

def quick_demo():
    """Show game features without user input"""
    print("🏴‍☠️" * 20)
    print("PIRATE GAME QUICK DEMO")
    print("🏴‍☠️" * 20)
    
    game = PirateGame()
    
    print("\n1. INITIAL STATE:")
    print("=" * 30)
    game.display_header()
    game.display_cargo()
    
    print("\n2. GAME MAP:")
    print("=" * 30)
    game.display_map()
    
    print("\n3. TRADING PRICES AT PORT ROYAL:")
    print("=" * 30)
    game.view_prices()
    
    print("\n4. SIMULATING GAMEPLAY:")
    print("=" * 30)
    
    # Buy some rum
    print("📦 Buying 3 Rum for 45 gold...")
    game.player.gold -= 45
    game.player.ship.cargo[GoodType.RUM] = 3
    game.display_cargo()
    
    # Sail to Nassau
    print("\n⛵ Sailing to Nassau...")
    game.player.x = 4
    game.player.y = 1
    game.player.turns_remaining -= 5  # Distance
    game.current_island = next(i for i in game.islands if i.name == "Nassau")
    
    print(f"Arrived at {game.current_island.name}!")
    print(f"Turns remaining: {game.player.turns_remaining}")
    
    # Show Nassau prices
    print("\n💰 Nassau trading prices:")
    game.view_prices()
    
    # Sell rum at Nassau
    print("\n💰 Selling 3 Rum at Nassau...")
    rum_price = game.current_island.goods_prices.get(GoodType.RUM, 10)
    earnings = 3 * rum_price
    game.player.gold += earnings
    game.player.ship.cargo[GoodType.RUM] = 0
    print(f"Sold for {earnings} gold! Profit: {earnings - 45} gold")
    
    # Find treasure
    print("\n💎 Simulating treasure hunt...")
    game.player.gold += 100
    game.player.treasures_found += 1
    game.player.reputation += 2
    print("Found treasure worth 100 gold! +2 reputation")
    
    print("\n5. FINAL STATE:")
    print("=" * 30)
    game.display_header()
    game.display_cargo()
    
    print("\n6. VICTORY CONDITIONS:")
    print("=" * 30)
    print(f"Gold needed: 1000 (Current: {game.player.gold})")
    print(f"Treasures needed: 3 (Current: {game.player.treasures_found})")
    print(f"Turns used: {20 - game.player.turns_remaining}/20")
    
    total_score = game.player.gold + (game.player.reputation * 10) + (game.player.treasures_found * 50)
    print(f"Current score: {total_score}")
    
    print("\n🎮 READY TO PLAY!")
    print("Run: python pirate_game.py")
    print("\nThe game uses simple number choices:")
    print("- Enter numbers 1-7 to choose actions")
    print("- Navigate with the map")
    print("- Trade goods for profit")
    print("- Hunt for treasure")
    print("- Manage your crew and ship")

if __name__ == "__main__":
    quick_demo()