from django.shortcuts import render
from InputOutputFiles import Speech_to_Text as listen

def Confluence(request):
    return render(request, 'Confluence/Confluence.html')

def listenConfluenceQuery(request):
    query = listen.listenInput()
    return render(request, 'Confluence/Confluence.html', {'query':query})