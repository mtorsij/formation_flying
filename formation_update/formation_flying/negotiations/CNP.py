# =============================================================================
# This file contains the function to do Contract Net Protocol (CNP). 
# =============================================================================


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
            # Calculate bid
            fuel_saving = flight.calculate_potential_fuelsavings(formation_target)
            bid_value = 0.15 * fuel_saving
            bid = {"bid_target": formation_target, "value":bid_value, "exp_date": bid_expiration_date}
            
            # Check if a bid already has been made to the manager
            if bid in flight.made_bids:
                old_bid = flight.made_bids[flight.made_bids.index(bid)]
                new_bid_value = old_bid['value'] * 1.1
                flight.make_bid(formation_target, new_bid_value, bid_expiration_date)
            else:
                flight.make_bid(formation_target, bid_value, bid_expiration_date)
            
        
    ### MANAGERS ###
    elif flight.accepting_bids == 1:
        for bid in flight.received_bids:    
            # Calculate reservation value
            reservation_value = 10#0.2 * (flight.calculate_potential_fuelsavings(bid['bidding_agent']))
            
            # Check bid list
            uf = bid['value']   # Add alliance and possible other stuff later
        
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
          
#                if bid['exp_date'] == 0:
#                    flight.received_bids.remove(flight.received_bids.index(bid))
#                else:
#                    bid['exp_date'] = bid['exp_date'] 

    
                

        
    
    
    
        
                
