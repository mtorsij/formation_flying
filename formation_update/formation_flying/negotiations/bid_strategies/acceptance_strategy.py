##############################################################################
### Acceptance strategy for the manager
##############################################################################
def acceptance_strategy(manager, bidding_agent):
       
    if manager.formation_state == 0:
        # Set initial reservation value
        # Using the calc fuelsaving function to compute the joining and leaving point
        total_fuelsaving, joining_point, leaving_point = bidding_agent.calculate_potential_fuelsavings(manager)
        
        original_dist_manager = manager.cal_dist(manager.pos, manager.destination)
        new_dist_manager = manager.calc_dist(manager.pos, joining_point) + manager.calc_dist(joining_point, leaving_point) + manager.calc_dist(leaving_point, manager.destination)
        
        # Calculate fuel difference:
        delta_fuel = new_dist_manager - original_dist_manager
        
        # Bid should be at least 10% above break even point
        reservation_value = delta_fuel * 1.1
        
        # If in alliance set reservation value lower
        if manager.alliance == 1 and bidding_agent.alliance == 1:
            reservation_value = delta_fuel * 1.05
            
    else:
        total_fuelsaving, joining_point, leaving_point = bidding_agent.calculate_potential_fuelsavings(manager)
        
        # Calculating new and original distance
        original_dist_manager = manager.calc_dist(manager.pos, manager.joining_point) + manager.calc_dist(manager.joining_point, manager.leaving_point) + manager.calc_dist(managerleaving_point, manager.destination)
        new_dist_manager = manager.calc_dist(manager.pos, joining_point) + manager.calc_dist(joining_point, leaving_point) + manager.calc_dist(leaving_point, manager.destination)
        
        # Calculate fuel difference:
        delta_fuel = new_dist_manager - original_dist_manager
        
        # Bid should be at least 10% above break even point
        reservation_value = delta_fuel * 1.1
        
        # If in alliance set reservation value lower
        if manager.alliance == 1 and bidding_agent.alliance == 1:
            reservation_value = delta_fuel * 1.05
        
    return reservation_value