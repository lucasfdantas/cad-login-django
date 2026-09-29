from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from login.utils import verificar_grupo
from django.contrib.auth.models import Group
from django.contrib.auth.models import User as Usuario

@login_required
def painel_principal(request):
    usuarios = {
            'usuarios': Usuario.objects.all()
    }
    return render(request, 'painel/home.html', usuarios)

# Create your views here.
@login_required
def view_administrador(request):
    if not verificar_grupo(request.user, 'administradores'):
        raise PermissionDenied # Retorna erro 403 nativo do Django
    if request.method == 'POST':
        usuarios = Usuario.objects.all()
        
        for usuario in usuarios:
            # Captura o ID do grupo selecionado no HTML
            novo_grupo_id = request.POST.get(f'grupo_usuario_{usuario.id}')
            
            # Se um ID foi enviado (o campo não ficou no "-- Selecione --")
            if novo_grupo_id: 
                try:
                    # Busca o grupo pelo ID numérico
                    grupo = Group.objects.get(id=novo_grupo_id)
                    
                    # Limpa o grupo atual e associa o novo grupo
                    usuario.groups.clear()
                    usuario.groups.add(grupo)
                except Group.DoesNotExist:
                    # Prevenção caso um ID inválido seja enviado de alguma forma
                    pass
                    
        return redirect('view_administrador')

    # Para requisições GET
    
    
    

    usuarios = {
            'usuarios': Usuario.objects.all(),
            'grupos': Group.objects.all()
        }
    return render(request, 'painel/administrador.html', usuarios )

@login_required
def view_diretoria(request):
    if not verificar_grupo(request.user, 'diretoria'):
        raise PermissionDenied  
    return render(request, 'painel/diretoria.html')

@login_required
def view_gerencia_geral(request):
    if not verificar_grupo(request.user, 'gerencia_geral'):
        raise PermissionDenied
    return render(request, 'painel/gerencia_geral.html')

@login_required
def view_gerencia(request):
    if not verificar_grupo(request.user, 'gerencia'):
        raise PermissionDenied
    return render(request, 'painel/gerencia.html')

@login_required
def view_supervisao(request):
    if not verificar_grupo(request.user, 'supervisao'):
        raise PermissionDenied
    return render(request, 'painel/supervisao.html')

@login_required
def view_atendente(request):
    if not verificar_grupo(request.user, 'atendente'):
        raise PermissionDenied
    return render(request, 'painel/atendente.html')

@login_required
def view_caixa(request):
    if not verificar_grupo(request.user, 'caixa'):
        raise PermissionDenied
    return render(request, 'painel/caixa.html')

@login_required
def view_checkout(request):
    if not verificar_grupo(request.user, 'cliente'):
        raise PermissionDenied
    return render(request,'carrinho/checkout.html')

def loja_carrinho(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        nome = request.POST.get('nome_produto')
        preco = request.POST.get('preco_produto')
        quantidade = request.POST.get('quantidade')
        
        if 'carrinho' not in request.session:
            request.session['carrinho'] = {}
            
        carrinho = request.session['carrinho']
        
        # O SEGREDOS ESTÁ AQUI: Cria uma chave com o ID do produto
        carrinho[produto_id] = {
            'id': produto_id,
            'nome': nome,
            'preco': preco,
            'qtd': quantidade
        }
        
        request.session.modified = True
        print(request.session.get('carrinho'))
        return redirect('loja_carrinho')
    return render(request, 'carrinho/loja.html')

def lista_carrinho(request):


    contexto = {
        'carrinho':request.session.get('carrinho')
        }
    print(contexto)
    return render(request, 'carrinho/lista_carrinho.html',contexto)