'''
# =============================================================================
# This file contains the function to do a Vickrey auction. 
# =============================================================================
'''

def do_Vickrey(flight):
    ### AUCTIONEERS ###
    if flight.accepting_bids == 0 and flight.formation_state == 0:
        # If the agent is not yet in a formation, auctioneers find managers to make bid to
        formation_targets = flight.find_greedy_candidate()
        
        # Make bids to managers
        for formation_target in formation_targets:
            # Calculate potential fuel saving
            potential_fuel_saving, joining_point, leaving_point  = flight.calculate_potential_fuelsavings(formation_target)
            
            # Bid generator function
            bid_value = 0.8 * potential_fuel_saving
            
            if bid_value > 0:
                # Make bid
                flight.make_bid(formation_target, bid_value, 5)
            
    ### MANAGERS ###
    elif flight.accepting_bids == 1:
        # Check if received bids
        if flight.received_bids != []:        
            
            # Find highest and second highest bids
            highest_bid = {"bidding_agent": 0, "value": 0, "exp_date": 0}
            second_highest_bid = {"bidding_agent": 0, "value": 0, "exp_date": 0}
            
            for bid in flight.received_bids:
                if bid['value'] > highest_bid['value']:
                    highest_bid = bid
                elif bid['value'] < highest_bid['value'] and bid['value'] > second_highest_bid['value']:
                    second_highest_bid = bid
            
            # Start formation with winner at second highest bid value
            # Check if flight is already in formation
            if flight.formation_state == 0:
                if highest_bid['bidding_agent'].formation_state == 0:    
                    flight.start_formation(highest_bid['bidding_agent'], second_highest_bid['value'])
            
            # Manager is already in formation
            elif flight.formation_state != 0 or flight.formation_state != 4:
                if highest_bid['bidding_agent'].formation_state == 0:
                    flight.add_to_formation(highest_bid['bidding_agent'], second_highest_bid['value'])
            
            # Clear received_bids list for next auction
            flight.received_bids = []