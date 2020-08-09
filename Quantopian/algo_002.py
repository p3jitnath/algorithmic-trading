# Boolinger Bands 


def initialize(context):
    context.jj = sid(4151)
    
    schedule_function(check_bands, date_rules.every_day())
    
    
def check_bands(context, data):
    current_price = data.current(context.jj, 'price')
    
    prices = data.history(context.jj, 'price', 20, '1d')
    
    avg = prices.mean()
    std = prices.std()
    
    upper_band = avg + 2*std
    lower_band = avg - 2*std
    
    if current_price >= upper_band:
        order_target_percent(context.jj, -1.0)
        print("Shorting ...")
        
    elif current_price <= lower_band:
        order_target_percent(context.jj, 1.0)
        print("Buying ...")
            
    else:
        pass
    
    record(upper=upper_band, 
           lower=lower_band,
           mavg_20=avg,
           price=current_price)