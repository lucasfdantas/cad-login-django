from django.shortcuts import render, redirect, get_object_or_404 #Importado obj_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from login.utils import verificar_grupo
from django.contrib.auth.models import Group
from django.contrib.auth.models import User as Usuario
from django.db import transaction #importado transaction do django.bd
from .models import Pedido, ItemPedido #CRIADO NO MODELS PARA SALVAR NO BD
from django.contrib.auth.views import redirect_to_login  # Importação importante para o login
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

# def loja_carrinho(request):
    
#     if request.method == 'POST':
#         produto_id = request.POST.get('produto_id')
#         nome = request.POST.get('nome_produto')
#         preco = request.POST.get('preco_produto')
#         quantidade = request.POST.get('quantidade')
#         print(nome,quantidade, preco)
#         if 'carrinho' not in request.session:
#             request.session['carrinho'] = {}
#         carrinho = request.session['carrinho']
#         #Cria uma chave com o ID do produto
#         carrinho[produto_id] ={
#             'id': produto_id,
#             'nome': nome,
#             'preco': preco,
#             'qtd': quantidade
#             }
#         request.session.modified = True
#         print(carrinho)
#         return redirect('loja_carrinho')
#     return render(request, 'carrinho/loja.html')


# #Lista de Carrinho e calculo de total
# def lista_carrinho(request):
#     compras = request.session.get('carrinho')
#     print(compras)
#     if request.method == 'POST':
#        item_id = request.POST.get('item_id')
#        acao = request.POST.get('acao')
#        print(compras.values(),item_id,acao)
#        if item_id in compras:
#            if acao == 'mais_item':
#                compras[item_id]['qtd'] = int(compras[item_id]['qtd']) + 1
#            elif acao == 'menos_item':
#                 compras[item_id]['qtd'] = int(compras[item_id]['qtd'])  - 1
#                 if compras[item_id]['qtd'] <= 0:
#                     del compras[item_id]
#             request.session['carrinho'] = compras
#             request.session.modified = True
#     if not compras:
#         return redirect('loja_carrinho')   
#    #Parte para calculo pegando carrinho do cliente e somando os produtos
   
#     cart = request.session.get('carrinho', {})
#     total = 0    
#     for i in cart.values():
#         subtotal = float(i['preco']) * float(i['qtd'])
#         total += subtotal    
#     request.session['total_carrinho'] = total
#     request.session.modified = True

#     contexto = {
#         'carrinho':request.session.get('carrinho'),
#         'total' : total
#         }
#     return render(request, 'carrinho/lista_carrinho.html',contexto)


# def view_checkout(request):
#     #O usuario vindo via Get tem que ter carrinho se não retorna para loja
#     carrinho = request.session.get('carrinho')

#     if not carrinho:
#         return redirect('loja_carrinho')
#     total = request.session.get('total_carrinho')
#     if not request.user.is_authenticated:
#         return redirect('login')
#     if request.method == 'POST':
#         #Principio A do ACID, Atomicidade para o banco de dados. 
#         with transaction.atomic():
#             #
#             pedido = Pedido.objects.create(
#                 usuario=request.user if request.user.is_authenticated else None,
#                 total=total
#             )
#             print('Pedido' , pedido)
#             # Cria cada item associado ao pedido fazendo associcação
#             for item in carrinho.values():
#                 ItemPedido.objects.create(
#                     pedido=pedido,
#                     id_produto = item['id'],
#                     nome_produto=item['nome'],
#                     preco = item['preco'],
#                     quantidade=item['qtd']                    
#                 )
#             #Limpa o carrinho da sessão após colocar os itens no pedido
#             del request.session['carrinho']
#             request.session.modified = True
            
#             #Redirect para tela de confirmação
#         return redirect('sucesso_pedido', pedido_id=pedido.id)



#     contexto = {
#         'carrinho': carrinho,
#         'total_carrinho': total}
#     return render(request,'carrinho/checkout.html',contexto)

# def sucesso_pedido(request,pedido_id):
#     pedido = get_object_or_404(Pedido,id = pedido_id)
#     return render(request, 'carrinho/sucesso.html', {'pedido':pedido})



def loja_carrinho(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        nome = request.POST.get('nome_produto')
        preco = request.POST.get('preco_produto')
        quantidade_vinda = request.POST.get('quantidade', 1)

        # Se o formulário enviar dados vazios (None ou string vazia), ignora
        if not produto_id or not preco or produto_id == 'None':
            return redirect('loja_carrinho')

        # Garante que os números sejam tratados corretamente
        quantidade_vinda = int(quantidade_vinda)
        
        
        # Verifica se existe o carrinho na sessão
        if 'carrinho' not in request.session:
            request.session['carrinho'] = {}
        carrinho = request.session['carrinho']
        
        id_str = str(produto_id)
        
        #SE id_str estiver em carrinho da sessão faz o calculo aumentando, atribuição em quantidade é feita
        # Tanto por clique em add ao carrinho quanto pela a quantidade adicionada pelo usuário
        if id_str in carrinho:
            carrinho[id_str]['qtd'] = int(carrinho[id_str]['qtd']) + quantidade_vinda
            
        #Se não existe o produto é adicionado.
        else:
            carrinho[id_str] = {
                'id': id_str,
                'nome': nome,
                'preco': preco,
                'qtd': quantidade_vinda
            }
        #Salva na sessão o carrinho e o modified = True confirma a persistencia do dado e redireciona para a loja novamente.    
        request.session['carrinho'] = carrinho
        request.session.modified = True
        return redirect('loja_carrinho')
        
    return render(request, 'carrinho/loja.html')


def lista_carrinho(request):
    
    # pega na sessão o carrinho
    compras = request.session.get('carrinho', {})
    
    #Remove qualquer item None que tenha ficado salvo na sessão antes
    if None in compras:
        del compras[None]
    if 'None' in compras:
        del compras['None']
    #Caso compras (carrinho) esteja vazio redireiciona para loja novamente
    if not compras:
        return redirect('loja_carrinho')   

    if request.method == 'POST':
        
        item_id = request.POST.get('item_id')
        acao = request.POST.get('acao')
        
        if item_id in compras:
            if acao == 'mais_item':
                compras[item_id]['qtd'] = int(compras[item_id]['qtd']) + 1
            elif acao == 'menos_item':
                compras[item_id]['qtd'] = int(compras[item_id]['qtd']) - 1
                if compras[item_id]['qtd'] <= 0:
                    del compras[item_id]
                    
        request.session['carrinho'] = compras
        request.session.modified = True
        return redirect('lista_carrinho')
   
    # Parte para cálculo pegando carrinho do cliente e somando os produtos
    total = 0    
    for i in compras.values():
        # DEFESA 3: Se por algum motivo o preço ou a quantidade forem nulos, pula o item para não dar erro
        if i['preco'] is None or i['qtd'] is None:
            continue
        subtotal = float(i['preco']) * float(i['qtd'])
        total += subtotal    
        
    request.session['total_carrinho'] = total
    request.session.modified = True

    contexto = {
        'carrinho': compras,
        'total': total
    }
    return render(request, 'carrinho/lista_carrinho.html', contexto)

def view_checkout(request):
    carrinho = request.session.get('carrinho')

    if not carrinho:
        return redirect('loja_carrinho')
        
    total = request.session.get('total_carrinho')
    
    if not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path(), login_url='login')
        
    if request.method == 'POST':
        with transaction.atomic():
            # Cria o pedido principal
            pedido = Pedido.objects.create(
                # Como seu modelo aceita CharField para usuário, salvamos o username ou email dele
                usuario=request.user.username, 
                total=total
            )
            
            # Cria cada item associado ao pedido
            for item in carrinho.values():
                # CORREÇÃO: Usando exatamente os nomes dos campos do seu Model (nome, preco, quantidade)
                ItemPedido.objects.create(
                    pedido=pedido,
                    nome=item['nome'],         # Ajustado de 'nome_produto' para 'nome'
                    preco=item['preco'],       # Mantido 'preco'
                    quantidade=item['qtd']     # Ajustado de 'item['qtd']' para o campo 'quantidade'
                )
            
            # Limpa o carrinho da sessão após colocar os itens no pedido
            del request.session['carrinho']
            if 'total_carrinho' in request.session:
                del request.session['total_carrinho']
            request.session.modified = True
            
        return redirect('sucesso_pedido', pedido_id=pedido.id)

    contexto = {
        'carrinho': carrinho,
        'total_carrinho': total
    }
    return render(request, 'carrinho/checkout.html', contexto)


def sucesso_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'carrinho/sucesso.html', {'pedido': pedido})