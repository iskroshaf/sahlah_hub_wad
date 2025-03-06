from django.shortcuts import render

def home_view (request):
    title = 'Home'
    context = {'title': title}
    return render(request, '_core_app/pages/home.html', context)
    
def about_view (request):
    title = 'About'
    context = {'title': title}
    return render(request, '_core_app/pages/about.html', context)
    
def contact_view (request):
    title = 'Contact'
    context = {'title': title}
    return render(request, '_core_app/pages/contact.html', context)
