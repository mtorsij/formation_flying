# =============================================================================
# This file contains the function to do Contract Net Protocol (CNP). 
# =============================================================================
from formation_flying.negotiations.bid_strategies.simple_strategy import simple_strategy


def do_CNP(flight):
    if not flight.departure_time:
        raise Exception("The object passed to the greedy protocol has no departure time, therefore it seems that it is not a flight.")
    
    ### AUCTIONEERS ###
    if flight.accepting_bids == 0 and flight.formation_state == 0:
        # If the agent is not yet in a formation, auctioneers find managers to make bid to
        formation_targets = flight.find_greedy_candidate()
        
        # Set bid expiration date
        bid_expiration_date = 3
        
        
        # Make bids to managers
        for formation_target in formation_targets:
            # Calculate potential fuel saving
            potential_fuel_saving = flight.calculate_potential_fuelsavings(formation_target)
            
            ### BIDDING STRATEGIES
            if flight.strategy == 0:
                bid_value = simple_strategy(flight, formation_target, potential_fuel_saving)
                
            ### HERE WE CAN IMPLEMENT MORE BID STRATEGIES
#            if flight.strategy ==1:
            
            flight.make_bid(formation_target, bid_value, bid_expiration_date)
            
        
    ### MANAGERS ###
    elif flight.accepting_bids == 1:
        for bid in flight.received_bids:    
            # Calculate reservation value
            reservation_value = 10 #0.2 * (flight.calculate_potential_fuelsavings(bid['bidding_agent']))
            
            # Check bid list
            uf = bid['value']  # Add alliance and possible other stuff later
        
            # Accept bid if uf >= reservation value 
            if uf >= reservation_value:
                if bid['bidding_agent'].formation_state == 0:
                    if flight.formation_state == 0:
                        flight.start_formation(bid['bidding_agent'], bid['value'])
                        break
                        
                    elif flight.formation_state != 0 or flight.formation_state != 4:
                        flight.add_to_formation(bid['bidding_agent'], bid['value'])
                        break
                else:
                    flight.received_bids.remove(bid)
            
            # Check the expiration date (NOT WORKING)
#            if bid['exp_date'] == 0:
#                flight.received_bids.remove(flight.received_bids.index(bid))
#            else:
#                bid['exp_date'] = bid['exp_date'] 
        
        ### MAKE OTHER AGENT MANAGER IF CURRENT MANAGER HAS NOT MADE FORMATION FOR N STEPS
        if flight.manager_expiration == 4 and flight.formation_state == 0:
            # Make other flight manager
            for bid in flight.received_bids:
                if bid['bidding_agent'].formation_state == 0:
                    bid['bidding_agent'].manager = 1
                    bid['bidding_agent'].accepting_bids = 1
                    bid['bidding_agent'].made_bids = []
                    new_manager = True
                    
            ### BUILD FUNCTION IF NO SUITABLE NEW MANAGER IS FOUND
            if not new_manager:
                new_manager
            
            # Make current manager auctioneer
            flight.manager = 0
            flight.accepting_bids = 0
            flight.received_bids = []
            
        elif flight.formation_state == 0:
            flight.manager_expiration += 1
            
     
#            ### HERE WE CAN IMPLEMENT MULTIPLE BIDDING STRATEGIES
#            # Calculate bid
#            fuel_saving = flight.calculate_potential_fuelsavings(formation_target)
#            bid_value = 0.15 * fuel_saving
#            bid = {"bid_target": formation_target, "value":bid_value}
#            
#            
#            # Check if a bid already has been made to the manager
#            if bid in flight.made_bids:
#                old_bid = flight.made_bids[flight.made_bids.index(bid)]
#                new_bid_value = old_bid['value'] * 1.1
#                flight.make_bid(formation_target, new_bid_value, bid_expiration_date)
#            
#            else:
    
                

        
    
    
    
        
                
