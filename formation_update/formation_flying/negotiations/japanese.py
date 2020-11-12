'''
# =============================================================================
# This file contains the function to do a Japanese auction. 
# =============================================================================
'''
from formation_flying.negotiations.bid_strategies.true_value_strategy import true_value_strategy

def do_Japanese(flight):
    ### AUCTIONEERS ###
    if flight.accepting_bids == 0 and flight.formation_state == 0:
        # If the agent is not yet in a formation, auctioneers find managers to make bid to
        formation_targets = flight.find_greedy_candidate()
        
        # Make bids to managers
        for formation_target in formation_targets:
            
            # Personal max
            max_bid_value = true_value_strategy(flight, formation_target)
            
            # Make sure that agent only enters an auction once
            already_entered = False                
            
            if formation_target.agents_in_auction == [] and formation_target.current_price < max_bid_value:
                formation_target.agents_in_auction.append({'agent': flight, 'state': 'in auction'})
                already_entered = True
                
            for agent in formation_target.agents_in_auction:
               
                # Check if agent is in the auction and is participating
                if agent['agent'] == flight and agent['state'] == 'in auction':
                    
                    # The agent already entered the auction
                    already_entered = True
                    
                    # If the current price is higher than personal max -> exit auction
                    if formation_target.current_price > max_bid_value:
                        formation_target.agents_in_auction[formation_target.agents_in_auction.index(agent)]['state'] = 'exit auction'
                        
                # If the agent already exited the auction it cannot enter again
                elif agent['agent'] == flight and agent['state'] == 'exit auction':
                    # The agent already entered
                    already_entered = True
                
            # If the agent has not entered the auction yet and the current price is below the personal max
            if formation_target.current_price < max_bid_value and already_entered != True: 
                formation_target.agents_in_auction.append({'agent': flight, 'state': 'in auction'})
        
    ### MANAGERS ###
    elif flight.accepting_bids == 1:
       
        # Check how many agents in auction
        flights_in_auction_counter = 0
        for agent in flight.agents_in_auction:
            if agent['state'] == 'in auction':
                flights_in_auction_counter += 1
                winner = agent['agent']
        
        # If one flight remains, pick the winner and start formation
        if flights_in_auction_counter == 1:
            
            # Start formation with the remaining agent
            # Check if flight is already in formation
            if flight.formation_state == 0:
                if winner.formation_state == 0:    
                    flight.start_formation(winner, flight.current_price)
            
            # Manager is already in formation
            elif flight.formation_state != 0 or flight.formation_state != 4:
                if winner.formation_state == 0:
                    flight.add_to_formation(winner, flight.current_price)
                    
            # Reset current price based on number of agents in formation and adjust price increase per step
            if len(flight.agents_in_my_formation) > 2:
                flight.current_price = 50
                flight.price_increase = 10
            else:
                flight.current_price = 80
                flight.price_increase = 20
            
            # Reset agents in auction list
            flight.agents_in_auction = []
        
        # If flights are in the auction decrease price
        if flights_in_auction_counter == 0:
             flight.current_price -= flight.price_increase
        
        if flight.current_price <= 0:
            flight.agents_in_auction = []
            flight.current_price = 20
        
             
        # If multiple flights are still in the auction increase price
        if flights_in_auction_counter > 1:
           # Current price is raised by five every round
           flight.current_price += flight.price_increase
            
            
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            