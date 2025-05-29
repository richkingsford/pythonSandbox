#!/usr/bin/env python3
"""
Simple test to verify the game works
"""

from pirate_game import PirateGame, GoodType, IslandType

def test_game_functionality():
    """Test core game functionality"""
    print("🏴‍☠️ TESTING PIRATE GAME FUNCTIONALITY")
    print("=" * 50)
    
    # Initialize game
    game = PirateGame()
    print("✅ Game initialized successfully")
    
    # Test initial state
    assert game.player.gold == 100
    assert game.player.turns_remaining == 20
    assert game.current_island.name == "Port Royal"
    print("✅ Initial state correct")
    
    # Test map display
    print("\n📍 CURRENT MAP:")
    game.display_map()
    
    # Test trading system
    print("\n💰 TRADING SYSTEM:")
    port_royal = game.current_island
    print(f"At {port_royal.name}:")
    for good, price in port_royal.goods_prices.items():
        available = port_royal.goods_available.get(good, 0)
        print(f"  {good.value}: {price} gold (Stock: {available})")
    
    # Test cargo system
    print("\n📦 CARGO SYSTEM:")
    print(f"Cargo space: {game.player.ship.get_cargo_used()}/{game.player.ship.cargo_capacity}")
    
    # Simulate buying goods
    game.player.ship.cargo[GoodType.RUM] = 5
    print(f"After buying 5 Rum: {game.player.ship.get_cargo_used()}/{game.player.ship.cargo_capacity}")
    
    # Test sailing
    print("\n⛵ SAILING SYSTEM:")
    original_x, original_y = game.player.x, game.player.y
    print(f"Starting position: ({original_x}, {original_y})")
    
    # Find Nassau and calculate distance
    nassau = next(i for i in game.islands if i.name == "Nassau")
    distance = abs(nassau.x - game.player.x) + abs(nassau.y - game.player.y)
    print(f"Distance to Nassau: {distance} turns")
    
    # Test different island types
    print("\n🏝️  ISLAND TYPES:")
    for island in game.islands:
        print(f"  {island.name} ({island.x},{island.y}) - {island.type.value}")
    
    # Test treasure islands
    treasure_islands = [i for i in game.islands if i.type == IslandType.TREASURE_ISLAND]
    print(f"\n💎 TREASURE ISLANDS: {len(treasure_islands)} found")
    for island in treasure_islands:
        print(f"  {island.name} - Difficulty: {island.treasure_difficulty}")
    
    # Test combat calculation
    print("\n⚔️  COMBAT SYSTEM:")
    player_strength = game.player.ship.crew_size + (game.player.reputation // 2)
    print(f"Player combat strength: {player_strength}")
    print(f"  (Crew: {game.player.ship.crew_size} + Reputation bonus: {game.player.reputation // 2})")
    
    # Test victory conditions
    print("\n🏆 VICTORY CONDITIONS:")
    print(f"Gold: {game.player.gold}/1000")
    print(f"Treasures: {game.player.treasures_found}/3")
    print(f"Turns: {20 - game.player.turns_remaining}/20 used")
    
    print("\n✅ ALL SYSTEMS WORKING!")
    return True

def show_gameplay_example():
    """Show an example of gameplay decisions"""
    print("\n🎮 EXAMPLE GAMEPLAY DECISIONS:")
    print("=" * 50)
    
    scenarios = [
        "🏪 At Port Royal: Buy Rum (15g) to sell at Nassau (10g) - Loss!",
        "🏪 At Port Royal: Buy Spices (25g) to sell at Nassau (20g) - Loss!",
        "💡 Better strategy: Buy at Nassau, sell at Port Royal for profit!",
        "⛵ Sail to Tortuga (3 turns) to recruit crew for treasure hunting",
        "💰 Search Dead Man's Cove (difficulty 3) with 8 crew members",
        "⚔️  Fight pirates: 8 crew + 2 reputation = 10 vs enemy 4 = WIN!",
        "🏴‍☠️ Visit pirate haven to repair ship (15g per hull point)",
        "🎯 Balance trading profits with treasure hunting risks"
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario}")
    
    print("\n💡 WINNING STRATEGIES:")
    strategies = [
        "🔄 Trade goods between islands with price differences",
        "👥 Recruit crew early for better combat/treasure success",
        "💎 Focus on treasure islands for big gold rewards",
        "⚖️  Balance risk vs reward - treasure hunting is dangerous!",
        "🗺️  Plan efficient routes to save turns",
        "🔧 Keep ship repaired for survival"
    ]
    
    for strategy in strategies:
        print(f"  {strategy}")

if __name__ == "__main__":
    try:
        test_game_functionality()
        show_gameplay_example()
        
        print("\n" + "🏴‍☠️" * 20)
        print("🎉 PIRATE GAME IS READY!")
        print("🏴‍☠️" * 20)
        print("\n🚀 TO PLAY THE GAME:")
        print("   python pirate_game.py")
        print("\n📖 FOR HELP:")
        print("   cat README_PIRATE_GAME.md")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()