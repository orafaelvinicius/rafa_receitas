from django.shortcuts import render

def index(request):
    receitas = {
        1:'Lasanha',
        2:'Suco de limão',
        3:'Sorvete',
        4:'Panqueca de banana'
    }

    dados = {
        'nome_das_receitas': receitas
    }

    return render(request, 'index.html', dados)

def receita(request):
    return render(request, 'receita.html')
