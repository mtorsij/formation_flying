'''
# =============================================================================
# When running this file the batchrunner will be used for the model. 
# No visulaization will happen.
# =============================================================================
'''
from mesa.batchrunner import BatchRunner
from formation_flying.model import FormationFlying
from formation_flying.parameters import model_params, max_steps, n_iterations, model_reporter_parameters, agent_reporter_parameters, variable_params
from matplotlib import pyplot as plt
import numpy as np

# Choose what has to be compared
greedy_comp = False
vision_comp = False
auction_comp = False

airport_pos_comp = True
# PLot data of all three runs
first = False
second = False
third = False
plot_all = True

# Number of iterations
iterations = 1

batch_run = BatchRunner(FormationFlying,
                            fixed_parameters=model_params,
                            variable_parameters=variable_params,
                            iterations = iterations,
                            max_steps=max_steps,
                            model_reporters=model_reporter_parameters,
                            agent_reporters=agent_reporter_parameters
                            )

batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
run_data.head()

#-----------------------------------------------------------------------------
### GREEDY COMPARISON
#-----------------------------------------------------------------------------
if greedy_comp:    
    # SPLIT DATA
    # Fuel saved per km
    spec_fuel_save_data = run_data['Real saved fuel'] / run_data['flight time']
    split_spec_fuel_save_data = np.array_split(spec_fuel_save_data, 2)
    
    # Fuel saved by alliance
    split_alliance_savings_data = np.array_split(run_data['Alliance saved fuel'], 2)
    
    # Number of formations
    split_n_formations_data = np.array_split(run_data['new formations'], 2)
    
    # Total distance flown
    split_dist_data = np.array_split(run_data['flight_time'], 2)
    
    # PLOT DATA
    # Fuel saved per kilometer comparison
    plt.figure()
    plt.bar(np.arange(1,(iterations+1)) - 0.15, split_spec_fuel_save_data[0], width=0.3, label='Greedy algorithm')
    plt.bar(np.arange(1,(iterations+1)) + 0.15, split_spec_fuel_save_data[1], width=0.3, label='CNP algorithm')
    plt.xlabel('Iteration')
    plt.ylabel('Fuel saved per kilometer [kg/km]')
    plt.title('Fuel saved per kilometer comparison')
    plt.legend()
    
    # Fuel saved by the alliance comparison
    plt.figure()
    plt.bar(np.arange(1,(iterations+1)) - 0.15, split_alliance_savings_data[0], width=0.3, label='Greedy algorithm')
    plt.bar(np.arange(1,(iterations+1)) + 0.15, split_alliance_savings_data[1], width=0.3, label='CNP algorithm')
    plt.xlabel('Iteration')
    plt.ylabel('Fuel saved by alliance [kg]')
    plt.title('Fuel saved by the alliance comparison')
    plt.legend()
    
    # Number of formations comparison
    plt.figure()
    plt.bar(np.arange(1,(iterations+1)) - 0.15, split_n_formations_data[0], width=0.3, label='Greedy algorithm')
    plt.bar(np.arange(1,(iterations+1)) + 0.15, split_n_formations_data[1], width=0.3, label='CNP algorithm')
    plt.xlabel('Iteration')
    plt.ylabel('Number of formations')
    plt.title('Number of formations comparison')
    plt.legend()
    
    # Total distance flown
    plt.figure()
    plt.bar(np.arange(1,(iterations+1)) - 0.15, split_dist_data[0], width=0.3, label='Greedy algorithm')
    plt.bar(np.arange(1,(iterations+1)) + 0.15, split_dist_data[1], width=0.3, label='CNP algorithm')
    plt.xlabel('Iteration')
    plt.ylabel('Total distance flown [km]')
    plt.title('Total distance flown comparison')
    plt.legend()

#-----------------------------------------------------------------------------
### VISION COMPARISON
#-----------------------------------------------------------------------------
if vision_comp:
    # SPLIT AND AVERAGE DATA
    # Fuel saved per km
    spec_fuel_save_data = (run_data['Real saved fuel'] / run_data['flight time'])
    split_spec_fuel_save_data = np.array_split(spec_fuel_save_data, 3)
    split_spec_fuel_save_data[0] = sum(split_spec_fuel_save_data[0]) / iterations
    split_spec_fuel_save_data[1] = sum(split_spec_fuel_save_data[1]) / iterations
    split_spec_fuel_save_data[2] = sum(split_spec_fuel_save_data[2]) / iterations
    
    # Fuel saved by alliance
    split_alliance_savings_data = np.array_split(run_data['Alliance saved fuel'], 3)
    split_alliance_savings_data[0] = sum(split_alliance_savings_data[0]) / iterations
    split_alliance_savings_data[1] = sum(split_alliance_savings_data[1]) / iterations
    split_alliance_savings_data[2] = sum(split_alliance_savings_data[2]) / iterations
    
    # Number of formations
    split_n_formations_data = np.array_split(run_data['new formations'], 3)
    split_n_formations_data[0] = sum(split_n_formations_data[0]) / iterations
    split_n_formations_data[1] = sum(split_n_formations_data[1]) / iterations
    split_n_formations_data[2] = sum(split_n_formations_data[2]) / iterations
    
     # Total distance flown
    split_dist_data = np.array_split(run_data['flight_time'], 3)
    split_dist_data[0] = sum(split_dist_data[0]) / iterations
    split_dist_data[1] = sum(split_dist_data[1]) / iterations
    split_dist_data[2] = sum(split_dist_data[2]) / iterations
    
    # PLOT DATA
    # Fuel saved per kilometer comparison
    plt.figure()
    plt.plot([50,200,500], split_spec_fuel_save_data, marker='o', color='b')
    plt.xlabel('Communication range [km]')
    plt.ylabel('Fuel saved per kilometer [kg/km]')
    plt.title('Fuel saved per kilometer comparison')

    # Fuel saved by the alliance comparison
    plt.figure()
    plt.plot([50,200,500], split_alliance_savings_data, marker='o', color='b')
    plt.xlabel('Communication range [km]')
    plt.ylabel('Fuel saved by alliance [kg]')
    plt.title('Fuel saved by the alliance comparison')
  
    # Number of formations comparison
    plt.figure()
    plt.plot([50,200,500], split_n_formations_data, marker='o', color='b')
    plt.xlabel('Communication range [km]')
    plt.ylabel('Number of formations')
    plt.title('Number of formations comparison')   
    
#-----------------------------------------------------------------------------
### ORIGIN AND DESTINATION COMPARISON
#-----------------------------------------------------------------------------
if airport_pos_comp:
    # SPLIT AND AVERAGE DATA
    # Fuel saved per km
    average_spec_fuel_save_data = sum((run_data['Real saved fuel'] / run_data['flight time'])) / iterations
    print(average_spec_fuel_save_data)
    
    # Fuel saved by alliance
    average_alliance_savings_data = sum(run_data['Alliance saved fuel']) / iterations
    print(average_alliance_savings_data)
    
    # Number of formations
    average_n_formations_data = sum(run_data['new formations']) / iterations
    print(average_n_formations_data)
    
    # VISUALISE HOW FAST FORMATIONS ARE FORMED AND ENDED
    split_formation_timeline_data = np.array_split(run_data['Formation timeline start'], iterations)
    
    # Convert to a list which can be split end averaged
    formation_timeline_data_converted = []
    for i in range(len(split_formation_timeline_data)):
        formation_timeline_data_converted.append(split_formation_timeline_data[i][i])    
    
    # Split and average
    split_formation_timeline_data_converted = np.array_split(formation_timeline_data_converted, iterations)
    average_split_formation_timeline_start_data = sum(split_formation_timeline_data_converted) / iterations
    
    # Save data of first, second and third run
    if first:
        np.save('temp_data/first', average_split_formation_timeline_start_data)
    elif second:
        np.save('temp_data/second', average_split_formation_timeline_start_data)
    elif third:
        np.save('temp_data/third', average_split_formation_timeline_start_data)
    
    # Load the data and plot
    if plot_all:
        first_formation_timeline_data = np.load('temp_data/first.npy')
        second_formation_timeline_data = np.load('temp_data/second.npy')
        third_formation_timeline_data = np.load('temp_data/third.npy')
    
        # PLOT DATA
        plt.figure()
        plt.plot(np.arange(0,50), first_formation_timeline_data[0], label = "First position of origin and destination airport")
        plt.plot(np.arange(0,50), second_formation_timeline_data[0], label = "Second position of origin and destination airport")
        plt.plot(np.arange(0,50), third_formation_timeline_data[0], label = "Third position of origin and destination airport")
        plt.xlabel('Step')
        plt.ylabel('Number of formations')
        plt.title('Speed of formations forming')
        plt.legend()
    
#-----------------------------------------------------------------------------
### AUCTION METHOD COMPARISON
#-----------------------------------------------------------------------------
if auction_comp:
    # SPLIT DATA
    # Fuel saved per km
    spec_fuel_save_data = run_data['Real saved fuel'] / run_data['flight time']
    split_spec_fuel_save_data = np.array_split(spec_fuel_save_data, 3)
    
    split_spec_fuel_save_data[0] = sum(split_spec_fuel_save_data[0]) / iterations
    split_spec_fuel_save_data[1] = sum(split_spec_fuel_save_data[1]) / iterations
    split_spec_fuel_save_data[2] = sum(split_spec_fuel_save_data[2]) / iterations
    
     # Number of formations
    split_n_formations_data = np.array_split(run_data['new formations'], 3)
    split_n_formations_data[0] = sum(split_n_formations_data[0]) / iterations
    split_n_formations_data[1] = sum(split_n_formations_data[1]) / iterations
    split_n_formations_data[2] = sum(split_n_formations_data[2]) / iterations
    
     # Total distance flown
    split_dist_data = np.array_split(run_data['flight_time'], 3)
    split_dist_data[0] = sum(split_dist_data[0]) / iterations
    split_dist_data[1] = sum(split_dist_data[1]) / iterations
    split_dist_data[2] = sum(split_dist_data[2]) / iterations
    
    # PLOT DATA
    # Fuel saved per kilometer comparison
    plt.figure()
    plt.bar(0.7, split_spec_fuel_save_data[0], width=0.3, label='English')
    plt.bar(1, split_spec_fuel_save_data[1], width=0.3, label='Vickrey')
    plt.bar(1.3, split_spec_fuel_save_data[2], width=0.3, label='Japanese')
    plt.xlabel('Iteration')
    plt.ylabel('Fuel saved per kilometer [kg/km]')
    plt.title('Fuel saved per kilometer comparison')
    plt.legend()

    # Fuel saved per kilometer comparison
    plt.figure()
    plt.bar(0.7, split_n_formations_data[0], width=0.3, label='English')
    plt.bar(1, split_n_formations_data[1], width=0.3, label='Vickrey')
    plt.bar(1.3, split_n_formations_data[2], width=0.3, label='Japanese')
    plt.xlabel('Iteration')
    plt.ylabel('Fuel saved per kilometer [kg/km]')
    plt.title('Fuel saved per kilometer comparison')
    plt.legend()
    
    # Fuel saved per kilometer comparison
    plt.figure()
    plt.bar( 0.7, split_dist_data[0], width=0.3, label='English')
    plt.bar( 1, split_dist_data[1], width=0.3, label='Vickrey')
    plt.bar( 1.3 , split_dist_data[2], width=0.3, label='Japanese')
    plt.xlabel('Iteration')
    plt.ylabel('Fuel saved per kilometer [kg/km]')
    plt.title('Fuel saved per kilometer comparison')
    plt.legend()
    


    