# =============================================================================
# This file contains the function to do Contract Net Protocol (CNP). 
# =============================================================================

#Imports


def do_CNP(flight):
    if not flight.departure_time:
        raise Exception("The object passed to the greedy protocol has no departure time, therefore it seems that it is not a flight.")

    if flight.formation_state == 0:

        ### AUCTIONEERS ###
        if flight.accepting_bids == 0:
            # If the agent is not yet in a formation, auctioneers find managers to make bid to
            formation_targets = flight.find_greedy_candidate()
            
            # Make bids to managers
            
            
        ### MANAGERS ###
        else:
            # Check bid list
            
            
            # Calculate utility function (uf)
            
            
            # Accept bid if uf >= reservation value 
            
            
            # Form formation if possible
            
            
            # If the manager does not accept bid for n steps choose another manager
            
    else:
        return
        
    
    
    
        
                
