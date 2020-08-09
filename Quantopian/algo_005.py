# Sentiment Analysis

from quantopian.algorithm import attach_pipeline, pipeline_output

from quantopian.pipeline import Pipeline

from quantopian.pipeline.factors import AverageDollarVolume

# from quantopian.pipeline.data.accern import alphaone_free

from quantopian.pipeline.data.sentdex import sentiment_free as sentdex
from quantopian.pipeline.factors import CustomFactor

import numpy as np

class AvgSentiment(CustomFactor):
    
    def compute(self, today, assets, out, impact):
        np.mean(impact, axis=0, out=out)

def make_pipeline():
    
    dollar_volume = AverageDollarVolume(window_length=20)
    is_liquid = dollar_volume.top(1000)
    
    # impact = alphaone_free.impact_score.latest
    # sentiment = alphaone_free.article.sentiment.latest
    # return Pipeline(column={'impact': impact, 'sentiment':sentiment}, screen=is_liquid)
    
    avg_sentiment = AvgSentiment(inputs=[sentdex.sentiment_signal], window_length=10)
   
    return Pipeline(columns={
        'sentiment': avg_sentiment       
    }, screen=is_liquid)


def initialize(context):
    
    schedule_function(rebalance, date_rules.every_day())
    attach_pipeline(make_pipeline(), 'pipeline')
    
    
def before_trading_start(context, data):
    
    port = pipeline_output('pipeline')
    context.longs = port[port['sentiment'] > 0].index.tolist()
    context.shorts = port[port['sentiment'] < 0].index.tolist()
    context.long_weight, context.short_weight = compute_weights(context)
    
    
def compute_weights(context):
    
    long_weight = 0.5 / len(context.longs) if len(context.longs) != 0 else 0
    short_weight = 0.5 / len(context.shorts) if len(context.shorts) != 0 else 0

    return (long_weight, short_weight)
    
    
def rebalance(context, data):
    for security in context.portfolio.positions:
        if security not in context.longs and security not in context.shorts and data.can_trade(security):
            order_target_percent(security, 0)
    
    for security in context.longs:
        if data.can_trade(security):
            order_target_percent(security, context.long_weight)

    for security in context.shorts:
        if data.can_trade(security):
            order_target_percent(security, context.short_weight)