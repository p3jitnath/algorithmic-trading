# Pairs Trading
## Research Notebook : Pairs Trading Research


import numpy as np

THRESHOLD = 1.0

def initialize(context):
    context.united = sid(28051)
    context.american = sid(45971)
    
    context.long_on_spread = False
    context.short_on_spread = False
    
    schedule_function(check_pairs, date_rules.every_day(), time_rules.market_close(minutes=60))
   
def check_pairs(context, data):
    american = context.american
    united = context.united
    
    prices = data.history([american, united], 'price', 30, '1d')
    
    short_prices = prices.iloc[-1:]
    
    spread = prices[american] - prices[united]
    mavg_30 = np.mean(spread)
    std_30 = np.std(spread)
    mavg_1 = np.mean(short_prices[american] - short_prices[united])
    
    if std_30 > 0 :
        zscore = (mavg_1 - mavg_30)/std_30
        
        if zscore > THRESHOLD and not context.short_on_spread:
            order_target_percent(american, -0.5)
            order_target_percent(united, 0.5)
            context.short_on_spread = True
            context.long_on_spread = False
            
        elif zscore < THRESHOLD and not context.long_on_spread:
            order_target_percent(american, 0.5)
            order_target_percent(united, -0.5)
            
            context.short_on_spread = False
            context.long_on_spread = True
            
        elif abs(zscore) < 0.1:
            
            order_target_percent(american, 0)
            order_target_percent(united, 0)
            context.short_on_spread = False
            context.long_on_spread = False
            
            
        record(Zscore = zscore)