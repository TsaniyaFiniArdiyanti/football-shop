from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'app_name': 'Football Shop', 
        'nama': 'Tsaniya',     
        'class': 'PBP E'    }

    return render(request, "main.html", context)