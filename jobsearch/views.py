from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

import json
import requests
import urllib.parse

URL = 'https://api.adzuna.com/v1/api/jobs/'
APP_ID = settings.APP_ID
APP_KEY = settings.APP_KEY
APP_ID_KEY = 'app_id=' + APP_ID + '&app_key=' + APP_KEY

# List of countries
COUNTRIES = ['GB', 'US', 'AT', 'AU', 'BE', 'BR', 'CA', 'CH', 'DE', 'ES', 'FR', 'IN', 'IT', 'MX', 'NL', 'NZ', 'PL', 'RU', 'SG', 'ZA']

# List of orderings
ORDERINGS = ['Default', 'Hybrid', 'Date', 'Salary', 'Relevance']

# Directions of order
DIRECTIONS = ['Up', 'Down']

from .models import User, SavedJob, SavedSearch, Resume


def index(request):
    country = request.GET.get('country', 'gb').lower()
    response = requests.get(URL + country + '/categories?' + APP_ID_KEY).json()
    categories = response.get('results', [])
    
    if country.upper() not in COUNTRIES:
        return JsonResponse({'error': 'Invalid country'})
    
    return render(request, "jobsearch/index.html", {
        'categories': categories,
        'countries': COUNTRIES,
        'selected_country': country.upper(),
        'orderings': ORDERINGS,
        'directions': DIRECTIONS
        })


def get_listings(
    request, type, country, tag, title, location, page, results_per_page, what_and, what_phrase, what_or,
    what_exclude, title_only, distance, location0, location1, location2, location3, location4, location5,
    location6, location7, max_days_old, sort_dir, sort_by, salary_min, salary_max, salary_include_unknown,
    full_time, part_time, contract, permanent, company
):
    is_authenticated = request.user.is_authenticated
    if country.upper() not in COUNTRIES:
        return JsonResponse({'error': 'Invalid country'})
    
    country = country.lower()
    
    response = requests.get(URL + country + '/categories?' + APP_ID_KEY).json()
    categories = response.get('results', [])
    
    url = URL + country + '/search/' + str(page) + '?' + APP_ID_KEY + '&results_per_page=16'
    
    if type == 'all':
        if country == 'gb':
            url += '&what_exclude=Four%20Wheels'
    
    elif type == 'category':
        # Check if the requested category is available
        category_found = False
        if tag:
            for cat in categories:
                if cat.get('tag', '') == tag:
                    category_found = True
                    break

        # If category not found, return empty results
        if not category_found:
            return JsonResponse({'results': []})

        url += '&category=' + tag

    elif type == 'search':
        if title and title != 'n' and title != '':
            url += '&what=' + title
        if location and location != 'n' and location != '':
            url += '&where=' + location

    elif type == 'advanced':
        # Check if the requested category is available
        if tag and tag != 'n' and tag != '':
            for cat in categories:
                if cat.get('tag', '') == tag:
                    url += '&category=' + tag
                    break
        if title and title != 'n' and title != '':
            url += '&what=' + title
        if location and location != 'n' and location != '':
            url += '&where=' + location
        if results_per_page and results_per_page != 'n' and results_per_page != '':
            url += '&results_per_page=' + results_per_page
        if what_and and what_and != 'n' and what_and != '':
            url += '&what_and=' + what_and
        if what_phrase and what_phrase != 'n' and what_phrase != '':
            url += '&what_phrase=' + what_phrase
        if what_or and what_or != 'n' and what_or != '':
            url += '&what_or=' + what_or
        if what_exclude and what_exclude != 'n' and what_exclude != '':
            url += '&what_exclude=' + what_exclude
        if title_only and title_only != 'n' and title_only != '':
            url += '&title_only=' + title_only
        if distance and distance != 'n' and distance != '':
            url += '&distance=' + distance
        if location0 and location0 != 'n' and location0 != '':
            url += '&location0=' + location0
        if location1 and location1 != 'n' and location1 != '':
            url += '&location1=' + location1
        if location2 and location2 != 'n' and location2 != '':
            url += '&location2=' + location2
        if location3 and location3 != 'n' and location3 != '':
            url += '&location3=' + location3
        if location4 and location4 != 'n' and location4 != '':
            url += '&location4=' + location4
        if location5 and location5 != 'n' and location5 != '':
            url += '&location5=' + location5
        if location6 and location6 != 'n' and location6 != '':
            url += '&location6=' + location6
        if location7 and location7 != 'n' and location7 != '':
            url += '&location7=' + location7
        if max_days_old and max_days_old != 'n' and max_days_old != '':
            url += '&max_days_old=' + max_days_old
        if sort_dir and sort_dir in DIRECTIONS:
            url += '&sort_dir=' + sort_dir.lower()
        if sort_by and sort_dir in ORDERINGS:
            url += '&sort_by=' + sort_by.lower()
        if salary_min and salary_min != 'n' and salary_min != '':
            url += '&salary_min=' + salary_min
        if salary_max and salary_max != 'n' and salary_max != '':
            url += '&salary_max=' + salary_max
        if salary_include_unknown and salary_include_unknown == '1':
            url += '&salary_max=' + '1'
        if full_time and full_time == '1':
            url += '&full_time=' + '1'
        if part_time and part_time == '1':
            url += '&part_time=' + '1'
        if contract and contract == '1':
            url += '&contract=' + '1'
        if permanent and permanent == '1':
            url += '&permanent=' + '1'
        if company and company != 'n' and company != '':
            url += '&company=' + company

    elif type == 'saved':
        if is_authenticated:
            profile_user = get_object_or_404(User, username=request.user)
            results = SavedJob.objects.filter(job_seeker=profile_user).order_by('-saved_date')
            # Convert the listings to a list of dictionaries
            results = [{
                'id': result.listing_id,
                'category': urllib.parse.unquote(result.category),
                'title': urllib.parse.unquote(result.title),
                'salary_max': result.salary_max,
                'company': result.company,
                'location': result.location,
                'description': urllib.parse.unquote(result.description),
                'redirect_url': result.redirect_url
                } for result in results]
    
            # Iterate over the results and check if each job listing is saved by the user
            saved_job_listings = list(SavedJob.objects.filter(job_seeker=profile_user).values_list('listing_id', flat=True))
        
            return JsonResponse({
                'count': len(results),
                'num_pages': len(results) // 16 + 1,
                'results': results,
                'is_authenticated': is_authenticated,
                'saved_job_listings': saved_job_listings
            })
        else:
            return render(request, "jobsearch/login.html")

    else:
        return JsonResponse({'error': 'Invalid job listing type'})

    try:
        response = requests.get(url).json()
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Error on the API provider side'})
    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred'})
    
    jobs_count = response.get('count')
    results = response.get('results', [])
    total_pages = jobs_count // 16 + 1
    
    # Iterate over the results and check if each job listing is saved by the user
    if request.user.is_authenticated:
        saved_job_listings = list(SavedJob.objects.filter(job_seeker=request.user).values_list('listing_id', flat=True))
    else:
        saved_job_listings = []
    
    return JsonResponse({
        'count': jobs_count,
        'num_pages': total_pages,
        'results': results,
        'is_authenticated': is_authenticated,
        'saved_job_listings': saved_job_listings
        })


def save_listing(request, listing_id, category, title, salary_max, company, location, description):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Check if the job listing is already saved by the user
        try:
            saved_job = SavedJob.objects.get(job_seeker=request.user, listing_id=listing_id)
            # Job listing is saved, delete it to toggle the status
            saved_job.delete()
            return JsonResponse({
                'success': True,
                'message': 'Job listing removed from saved listings',
                'category': 'success',
                'is_saved': False
                })
        except SavedJob.DoesNotExist:
            # Job listing is not saved, create a new saved job
            description = description.replace('garismiring', '/')
            redirect_url = 'https://www.adzuna.co.uk/jobs/details/' + listing_id
            SavedJob.objects.create(job_seeker=request.user, listing_id=listing_id, category=category,
                                    title=title, salary_max=salary_max, company=company, location=location,
                                    description=description, redirect_url=redirect_url)
            return JsonResponse({
                'success': True,
                'message': 'Job listing saved',
                'category': 'success',
                'is_saved': True
                })

    # User is not authenticated, return an error response
    return JsonResponse({
        'success': False,
        'message': 'User is not authenticated',
        'category': 'warning',
        }, status=401)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "jobsearch/login.html", {
                "message": "Invalid username and/or password.",
                'category': 'danger'
            })
    else:
        return render(request, "jobsearch/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "jobsearch/register.html", {
                "message": "Passwords must match.",
                'category': 'danger'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "jobsearch/register.html", {
                "message": "Username already taken.",
                'category': 'warning'
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "jobsearch/register.html")
