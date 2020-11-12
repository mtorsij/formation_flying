##Strategy for bidders in auction to bid to their true value##

def calc_distance(p1, p2):
    # p1 = tuple(p1)
    # p2 = tuple(p2)
    dist = (((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5)  ##x and y position x=0 y=1
    return dist

def true_value_strategy(bidder, auctioneer): ##input is self(bidder) and auctioneer
    total_fuelsaving, joining_point, leaving_point = bidder.calculate_potential_fuelsavings(auctioneer)
    original_distance = calc_distance(bidder.pos,bidder.destination)
    new_dist = calc_distance(bidder.pos,joining_point)+calc_distance(joining_point,leaving_point) + calc_distance(leaving_point,bidder.destination)

    ##Calculate the difference in distance, fuel and time to use for trade-off
    diff_km = new_dist - original_distance #without savings factor
    if diff_km > 0:
        fuel_km = total_fuelsaving/diff_km
        if fuel_km >= 2:        #the bidder receives at least double the fuel savings over the extra kilometers flown
            true_value = 2 * diff_km
        else:
            true_value = 0
    
    else:
        true_value = 0
    #alliance


    return true_value
