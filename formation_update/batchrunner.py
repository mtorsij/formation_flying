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

iterations = 20

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

#print((run_data["Real saved fuel"] - run_data["Total saved potential saved fuel"])/ run_data["Total Fuel Used"])

# SPLIT DATA
## Total fuel used per km
#spec_fuel_data = run_data['Total Fuel Used'] / run_data['flight time']
#split_spec_fuel_data = np.array_split(spec_fuel_data, 2)

# Fuel saved per km
spec_fuel_save_data = run_data['Real saved fuel'] / run_data['flight time']
split_spec_fuel_save_data = np.array_split(spec_fuel_save_data, 2)

# Fuel saved by alliance
split_alliance_savings_data = np.array_split(run_data['Alliance saved fuel'], 2)

# Number of formations
split_n_formations_data = np.array_split(run_data['new formations'], 2)

# PLOT DATA
# Fuel saved per kilometer comparison
plt.figure()
plt.bar(np.arange(1,(iterations+1)) - 0.05, split_spec_fuel_save_data[0], width=0.1, label='Greedy algorithm')
plt.bar(np.arange(1,(iterations+1)) + 0.05, split_spec_fuel_save_data[1], width=0.1, label='CNP algorithm')
plt.xlabel('Iteration')
plt.ylabel('Fuel saved per kilometer [kg/km]')
plt.title('Fuel saved per kilometer comparison')
plt.legend()

# Fuel saved by the alliance comparison
plt.figure()
plt.bar(np.arange(1,(iterations+1)) - 0.05, split_alliance_savings_data[0], width=0.1, label='Greedy algorithm')
plt.bar(np.arange(1,(iterations+1)) + 0.05, split_alliance_savings_data[1], width=0.1, label='CNP algorithm')
plt.xlabel('Iteration')
plt.ylabel('Fuel saved by alliance [kg]')
plt.title('Fuel saved by the alliance comparison')
plt.legend()

# Number of formations comparison
plt.figure()
plt.bar(np.arange(1,(iterations+1)) - 0.05, split_n_formations_data[0], width=0.1, label='Greedy algorithm')
plt.bar(np.arange(1,(iterations+1)) + 0.05, split_n_formations_data[1], width=0.1, label='CNP algorithm')
plt.xlabel('Iteration')
plt.ylabel('Number of formations')
plt.title('Number of formations comparison')
plt.legend()

## Total fuel used per km
#plt.figure()
#plt.bar(np.arange(1,(iterations+1)) - 0.05, split_spec_fuel_data[0], width=0.1, label='Greedy algorithm')
#plt.bar(np.arange(1,(iterations+1)) + 0.05, split_spec_fuel_data[1], width=0.1, label='CNP algorithm')
#plt.xlabel('Iteration')
#plt.ylabel('Fuel used per kilometer[kg/km]')
#plt.legend()