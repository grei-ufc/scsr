# -*- encoding: utf-8 -*-
from mygrid.power_flow import backward_forward_sweep
import mygrid.short_circuit.symmetrical_components as curto
from collections import OrderedDict
from xml.etree import ElementTree
from xml.dom import minidom
from PySide2 import QtCore, QtGui
from smartpower.core.graphics import Node, Edge, Text
from bs4 import BeautifulSoup
from smartpower.core.elementos import NoConect, Terminal, Religador, EnergyConsumer, Substation, BusBarSection

from mygrid.grid import  Feeder, Sector, Switch

import mygrid.grid
from mygrid.grid import Section, LoadNode, Transformer, Conductor
from mygrid.util import R, P
import pandas as pd




class DiagramToXML(ElementTree.Element):
    '''
        Esta classe possui as funções que armazenam as informações
        necessárias à conversão do diagrama grafico em um
        arquivo XML
    '''
    def __init__(self, scene):
        '''
            Função que inicializa o objeto criado pela classe DiagramToXML
        '''
        super(DiagramToXML, self).__init__('items')

        self.scene = scene
        lista = self.scene.items()
        lista.reverse()
        for item in self.scene.items():
            if isinstance(item, Node):
                CE = ElementTree.Element(
                    'CE', attrib={'type': str(item.myItemType)})
                id = ElementTree.Element('id')
                id.text = str(item.id)
                CE.append(id)

                x = ElementTree.Element('x')
                x.text = str(item.scenePos().x())
                CE.append(x)

                y = ElementTree.Element('y')
                y.text = str(item.scenePos().y())
                CE.append(y)

                width = ElementTree.Element('width')
                width.text = str(item.rect().width())
                CE.append(width)

                height = ElementTree.Element('height')
                height.text = str(item.rect().height())
                CE.append(height)

                # Salva as informações referente ao item gráfico religador
                # e os parâmetros da sua chave associada

                if item.myItemType == Node.Religador:

                    padrao = ElementTree.Element('padrao')
                    padrao.text = str(item.text_config)

                    identificador = ElementTree.Element('identificador')
                    identificador.text = str(item.text.toPlainText())

                    corrente = ElementTree.Element('corrente')
                    corrente.text = str(item.chave.ratedCurrent)

                    in_tt = ElementTree.Element('intt')
                    in_tt.text = str(item.chave.inTransitTime)

                    cap_int = ElementTree.Element('capint')
                    cap_int.text = str(item.chave.breakingCapacity)

                    seq_rel = ElementTree.Element('seqrel')
                    seq_rel.text = str(item.chave.recloseSequences)

                    estado = ElementTree.Element('estado')
                    estado.text = str(item.chave.normalOpen)

                    CE.append(estado)
                    CE.append(corrente)
                    CE.append(in_tt)
                    CE.append(cap_int)
                    CE.append(seq_rel)
                    CE.append(padrao)
                    CE.append(identificador)

                # Salva as informações referente ao item gráfico nó de carga
                # e seus parâmetros associados
                if item.myItemType == Node.NoDeCarga:
                    identificador = ElementTree.Element('identificador')
                    identificador.text = str(item.text.toPlainText().split()[0])

                    p_ativa = ElementTree.Element('pativa')
                    p_ativa.text = str(item.no_de_carga.potencia_ativa)

                    p_reativa = ElementTree.Element('preativa')
                    p_reativa.text = str(item.no_de_carga.potencia_reativa)

                    CE.append(identificador)
                    CE.append(p_ativa)
                    CE.append(p_reativa)

                # Salva as informações referente ao item gráfico subestação
                # e seus parâmetros associados
                if item.myItemType == Node.Subestacao:
                    identificador = ElementTree.Element('identificador')
                    identificador.text = str(item.text.toPlainText())

                    n_transformadores = ElementTree.Element('n_transformadores')
                    n_transformadores.text = str(item.substation.n_transformadores)

                    tensao_p = ElementTree.Element('tensaop')
                    tensao_p.text = str(item.substation.tensao_primario)

                    tensao_s = ElementTree.Element('tensaos')
                    tensao_s.text = str(item.substation.tensao_secundario)

                    potencia = ElementTree.Element('potencia')
                    potencia.text = str(item.substation.potencia)

                    resistencia_positiva = ElementTree.Element('r_pos')
                    resistencia_positiva.text = str(item.substation.r_pos)

                    reatancia_positiva = ElementTree.Element('i_pos')
                    reatancia_positiva.text = str(item.substation.i_pos)

                    resistencia_zero = ElementTree.Element('r_zero')
                    resistencia_zero.text = str(item.substation.r_zero)

                    reatancia_zero = ElementTree.Element('i_zero')
                    reatancia_zero.text = str(item.substation.i_zero)

                    CE.append(identificador)
                    CE.append(n_transformadores)
                    CE.append(tensao_p)
                    CE.append(tensao_s)
                    CE.append(potencia)
                    CE.append(resistencia_positiva)
                    CE.append(reatancia_positiva)
                    CE.append(resistencia_zero)
                    CE.append(reatancia_zero)

                # Salva as informações referente ao item gráfico barra
                # e seus parâmetros associados
                if item.myItemType == Node.Barra:
                    identificador = ElementTree.Element('identificador')
                    identificador.text = str(item.text.toPlainText())

                    fases = ElementTree.Element('fases')
                    fases.text = str(item.barra.phases)

                    resistencia_positiva = ElementTree.Element('r_pos')
                    resistencia_positiva.text = str(item.barra.r_pos)

                    reatancia_positiva = ElementTree.Element('i_pos')
                    reatancia_positiva.text = str(item.barra.i_pos)

                    resistencia_zero = ElementTree.Element('r_zero')
                    resistencia_zero.text = str(item.barra.r_zero)

                    reatancia_zero = ElementTree.Element('i_zero')
                    reatancia_zero.text = str(item.barra.i_zero)

                    CE.append(identificador)
                    CE.append(fases)
                    CE.append(resistencia_positiva)
                    CE.append(reatancia_positiva)
                    CE.append(resistencia_zero)
                    CE.append(reatancia_zero)

                self.append(CE)
        for item in lista:
            # Verifica se o item é um condutor e salva seus parâmetros
            if isinstance(item, Edge):
                edge = ElementTree.Element('edge')
                w1 = ElementTree.Element('w1')
                w1.text = str(item.w1.id)

                w2 = ElementTree.Element('w2')
                w2.text = str(item.w2.id)

                comprimento = ElementTree.Element('comprimento')
                comprimento.text = str(item.linha.comprimento)

                r1=ElementTree.Element('r1')
                r1.text= str(item.linha.resistencia)

                z1=ElementTree.Element('z1')
                z1.text= str(item.linha.reatancia)

                r0=ElementTree.Element('r0')
                r0.text= str(item.linha.resistencia_zero)

                z0=ElementTree.Element('z0')
                z0.text= str(item.linha.reatancia_zero)

                amp=ElementTree.Element('ampacidade')
                amp.text= str(item.linha.ampacidade)

                padrao = ElementTree.Element('padrao')
                padrao.text = str(item.text_config)

                edge.append(comprimento)
                edge.append(w1)
                edge.append(w2)
                edge.append(r1)
                edge.append(z1)
                edge.append(r0)
                edge.append(z0)
                edge.append(amp)
                edge.append(padrao)
                self.append(edge)

    def write_xml(self, path):
        '''
            Função que cria o arquivo XML na localização indicada pelo
            argumento path.
        '''
        xml_string = ElementTree.tostring(self)
        dom_element = (minidom.parseString(xml_string))
        f = open(path, 'w')
        f.write(dom_element.toprettyxml())
        f.close()


class XMLToDiagram(object):
    '''
        Classe que constrói um diagrama gráfico a partir de um arquivo XML.
    '''

    def __init__(self, scene, file_path):
        self.scene = scene
        self.file_path = file_path

        xml_tree = ElementTree.parse(self.file_path)
        xml_element = xml_tree.getroot()
        self.scene.clear()
        for child in xml_element:

            if child.tag == 'CE':
                # Verifica qual tipo de elemento e converte as informações
                # Subestação
                if child.attrib['type'] == '0':
                    item = Node(
                        int(child.attrib['type']), self.scene.mySubstationMenu)
                    identificador = child.find('identificador').text
                    tensaop = child.find('tensaop').text
                    tensaos = child.find('tensaos').text
                    potencia = child.find('potencia').text
                    n_transformadores = child.find('n_transformadores').text
                    r_pos = child.find('r_pos').text
                    i_pos = child.find('i_pos').text
                    r_zero = child.find('r_zero').text
                    i_zero = child.find('i_zero').text
                    item.substation = Substation(identificador, n_transformadores, float(tensaop), float(tensaos), float(potencia), float(r_pos), float(i_pos),float(r_zero),float(i_zero))
                    self.scene.addItem(item)
                    item.setPos(
                        float(child.find('x').text), float(
                            child.find('y').text))
                    item.id = int(child.find('id').text)
                    item.text.setPlainText(identificador)

                # Religador
                elif child.attrib['type'] == '1':
                    item = Node(
                        int(child.attrib['type']), self.scene.myRecloserMenu)
                    item.text_config = str(child.find('padrao').text)
                    state = child.find('estado').text
                    corrente = child.find('corrente').text
                    in_tt = child.find('intt').text
                    cap_int = child.find('capint').text
                    seq_rel = child.find('seqrel').text
                    identificador = child.find('identificador').text
                    item.chave = Religador(identificador,int(corrente),int(in_tt),int(cap_int),int(seq_rel),int(state))
                    self.scene.create_dict_recloser(corrente,cap_int,seq_rel,item.text_config)
                    item.id = int(child.find('id').text)
                    item.setPos(float(child.find('x').text), float(
                        child.find('y').text))
                    self.scene.addItem(item)
                    item.text.setPlainText(identificador)

                # Barra
                elif child.attrib['type'] == '2':
                    item = Node(int(
                        child.attrib['type']), self.scene.myBusMenu)
                    identificador = child.find('identificador').text
                    fases = child.find('fases').text
                    r_pos = child.find('r_pos').text
                    i_pos = child.find('i_pos').text
                    r_zero = child.find('r_zero').text
                    i_zero = child.find('i_zero').text
                    item.barra = BusBarSection(identificador,float(fases),float(r_pos),float(i_pos),float(r_zero),float(i_zero))

                    item.setPos(float(child.find('x').text), float(
                        child.find('y').text))
                    item.id = int(child.find('id').text)
                    item.setRect(
                        0, 0, float(child.find('width').text), float(
                            child.find('height').text))
                    self.scene.addItem(item)
                    item.text.setPlainText(identificador)

                elif child.attrib['type'] == '3':
                    item = Node(int(child.attrib['type']), None)
                    item.setPos(
                        float(child.find('x').text), float(
                            child.find('y').text))
                    item.id = int(child.find('id').text)
                    self.scene.addItem(item)

                # Nó de carga
                elif child.attrib['type'] == '4':
                    item = Node(int(child.attrib['type']), self.scene.mySubstationMenu)
                    p_ativa = child.find('pativa').text
                    p_reativa = child.find('preativa').text
                    identificador = str(child.find('identificador').text)
                    item.no_de_carga = EnergyConsumer(identificador, p_ativa, p_reativa)
                    item.setPos(
                        float(child.find('x').text), float(
                            child.find('y').text))
                    item.id = int(child.find('id').text)
                    self.scene.addItem(item)

                    item.text.setPlainText(identificador)

                elif child.attrib['type'] == '5':
                    item = Node(int(child.attrib['type']), None)
                    item.setPos(
                        float(child.find('x').text), float(
                            child.find('y').text))
                    item.id = int(child.find('id').text)
                    self.scene.addItem(item)

            # Condutor
            elif child.tag == 'edge':
                for item in self.scene.items():
                    if isinstance(item, Node) and item.id == int(child.find('w1').text):
                        w1 = item
                    elif isinstance(item, Node) and item.id == int(child.find('w2').text):
                        w2 = item
                edge = Edge(w1, w2, self.scene.myLineMenu)
                edge.linha.comprimento = float(child.find('comprimento').text)
                edge.linha.resistencia = float(child.find('r1').text)
                edge.linha.resistencia_zero = float(child.find('r0').text)
                edge.linha.reatancia = float(child.find('z1').text)
                edge.linha.reatancia_zero = float(child.find('z0').text)
                edge.linha.ampacidade = float(child.find('ampacidade').text)
                try:
                    edge.text_config=str(child.find('padrao').text)
                except:
                    edge.text_config="Custom"

                self.scene.addItem(edge)
                edge.update_position()
                


class CimXML(object):
    '''
        Classe que representa os dados dos componentes em padrão CIM
    '''

    def __init__(self, scene):
        self.scene = scene
        self.lista_no_conectivo = []
        self.lista_terminais = []
        self.montar_rede(scene)

        self.cim_xml = BeautifulSoup()

        # Percorre toda a lista buscando elementos do tipo Religador
        for item in scene.items():
            if isinstance(item, Node):

                if item.myItemType == item.Religador:

                    tag_breaker = self.cim_xml.new_tag("Breaker")
                    self.cim_xml.append(tag_breaker)

                    tag_id = self.cim_xml.new_tag("mRID")
                    tag_id.append(item.text.toPlainText())
                    tag_breaker.append(tag_id)

                    tag_rc = self.cim_xml.new_tag("ratedCurrent")
                    tag_rc.append(str(item.chave.ratedCurrent))
                    tag_breaker.append(tag_rc)

                    tag_itt = self.cim_xml.new_tag("inTransitTime")
                    tag_itt.append(str(item.chave.inTransitTime))
                    tag_breaker.append(tag_itt)

                    tag_bc = self.cim_xml.new_tag("breakingCapacity")
                    tag_bc.append(str(item.chave.breakingCapacity))
                    tag_breaker.append(tag_bc)

                    tag_rs = self.cim_xml.new_tag("recloseSequences")
                    tag_rs.append(str(item.chave.recloseSequences))
                    tag_breaker.append(tag_rs)

                    tag_NO = self.cim_xml.new_tag("normalOpen")
                    tag_NO.append(str(item.chave.normalOpen))
                    tag_breaker.append(tag_NO)

                    tag_terminal1= self.cim_xml.new_tag("terminal")
                    tag_seqNumber = self.cim_xml.new_tag("SequenceNumber")
                    tag_seqNumber.append("1")
                    tag_terminal1.append(tag_seqNumber)
                    tag_mRID = self.cim_xml.new_tag("mRID")
                    tag_mRID.append(str(item.terminal1.mRID))
                    tag_terminal1.append(tag_mRID)
                    tag_breaker.append(tag_terminal1)

                    tag_terminal2= self.cim_xml.new_tag("terminal")
                    tag_seqNumber = self.cim_xml.new_tag("SequenceNumber")
                    tag_seqNumber.append("2")
                    tag_terminal2.append(tag_seqNumber)
                    tag_mRID = self.cim_xml.new_tag("mRID")
                    tag_mRID.append(str(item.terminal2.mRID))
                    tag_terminal2.append(tag_mRID)
                    tag_breaker.append(tag_terminal2)

        # Percorre toda a lista buscando elementos do tipo Barra
        for item in scene.items():
            if isinstance(item, Node):

                if item.myItemType == item.Barra:

                    tag_barra = self.cim_xml.new_tag("busBarSection")
                    self.cim_xml.append(tag_barra)

                    tag_id = self.cim_xml.new_tag("mRID")
                    tag_id.append(item.text.toPlainText())
                    tag_barra.append(tag_id)

                    tag_phases = self.cim_xml.new_tag("phases")
                    tag_phases.append(str(item.barra.phases))
                    tag_barra.append(tag_phases)

                    tag_rpos = self.cim_xml.new_tag("r")
                    tag_rpos.append(str(item.barra.r_pos))
                    tag_barra.append(tag_rpos)

                    tag_ipos = self.cim_xml.new_tag("x")
                    tag_ipos.append(str(item.barra.i_pos))
                    tag_barra.append(tag_ipos)

                    tag_rzero = self.cim_xml.new_tag("r0")
                    tag_rzero.append(str(item.barra.r_zero))
                    tag_barra.append(tag_rzero)

                    tag_izero = self.cim_xml.new_tag("x0")
                    tag_izero.append(str(item.barra.i_zero))
                    tag_barra.append(tag_izero)

                    for Terminal in (item.terminals):
                        tag_terminal = self.cim_xml.new_tag("terminal")
                        tag_mRID = self.cim_xml.new_tag('mRID')
                        tag_mRID.append(str(Terminal.mRID))
                        tag_terminal.append(tag_mRID)
                        tag_barra.append(tag_terminal)


        # Percorre toda a lista buscando elementos do tipo Subestação
        for item in scene.items():
            if isinstance(item, Node):

                if item.myItemType == item.Subestacao:

                    tag_substation = self.cim_xml.new_tag("Substation")
                    self.cim_xml.append(tag_substation)

                    tag_id = self.cim_xml.new_tag("mRID")
                    tag_id.append(str(item.text.toPlainText()).strip())
                    tag_substation.append(tag_id)

                    tag_ntrafo = self.cim_xml.new_tag("n_trafo")
                    tag_ntrafo.append(str(item.substation.n_transformadores))
                    tag_substation.append(tag_ntrafo)

                    tag_tensaop = self.cim_xml.new_tag("tensaop")
                    tag_tensaop.append(str(item.substation.tensao_primario))
                    tag_substation.append(tag_tensaop)

                    tag_tensaos = self.cim_xml.new_tag("tensaos")
                    tag_tensaos.append(str(item.substation.tensao_secundario))
                    tag_substation.append(tag_tensaos)

                    tag_potencia = self.cim_xml.new_tag("power")
                    tag_potencia.append(str(item.substation.potencia))
                    tag_substation.append(tag_potencia)

                    tag_rpos = self.cim_xml.new_tag("r")
                    tag_rpos.append(str(item.substation.r_pos))
                    tag_substation.append(tag_rpos)

                    tag_ipos = self.cim_xml.new_tag("x")
                    tag_ipos.append(str(item.substation.i_pos))
                    tag_substation.append(tag_ipos)

                    tag_rzero = self.cim_xml.new_tag("r0")
                    tag_rzero.append(str(item.substation.r_zero))
                    tag_substation.append(tag_rzero)

                    tag_izero = self.cim_xml.new_tag("x0")
                    tag_izero.append(str(item.substation.i_zero))
                    tag_substation.append(tag_izero)

                    tag_terminal1= self.cim_xml.new_tag("terminal")
                    tag_seqNumber = self.cim_xml.new_tag("SequenceNumber")
                    tag_seqNumber.append("1")
                    tag_terminal1.append(tag_seqNumber)
                    tag_mRID = self.cim_xml.new_tag("mRID")
                    tag_mRID.append(str(item.terminal1.mRID))
                    tag_terminal1.append(tag_mRID)
                    tag_substation.append(tag_terminal1)

                    tag_terminal2= self.cim_xml.new_tag("terminal")
                    tag_seqNumber = self.cim_xml.new_tag("SequenceNumber")
                    tag_seqNumber.append("2")
                    tag_terminal2.append(tag_seqNumber)
                    tag_mRID = self.cim_xml.new_tag("mRID")
                    tag_mRID.append(str(item.terminal2.mRID))
                    tag_terminal2.append(tag_mRID)
                    tag_substation.append(tag_terminal2)

        # Percorre toda a lista buscando elementos do tipo Nó de carga
        for item in scene.items():
            if isinstance(item, Node):

                if item.myItemType == item.NoDeCarga:

                    tag_energyConsumer = self.cim_xml.new_tag("EnergyConsumer")
                    self.cim_xml.append(tag_energyConsumer)

                    tag_id = self.cim_xml.new_tag("mRID")
                    tag_id.append(item.no_de_carga.nome)
                    tag_energyConsumer.append(tag_id)

                    tag_pFixed = self.cim_xml.new_tag("pFixed")
                    tag_pFixed.append(str(item.no_de_carga.potencia_ativa))
                    tag_energyConsumer.append(tag_pFixed)


                    tag_qFixed = self.cim_xml.new_tag("qFixed")
                    tag_qFixed.append(str(item.no_de_carga.potencia_reativa))
                    tag_energyConsumer.append(tag_qFixed)


                    for Terminal in (item.terminals):
                        tag_terminal = self.cim_xml.new_tag("terminal")
                        tag_mRID = self.cim_xml.new_tag('mRID')
                        tag_mRID.append(str(Terminal.mRID))
                        tag_terminal.append(tag_mRID)
                        tag_energyConsumer.append(tag_terminal)

        # Percorre toda a lista buscando elementos do tipo Condutor
        for item in scene.items():
            if isinstance(item, Edge):

                if item.w1.myItemType == Node.Subestacao or item.w2.myItemType == Node.Subestacao:
                    continue

                tag_conductor = self.cim_xml.new_tag("Conductor")
                self.cim_xml.append(tag_conductor)

                tag_id = self.cim_xml.new_tag("mRID")

                if item.w1.myItemType == Node.Religador:

                    tag_id.append(item.w1.text.toPlainText() + item.w2.text.toPlainText().split()[0])

                if item.w2.myItemType == Node.Religador:
                    tag_id.append(item.w1.text.toPlainText().split()[0] + item.w2.text.toPlainText())
                else:
                    tag_id.append(item.w1.text.toPlainText().split()[0] + item.w2.text.toPlainText().split()[0])

                tag_conductor.append(tag_id)

                tag_length = self.cim_xml.new_tag("length")
                tag_length.append(str(item.linha.comprimento))
                tag_conductor.append(tag_length)

                tag_r = self.cim_xml.new_tag("r")
                tag_r.append(str(item.linha.resistencia))
                tag_conductor.append(tag_r)

                tag_r0 = self.cim_xml.new_tag("r0")
                tag_r0.append(str(item.linha.resistencia_zero))
                tag_conductor.append(tag_r0)

                tag_x = self.cim_xml.new_tag("x")
                tag_x.append(str(item.linha.reatancia))
                tag_conductor.append(tag_x)

                tag_x0 = self.cim_xml.new_tag("x0")
                tag_x0.append(str(item.linha.reatancia_zero))
                tag_conductor.append(tag_x0)

                tag_currentLimit = self.cim_xml.new_tag("currentLimit")
                tag_currentLimit.append(str(item.linha.ampacidade))
                tag_conductor.append(tag_currentLimit)

                tag_terminal1= self.cim_xml.new_tag("terminal")
                tag_seqNumber = self.cim_xml.new_tag("SequenceNumber")
                tag_seqNumber.append("1")
                tag_terminal1.append(tag_seqNumber)
                tag_mRID = self.cim_xml.new_tag("mRID")
                tag_mRID.append(str(item.terminal1.mRID))
                tag_terminal1.append(tag_mRID)
                tag_conductor.append(tag_terminal1)

                tag_terminal2= self.cim_xml.new_tag("terminal")
                tag_seqNumber = self.cim_xml.new_tag("SequenceNumber")
                tag_seqNumber.append("2")
                tag_terminal2.append(tag_seqNumber)
                tag_mRID = self.cim_xml.new_tag("mRID")
                tag_mRID.append(str(item.terminal2.mRID))
                tag_terminal2.append(tag_mRID)
                tag_conductor.append(tag_terminal2)


        for no in self.lista_no_conectivo:
            tag_mRID = self.cim_xml.new_tag("mRID")
            tag_mRID.append(str(id(no)))

            tag_no_conectivo = self.cim_xml.new_tag("ConnectivityNode")
            tag_no_conectivo.append(tag_mRID)

            self.cim_xml.append(tag_no_conectivo)


            for terminal in no.terminal_list:
                tag_terminal = self.cim_xml.new_tag("terminal")
                tag_mRID_terminal = self.cim_xml.new_tag("mRID")
                tag_mRID_terminal.append(str(terminal.mRID))
                tag_terminal.append(tag_mRID_terminal)
                tag_no_conectivo.append(tag_terminal)



    def write_xml(self, path):
        '''
            Função que cria o arquivo XML na localização indicada pelo
            argumento path
        '''
        soup = BeautifulSoup("<b></b>")
        original_tag = soup.b
        new_tag=self.cim_xml
        original_tag.append(new_tag)

        f = open(path, 'w')
        f.write(original_tag.prettify())
        f.close()

    def check_errors(self):
        noc_to_remove = []
        for noc in self.lista_no_conectivo:
            if noc.terminal_list[0]==noc.terminal_list[1]:
                noc_to_remove.append(noc)
                print("Erro encontrado! Solucionando...")
        for no in noc_to_remove:
            noc.remove(no)



    def montar_rede(self, scene):
        '''
            Função que lê os elementos contidos na scene, os classifica e os divide em listas
            de acordo com a função deles na rede, para então montar a rede seguindo o padrão CIM.
        '''

        # Definir número de terminais de acordo com o tipo de elemento

        for item in self.scene.items():
            if isinstance(item, Node):
                # 1º Caso: elemento é um religador ou uma SE
                if item.myItemType != Node.NoConectivo and item.myItemType != Node.Barra and item.myItemType != Node.NoDeCarga:
                    item.terminal1 = Terminal(item)
                    item.terminal2 = Terminal(item)
                    self.lista_terminais.append(item.terminal1)
                    self.lista_terminais.append(item.terminal2)
                # 2º Caso: elemento é uma barra ou um nó de carga
                if item.myItemType == Node.Barra or item.myItemType == Node.NoDeCarga:
                    for i in range(len(item.edges)):
                        terminal = Terminal(item)
                        item.terminals.append(terminal)
                        self.lista_terminais.append(terminal)

            # 3º Caso: elemento é um condutor
            if isinstance(item, Edge):
                item.terminal1 = Terminal(item)
                item.terminal2 = Terminal(item)
                self.lista_terminais.append(item.terminal1)
                self.lista_terminais.append(item.terminal1)

        # Definição dos nós conectivos
        for edge in self.scene.items():
            if isinstance(edge, Edge):
                no_conectivo_1 = NoConect([])
                no_conectivo_2 = NoConect([])

                # Ligação do Nó Conectivo relativo à ligação do terminal de w1 com o terminal 1 da linha - CONVENÇÃO!
                if edge.w1.myItemType != Node.NoConectivo and edge.w1.myItemType != Node.Barra and edge.w2.myItemType != Node.Barra and edge.w1.myItemType != Node.NoDeCarga:
                    if edge.w1.terminal1.connected:
                        if edge.w1.terminal2.connected:
                            pass
                        else:
                            no_conectivo_1.terminal_list.append(edge.w1.terminal2)
                            edge.w1.terminal2.connect()
                            no_conectivo_1.terminal_list.append(edge.terminal1)
                            edge.terminal1.connect()
                            self.lista_no_conectivo.append(no_conectivo_1)
                    else:
                        no_conectivo_1.terminal_list.append(edge.w1.terminal1)
                        edge.w1.terminal1.connect()
                        no_conectivo_1.terminal_list.append(edge.terminal1)
                        edge.terminal1.connect()
                        self.lista_no_conectivo.append(no_conectivo_1)
                elif edge.w1.myItemType == Node.NoConectivo and edge.w1.con_lock is False:
                    #print("w1 is noC")
                    edge.w1.con_lock = True


                    #print(len(edge.w1.edges))
                    no_conectivo = NoConect([])
                    #print(id(no_conectivo.terminal_list))
                    for derivation in edge.w1.edges:

                        if derivation.terminal1.connected:
                            #print("cp1")
                            if derivation.terminal2.connected:
                                pass
                            else:
                                no_conectivo.terminal_list.append(derivation.terminal2)
                                derivation.terminal2.connect()
                        else:
                            #print("cp2")
                            no_conectivo.terminal_list.append(derivation.terminal1)
                            derivation.terminal1.connect()
                    self.lista_no_conectivo.append(no_conectivo)

                elif edge.w1.myItemType == Node.Barra:
                    for terminal in edge.w1.terminals:
                        no_conectivo = NoConect([])
                        if terminal.connected:
                            continue
                        else:
                            no_conectivo.terminal_list.append(terminal)
                            terminal.connect()
                            if edge.w2.terminal1.connected:
                                if edge.w2.terminal2.connected:
                                    pass
                                else:
                                    no_conectivo.terminal_list.append(edge.w2.terminal2)
                                    edge.w2.terminal2.connect()
                            else:
                                no_conectivo.terminal_list.append(edge.w2.terminal1)
                                edge.w2.terminal1.connect()
                            self.lista_no_conectivo.append(no_conectivo)
                            break

                elif edge.w1.myItemType == Node.NoDeCarga:
                    for terminal in edge.w1.terminals:
                        no_conectivo = NoConect([])
                        if terminal.connected:
                            continue
                        else:
                            if edge.terminal1.connected:
                                if edge.terminal2.connected:
                                    pass
                                else:
                                    no_conectivo.terminal_list.append(terminal)
                                    terminal.connect()
                                    no_conectivo.terminal_list.append(edge.terminal2)
                                    edge.terminal2.connect()
                            else:
                                no_conectivo.terminal_list.append(terminal)
                                terminal.connect()
                                no_conectivo.terminal_list.append(edge.terminal1)
                                edge.terminal1.connect()



                            self.lista_no_conectivo.append(no_conectivo)
                            break

                # Ligação do Nó Conectivo relativo à ligação do terminal de w2 com o terminal 2 da linha - CONVENÇÃO!
                if edge.w2.myItemType != Node.NoConectivo and edge.w2.myItemType != Node.Barra and edge.w1.myItemType != Node.Barra and edge.w2.myItemType != Node.NoDeCarga:
                    #print("w2 is not NoC")
                    if edge.w2.terminal1.connected:
                        if edge.w2.terminal2.connected:
                            pass
                        else:
                            no_conectivo_2.terminal_list.append(edge.w2.terminal2)
                            edge.w2.terminal2.connect()
                            no_conectivo_2.terminal_list.append(edge.terminal2)
                            edge.terminal2.connect()
                            self.lista_no_conectivo.append(no_conectivo_2)
                    else:
                        no_conectivo_2.terminal_list.append(edge.w2.terminal1)
                        edge.w2.terminal1.connect()
                        no_conectivo_2.terminal_list.append(edge.terminal2)
                        edge.terminal1.connect()
                        self.lista_no_conectivo.append(no_conectivo_2)

                elif edge.w2.myItemType == Node.NoConectivo and edge.w2.con_lock is False:
                    #print("w2 is noC")
                    edge.w2.con_lock = True
                    no_conectivo = NoConect([])
                    #print(id(no_conectivo.terminal_list))

                    for derivation in edge.w2.edges:

                        if derivation.terminal1.connected:
                            if derivation.terminal2.connected:
                                pass
                            else:
                                no_conectivo.terminal_list.append(derivation.terminal2)
                                derivation.terminal2.connect()
                        else:
                            no_conectivo.terminal_list.append(derivation.terminal1)
                            derivation.terminal1.connect()

                    self.lista_no_conectivo.append(no_conectivo)

                elif edge.w2.myItemType == Node.Barra:
                    for terminal in edge.w2.terminals:
                        no_conectivo = NoConect([])
                        if terminal.connected:
                            continue
                        else:
                            no_conectivo.terminal_list.append(terminal)
                            terminal.connect()
                            if edge.w1.terminal1.connected:
                                if edge.w1.terminal2.connected:
                                    pass
                                else:
                                    no_conectivo.terminal_list.append(edge.w1.terminal2)
                                    edge.w1.terminal2.connect()
                            else:
                                no_conectivo.terminal_list.append(edge.w1.terminal1)
                                edge.w1.terminal1.connect()
                            self.lista_no_conectivo.append(no_conectivo)
                            break

                elif edge.w2.myItemType == Node.NoDeCarga:
                    for terminal in edge.w2.terminals:
                        no_conectivo = NoConect([])
                        if terminal.connected:
                            continue
                        else:
                            if edge.terminal1.connected:
                                if edge.terminal2.connected:
                                    pass
                                else:
                                    no_conectivo.terminal_list.append(terminal)
                                    terminal.connect()
                                    no_conectivo.terminal_list.append(edge.terminal2)
                                    edge.terminal2.connect()
                            else:
                                no_conectivo.terminal_list.append(terminal)
                                terminal.connect()
                                no_conectivo.terminal_list.append(edge.terminal1)
                                edge.terminal1.connect()
                            self.lista_no_conectivo.append(no_conectivo)
                            break

                self.check_errors()
                #print("end")


        # #print("=========================Lista de Nós Conectivos=========================\n\n")
        # for no in self.lista_no_conectivo:
        #     #print(str(id(no)) + "\n")
        # #print("=========================================================================\n\n")
        # for no in self.lista_no_conectivo:
        #     #print("===============================NÓ CONECTIVO - " + str(id(no)) + "============\n\n")
        #     for no2 in no.terminal_list:
        #         if isinstance(no2.parent, Edge):
        #             #print("terminal: " + str(id(no2)) + "\n" + "objeto: " + "Edge" + "\n" + "Posição: " + str(no2.parent.scenePos()) + "\n")
        #         else:
        #             #print("terminal: " + str(id(no2)) + "\n" + "objeto: " + str(no2.parent.text.toPlainText()) + "\n" + "Posição: " + str(no2.parent.scenePos()) + "\n")
        #     #print("=====================================================================\n\n")

        # #raw_input("Press enter to complete conversion.")

        # #print("--------------------------------------------------------------------------")

def carregar_dados(scene):

    chaves_dados=list()
    nos_dados=list()
    transformadores_dados=list()
    busbar_dados=list()
    condutores_dados1=list()
    condutores_dados=list()

    for item in scene.items():
        if isinstance(item, Node):
            if item.myItemType == Node.Religador:
                chave_lista=OrderedDict()
                chave_lista['nome']= item.text.toPlainText()
                chave_lista['estado']=int(item.chave.normalOpen)^1
                chave_lista['ids']=str(item.id)
                chaves_dados.append(chave_lista)

            if item.myItemType == Node.NoDeCarga:
                no=OrderedDict()
                no['nome']=str(item.text.toPlainText().split()[0])
                no['p']=float(str(item.no_de_carga.potencia_ativa))
                no['q']=float(str(item.no_de_carga.potencia_reativa))
                no['ids']=str(item.id)
                nos_dados.append(no)

            if item.myItemType == Node.Subestacao:
                trafo=OrderedDict()
                trafo['nome']=str(item.text.toPlainText())
                trafo['n_trafo']=float(item.substation.n_transformadores)
                trafo['tensao_p']=float(item.substation.tensao_primario)
                trafo['tensao_s']=float(item.substation.tensao_secundario)
                trafo['potencia']=float(item.substation.potencia)
                trafo['r']=float(item.substation.r_pos)
                trafo['x']=float(item.substation.i_pos)
                trafo['r0']=float(item.substation.r_zero)
                trafo['x0']=float(item.substation.i_zero)
                trafo['ids']=str(item.id)
                transformadores_dados.append(trafo)

            if item.myItemType == Node.Barra:

                bus=OrderedDict()
                bus['nome']=str(item.text.toPlainText())
                bus['fase']=float(item.barra.phases)
                bus['r']=float(item.barra.r_pos)
                bus['x']=float(item.barra.i_pos)
                bus['r0']=float(item.barra.r_zero)
                bus['x0']=float(item.barra.i_zero)
                bus['ids']=str(item.id)
                busbar_dados.append(bus)


        elif isinstance(item, Edge):
          

            tag_id = ''

            if item.w1.myItemType == Node.Religador:

                tag_id=(item.w1.text.toPlainText() + item.w2.text.toPlainText().split()[0])

            if item.w2.myItemType == Node.Religador:
                tag_id=(item.w1.text.toPlainText().split()[0] + item.w2.text.toPlainText())

            else:
                tag_id=(item.w1.text.toPlainText().split()[0] + item.w2.text.toPlainText().split()[0])
            
            condutor=OrderedDict()
            condutor['nome']=str(tag_id)
            condutor['comprimento']=float(item.linha.comprimento)
            condutor['r']=float(item.linha.resistencia)
            condutor['x']=float(item.linha.reatancia)
            condutor['r0']=float(item.linha.resistencia_zero)
            condutor['x0']=float(item.linha.reatancia_zero)
            condutor['ampacidade']=float(item.linha.ampacidade)
            condutor['condutor']=str(tag_id)
            condutor['n1_id']=str(item.w1.id)
            condutor['n2_id']=str(item.w2.id)
            condutores_dados.append(condutor)
            condutores_dados1.append(condutor)



        





    

    dados_rede={}
    dados_rede['chaves']=chaves_dados
    dados_rede['busbar']=busbar_dados
    dados_rede['trafos']=transformadores_dados
    dados_rede['condutor']=condutores_dados1
    dados_rede['condutores']=condutores_dados
    condutores_dados
    dados_rede['nos']=nos_dados
    print('Carregou')
    return dados_rede
    



def gerar_trechos(data):
    nos=data['nos']
    chaves=data['chaves']
    inicio_caminho=data['busbar']
    condutor=data['condutor']
    trechos=list()
    trechos_inter=list()
    alimentador={}
    chaves_nomes=[]
    delete=list()

    for i in nos:
        print(i['nome'])
    a=0
    for i in inicio_caminho:
        for j in condutor:
            if i['ids']==j['n1_id']:
                a=+1
                for k in chaves:
                    if k['ids']==j['n2_id']:
                        #print(i['nome'],j['nome'],k['nome'])
                        trecho=OrderedDict()
                        trecho['nome']=j['nome']
                        trecho['n1']=i['nome']
                        trecho['n2']=k['nome']
                        trecho['setor']=i['nome']
                        trecho['comprimento']=10
                        trecho['alimentador']=i['nome']+'_al'+str(a)
                        trecho['condutor']= j['nome']
                        trecho['id2']=k['ids']
                        #trecho['flag']=0
                        trechos.append(trecho)
                        delete.append(j)
                        
                        

            elif i['ids']==j['n2_id']:
                for k in chaves:
                    if k['ids']==j['n1_id']:
                        #print(i['nome'],j['nome'],k['nome'])
                        trecho=OrderedDict()
                        trecho['nome']=j['nome']
                        trecho['n1']=i['nome']
                        trecho['n2']=k['nome']
                        trecho['setor']=i['nome']
                        trecho['comprimento']=10
                        trecho['alimentador']=i['nome']+'_al'+str(a)
                        trecho['condutor']= j['nome']
                        trecho['id2']=k['ids']
                        trecho['flag']=None
                        trechos.append(trecho)
                        delete.append(j)
            
            if j['nome']==i['nome']+i['nome']:
                delete.append(j)
                        

    for i in delete:
        condutor.remove(i)

    

    for i in chaves:
        chaves_nomes.append(i['nome'])

    condutor_nome=list()
    for i in condutor:
        condutor_nome.append(i['nome'])



    trechos_inter=trechos
    
    while condutor != []:
        for i in trechos_inter:
            a=list()
            for j in condutor:
                if i['id2']==j['n1_id']:
                    
                    trecho=OrderedDict()
                    trecho['nome']=j['nome']
                    trecho['n1']=i['n2']
                    n2,id2=descubra(j['n2_id'],chaves,nos,condutor,j['n1_id'])
                    trecho['n2']=n2

                    setor=define_setores(i['n2'],n2,chaves_nomes)
                    trecho['setor']=setor
                    trecho['comprimento']=j['comprimento']
                    trecho['alimentador']=i['alimentador']
                    trecho['condutor']=j['nome']

                 
                    trecho['id2']=id2
                    a.append(trecho)
                    condutor.remove(j)
                    


                elif i['id2']==j['n2_id']:
                    trecho=OrderedDict()
                    trecho['nome']=j['nome']
                    trecho['n1']=i['n2']
                    n2,id2=descubra(j['n1_id'],chaves,nos,condutor,j['n2_id'])
                    trecho['n2']=n2

                    setor=define_setores(i['n2'],n2,chaves_nomes)
                    trecho['setor']=setor
                    trecho['comprimento']=j['comprimento']
                    trecho['alimentador']=i['alimentador']
                    trecho['condutor']=j['nome']

                    trecho['id2']=id2
                    a.append(trecho)
                    condutor.remove(j)
                        

                
                
                if trechos_inter==[]:
                    break
                else:
                    for i in a:
                        if i not in trechos:
                            trechos.append(i)

    
    return trechos

def descubra(n2,chaves,nos,condutor,n1):


    for i in nos:
        if n2 == i['ids']:
            return i['nome'],n2

   
    for i in chaves:
        if n2==i['ids']:
            if i['estado']==1:
                return i['nome'],n2
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
            sub= mygrid.grid.Substation(name=nome,feeders=aliment,transformers=transformador)
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
def start_conversion(scene):


    data=carregar_dados(scene)
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
        

    #a=pd.DataFrame(trechos_lista,columns=trechos_colunas)
    # a.to_excel(writer,'Trechos')
    # writer.sheets['Trechos'].set_column('B:J', 20)
    tabela['trechos']=trechos_lista
    # writer.save()



    return tabela
