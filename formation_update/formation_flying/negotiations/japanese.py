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
            # Calculate potential fuel saving
            potential_fuel_saving, joining_point, leaving_point  = flight.calculate_potential_fuelsavings(formation_target)
            
            # Personal max
            max_bid_value = true_value_strategy(flight, formation_target)
            
            for agent in formation_target.agents_in_auction:
                # Check if agent is in the auction and is participating
                if agent['agent'] == flight and agent['state'] == 'in auction':
                    # If the current price is higher than personal max -> exit auction
                    if formation_target.current_price > max_bid_value:
                        formation_target.agents_in_auction[formation_target.agents_in_auction.index(agent)]['state'] = 'exit auction'
                
                # If the agent already exited the auction it cannot enter again
                elif agent['agent'] == flight and agent['state'] == 'exit auction':
                    continue
                
                # If the agent has not entered the auction yet and the current price is below the personal max
                elif formation_target.current_price > max_bid_value: 
                    formation_target.append({'agent': flight, 'state': 'in auction'})
                
            
    ### MANAGERS ###
    elif flight.accepting_bids == 1:
       
        # Check how many agents in auction
        flights_in_auction_counter = 0
        for agent in flight.agents_in_auction:
            if agent['state'] == 'in auction':
                flights_in_auction_counter += 1
        
        # If one flight remains, pick the winner and start formation
        if flights_in_auction_counter == 1:
            # Find the winner
            for agent in flight.agents_in_auction:
                if agent['state'] == 'in auction':
                    winner = agent['agent']
        
            # Start formation with the remaining agent
            # Check if flight is already in formation
            if flight.formation_state == 0:
                if winner.formation_state == 0:    
                    flight.start_formation(winner, flight.current_price)
            
            # Manager is already in formation
            elif flight.formation_state != 0 or flight.formation_state != 4:
                if winner.formation_state == 0:
                    flight.add_to_formation(winner, flight.current_price)
                    
            # When formation is formed, reset agents in auction list and the current price
            flight.current_price = 60
            flight.agents_in_auction = []
        
        # If flights are in the auction decrease price
        if flights_in_auction_counter == 0:
             flight.current_price -= 5
        
        # If multiple flights are still in the auction increase price
        if flights_in_auction_counter > 1:
           # Current price is raised by five every round
           flight.current_price += 5
            
            
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            