from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from textblob import TextBlob
import json
def home(request):
    return HttpResponse("Hello, Django!.I am setting up..for apis")
reviews = []

@csrf_exempt
def post_review(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            review_text = data.get('review', '')
            if not review_text:
                return JsonResponse({'error': 'Review text is required'}, status=400)
            
            analysis = TextBlob(review_text)
            sentiment_score = analysis.sentiment.polarity
            sentiment_label = 'positive' if sentiment_score > 0 else 'negative' if sentiment_score < 0 else 'neutral'

            reviews.append({'review': review_text, 'sentiment': sentiment_label, 'score': sentiment_score})
            
            return JsonResponse({'review': review_text, 'sentiment': sentiment_label, 'score': sentiment_score}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_analysis(request):
    if request.method == 'GET':
        total_reviews = len(reviews)
        if total_reviews == 0:
            return JsonResponse({'total_reviews': 0, 'average_sentiment': None})
        
        average_score = sum(r['score'] for r in reviews) / total_reviews
        return JsonResponse({'total_reviews': total_reviews, 'average_sentiment': average_score})
    return JsonResponse({'error': 'Invalid request method'}, status=405)