# =============================================================================
# This file contains the function to do Contract Net Protocol (CNP). 
# =============================================================================
from formation_flying.negotiations.bid_strategies.simple_strategy import simple_strategy


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
            potential_fuel_saving = flight.calculate_potential_fuelsavings(formation_target)
            
            ### BIDDING STRATEGIES
            if flight.strategy == 0:
                bid_value, bid_expiration_date = simple_strategy(flight, formation_target, potential_fuel_saving)
                
            ### HERE WE CAN IMPLEMENT MORE BID STRATEGIES
#            if flight.strategy ==1:
            
            # Make bid with values from a bid strategy
            flight.make_bid(formation_target, bid_value, bid_expiration_date)
            
    ### MANAGERS ###
    elif flight.accepting_bids == 1:
        for bid in flight.received_bids:    
            
            # Set initial reservation value
            reservation_value = 40
            
            # If in alliance set reservation value lower
            if flight.alliance == 1 and bid['bidding_agent'].alliance == 1:
                reservation_value = 30
            
            # Check bid list
            uf = bid['value']
            
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

                ### MAKE OTHER AGENT MANAGER IF CURRENT MANAGER HAS NOT MADE FORMATION FOR N STEPS
        if flight.formation_state == 0:
            if flight.manager_expiration == 10 and flight.formation_state == 0:
               
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
#                flight.manager = 0
                flight.accepting_bids = 0
                flight.received_bids = []
                
            elif flight.formation_state == 0:
                flight.manager_expiration += 1

       
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
    
                

        
    
    
    
        
                
