from django.urls import get_resolver
from django.http import HttpResponse
from django.shortcuts import render


def list_urls(request):
    url_patterns = get_resolver().url_patterns  # Fetches the main URL patterns
    urls = []

    def fetch_urls(patterns, prefix=""):
        for pattern in patterns:
            if hasattr(pattern, "url_patterns"):  # If it's an included URLconf
                fetch_urls(pattern.url_patterns, prefix + pattern.pattern.regex.pattern)
            else:
                urls.append(
                    prefix + pattern.pattern.regex.pattern
                )  # Add pattern to the list

    fetch_urls(url_patterns)  # Populate the list of URLs
    return render(request, "home.html", {"urls": urls})
