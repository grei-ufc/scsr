from mygrid.power_flow import backward_forward_sweep
import mygrid.short_circuit.symmetrical_components as curto
import pandas as pd
import smartpower.core.models as models
# import plotly.plotly as py
# import plotly.figure_factory as ff
# import plotly
import numpy as np
# import subprocess, os
# import sys
from collections import OrderedDict

def start_conversion(scene):


    data=models.carregar_dados(scene)
    trechos_data=models.gerar_trechos(data)
    chaves,chaves_nome=models.gerar_chaves(data['chaves'])
    vizinhos=models._identificar_nos_vizinhos(data['nos'],trechos_data,data)
    nos_de_carga=models.gerar_nos_de_carga(vizinhos,data)
    trechos=models.gerar_trechos_grid(trechos_data,nos_de_carga,chaves,data)
    setores=models.gerar_setores(trechos_data,nos_de_carga,data)
    models.gerar_ligacao_chaves_setores(trechos_data,chaves,setores,data)
    transformadores=models.gerar_transformadores(data)
    alimentadores=models.gerar_alimentadores(data,trechos_data,trechos,setores,chaves)
    subestacoes=models.gerar_sub_estacao(alimentadores,data,transformadores)
 

    for i in subestacoes:
        backward_forward_sweep.calc_power_flow(i)
        


    tabela={}
    curtos={}
    # path=path.replace('CIM.xml','resultados.xlsx')
    # writer=pd.ExcelWriter(path)
    for i in subestacoes:
        data_curtos=list()
        curto.config_objects(i)
        data_curtos=curto.calc_short_circuit(i,'three-phase')
        data_curtos.extend(curto.calc_short_circuit(i,'line-to-line'))
        data_curtos.extend(curto.calc_short_circuit(i,'line-to-ground'))

        #a=pd.concat(data_curtos[0:3],axis=1)
        #a.drop([0], axis=0, inplace=True)
        #b=pd.concat(data_curtos[3:6],axis=1)
        #b=b.values.tolist()
        # a.to_excel(writer,i.nome)
        # writer.sheets[i.nome].set_column('B:J', 20)
        curtos[i.name]=data_curtos
    tabela['curtos']=curtos

    colunas_no_de_carga=['No','Tensao (V)','(kW)','(KQ)']
    lista_nos=list()
    for i in nos_de_carga:
        linha_nos_de_carga=list()
        linha_nos_de_carga.append(i.name)
        linha_nos_de_carga.append(str(i.voltage.m))
        linha_nos_de_carga.append(str(i.power.r/1000))
        linha_nos_de_carga.append(str(i.power.i/1000))
        lista_nos.append(linha_nos_de_carga)
    a=pd.DataFrame(lista_nos,columns=colunas_no_de_carga)
    # a.to_excel(writer,'fluxo_de_carga')
    # writer.sheets['fluxo_de_carga'].set_column('B:J', 20)
    tabela['niveis_de_tensao']=a.values.tolist()



    
    trechos_colunas=['Nome','comprimento (km)','corrente (A)']
    trechos_lista=list()
    for i in trechos:
        trechos_linha=list()
        trechos_linha.append(i.name)
        trechos_linha.append(str(i.length))
        trechos_linha.append(str(i.flow.m))
        trechos_lista.append(trechos_linha)
        print(i.n2.name)

    #a=pd.DataFrame(trechos_lista,columns=trechos_colunas)
    # a.to_excel(writer,'Trechos')
    # writer.sheets['Trechos'].set_column('B:J', 20)
    tabela['trechos']=trechos_lista
    # writer.save()



    return tabela

    pass

####################################################
#     data=cim.carregar_dados(path)
#     trechos_data=cim.gerar_trechos(data)
#     for i in trechos_data:
#         print i
#     chaves,chaves_nome=cim.gerar_chaves(data['chaves'])
#     vizinhos=cim._identificar_nos_vizinhos(data['nos'],trechos_data,data)
#     nos_de_carga=cim.gerar_nos_de_carga(vizinhos,data)
#     trechos=cim.gerar_trechos_grid(trechos_data,nos_de_carga,chaves,data)
#     setores=cim.gerar_setores(trechos_data,nos_de_carga,data)
#     cim.gerar_ligacao_chaves_setores(trechos_data,chaves,setores,data)
#     transformadores=cim.gerar_transformadores(data)
#     alimentadores=cim.gerar_alimentadores(data,trechos_data,trechos,setores,chaves)
#     subestacoes=cim.gerar_sub_estacao(alimentadores,data,transformadores)
#     for i in trechos:
#         print i.condutor.rp

#     for i in subestacoes:
#     	varred_dir_inv.calcular_fluxo_de_carga(i)
#     	curto.config_objects(i)


#     tabela={}
#     curtos={}
#     # path=path.replace('CIM.xml','resultados.xlsx')
#     # writer=pd.ExcelWriter(path)
#     for i in subestacoes:
#         data_curtos=[]
#         tuples=[('trifasico','Trecho'),('trifasico','Curto (pu)'),('trifasico','Curto (A)')]
#         index = pd.MultiIndex.from_tuples(tuples)
#         data_curtos.append(pd.DataFrame(curto.calculacurto(i,'trifasico'),columns=index))
#         tuples=[('bifasico','Trecho'),('bifasico','Curto (pu)'),('bifasico','Curto (A)')]
#         index = pd.MultiIndex.from_tuples(tuples)
#         data_curtos.append(pd.DataFrame(curto.calculacurto(i,'bifasico'),columns=index))
#         tuples=[('monofasico','Trecho'),('monofasico','Curto (pu)'),('monofasico','Curto (A)')]
#         index = pd.MultiIndex.from_tuples(tuples)
#         data_curtos.append(pd.DataFrame(curto.calculacurto(i,'monofasico'),columns=index))
#         data_curtos.append(pd.DataFrame(curto.calculacurto(i,'trifasico')))
#         data_curtos.append(pd.DataFrame(curto.calculacurto(i,'bifasico')))
#         data_curtos.append(pd.DataFrame(curto.calculacurto(i,'monofasico')))

#         a=pd.concat(data_curtos[0:3],axis=1)
#         a.drop([0], axis=0, inplace=True)
#         b=pd.concat(data_curtos[3:6],axis=1)
#         b=b.values.tolist()
#         # a.to_excel(writer,i.nome)
#         # writer.sheets[i.nome].set_column('B:J', 20)
#         curtos[i.nome]=b
#     tabela['curtos']=curtos

#     colunas_no_de_carga=['No','Tensao (V)','(kW)','(KQ)']
#     lista_nos=list()
#     for i in nos_de_carga:
#         linha_nos_de_carga=list()
#         linha_nos_de_carga.append(i.nome)
#         linha_nos_de_carga.append(str(i.tensao.mod))
#         linha_nos_de_carga.append(str(i.potencia.real/1000))
#         linha_nos_de_carga.append(str(i.potencia.imag/1000))
#         lista_nos.append(linha_nos_de_carga)
#     a=pd.DataFrame(lista_nos,columns=colunas_no_de_carga)
#     # a.to_excel(writer,'fluxo_de_carga')
#     # writer.sheets['fluxo_de_carga'].set_column('B:J', 20)
#     tabela['niveis_de_tensao']=a.values.tolist()



#     for i in subestacoes:
#         	varred_dir_inv.calcular_fluxo_de_carga(i)
#     trechos_colunas=['Nome','comprimento (km)','corrente (A)']
#     trechos_lista=list()
#     for i in trechos:
#     	trechos_linha=list()
#     	trechos_linha.append(i.nome)
#     	trechos_linha.append(str(i.comprimento))
#     	trechos_linha.append(str(i.fluxo.mod))
#     	trechos_lista.append(trechos_linha)

#     a=pd.DataFrame(trechos_lista,columns=trechos_colunas)
#     # a.to_excel(writer,'Trechos')
#     # writer.sheets['Trechos'].set_column('B:J', 20)
#     tabela['trechos']=a.values.tolist()
#     # writer.save()
#     return tabela
# #writer.save()
# #if sys.platform.startswith('darwin'):
# #    subprocess.call(('open', 'output.xlsx'))
# #elif os.name == 'nt':
# #    os.startfile('output.xlsx')
# #elif os.name == 'posix':
# #    subprocess.call(('xdg-open', 'output.xlsx'))
