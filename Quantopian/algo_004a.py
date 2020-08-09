# Leverage

FRACTION = 0.5

def initialize(context):
    
    set_max_leverage(1.05) # ERROR !!!
    
    context.amzn = sid(16841)
    context.ibm = sid(3766)
    
    schedule_function(rebalance, date_rules.every_day(), time_rules.market_open())
    schedule_function(record_vars, date_rules.every_day(), time_rules.market_close())
    
def rebalance(context, data):
    order_target_percent(context.amzn, FRACTION)
    order_target_percent(context.ibm, -1*FRACTION)
    
def record_vars(context, data):
    record(amzn_close=data.current(context.amzn, 'close'))
    record(ibm_close=data.current(context.ibm, 'close'))
    record(Leverage=context.account.leverage)
    record(Exposure=context.account.net_leverage)