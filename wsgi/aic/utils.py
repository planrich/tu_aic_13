def get_raw_answer(request):
    raw_answer = request.get_json(force=True,silent=True)
    if not raw_answer or not 'answer' in raw_answer or not 'user' in raw_answer:
        return None
    raw_answer['answer'] = raw_answer['answer'].lower()
    if not raw_answer['answer'] in ['positive', 'negative', 'neutral']:
        return None
    return raw_answer

def map_rating(answer):
    if answer == "positive":
        return 10
    elif answer == "neutral":
        return 5
    elif answer == "negative":
        return 0
    return None