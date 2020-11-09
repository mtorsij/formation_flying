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
        best_bid = []
        
        # Filter bids that pass the acceptance criteria
        for bid in flight.received_bids:      
            # Get reservation value from the acceptance function
            reservation_value, original_dist_manager, new_dist_manager = acceptance_strategy(flight, bid['bidding_agent'])
            
            # Append bid to best bid list if bid value >= reservation value 
            if bid['value'] > reservation_value:
                if bid['bidding_agent'].formation_state == 0:
                    highest_bid_lst.append([bid,original_dist_manager,new_dist_manager])
                else:
                    flight.received_bids.remove(bid)
            
        if highest_bid_lst != []:
#            print(highest_bid_lst)
            
            if len(highest_bid_lst) > 1:     
                # Choose 2 bids that pass the reservation value and minimize delay
                optimal_bid_1 = highest_bid_lst[0]
                optimal_bid_2 = highest_bid_lst[1]
                
                for bid in highest_bid_lst:
                    if bid[2] - bid[1] < optimal_bid_1[2] - optimal_bid_1[1]:
                        optimal_bid_1 = bid
                        continue
                    elif bid[2] - bid[1] < optimal_bid_2[2] - optimal_bid_2[1]:
                        optimal_bid_2 = bid
                        continue
            
                # From bids that minimize delay choose the one with highest bid value
                if optimal_bid_1[0]['value'] > optimal_bid_2[0]['value']: #and optimal_bid_1[0]['value'] > optimal_bid_3[0]['value']:
                    best_bid = optimal_bid_1
                
                else:
                    best_bid = optimal_bid_2
            
            # If only one bid that passes the criteria      
            else:
                best_bid = highest_bid_lst[0]
                
        if best_bid != []:
            if best_bid[0]['bidding_agent'].formation_state != 0 and flight.formation_state != 0:
                raise Exception('Both in formation')
        
        # Start formation or add formation with best bid agent
        if best_bid != []:    
            if best_bid[0]['value'] > 0:
                if flight.formation_state == 0:
                    flight.start_formation(best_bid[0]['bidding_agent'], best_bid[0]['value'])
                    
                elif flight.formation_state != 0 or flight.formation_state != 4:
                    if best_bid[0]['bidding_agent'].formation_state == 0:
                        flight.add_to_formation(best_bid[0]['bidding_agent'], best_bid[0]['value'])
                        
        flight.received_bids = []
        
        ### MAKE OTHER AGENT MANAGER IF CURRENT MANAGER HAS NOT MADE FORMATION FOR N STEPS
        if flight.formation_state == 0:
            if flight.manager_expiration == 100 and flight.formation_state == 0:
               
                # Make other flight manager
                for bid in flight.received_bids:
                    if bid['bidding_agent'].formation_state == 0:
                        bid['bidding_agent'].manager = 1
                        bid['bidding_agent'].accepting_bids = 1
                        bid['bidding_agent'].made_bids = []
#                        new_manager = True
                        
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
    
                

        
    
    
    
        
                
