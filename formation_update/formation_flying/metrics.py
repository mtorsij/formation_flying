'''
# =============================================================================
# Data functions are saved here (instead of Model.py) for a better overview. 
# These functions can be called upon by the DataCollector. 
# You can add more advanced metric here!
# =============================================================================
'''
def compute_total_fuel_used(model):
    return model.total_fuel_consumption

def compute_planned_fuel(model):
    return model.total_planned_fuel

def fuel_savings_closed_deals(model):
    return model.fuel_savings_closed_deals

def real_fuel_saved(model):
    return model.total_planned_fuel - model.total_fuel_consumption

def total_deal_value(model):
    return model.total_auction_value

def n_bidding_agents(model):
    return model.n_auctions_won
    
def compute_total_flight_time(model):
    return model.total_flight_time

def compute_model_steps(model):
    return model.schedule.steps

def new_formation_counter(model):
    return model.new_formation_counter

def add_to_formation_counter(model):
    return model.add_to_formation_counter

def alliance_saved_fuel(model):
    return model.alliance_saved_fuel

def n_agents_per_formation(model):
    return model.formation_list

def negotiation_method(model):
    return model.negotiation_method

def formation_timeline_start(model):
    return model.n_formation_list[0:50]
    