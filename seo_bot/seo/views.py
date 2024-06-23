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
            
def analyze_scraped_data(request):
    if request.method == 'POST':
        data = request.POST.getlist('scraped_data[]', [])
        if not data:
            return JsonResponse({'error': 'No data provided'}, status=400)
        
        categorized_data = categorize_scraped_data(data)
        return JsonResponse(categorized_data)
    else:
        return JsonResponse({'error': 'POST method required'}, status=405)


""" @api_view(['POST'])
def analyze_spreadsheet(request):
    file = request.FILES.get('file')
    if not file:
        return Response({'error': 'File is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        import openpyxl
        print("openpyxl is installed.")
    except ImportError as e:
        print(f"openpyxl import error: {str(e)}")
        return Response({'error': "Missing optional dependency 'openpyxl'. Use pip or conda to install openpyxl."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        if file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            df = pd.read_csv(file)
        
        print("File read successfully.")
        
        if 'URL' not in df.columns:
            print(f"Columns present in the file: {df.columns}")
            return Response({'error': "'URL' column not found in the file. Columns present: " + ", ".join(df.columns)}, status=status.HTTP_400_BAD_REQUEST)
        
        links = df['URL'].dropna().tolist()
        print(f"Extracted {len(links)} links.")
        
        return Response({'links': links})
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AnalyzeSpreadsheet(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'File is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        print(f"Received file: {file.name}")
        try:
            results = self.analyze_spreadsheet(file)
            return Response({'results': results})
        except Exception as e:
            print(f"Error analyzing spreadsheet: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def analyze_spreadsheet(self, file):
        try:
            import openpyxl
            print("openpyxl is installed in AnalyzeSpreadsheet.")
        except ImportError as e:
            print(f"openpyxl import error in AnalyzeSpreadsheet: {str(e)}")
            raise ImportError("Missing optional dependency 'openpyxl'. Use pip or conda to install openpyxl.")

        try:
            if file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
            else:
                df = pd.read_csv(file)
            print("File read successfully in AnalyzeSpreadsheet.")
            
            if 'URL' not in df.columns:
                print(f"Columns present in the file: {df.columns}")
                raise ValueError("'URL' column not found in the file.")
        except Exception as e:
            print(f"Error reading file in AnalyzeSpreadsheet: {str(e)}")
            raise

        links = df['URL'].dropna().tolist()  # Drop any NaN values and convert to list
        print(f"Extracted {len(links)} links in AnalyzeSpreadsheet.")
        
        return links """