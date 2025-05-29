#!/usr/bin/env python3
"""
Test script for the pirate game to verify basic functionality
"""

from pirate_game import PirateGame, IslandType, GoodType

def test_game_initialization():
    """Test that the game initializes correctly"""
    game = PirateGame()
    
    # Check player initialization
    assert game.player.name == "Captain"
    assert game.player.gold == 100
    assert game.player.reputation == 0
    assert game.player.turns_remaining == 20
    
    # Check ship initialization
    assert game.player.ship.name == "The Black Pearl"
    assert game.player.ship.hull_points == 10
    assert game.player.ship.max_hull == 10
    assert game.player.ship.cargo_capacity == 15
    assert game.player.ship.crew_size == 5
    
    # Check starting location
    assert game.current_island.name == "Port Royal"
    assert game.player.x == 0
    assert game.player.y == 0
    
    # Check islands exist
    assert len(game.islands) == 6
    
    print("✅ Game initialization test passed!")

def test_cargo_system():
    """Test cargo management"""
    game = PirateGame()
    
    # Test empty cargo
    assert game.player.ship.get_cargo_used() == 0
    assert game.player.ship.get_cargo_space() == 15
    
    # Add some cargo
    game.player.ship.cargo[GoodType.RUM] = 5
    game.player.ship.cargo[GoodType.SPICES] = 3
    
    assert game.player.ship.get_cargo_used() == 8
    assert game.player.ship.get_cargo_space() == 7
    
    print("✅ Cargo system test passed!")

def test_island_types():
    """Test that different island types exist"""
    game = PirateGame()
    
    island_types = [island.type for island in game.islands]
    
    assert IslandType.TRADING_POST in island_types
    assert IslandType.TREASURE_ISLAND in island_types
    assert IslandType.PIRATE_HAVEN in island_types
    assert IslandType.NAVAL_FORT in island_types
    
    print("✅ Island types test passed!")

def test_trading_post_setup():
    """Test that trading posts have goods and prices"""
    game = PirateGame()
    
    trading_posts = [island for island in game.islands if island.type == IslandType.TRADING_POST]
    
    for post in trading_posts:
        assert len(post.goods_prices) > 0
        assert len(post.goods_available) > 0
        
        # Check that prices are reasonable
        for good_type, price in post.goods_prices.items():
            assert price > 0
            assert price < 100  # Reasonable upper bound
    
    print("✅ Trading post setup test passed!")

def test_treasure_islands():
    """Test that treasure islands have appropriate difficulty"""
    game = PirateGame()
    
    treasure_islands = [island for island in game.islands if island.type == IslandType.TREASURE_ISLAND]
    
    for island in treasure_islands:
        assert island.treasure_difficulty > 0
        assert island.enemy_strength >= 0
    
    print("✅ Treasure islands test passed!")

def run_all_tests():
    """Run all tests"""
    print("🏴‍☠️ Running Pirate Game Tests...")
    print("=" * 40)
    
    test_game_initialization()
    test_cargo_system()
    test_island_types()
    test_trading_post_setup()
    test_treasure_islands()
    
    print("=" * 40)
    print("🎉 All tests passed! The game is ready to play!")

if __name__ == "__main__":
    run_all_tests()