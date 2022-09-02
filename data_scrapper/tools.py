from datetime import timedelta

# returns the next date in the interval of days displayed by the lotto webpage
def get_limit(today):
    return today - timedelta(days=270)