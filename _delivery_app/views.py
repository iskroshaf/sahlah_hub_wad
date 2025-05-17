from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'nama_app/home.html', {
        'title': 'Halaman Utama Nama App'
    })