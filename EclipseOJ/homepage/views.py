from django.shortcuts import render, redirect

def main(request):
    if request.user.is_authenticated():
        return redirect('contests_index')
    return render(request, 'homepage/main.html')
