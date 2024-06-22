from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
from bs4 import BeautifulSoup
import pandas as pd
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


@api_view(['POST'])
def analyze_spreadsheet(request):
    file = request.FILES.get('file')
    if not file:
        return Response({'error': 'File is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)
        links = df['URL'].tolist()  # Assuming 'URL' is the column containing links
        return Response({'links': links})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AnalyzeSpreadsheet(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'File is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            results = self.analyze_spreadsheet(file)
            return Response({'results': results})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def analyze_spreadsheet(self, file):
        df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)
        
        results = {}
        for url in df['URL']:
            try:
                broken_links = self.check_broken_links(url)
                results[url] = broken_links
            except requests.exceptions.RequestException:
                results[url] = ['Error fetching links']
        
        return results
    
    def check_broken_links(self, url):
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
        
        return broken_links
