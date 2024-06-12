"""Views.py file"""
import os
import csv
from datetime import datetime, timedelta

from allauth.account.views import LoginView, SignupView, LogoutView

from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q

from rest_framework.response import Response
from rest_framework import viewsets

from .forms import CompanySearchForm
from .models import Company, UserActivity

from .serializers import RecordCountSerializer




class CustomLoginView(LoginView):
    """
    Custom login view extending Django's built-in LoginView.

    This view class extends Django's LoginView to customize the behavior
    or appearance of the login functionality in the application.

    Attributes:
        template_name (str): The name of the template used to render the login page.
    """
    template_name = 'count_query/login.html'

class CustomSignupView(SignupView):
    """
    Custom Signup view extending Django's built-in SignupView.

    This view class extends Django's SignupView to customize the behavior
    or appearance of the signup functionality in the application.

    Attributes:
        template_name (str): The name of the template used to render the signup page.
    """
    template_name = 'count_query/signup.html'


class CustomLogoutView(LogoutView):
    """
    Custom logout view extending Django's built-in LogoutView.

    This view class extends Django's LogoutView to customize the behavior
    or appearance of the LogoutView functionality in the application.

    Attributes:
        template_name (str): The name of the template used to render the logout page.
    """
    template_name = 'count_query/logout.html'

def query_builder(request):
    """
    View function to build and execute queries based on user input.

    This function handles the logic for building and executing queries based on the user's input
    through the CompanySearchForm. It filters the Company objects based on the provided parameters
    (company_name, industry, city, state, country) and displays the results along with a message indicating
    the number of records found.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response containing the rendered HTML template with the query form,
        search results, and message.

    """
    form = CompanySearchForm(request.POST or None)
    results = None
    message = None
    

    if request.method == 'POST':
        if form.is_valid():
            company_name = form.cleaned_data.get('company_name')
            industry = form.cleaned_data.get('industry')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            country = form.cleaned_data.get('country')
            
            
            results = Company.objects.all()  # Replace YourModel with your actual model
            filters = Q()
            if company_name:
                filters &= Q(company_name__icontains=company_name)
            if industry:
                filters &= Q(industry__icontains=industry)
            if city:
                filters &= Q(city__icontains=city)
            if state:
                filters &= Q(state__icontains=state)
            if country:
                filters &= Q(country__icontains=country)
        
        # Apply filters to query
            results = results.filter(filters)
            count = results.count()
            if count > 0:
                message = f"{count} records found."
            else:
                message = "No records found."
            
        elif 'reset' in request.POST:  # Check if reset button is pressed
            form = CompanySearchForm()  # Reset the form
            message = None  # Reset the message
            results = None  # Reset the results
    if message is None:
        return render(request, 'count_query/query_builder.html', {'form': form})
    else:
        return render(request, 'count_query/query_builder.html', {'form': form, 'message': message, 'results': results})

class UploadDataView(View):
    """
    View class for uploading data via CSV file.

    This view class provides functionality to upload CSV data files. Upon receiving a POST request,
    the uploaded file is processed, and its data is saved to the database in chunks. The class also
    provides a GET method to render the upload form.

    Attributes:
        template_name (str): The name of the HTML template used for rendering the upload form.

    Methods:
        get(self, request): Renders the upload form HTML template.
        post(self, request): Handles the file upload POST request, processes the uploaded CSV file,
            and saves its data to the database in chunks.
        save_chunk_data(self, chunk_data): Saves a chunk of data to the database.
        chunk(self, iterable, chunk_size): Generator function to yield successive chunks of data from an iterable.
    """
    template_name = 'count_query/upload_data.html'

    def get(self, request):
        """
        Render the upload form HTML template.

        Args:
            request (HttpRequest): The HTTP GET request object.

        Returns:
            HttpResponse: A response containing the rendered HTML template for the upload form.
        """
        return render(request, self.template_name)

    def post(self, request):
        """
        Handle the file upload POST request, process the uploaded CSV file,
        and save its data to the database in chunks.

        Args:
            request (HttpRequest): The HTTP POST request object.

        Returns:
            HttpResponse: A redirect response indicating the result of the file upload.
        """
        if 'file' not in request.FILES:
            json_response = {'status': 'error', 'message': 'No file uploaded'}
            return JsonResponse(json_response, status=400)

        file = request.FILES['file']
        file_name = file.name

        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, file_name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Process the uploaded CSV file and fill the database in chunks
        with open(file_path, 'r', encoding='latin-1') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            chunk_size = 1000
            chunk_data = []
            for row in csv_reader:
                # Process each row and prepare Company object
                # You need to handle any field conversion or formatting here
                if '+' in row['size range']:
                    size_range = int(row['size range'].replace('+', ''))
                    size_min = size_range
                    size_max = None
                elif '-' in row['size range']:
                    size_min, size_max = map(int, row['size range'].split('-'))
                locality = row['locality']
                if locality:
                    city=row['locality'].split(',')[0].replace("(", "").replace(")", "").replace("'", "").replace(" ", "")
                    print(city)
                    state=row['locality'].split(',')[1].replace("(", "").replace(")", "").replace("'", "").replace(" ", "")
                year_founded = int(float(row['year founded'])) if row['year founded'] else None
                company = Company(
                    name=row['name'],
                    domain=row['domain'],
                    year_founded=year_founded,
                    industry=row['industry'],
                    size_min=size_min,
                    size_max=size_max,
                    city=city,
                    state=state,
                    country=row['country'],
                    linkedin_url=row['linkedin url'],
                    current_employee_estimate=row['current employee estimate'],
                    total_employee_estimate=row['total employee estimate']
                )
                chunk_data.append(company)

                # If the chunk size is reached, save the data to the database
                if len(chunk_data) == chunk_size:
                    self.save_chunk_data(chunk_data)
                    chunk_data = []

            # Save any remaining data
            if chunk_data:
                self.save_chunk_data(chunk_data)

        # Respond with JSON indicating successful upload
        json_response = {'status': 'ok', 'message': 'File uploaded successfully'}
        success_message = json_response['message']
        redirect_url = request.path + '?message=' + success_message.replace(' ', '+')
        return redirect(redirect_url)

    def save_chunk_data(self, chunk_data):
        """
        Save a chunk of data to the database.

        This method should handle saving a chunk of data to the database, typically using bulk_create or a similar method.

        Args:
            chunk_data (list): The list of Company objects representing the chunk of data to be saved.

        Returns:
            None
        """
        try:
            Company.objects.bulk_create(chunk_data)
        except Exception as e:
            print(f"Error saving chunk data: {e}")

    def chunk(self, iterable, chunk_size):
        """
        Generator function to yield successive chunks of data from an iterable.

        Args:
            iterable (iterable): The iterable object to be chunked.
            chunk_size (int): The size of each chunk.

        Yields:
            list: Successive chunks of data from the iterable.
        """
        for i in range(0, len(iterable), chunk_size):
            yield iterable[i:i + chunk_size]

class RecordCountViewSet(viewsets.ViewSet):
    """
    ViewSet to retrieve the count of records from the Company model.

    This ViewSet provides an endpoint to retrieve the count of records from the Company model.
    The count is serialized using the RecordCountSerializer and returned as a response.

    Attributes:
        queryset (QuerySet): The queryset containing the Company model data.

    Methods:
        list(self, request): Retrieves the count of records from the Company model and returns the count as a serialized response.

    """
    def list(self, request):
        count = Company.objects.count()  # Replace YourModel with your actual model
        serializer = RecordCountSerializer({'count': count})
        return Response(serializer.data)

def active_users(request):
    """
        Retrieve the count of records from the Company model.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A serialized response containing the count of records from the Company model.

        """
    active_users = UserActivity.objects.filter(last_login__gte=datetime.now() - timedelta(days=7))
    return render(request, 'count_query/users.html', {'active_users': active_users})
