import numpy as np
from scipy import optimize

def optimize_parking_allocation(config):
    """
    Optimize parking space allocation using linear programming
    
    Args:
        config: ParkingConfiguration object with all required parameters
    
    Returns:
        dict: Results of the optimization
    """
    # Define the objective function (negative because we're maximizing)
    # c = [hourly_revenue * hourly_reliability, monthly_revenue * monthly_reliability, corporate_revenue * corporate_reliability]
    c = [-config.hourly_revenue * config.hourly_reliability, 
         -config.monthly_revenue * config.monthly_reliability, 
         -config.corporate_revenue * config.corporate_reliability]
    
    # Define the constraints in standard form Ax <= b
    A = [
        [1, 1, 1],  # Total spaces constraint
        [-1, 0, 0],  # Minimum hourly spaces constraint (convert to <= form)
        [-config.hourly_reliability, -config.monthly_reliability, -config.corporate_reliability]  # Occupancy requirement (convert to <= form)
    ]
    
    b = [
        config.total_spaces,  # Total spaces constraint value
        -config.min_hourly_spaces,  # Minimum hourly spaces constraint value (negative because of conversion)
        -config.occupancy_requirement * config.total_spaces  # Occupancy requirement value (negative because of conversion)
    ]
    
    # Non-negativity bounds
    bounds = [(0, None), (0, None), (0, None)]
    
    # Solve the linear programming problem
    result = optimize.linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
    
    if result.success:
        # Round the solution to integers
        hourly_spaces = round(result.x[0])
        monthly_spaces = round(result.x[1])
        corporate_spaces = round(result.x[2])
        
        # Adjust to make sure we don't exceed total spaces after rounding
        total = hourly_spaces + monthly_spaces + corporate_spaces
        if total > config.total_spaces:
            # Reduce the largest allocation first
            max_idx = np.argmax([hourly_spaces, monthly_spaces, corporate_spaces])
            if max_idx == 0:
                hourly_spaces -= (total - config.total_spaces)
            elif max_idx == 1:
                monthly_spaces -= (total - config.total_spaces)
            else:
                corporate_spaces -= (total - config.total_spaces)
        
        # Calculate expected revenue
        expected_revenue = (hourly_spaces * config.hourly_revenue * config.hourly_reliability + 
                           monthly_spaces * config.monthly_revenue * config.monthly_reliability + 
                           corporate_spaces * config.corporate_revenue * config.corporate_reliability)
        
        # Calculate expected occupancy
        expected_occupancy = (hourly_spaces * config.hourly_reliability + 
                             monthly_spaces * config.monthly_reliability + 
                             corporate_spaces * config.corporate_reliability) / config.total_spaces
        
        return {
            'success': True,
            'hourly_spaces': hourly_spaces,
            'monthly_spaces': monthly_spaces,
            'corporate_spaces': corporate_spaces,
            'expected_revenue': expected_revenue,
            'expected_occupancy': expected_occupancy
        }
    else:
        return {
            'success': False,
            'message': 'Optimization failed: ' + result.message
        }