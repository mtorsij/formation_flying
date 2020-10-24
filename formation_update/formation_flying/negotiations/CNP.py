# =============================================================================
# This file contains the function to do Contract Net Protocol (CNP). 
# =============================================================================
from formation_flying.negotiations.bid_strategies.simple_strategy import simple_strategy
from formation_flying.negotiations.bid_strategies.acceptance_strategy import acceptance_strategy

def do_CNP(flight):
    if not flight.departure_time:
        raise Exception("The object passed to the CNP protocol has no departure time, therefore it seems that it is not a flight.")
    
    ### AUCTIONEERS ###
    if flight.accepting_bids == 0 and flight.formation_state == 0:
        # If the agent is not yet in a formation, auctioneers find managers to make bid to
        formation_targets = flight.find_greedy_candidate()
        
        # Make bids to managers
        for formation_target in formation_targets:
            # Calculate potential fuel saving
            potential_fuel_saving, joining_point, leaving_point  = flight.calculate_potential_fuelsavings(formation_target)
            
            ### BIDDING STRATEGIES
            if flight.strategy == 0:
                bid_value, bid_expiration_date = simple_strategy(flight, formation_target, potential_fuel_saving)
            
            ### HERE WE CAN IMPLEMENT MORE BID STRATEGIES
#            if flight.strategy ==1:
            
            # Make bid with values from a bid strategy
            if bid_value > 0:
                flight.make_bid(formation_target, bid_value, bid_expiration_date)
            
    ### MANAGERS ###
    elif flight.accepting_bids == 1:
        highest_bid_lst = []
       
        # Filter bids that pass the acceptance criteria
        for bid in flight.received_bids:      
            # Get reservation value from the acceptance function
            reservation_value, original_dist_manager, new_dist_manager = acceptance_strategy(flight, bid['bidding_agent'])
            
            print('value')
            print(bid['value'])
            print('reservation')            
            print(reservation_value)
            
            # Append bid to best bid list if bid value >= reservation value 
            if bid['value'] >= reservation_value:
                if bid['bidding_agent'].formation_state == 0:
                    highest_bid_lst.append([bid,original_dist_manager,new_dist_manager])
                else:
                    flight.received_bids.remove(bid)
     
        print(highest_bid_lst)
        
        # Choose bid that minimizes the delay
        min_delay = 1e6
        best_bid = []
        for bid in highest_bid_lst:
            if bid[2] - bid[1] < min_delay:
                best_bid = bid    
        print(best_bid)
        
        if best_bid != []:
            raise Exception('Niet goed genoeg')
        
        # Start formation or add formation with best bid agent
#        if flight.formation_state == 0:
#            flight.start_formation(best_bid[0]['bidding_agent'], best_bid[0]['value'])         
#                        
#        elif flight.formation_state != 0 or flight.formation_state != 4:
#            flight.add_to_formation(best_bid[0]['bidding_agent'], best_bid[0]['value'])
            
        
        ### MAKE OTHER AGENT MANAGER IF CURRENT MANAGER HAS NOT MADE FORMATION FOR N STEPS
        if flight.formation_state == 0:
            if flight.manager_expiration == 100 and flight.formation_state == 0:
               
                # Make other flight manager
                for bid in flight.received_bids:
                    if bid['bidding_agent'].formation_state == 0:
                        bid['bidding_agent'].manager = 1
                        bid['bidding_agent'].accepting_bids = 1
                        bid['bidding_agent'].made_bids = []
                        new_manager = True
                        
                ### BUILD FUNCTION IF NO SUITABLE NEW MANAGER IS FOUND
#                if not new_manager:
                
                # Make current manager auctioneer
                flight.manager = 0
                flight.accepting_bids = 0
                flight.received_bids = []
                
            elif flight.formation_state == 0:
                flight.manager_expiration += 1

#=============================================================================       
# BID EXPIRATION CHECKER (NOT WORKING)
#=============================================================================
#            # Check the expiration date
#            if bid['exp_date'] == 0:
#                # Remove bid from manager received bid list
#                flight.received_bids.remove(bid)
#                
#                # Same for made bid list of auctioneer
#                for made_bid in bid['bidding_agent'].made_bids:
#                    if made_bid['bid_target'] == flight:
#                        bid['bidding_agent'].made_bids.remove(made_bid)
#            else:
#                # Update expiration date in manager received bids list
#                if bid in flight.received_bids:    
#                    flight.received_bids[flight.received_bids.index(bid)]['exp_date'] -= 1
#                
#                # Do the same for the made bids list of auctioneer
#                for i in range(len(bid['bidding_agent'].made_bids)):
#                    if bid['bidding_agent'].made_bids[i]['bid_target'] == flight:
#                        bid['bidding_agent'].made_bids[i]['exp_date'] -= 1
    
                

        
    
    
    
        
                
