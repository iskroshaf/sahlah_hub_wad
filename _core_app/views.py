from django.shortcuts import render

def home_view (request):
    title = 'Home'
    theme = 'customer_theme'
    context = {'title': title,'theme': theme}
    return render(request, '_core_app/pages/home.html', context)
    
def about_view (request):
    title = 'About'
    theme = 'customer_theme'
    context = {'title': title,'theme': theme}
    return render(request, '_core_app/pages/about.html', context)
    
def contact_view (request):
    title = 'Contact'
    theme = 'customer_theme'
    context = {'title': title,'theme': theme}
    return render(request, '_core_app/pages/contact.html', context)
