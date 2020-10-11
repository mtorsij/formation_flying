def simple_strategy(flight, formation_target, potential_fuel_saving):
    bid_already = False
    
    # Check if bid has already been made
    # If already made return bid with higher value
    for bid in flight.made_bids:
        if bid['bid_target'] == formation_target:
            new_bid_value = bid['value'] * 1.1
            bid_expiration_date = 5 #bid['exp_date']
            
            # Check if not bidding more than half
            if new_bid_value < (0.5 * potential_fuel_saving):
                del flight.made_bids[flight.made_bids.index(bid)]
                bid_value = new_bid_value
                bid_already = True
    
    # If no bid has been made yet, make initial bid
    if not bid_already:
#        frac_fuel_saving = flight.planned_fuel / potential_fuel_saving
        bid_value = 0.15 * potential_fuel_saving
        bid_expiration_date = 5
    
    return bid_value, bid_expiration_date