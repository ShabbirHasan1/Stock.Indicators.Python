import pytest
from stock_indicators import indicators

class TestDoubleEMA:
    def test_standard(self, quotes):
        results = indicators.get_double_ema(quotes, 20)
        
        assert 502 == len(results)
        assert 464 == len(list(filter(lambda x: x.dema is not None, results)))
        
        r = results[51]
        assert 226.0011 == round(float(r.dema), 4)
        
        r = results[249]
        assert 258.4452 == round(float(r.dema), 4)
        
        r = results[501]
        assert 241.1677 == round(float(r.dema), 4)
        
    def test_bad_data(self, bad_quotes):
        r = indicators.get_double_ema(bad_quotes, 15)
        assert 502 == len(r)
        
    def test_removed(self, quotes):
        results = indicators.get_double_ema(quotes, 20).remove_warmup_periods()
        
        assert 502 - (2 * 20 + 100) == len(results)
        
        last = results.pop()
        assert 241.1677 == round(float(last.dema), 4)
        
    def test_exceptions(self, quotes, longish_quotes):
        from System import ArgumentOutOfRangeException
        with pytest.raises(ArgumentOutOfRangeException):
            indicators.get_double_ema(quotes, 0)
        
        from Skender.Stock.Indicators import BadQuotesException
        with pytest.raises(BadQuotesException):
            indicators.get_double_ema(quotes[:159], 30)

        with pytest.raises(BadQuotesException):
            indicators.get_double_ema(longish_quotes[:749], 250)
