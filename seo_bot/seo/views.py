from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from .analyze_data import categorize_scraped_data



class CheckBrokenLinks(APIView):
    def get(self, request):
        url = request.query_params.get('url')
        if not url:
            return Response({'error': 'URL parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            
            broken_links = []
            for link in links:
                try:
                    res = requests.head(link['href'])
                    if res.status_code != 200:
                        broken_links.append(link['href'])
                except requests.exceptions.RequestException:
                    broken_links.append(link['href'])
            
            return Response({'broken_links': broken_links})
        
        except requests.exceptions.RequestException as e:
            # Log the exception for debugging purposes
            print(f"RequestException occurred: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            # Log the exception for debugging purposes
            print(f"Unexpected error occurred: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
def analyze_scraped_data(request):
    if request.method == 'POST':
        data = request.POST.getlist('scraped_data[]', [])
        if not data:
            return JsonResponse({'error': 'No data provided'}, status=400)
        
        categorized_data = categorize_scraped_data(data)
        return JsonResponse(categorized_data)
    else:
        return JsonResponse({'error': 'POST method required'}, status=405)


