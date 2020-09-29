# =============================================================================
# This file contains the function to do Contract Net Protocol (CNP). 
# =============================================================================

#Imports


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
            # Check if a bid already has been made to the auctioneer
            
            fuel_saving = flight.calculate_potential_fuelsavings(formation_target)
            
            bid_value = 0.25 * fuel_saving
            flight.make_bid(formation_target, bid_value, bid_expiration_date)
            
        
    ### MANAGERS ###
    elif flight.accepting_bids == 1:
        for bid in flight.received_bids:    
            # Calculate reservation value
            reservation_value = 10
            
            # Check bid list
            uf = bid['value']   # Add alliance and possible other stuff later
        
            # Accept bid if uf >= reservation value 
            if uf >= reservation_value:
                if flight.formation_state == 0:
                    flight.start_formation(bid['bidding_agent'], bid['value'])
                    
                elif flight.formation_state != 0 or flight.formation_state != 4:
                    flight.add_to_formation(bid['bidding_agent'], bid['value'])
            
            else:
                if bid['exp_date'] == 0:
                    flight.received_bids.remove(flight.received_bids.index(bid))
                else:
                    bid['exp_date'] -= 1
                

        
    
    
    
        
                
