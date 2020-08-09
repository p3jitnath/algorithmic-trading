def initialize(context):
    context.spy = sid(8554)
    schedule_function(rebalance, date_rules.every_day(), time_rules.market_open())
    
    
def rebalance(context, data):
    order_target_percent(context.spy, 1)