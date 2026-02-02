"""
Comprehensive Validation Script for EpiControl AI
Tests all components end-to-end before hackathon
"""

import sys
import os
import numpy as np
import traceback

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_imports():
    """Test all critical module imports"""
    print_section("TEST 1: Module Imports")
    
    errors = []
    
    try:
        from env.population import generate_population, update_agent_positions, get_nearby_agents
        print("✅ env.population")
    except Exception as e:
        errors.append(f"env.population: {e}")
        print(f"❌ env.population: {e}")
    
    try:
        from env.seir import set_virus_params, update_seir, get_current_virus_config
        print("✅ env.seir")
    except Exception as e:
        errors.append(f"env.seir: {e}")
        print(f"❌ env.seir: {e}")
    
    try:
        from env.mutation import (MutationTracker, check_mutation_trigger, 
                                  apply_mutation, reset_mutation_tracker)
        print("✅ env.mutation")
    except Exception as e:
        errors.append(f"env.mutation: {e}")
        print(f"❌ env.mutation: {e}")
    
    try:
        from env.policies import apply_policy
        print("✅ env.policies")
    except Exception as e:
        errors.append(f"env.policies: {e}")
        print(f"❌ env.policies: {e}")
    
    try:
        from rl.env import EpiControlEnv
        print("✅ rl.env (EpiControlEnv)")
    except Exception as e:
        errors.append(f"rl.env: {e}")
        print(f"❌ rl.env: {e}")
    
    try:
        from rl.agent import QLearningAgent
        print("✅ rl.agent (QLearningAgent)")
    except Exception as e:
        errors.append(f"rl.agent: {e}")
        print(f"❌ rl.agent: {e}")
    
    try:
        from rl.utils import discretize_state
        print("✅ rl.utils (discretize_state)")
    except Exception as e:
        errors.append(f"rl.utils: {e}")
        print(f"❌ rl.utils: {e}")
    
    try:
        from rl.load_agent import load_trained_agent
        print("✅ rl.load_agent")
    except Exception as e:
        errors.append(f"rl.load_agent: {e}")
        print(f"❌ rl.load_agent: {e}")
    
    try:
        from data.virus_configs import VIRUS_CONFIGS
        print(f"✅ data.virus_configs ({len(VIRUS_CONFIGS)} viruses)")
    except Exception as e:
        errors.append(f"data.virus_configs: {e}")
        print(f"❌ data.virus_configs: {e}")
    
    try:
        from visualization.plotly_plots import (plot_seir_plotly, plot_infection_heatmap,
                                                plot_spatial_scatter, plot_mutation_timeline)
        print("✅ visualization.plotly_plots (all functions)")
    except Exception as e:
        errors.append(f"visualization.plotly_plots: {e}")
        print(f"❌ visualization.plotly_plots: {e}")
    
    return len(errors) == 0, errors


def test_rl_environment():
    """Test RL environment initialization and basic functionality"""
    print_section("TEST 2: RL Environment")
    
    try:
        from rl.env import EpiControlEnv
        from data.virus_configs import VIRUS_CONFIGS
        
        virus_config = VIRUS_CONFIGS["COVID-19"].copy()
        
        # Test environment creation
        env = EpiControlEnv(population_size=500, days=30, virus_config=virus_config)
        
        print(f"✅ Environment created")
        print(f"   Population size: {env.population_size}")
        print(f"   Days: {env.days}")
        print(f"   Action space: {env.action_space.n}")
        print(f"   Observation space: {env.observation_space.shape}")
        
        # Test reset
        obs = env.reset()
        print(f"✅ Environment reset successful")
        print(f"   Observation shape: {obs.shape}")
        print(f"   Observation values: {obs}")
        
        # Test step
        action = 0  # No policy
        obs, reward, done, info = env.step(action)
        print(f"✅ Environment step successful")
        print(f"   Reward: {reward:.2f}")
        print(f"   Done: {done}")
        
        # Test all actions
        env.reset()
        for action in range(env.action_space.n):
            obs, reward, done, info = env.step(action)
            print(f"   Action {action}: reward={reward:.2f}")
        
        return True, None
        
    except Exception as e:
        print(f"❌ Environment test failed: {e}")
        traceback.print_exc()
        return False, str(e)


def test_q_learning_agent():
    """Test Q-Learning agent"""
    print_section("TEST 3: Q-Learning Agent")
    
    try:
        from rl.agent import QLearningAgent
        from rl.utils import discretize_state
        import numpy as np
        
        # Create agent
        agent = QLearningAgent(action_size=5)
        print(f"✅ Agent created")
        print(f"   Action size: {agent.action_size}")
        print(f"   Learning rate (α): {agent.alpha}")
        print(f"   Discount (γ): {agent.gamma}")
        print(f"   Initial epsilon: {agent.epsilon}")
        
        # Test choose_action
        test_state = (5, 3, 2, 4)
        action = agent.choose_action(test_state)
        print(f"✅ Action selection works (action={action})")
        
        # Test learn
        next_state = (4, 2, 2, 3)
        reward = -5.0
        agent.learn(test_state, action, reward, next_state)
        print(f"✅ Learning works")
        print(f"   Q-value updated: {agent.q_table[test_state][action]:.4f}")
        
        # Test epsilon decay
        old_epsilon = agent.epsilon
        agent.decay_epsilon()
        print(f"✅ Epsilon decay works ({old_epsilon:.4f} → {agent.epsilon:.4f})")
        
        # Test state discretization
        obs = np.array([0.35, 0.12, 0.23, 0.30, 0.15])
        state = discretize_state(obs)
        print(f"✅ State discretization works")
        print(f"   Continuous obs: {obs}")
        print(f"   Discrete state: {state}")
        
        return True, None
        
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        traceback.print_exc()
        return False, str(e)


def test_training_loop():
    """Test a mini training loop"""
    print_section("TEST 4: Mini Training Loop (10 episodes)")
    
    try:
        from rl.env import EpiControlEnv
        from rl.agent import QLearningAgent
        from rl.utils import discretize_state
        from data.virus_configs import VIRUS_CONFIGS
        from env.seir import set_virus_params
        
        virus_config = VIRUS_CONFIGS["COVID-19"].copy()
        set_virus_params(virus_config)
        
        env = EpiControlEnv(population_size=500, days=30, virus_config=virus_config)
        agent = QLearningAgent(action_size=env.action_space.n)
        
        print("Running 10 training episodes...")
        rewards = []
        
        for episode in range(10):
            obs = env.reset()
            state = discretize_state(obs)
            done = False
            total_reward = 0
            
            while not done:
                action = agent.choose_action(state)
                next_obs, reward, done, _ = env.step(action)
                next_state = discretize_state(next_obs)
                agent.learn(state, action, reward, next_state)
                state = next_state
                total_reward += reward
            
            agent.decay_epsilon()
            rewards.append(total_reward)
            
            if episode % 2 == 0:
                print(f"   Episode {episode:2d}: reward={total_reward:7.2f}, epsilon={agent.epsilon:.3f}")
        
        print(f"✅ Training loop successful")
        print(f"   States learned: {len(agent.q_table)}")
        print(f"   Average reward: {np.mean(rewards):.2f}")
        print(f"   Final epsilon: {agent.epsilon:.4f}")
        
        return True, None
        
    except Exception as e:
        print(f"❌ Training loop test failed: {e}")
        traceback.print_exc()
        return False, str(e)


def test_mutation_system():
    """Test mutation detection and application"""
    print_section("TEST 5: Mutation System")
    
    try:
        from env.mutation import (check_mutation_trigger, apply_mutation, 
                                  MutationTracker, reset_mutation_tracker)
        from env.population import generate_population
        from env.seir import seed_infection, set_virus_params, update_seir
        from data.virus_configs import VIRUS_CONFIGS
        
        virus_config = VIRUS_CONFIGS["COVID-19"].copy()
        set_virus_params(virus_config)
        
        # Create high-infection scenario
        population = generate_population(200)
        seed_infection(population, initial_infected=70)  # 35% infected
        
        print(f"   Created population: 200 agents, 70 infected (35%)")
        
        # Test mutation trigger
        should_mutate, reason = check_mutation_trigger(population, day=20)
        print(f"✅ Mutation trigger check: {should_mutate}")
        if reason:
            print(f"   Reason: {reason}")
        
        # Test mutation application
        original_R0 = virus_config['R0']
        original_beta = virus_config['base_beta']
        
        mutated_config = apply_mutation(virus_config, mutation_severity="moderate")
        
        print(f"✅ Mutation application successful")
        print(f"   R0: {original_R0:.2f} → {mutated_config['R0']:.2f}")
        print(f"   Beta: {original_beta:.3f} → {mutated_config['base_beta']:.3f}")
        
        # Test mutation tracker
        tracker = reset_mutation_tracker()
        event = tracker.log_mutation(
            day=20,
            trigger_reason="Test mutation",
            old_params=virus_config,
            new_params=mutated_config
        )
        
        print(f"✅ Mutation tracker working")
        print(f"   Mutations logged: {tracker.mutation_count}")
        
        # Test SEIR with mutation
        tracker = reset_mutation_tracker()
        population = generate_population(200)
        seed_infection(population, initial_infected=60)
        
        for day in range(30):
            update_seir(population, mutation_tracker=tracker, current_day=day)
        
        print(f"✅ SEIR with mutation tracking: {tracker.mutation_count} mutations")
        
        return True, None
        
    except Exception as e:
        print(f"❌ Mutation test failed: {e}")
        traceback.print_exc()
        return False, str(e)


def test_spatial_features():
    """Test spatial positioning and heatmap generation"""
    print_section("TEST 6: Spatial Features")
    
    try:
        from env.population import generate_population
        from env.seir import seed_infection
        from visualization.plotly_plots import plot_infection_heatmap, plot_spatial_scatter
        from data.virus_configs import VIRUS_CONFIGS
        
        virus_config = VIRUS_CONFIGS["COVID-19"].copy()
        
        # Generate population with spatial coordinates
        population = generate_population(300, virus_config=virus_config, spatial=True)
        seed_infection(population, initial_infected=50)
        
        # Check spatial coordinates
        agents_with_coords = sum(1 for a in population if "x" in a and "y" in a)
        
        print(f"✅ Spatial population generated")
        print(f"   Total agents: {len(population)}")
        print(f"   Agents with coordinates: {agents_with_coords}")
        
        if agents_with_coords != len(population):
            print(f"❌ Not all agents have coordinates!")
            return False, "Missing spatial coordinates"
        
        # Test heatmap generation
        heatmap_fig = plot_infection_heatmap(population, grid_size=10)
        print(f"✅ Heatmap generated: {type(heatmap_fig).__name__}")
        
        # Test spatial scatter
        scatter_fig = plot_spatial_scatter(population)
        print(f"✅ Spatial scatter generated: {type(scatter_fig).__name__}")
        
        # Check coordinate ranges
        x_coords = [a["x"] for a in population]
        y_coords = [a["y"] for a in population]
        
        print(f"   X range: [{min(x_coords):.3f}, {max(x_coords):.3f}]")
        print(f"   Y range: [{min(y_coords):.3f}, {max(y_coords):.3f}]")
        
        return True, None
        
    except Exception as e:
        print(f"❌ Spatial features test failed: {e}")
        traceback.print_exc()
        return False, str(e)


def test_q_table_save_load():
    """Test Q-table saving and loading"""
    print_section("TEST 7: Q-Table Save/Load")
    
    try:
        from rl.agent import QLearningAgent
        import pickle
        import os
        
        # Create agent and train a bit
        agent = QLearningAgent(action_size=5)
        
        # Add some fake Q-values
        agent.q_table[(1, 2, 3, 4)] = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        agent.q_table[(2, 3, 4, 5)] = np.array([0.5, 0.4, 0.3, 0.2, 0.1])
        
        print(f"   Created agent with {len(agent.q_table)} states")
        
        # Save Q-table
        test_filename = "rl/test_q_table.pkl"
        os.makedirs("rl", exist_ok=True)
        
        q_table_safe = {}
        for state, values in agent.q_table.items():
            q_table_safe[state] = values.copy()
        
        with open(test_filename, "wb") as f:
            pickle.dump(q_table_safe, f)
        
        print(f"✅ Q-table saved to {test_filename}")
        
        # Load Q-table
        with open(test_filename, "rb") as f:
            loaded_q_table = pickle.load(f)
        
        print(f"✅ Q-table loaded ({len(loaded_q_table)} states)")
        
        # Verify contents
        original_value = agent.q_table[(1, 2, 3, 4)]
        loaded_value = loaded_q_table[(1, 2, 3, 4)]
        
        if np.allclose(original_value, loaded_value):
            print(f"✅ Q-table values match exactly")
        else:
            print(f"❌ Q-table values don't match!")
            print(f"   Original: {original_value}")
            print(f"   Loaded: {loaded_value}")
            return False, "Q-table mismatch"
        
        # Clean up
        os.remove(test_filename)
        print(f"   Cleaned up test file")
        
        return True, None
        
    except Exception as e:
        print(f"❌ Q-table save/load test failed: {e}")
        traceback.print_exc()
        return False, str(e)


def test_virus_configs():
    """Test virus configuration loading and WHO parameters"""
    print_section("TEST 8: Virus Configurations")
    
    try:
        from data.virus_configs import VIRUS_CONFIGS
        import json
        
        print(f"✅ Custom virus configs loaded: {len(VIRUS_CONFIGS)} models")
        for name, config in VIRUS_CONFIGS.items():
            print(f"   {name}: R0={config['R0']}, β={config['base_beta']}")
        
        # Test WHO parameters
        try:
            with open("data/who_params.json", "r") as f:
                who_params = json.load(f)
            print(f"✅ WHO parameters loaded: {len(who_params)} diseases")
            for key, data in who_params.items():
                print(f"   {key}: {data['disease_name']}")
        except FileNotFoundError:
            print(f"⚠️  WHO parameters file not found (optional)")
        
        return True, None
        
    except Exception as e:
        print(f"❌ Virus config test failed: {e}")
        traceback.print_exc()
        return False, str(e)


def run_all_tests():
    """Run all validation tests"""
    print("\n" + "🧪" * 35)
    print("EPICONTROL AI - COMPREHENSIVE VALIDATION")
    print("🧪" * 35)
    
    tests = [
        ("Module Imports", test_imports),
        ("RL Environment", test_rl_environment),
        ("Q-Learning Agent", test_q_learning_agent),
        ("Mini Training Loop", test_training_loop),
        ("Mutation System", test_mutation_system),
        ("Spatial Features", test_spatial_features),
        ("Q-Table Save/Load", test_q_table_save_load),
        ("Virus Configurations", test_virus_configs)
    ]
    
    results = {}
    detailed_errors = []
    
    for test_name, test_func in tests:
        try:
            success, error = test_func()
            results[test_name] = success
            if not success and error:
                detailed_errors.append((test_name, error))
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {e}")
            traceback.print_exc()
            results[test_name] = False
            detailed_errors.append((test_name, str(e)))
    
    # Summary
    print("\n" + "=" * 70)
    print("  VALIDATION SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} - {test_name}")
    
    print("\n" + "=" * 70)
    print(f"RESULTS: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("=" * 70)
    
    if detailed_errors:
        print("\n📋 DETAILED ERRORS:")
        for test_name, error in detailed_errors:
            print(f"\n{test_name}:")
            print(f"  {error}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is ready for hackathon! 🎉")
        print("\n✅ Next steps:")
        print("   1. Run 'python rl/train.py' to train the agent")
        print("   2. Run 'streamlit run app.py' to launch dashboard")
        print("   3. Test all 3 control modes in dashboard")
        print("   4. Verify mutations appear")
        print("   5. Check heatmaps display correctly")
    elif passed >= total * 0.8:
        print("\n⚠️  Most tests passed. Review failures before presenting.")
    else:
        print("\n❌ Multiple failures detected. Debug before hackathon.")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
