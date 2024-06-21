from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from bs4 import BeautifulSoup
import pandas as pd

class CheckBrokenLinks(APIView):
    def get(self, request):
        url = request.query_params.get('url')
        if not url:
            return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        broken_links = self.check_broken_links(url)
        return Response({'broken_links': broken_links})

    def check_broken_links(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        
        broken_links = []
        for link in links:
            try:
                res = requests.head(link['href'])
                if res.status_code != 200:
                    broken_links.append(link['href'])
            except:
                broken_links.append(link['href'])
        
        return broken_links

class AnalyzeSpreadsheet(APIView):
    def post(self, request):
        file = request.FILES['file']
        df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)
        
        results = {}
        for url in df['URL']:
            broken_links = self.check_broken_links(url)
            results[url] = broken_links
        
        return Response({'results': results})

    def check_broken_links(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        
        broken_links = []
        for link in links:
            try:
                res = requests.head(link['href'])
                if res.status_code != 200:
                    broken_links.append(link['href'])
            except:
                broken_links.append(link['href'])
        
        return broken_links
