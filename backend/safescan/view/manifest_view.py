import json
from django.conf import settings
from django.shortcuts import render

def get_vite_manifest():
    try:
        with open(settings.VITE_MANIFEST_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def index(request):
    manifest = get_vite_manifest()
    return render(request, 'safescan/index.html', {'manifest': manifest})