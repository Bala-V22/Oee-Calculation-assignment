
def calculate_oee_components(available_time, unplanned_downtime, ideal_cycle_time, total_products, good_products):
    availability = (available_time - unplanned_downtime) / available_time
    if total_products != 0:
        performance = (ideal_cycle_time * total_products) / (total_products * ideal_cycle_time)
    else:
        performance = 0 
    quality = good_products / total_products if total_products != 0 else 0

    return availability, performance, quality
