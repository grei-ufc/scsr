from mygrid.grid import Substation, Feeder, Sector, Switch
from mygrid.grid import Section, LoadNode, Transformer, Conductor
from mygrid.util import R, P
from bs4 import BeautifulSoup as bs
from collections import OrderedDict





def carregar_dados(doc):
   ############################################################################
    '''Carrega o arquivo'''

    cim=bs(open(doc,'r'),'xml')
    Breaker_xml=cim.find_all('Breaker')
    BusBar_xml=cim.find_all('busBarSection')
    Transformadores_xml=cim.find_all('Substation')
    Nos_xml=cim.find_all('EnergyConsumer')
    Condutor_xml=cim.find_all('Conductor')
    Conexao_xml=cim.find_all('ConnectivityNode')

    ###########################################################################
    '''Carrega conexoes em listas'''
    conexao_dados=list()
    for i in Conexao_xml:
        conex=OrderedDict()
        conex['id_conex']=int(str(i.find('mRID').string).rsplit()[0])
        p=list()
        for j in i.find_all('terminal'):
            p.append(int(str(j.find('mRID').string).rsplit()[0]))
        conex['conexoes']=p
        conexao_dados.append(conex)

   ############################################################################
    '''Carrega as chaves em listas'''
    chaves_dados=list()
    for i in Breaker_xml:
        chave_lista=OrderedDict()
        chave_lista['nome']= str(i.find('mRID').string).rsplit()[0]
        chave_lista['estado']=int(str(i.find('normalOpen').string).rsplit()[0])^1

        for j in i.find_all('terminal'):
            p=str(j.find('SequenceNumber').string).rsplit()[0]
            for x in conexao_dados:
                if int(str(j.find('mRID').string).rsplit()[0]) in x['conexoes']:
                    chave_lista['n'+p+'_'+'id']=x['id_conex']
                    break

        chaves_dados.append(chave_lista)
    ############################################################################
    '''Carrega os barramentos em listas'''
    busbar_dados=list()
    for i in BusBar_xml:
        bus=OrderedDict()
        bus['nome']=str(i.find('mRID').string).rsplit()[0]
        bus['fase']=float(str(i.find('phases').string).rsplit()[0])
        bus['r']=float(str(i.find('r').string).rsplit()[0])
        bus['x']=float(str(i.find('x').string).rsplit()[0])
        bus['r0']=float(str(i.find('r0').string).rsplit()[0])
        bus['x0']=float(str(i.find('x0').string).rsplit()[0])

        a=list()
        for j in i.find_all('terminal'):
            for x in conexao_dados:
                if int(str(j.find('mRID').string).rsplit()[0]) in x['conexoes']:
                    a.append(x['id_conex'])
                    break

        bus['ids']=a
        busbar_dados.append(bus)

    ############################################################################
    '''Carrega transformadores em listas'''
    transformadores_dados=list()
    for i in Transformadores_xml:
        trafo=OrderedDict()
        trafo['nome']=str(i.find('mRID').string).rsplit()[0]
        trafo['n_trafo']=float(str(i.find('n_trafo').string).rsplit()[0])
        trafo['tensao_p']=float(str(i.find('tensaop').string).rsplit()[0])
        trafo['tensao_s']=float(str(i.find('tensaos').string).rsplit()[0])
        trafo['potencia']=float(str(i.find('power').string).rsplit()[0])
        trafo['tensao_s']=float(str(i.find('tensaos').string).rsplit()[0])
        trafo['r']=float(str(i.find('r').string).rsplit()[0])
        trafo['x']=float(str(i.find('x').string).rsplit()[0])
        trafo['r0']=float(str(i.find('r0').string).rsplit()[0])
        trafo['x0']=float(str(i.find('x0').string).rsplit()[0] )

        a=list()
        for j in i.find_all('terminal'):
            p=str(j.find('SequenceNumber').string).rsplit()[0]
            for x in conexao_dados:
                if int(str(j.find('mRID').string).rsplit()[0]) in x['conexoes']:
                    trafo['n'+p+'_'+'id']=x['id_conex']
                    break
        transformadores_dados.append(trafo)

    ############################################################################
    '''Carrega nos em listas'''
    nos_dados=list()
    for i in Nos_xml:
        no=OrderedDict()
        no['nome']=str(i.find('mRID').string).rsplit()[0]
        no['p']=float(str(i.find('pFixed').string).rsplit()[0])
        no['q']=float(str(i.find('qFixed').string).rsplit()[0])

        a=list()
        for j in i.find_all('terminal'):
            for x in conexao_dados:
                if int(str(j.find('mRID').string).rsplit()[0]) in x['conexoes']:
                    a.append(x['id_conex'])
                    break
        no['ids']=a
        nos_dados.append(no)

    ############################################################################
    '''Carrega condutores em listas'''
    condutores_dados=list()
    for i in Condutor_xml:
        condutor=OrderedDict()
        condutor['nome']=str(i.find('mRID').string).rsplit()[0]
        condutor['comprimento']=float(str(i.find('length').string).rsplit()[0])
        condutor['r']=float(str(i.find('r').string).rsplit()[0])
        condutor['x']=float(str(i.find('x').string).rsplit()[0])
        condutor['r0']=float(str(i.find('r0').string).rsplit()[0])
        condutor['x0']=float(str(i.find('x0').string).rsplit()[0] )
        condutor['ampacidade']=float(str(i.find('currentLimit').string)\
        .rsplit()[0] )
        a=list()
        for j in i.find_all('terminal'):
            p=str(j.find('SequenceNumber').string).rsplit()[0]
            for x in conexao_dados:
                if int(str(j.find('mRID').string).rsplit()[0]) in x['conexoes']:
                    condutor['n'+p+'_'+'id']=x['id_conex']
                    break
                else:
                    condutor['n'+p+'_'+'id']=None

        condutores_dados.append(condutor)


    dados_rede={}
    dados_rede['chaves']=chaves_dados
    dados_rede['busbar']=busbar_dados
    dados_rede['trafos']=transformadores_dados
    dados_rede['condutores']=condutores_dados
    dados_rede['nos']=nos_dados

    return dados_rede



def gerar_trechos(data):
    nos=data['nos']
    chaves=data['chaves']
    inicio_caminho=data['busbar']
    condutor=data['condutores']
    trechos=list()
    trechos_inter=list()
    alimentador={}
    chaves_nomes=[]

    for i in chaves:
        print(i)
    for i in chaves:
        chaves_nomes.append(i['nome'])

    condutor_nome=list()
    for i in condutor:
        condutor_nome.append(i['nome'])

    for i in inicio_caminho:
        a=0
        for j in chaves:


            if j['n2_id'] in i['ids']:
                a+=1
                trecho=OrderedDict()

                if i['nome']+j['nome'] in condutor_nome:
                    trecho['nome']=i['nome']+j['nome']

                elif j['nome']+i['nome']in condutor_nome:
                    trecho['nome']=j['nome']+i['nome']

                trecho['n1']=i['nome']
                trecho['n2']=j['nome']
                trecho['setor']=i['nome']
                trecho['comprimento']=10
                trecho['alimentador']=i['nome']+'_al'+str(a)
                trecho['condutor']= trecho['nome']
                trecho['id2']=[j['n1_id']]
                trechos.append(trecho)


            elif j['n1_id'] in i['ids']:
                trecho=OrderedDict()

                if i['nome']+j['nome'] in condutor_nome:
                    trecho['nome']=i['nome']+j['nome']

                elif j['nome']+i['nome']in condutor_nome:
                    trecho['nome']=j['nome']+i['nome']

                trecho['n1']=i['nome']
                trecho['n2']=j['nome']
                trecho['setor']=i['nome']
                trecho['comprimento']=10
                trecho['condutor']= trecho['nome']
                trecho['alimentador']=i['nome']+'_al'+str(a)
                trecho['id2']=[j['n2_id']]
                trechos.append(trecho)


    trechos_inter=trechos


    while trechos_inter!=[]:
        a=list()
        for y in trechos_inter:
            for i in y['id2']:
                for j in condutor:
                    if i==j['n1_id']:

                        n1=j['n2_id']
                        n2,id2=descubra(n1,chaves,nos)
                        setor=define_setores(y['n2'],n2,chaves_nomes)
                        trecho=OrderedDict()
                        trecho['nome']=j['nome']
                        trecho['n1']=y['n2']
                        trecho['n2']=n2
                        trecho['setor']=setor
                        trecho['comprimento']=j['comprimento']
                        trecho['alimentador']=y['alimentador']
                        trecho['condutor']=j['nome']
                        trecho['id2']=id2
                        a.append(trecho)

                    elif i==j['n2_id']:
                        n1=j['n1_id']
                        n2,id2=descubra(n1,chaves,nos)
                        setor=define_setores(y['n2'],n2,chaves_nomes)
                        trecho=OrderedDict()
                        trecho['nome']=j['nome']
                        trecho['n1']=y['n2']
                        trecho['n2']=n2
                        trecho['setor']=setor
                        trecho['comprimento']=j['comprimento']
                        trecho['alimentador']=y['alimentador']
                        trecho['condutor']= j['nome']
                        trecho['id2']=id2
                        a.append(trecho)
        for i in a:
            trechos.append(i)
        trechos_inter=a

    # for i in trechos:
    #     print(i)

    return trechos

def descubra(n2,chaves,nos):


    for i in nos:
        if n2 in i['ids']:
            a=i['ids']
            a.remove(n2)
            return i['nome'],a


    for i in chaves:

        if n2==i['n1_id']:
            if i['estado']==1:
                return i['nome'],[i['n2_id']]
            else:
                return i['nome'],[]



        elif n2==i['n2_id']:
            if i['estado']==1:
                return i['nome'],[i['n1_id']]
            else:
                return i['nome'],[]
def define_setores(n1,n2,chaves):

    if n1 not in chaves:
        return n1[0].upper()
    elif n2 not in chaves:
        return n2[0].upper()

def gerar_chaves(data_chaves):

    chaves=list()
    for i in data_chaves:
        chave=OrderedDict()
        nome=i['nome']
        estado=i['estado']
        chave=Switch(name=nome,state=estado)
        chaves.append(chave)

    chaves_nome=[]

    for i in data_chaves:
        chaves_nome.append(i['nome'])

    return chaves,chaves_nome

def _identificar_nos_vizinhos(nos_,trechos_,data): # identifica os nos vizinhos
    trechos = trechos_
    nos = nos_

    for i in data['busbar']:
        no_bus=OrderedDict()
        no_bus['nome']=i['nome']
        no_bus['p']=0
        no_bus['q']=0
        nos.append(no_bus)

    vizinhos = list()
    for no in nos:
        vizinhanca = OrderedDict()
        vizinhanca['no'] = no['nome']
        vizinhanca['vizinhos'] = list()

        for trecho in trechos:
            if trecho['n1'] == no['nome']:
                vizinhanca['vizinhos'].append(trecho['n2'])
            elif trecho['n2'] == no['nome']:
                vizinhanca['vizinhos'].append(trecho['n1'])
        vizinhos.append(vizinhanca)

    return vizinhos

def gerar_nos_de_carga(vizinhos,dados): #Gera os objetos NoDeCarga
    potencia=dados['nos']
    chaves=[]

    for i in dados['busbar']:
        no_bus=OrderedDict()
        no_bus['nome']=i['nome']
        no_bus['p']=0
        no_bus['q']=0
        potencia.append(no_bus)

    for i in dados['chaves']:
        chaves.append(i['nome'])

    nos_de_cargas=list()
    chaves_vizinhas=list()

    for i in range(len(vizinhos)):
        chave_vizinha=OrderedDict()
        chave_vizinha['nome']=vizinhos[i]['no']
        chave_vizinha['vizinhos']=list()
        for j in range(len(vizinhos[i]['vizinhos'])):
            if vizinhos[i]['vizinhos'][j] in chaves:
                chave_vizinha['vizinhos'].append(vizinhos[i]['vizinhos'][j])
        chaves_vizinhas.append(chave_vizinha)



    for i in range(len(vizinhos)):
        nos_de_carga=OrderedDict()
        nome=vizinhos[i]['no'].upper()
        real= float(potencia[i]['p']*1e3)
        img=float(potencia[i]['q']*1e3)
        vizinhos_i=[]
        chaves_i=chaves_vizinhas[i]['vizinhos']
        for j in range(len(vizinhos[i]['vizinhos'])):
            if vizinhos[i]['vizinhos'][j] not in chaves:
                vizinhos_i.append(vizinhos[i]['vizinhos'][j].upper())
            else:
                for x in range(len(vizinhos)):
                    if vizinhos[i]['vizinhos'][j] in vizinhos[x]['vizinhos'] \
                    and x!=i:
                         vizinhos_i.append(vizinhos[x]['no'].upper())


        nos_de_carga=LoadNode(name=nome,neighbors=vizinhos_i,power=R(real, img), switchs=chaves_i)
        nos_de_cargas.append(nos_de_carga)
    return nos_de_cargas

def gerar_trechos_grid(trechos_data,nos_de_carga,chaves,data): #Gera os Objetos do tipo Trecho
    trechos_lista=trechos_data
    trechos=list()
    cabos=data['condutores']

    for i in range(len(trechos_lista)):
        trecho=OrderedDict()

        for j in range(len(nos_de_carga)):

            if trechos_lista[i]['n1'].upper()==nos_de_carga[j].name:
                n1=nos_de_carga[j]
            if trechos_lista[i]['n2'].upper()==nos_de_carga[j].name:
                n2=nos_de_carga[j]


        for j in range(len(chaves)):
            if trechos_lista[i]['n1']==chaves[j].name:
                n1=chaves[j]
            if trechos_lista[i]['n2']==chaves[j].name:
                n2=chaves[j]


        for cab in cabos:
            if cab['nome']==trechos_lista[i]['condutor']:

                cond_1=Conductor(name=cab['nome'],
                                rp=float(cab['r']),
                                rz=float(cab['r0']),
                                xp=float(cab['x']),
                                xz=float(cab['x0']),
                                ampacity=float(cab['ampacidade']))

        nome=trechos_lista[i]['nome'].upper()
        comprimento=float(trechos_lista[i]['comprimento'])
        trecho=Section(name=nome,n1=n1,n2=n2,conductor=cond_1,length=comprimento/1000)
        trechos.append(trecho)
    return trechos

def gerar_setores(trechos_data,nos_de_cargas,data): #Gera os objetos do tipo Setor
    setor_dados=trechos_data
    setor_nome=list()
    chaves_nome=[]

    for i in data['chaves']:
        chaves_nome.append(i['nome'])

    for i in range(len(setor_dados)):
        if setor_dados[i]['setor'] not in setor_nome:
            setor_nome.append(setor_dados[i]['setor'])

    setor_ii=list()
    for i in range(len(setor_nome)):
        setor_i=OrderedDict()
        setor_i['nome']=setor_nome[i]
        setor_i['nos_contidos_setor']=list()
        for j in range(len(setor_dados)):
            if setor_nome[i]==setor_dados[j]['setor']:
                if setor_dados[j]['n1'] not in setor_i['nos_contidos_setor']:
                    setor_i['nos_contidos_setor'].append(setor_dados[j]['n1'])
                if setor_dados[j]['n2'] not in setor_i['nos_contidos_setor']:
                    setor_i['nos_contidos_setor'].append(setor_dados[j]['n2'])
        setor_ii.append(setor_i)

    setores=list()
    for i in range(len(setor_ii)):
        setores_i=OrderedDict()
        nome=setor_ii[i]['nome'].upper();
        vizinhos=[]
        nos_cargas=[]
        nos=[]
        for j in range(len(setor_ii)):
            if setor_ii[i]['nome']!=setor_ii[j]['nome']:
                for y in range(len(setor_ii[i]['nos_contidos_setor'])):
                    if setor_ii[i]['nos_contidos_setor'][y] not in chaves_nome\
                     and setor_ii[i]['nos_contidos_setor'][y] not in nos :
                        nos.append(setor_ii[i]['nos_contidos_setor'][y])

                    if setor_ii[i]['nos_contidos_setor'][y] in setor_ii[j]['nos_contidos_setor']:
                        vizinhos.append(setor_ii[j]['nome'].upper())

        for j in range(len(nos)):
            for x in range(len(nos_de_cargas)):
                if nos[j].upper()==nos_de_cargas[x].name:
                    nos_cargas.append(nos_de_cargas[x])
        setores_i=(Sector(name=nome,neighbors=vizinhos, load_nodes=nos_cargas))
        setores.append(setores_i)
    return setores

def gerar_ligacao_chaves_setores(trechos_data,chaves,setores,data): # Faz a ligacao das chaves com seus respectivos setores
    trechos=trechos_data
    chaves_nome=[]

    for i in data['chaves']:
        chaves_nome.append(i['nome'])

    ligacao_chave=list()
    ch_exist=[]
    for i in range(len(trechos)):
        ligacao=OrderedDict()
        n_1='nope'
        n_2='nope'

        if trechos[i]['n1'] in chaves_nome and trechos[i]['n1'] not in ch_exist :
            ch_exist.append(trechos[i]['n1'])
            n_1=trechos[i]['n1']
            ligacao['nome_chave']=n_1
            ligacao['n1']=trechos[i]['setor']

            for j in range(len(trechos)-(1+i)):
                if trechos[j+1+i]['n1']==n_1:
                    ligacao['n2']=trechos[j+1+i]['setor']
                elif trechos[j+1+i]['n2'][0:2]==n_1:
                    ligacao['n2']=trechos[j+1+i]['setor']

        elif trechos[i]['n2'] in chaves_nome and trechos[i]['n2'] not in ch_exist :
            ch_exist.append(trechos[i]['n2'])
            n_2=trechos[i]['n2']
            ligacao['nome_chave']=n_2
            ligacao['n1']=trechos[i]['setor']

            for j in range(len(trechos)-(1+i)):
                if trechos[j+1+i]['n1']==n_2:
                    ligacao['n2']=trechos[j+1+i]['setor']
                elif trechos[j+1+i]['n2']==n_2:
                    ligacao['n2']=trechos[j+1+i]['setor']

        if n_1!='nope' or n_2!='nope':
            ligacao_chave.append(ligacao)

    for i in range(len(ligacao_chave)):
        for j in range(len(chaves)):
            if ligacao_chave[i]['nome_chave']==chaves[j].name:
                for x in range(len(setores)):
                    if  ligacao_chave[i]['n1'].upper()==setores[x].name:
                        chaves[j].n1=setores[x]
                for x in range(len(setores)):
                    if  ligacao_chave[i]['n2'].upper()==setores[x].name:
                        chaves[j].n2=setores[x]

    return chaves

def gerar_transformadores(data): # gera os objetos do tipo Transformador

    transformadores_data=data['trafos']
    transformadores=list()
    for i in transformadores_data:
        transformador=OrderedDict()
        nome=i['nome']
        tensao_primario_mod=float(i['tensao_p']*1e3)
        tensao_primario_ang=float(0)
        tensao_secundario_mod=float(i['tensao_s']*1e3)
        tensao_secundario_ang=float(0)
        potencia_mod=float(i['potencia']*1e6)
        potencia_ang=float(0)
        impedancia_real=float(i['r'])
        impedancia_imag=float(i['x'])
        transformador=Transformer(name=nome,
                                    primary_voltage=P(tensao_primario_mod,tensao_primario_ang),
                                    secondary_voltage=P(tensao_secundario_mod,tensao_secundario_ang),
                                    power=P(potencia_mod,potencia_ang),
                                    impedance=R(impedancia_real,impedancia_imag))
        transformadores.append(transformador)
    return transformadores

def gerar_alimentadores(data,trechos_data,trechos_d,setores,chaves): # Gera objetos do tipo Alimentador

    alimentadores_sheet = []
    for i in trechos_data:
        if i['alimentador'] not in alimentadores_sheet:
             alimentadores_sheet.append(i['alimentador'])

    trechos_alimentadores=trechos_data

    trechos=trechos_d

    chaves_nome=[]
    for i in data['chaves']:
        chaves_nome.append(i['nome'])


    alimentador=list()
    for i in range(len(alimentadores_sheet)):
        alimentadores_i=OrderedDict()
        alimentadores_i['nome']=alimentadores_sheet[i]
        alimentadores_i['setores']=list()
        alimentadores_i['trechos']=list()
        alimentadores_i['chaves']=list()

        for j in range(len(trechos_alimentadores)):
            if alimentadores_sheet[i]==trechos_alimentadores[j]['alimentador']:
                if trechos_alimentadores[j]['setor'] not in alimentadores_i['setores']:
                    alimentadores_i['setores'].append(trechos_alimentadores[j]['setor'])

                if  trechos_alimentadores[j]['nome'] not in  alimentadores_i['trechos']:
                    alimentadores_i['trechos'].append( trechos_alimentadores[j]['nome'])
                if trechos_alimentadores[j]['n1'] in chaves_nome:
                    if trechos_alimentadores[j]['n1'] not in alimentadores_i['chaves']:
                        alimentadores_i['chaves'].append(trechos_alimentadores[j]['n1'])
                if trechos_alimentadores[j]['n2'] in chaves_nome:
                    if trechos_alimentadores[j]['n2'] not in alimentadores_i['chaves']:
                        alimentadores_i['chaves'].append(trechos_alimentadores[j]['n2'])

        alimentador.append(alimentadores_i)


    alimentadores=list()
    for i in range(len(alimentador)):
        nome=alimentador[i]['nome'].upper()
        setor=list()
        trecho1=list()
        chave=list()
        alimentadores_ii=OrderedDict()
        for j in range(len(alimentador[i]['setores'])):
            for x in range(len(setores)):
                if alimentador[i]['setores'][j].upper()==setores[x].name:
                    setor.append(setores[x])

        for j in range(len(alimentador[i]['trechos'])):
            for x in range(len(trechos_d)):
                if alimentador[i]['trechos'][j].upper()==trechos_d[x].name:
                    trecho1.append(trechos_d[x])

        for j in range(len(alimentador[i]['chaves'])):
            for x in range(len(chaves)):
                if alimentador[i]['chaves'][j]==chaves[x].name:
                    chave.append(chaves[x])
        alimentadores_ii=Feeder(name=nome,sectors=setor,sections=trecho1,switchs=chave)
        alimentadores.append(alimentadores_ii)
    return alimentadores

def gerar_sub_estacao(alimentadores,data,transformadores): #gera os objetos do tipo Subestacao

    bus=data['busbar']

    lista_nome_sub_est=list()
    for i in range(len(alimentadores)):
        nome_sub_est=''
        for j in range(len(alimentadores[i].name)):
            if alimentadores[i].name[j]!='_':
                nome_sub_est=nome_sub_est+(alimentadores[i].name[j])
            else:
                break
        if nome_sub_est not in lista_nome_sub_est:
            lista_nome_sub_est.append(nome_sub_est)

    subestacao=list()
    sub_est_usadas=[]

    for i in range(len(lista_nome_sub_est)):
        sub=OrderedDict()
        aliment=list()
        for j in range(len(alimentadores)):
            a=0
            for x in alimentadores[j].name:
                if x != '_':
                    a+=1
                else:
                    break
            if lista_nome_sub_est[i]==alimentadores[j].name[0:a]:
                nome=lista_nome_sub_est[i]
                aliment.append(alimentadores[j])

        transformador=[]
        for j in range(len(transformadores)):
            a=0
            for x in transformadores[j].name:
                if x != '_':
                    a+=1
                else:
                    break
            if nome==transformadores[j].name[0:a]:
                transformador.append(transformadores[j])

        if nome not in sub_est_usadas:
            sub=Substation(name=nome,feeders=aliment,transformers=transformador)
            subestacao.append(sub)
            sub_est_usadas.append(nome)

    lista_nome_alimentadores=list()
    for i in range(len(alimentadores)):
        p={alimentadores[i].name:alimentadores[i]}
        lista_nome_alimentadores.append(p)

    for i in sub_est_usadas:
        for j in range(len(alimentadores)):
            a=0
            for x in alimentadores[j].name:
                if x != '_':
                    a+=1
                else:
                    break
            if i==alimentadores[j].name[0:a]:
                alimentadores[j].order(i)


    arvore_subestacao=list()
    for i in range(len(alimentadores)):
        p=alimentadores[i].generate_load_nodes_tree()
        arvore_subestacao.append(p)


    return subestacao

if __name__ == '__main__':

    data=carregar_dados('oi_test_CIM.xml')
    trechos_data=gerar_trechos(data)
    chaves,chaves_nome=gerar_chaves(data['chaves'])
    vizinhos=_identificar_nos_vizinhos(data['nos'],trechos_data,data)
    nos_de_carga=gerar_nos_de_carga(vizinhos,data)
    trechos=gerar_trechos_grid(trechos_data,nos_de_carga,chaves,data)
    setores=gerar_setores(trechos_data,nos_de_carga,data)
    gerar_ligacao_chaves_setores(trechos_data,chaves,setores,data)
    transformadores=gerar_transformadores(data)
    alimentadores=gerar_alimentadores(data,trechos_data,trechos,setores,chaves)
    subestacoes=gerar_sub_estacao(alimentadores,data,transformadores)
    # no={}
    # for i in range(len(nos_de_carga)):
    #     no[nos_de_carga[i].name]=nos_de_carga[i]
    # chave={}
    # for i in range(len(chaves)):
    #     chave[chaves[i].name]=chaves[i]
    # trecho={}
    # for i in range(len(trechos)):
    #     trecho[trechos[i].name]=trechos[i]
    # setor={}
    # for i in range(len(setores)):
    #     setor[setores[i].name]=setores[i]
    # alimentador={}
    # for i in range(len(alimentadores)):
    #     alimentador[alimentadores[i].name]=alimentadores[i]
    # subestacao={}
    # for i in range(len(subestacoes)):
    #     subestacao[subestacoes[i].name]=subestacoes[i]
