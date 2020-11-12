'''
# =============================================================================
# This file contains the function to do an English auction. 
# =============================================================================
'''
from formation_flying.negotiations.bid_strategies.true_value_strategy import true_value_strategy

def do_English(flight):
    ### AUCTIONEERS ###
    if flight.accepting_bids == 0 and flight.formation_state == 0:
        # If the agent is not yet in a formation, auctioneers find managers to make bid to
        formation_targets = flight.find_greedy_candidate()
        
        # Make bids to managers
        for formation_target in formation_targets:
            # Calculate potential fuel saving
            potential_fuel_saving, joining_point, leaving_point  = flight.calculate_potential_fuelsavings(formation_target)
            
            # Personal max
            max_bid_value = true_value_strategy(flight, formation_target)
            
            # If no bids have been made to manager so far, make first bid
            if len(formation_target.received_bids) == 0:
                flight.make_bid(formation_target, potential_fuel_saving * 0.5, 5)
            
            # If bids have been made, update bid if under personal max
            else:
                if formation_target.received_bids[0]['bidding_agent'] != flight:
                    if formation_target.received_bids[0]['value'] * 1.1 < max_bid_value:
                        formation_target.received_bids[0] = {"bidding_agent": flight, "value": formation_target.received_bids[0]['value'] * 1.1, "exp_date": 5}
            
    ### MANAGERS ###
    elif flight.accepting_bids == 1:
        # Check if received bids
        if flight.received_bids != []:        
            
            # If current highest is highest from last round -> formation
            if flight.highest_bidding_agent == flight.received_bids[0]['bidding_agent']:
                # Check if flight is already in formation
                if flight.formation_state == 0:
                    if flight.received_bids[0]['bidding_agent'].formation_state == 0:    
                        flight.start_formation(flight.received_bids[0]['bidding_agent'], flight.received_bids[0]['value'])
                
                # Manager is already in formation
                elif flight.formation_state != 0 or flight.formation_state != 4:
                    if flight.received_bids[0]['bidding_agent'].formation_state == 0:
                        flight.add_to_formation(flight.received_bids[0]['bidding_agent'], flight.received_bids[0]['value'])
                
                # Clear received_bids list for next auction
                flight.received_bids = []
            
            # Update current highest bidding agent
            else:
                flight.highest_bidding_agent = flight.received_bids[0]['bidding_agent']
            