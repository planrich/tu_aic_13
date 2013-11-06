def get_raw_answer(request):
    json = request.get_json(force=True,silent=True)
    if not json or not 'answer' in json or not 'user' in json:
        return None
    if not json['answer'] in ['positive', 'negative', 'neutral']:
        return None
    return json

def map_rating(answer):
    if answer.lower() == "positive":
        return 10
    elif answer.lower() == "neutral":
        return 5
    elif answer.lower() == "negative":
        return 0
    return None