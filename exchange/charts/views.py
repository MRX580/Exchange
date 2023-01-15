from django.shortcuts import render


def get_chart(request):
    return render(request, 'charts/chart.html')
