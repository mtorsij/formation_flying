##############################################################################
### Acceptance strategy for the manager
##############################################################################
def acceptance_strategy(manager, bidding_agent):
       
    if manager.formation_state == 0:
        # Set initial reservation value
        # Using the calc fuelsaving function to compute the joining and leaving point
        total_fuelsaving, joining_point, leaving_point = bidding_agent.calculate_potential_fuelsavings(manager)
        
        original_dist_manager = calc_distance(manager.pos, manager.destination)
        new_dist_manager = calc_distance(manager.pos, joining_point) + calc_distance(joining_point, leaving_point) + calc_distance(leaving_point, manager.destination)
        
        # Calculate fuel difference:
        delta_fuel = new_dist_manager - original_dist_manager
        
        # Bid should be at least 10% above break even point
        reservation_value = delta_fuel * 1.2
        
        # If in alliance set reservation value lower
        if manager.alliance == 1 and bidding_agent.alliance == 1:
            reservation_value = delta_fuel * 1.1
            
    else:
        # Check if bidding agent is not in formation
        if bidding_agent.formation_state == 0:
            total_fuelsaving, joining_point, leaving_point = bidding_agent.calculate_potential_fuelsavings(manager)
            
            # Calculating new and original distance
            original_dist_manager = calc_distance(manager.pos, manager.joining_point) + calc_distance(manager.joining_point, manager.leaving_point) + calc_distance(manager.leaving_point, manager.destination)
            new_dist_manager = calc_distance(manager.pos, joining_point) + calc_distance(joining_point, leaving_point) + calc_distance(leaving_point, manager.destination)
            
            # Calculate fuel difference:
            delta_fuel = new_dist_manager - original_dist_manager
            
            # Bid should be at least 10% above break even point
            reservation_value = delta_fuel * 1.1
            
            # If in alliance set reservation value lower
            if manager.alliance == 1 and bidding_agent.alliance == 1:
                reservation_value = delta_fuel * 1.05
        # If bidding agent in formation return 0    
        else:
            reservation_value, original_dist_manager, new_dist_manager = 0,0,0
        
        
    return reservation_value, original_dist_manager, new_dist_manager

def calc_distance(p1, p2):
    # p1 = tuple(p1)
    # p2 = tuple(p2)
    dist = (((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5)  ##x and y position x=0 y=1
    return dist