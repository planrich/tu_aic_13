def get_raw_answer(request):
    raw_answer = request.get_json(force=True,silent=True)
    if not raw_answer or not 'answer' in raw_answer or not 'user' in raw_answer:
        return None
    raw_answer['answer'] = raw_answer['answer'].lower()
    if not raw_answer['answer'] in ['positive', 'negative', 'neutral']:
        return None
    return raw_answer

def humanize_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"

def rate_score(score):
    if score > 9:
        return 'Very good'
    elif score > 6:
        return 'Good'
    elif score > 4:
        return 'Neutral'
    elif score > 1:
        return 'bad'
    else:
        return 'Very bad'