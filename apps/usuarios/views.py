import time

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.models import User
from receitas.models import Receita


def cadastro(request):
    '''Cadastra uma nova pessoa no sistema'''
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if campo_vazio(nome):
            messages.error(request, 'O campo "nome" não pode ficar em branco')
            return redirect('cadastro')

        if campo_vazio(email):
            messages.error(request, 'O campo "email" não pode ficar em branco.')
            return redirect('cadastro')

        if senhas_diferentes(senha, senha2):
            messages.error(request, 'As senhas não são iguais!')
            return redirect('cadastro')

        if usuario_cadastrado(email, nome):
            messages.error(request, 'Usuário já cadastrado.')
            return redirect('cadastro')

        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso.')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    '''Realiza o login do usuário no sistema'''
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']

        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'Os campos email e senha não podem ficar vazios')
            return redirect('login')

        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(username=nome, password=senha)

            if user is not None:
                auth.login(request, user)
                print('Login realizado com sucesso')
                messages.success(request, 'Login realizado com sucesso.')
                return redirect('dashboard')
            else:
                print('Usuário não cadastrado')
                messages.error(request, 'Login ou senha não está correto. Tente novamente')
                return redirect('login')

    return render(request, 'usuarios/login.html')

def logout(request):
    '''Realiza a SAIDA do usuário do sistema'''
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    '''Exibe as receitas exclusivas do usuário'''
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)

        dados = {
            'receitas': receitas
        }

        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')

def campo_vazio(campo):
    '''Retira os campos vazios'''
    return not campo.strip()

def senhas_diferentes(senha, senha2):
    '''Validação de senhas do cadastro'''
    return senha != senha2

def usuario_cadastrado(email, nome):
    '''Valida se o usuário já está cadastrado no sistema'''
    return User.objects.filter(email=email).exists() or User.objects.filter(username=nome).exists()
