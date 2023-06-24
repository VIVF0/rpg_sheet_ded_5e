from database import mydb,attributes
from src import Usuario
import pymysql

class Personagem(Usuario):
    def __init__(self, id_usuario,id_personagem):
        super().__init__(id=id_usuario)
        self._id_personagem = id_personagem
        self._nome_personagem=None
        self._classe = []
        self._raca = None
        self._salvaguardas = []
        self._feitico = []
        self._armas=[]
        self._equipamentos=[]
        self._caracteristicas = {
            'idade': None,
            'altura': None,
            'peso': None,
            'cor dos olhos': None,
            'cor da pele': None,
            'cor do cabelo': None,
            'imagem_personagem':None
        }
        self._pericias=[]
        self._bonus_proficiencia = None
        self._atributos = {
            'forca': None,
            'destreza': None,
            'contituicao': None,
            'inteligencia': None,
            'sabedoria': None,
            'carisma': None
        }
        self._alinhamento = None
        self._antecendente = None
        self._ca = None
        self._deslocamento = None
        self._faccao = None
        self._inspiracao = None
        self._iniciativa = None
        self._nivel = None
        self._vida = None
        self._vida_atual = None
        self._vida_temporaria = None
        self._xp = None
#-----------------------------------------------BASE----------------------------------------------- 
    def adicionar_classe_banco(self,id_classe):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """INSERT INTO classe_personagem
                (id_personagem,id_classe) 
                VALUES(%s,%s);"""
                mycursor.execute(query, (self._id_personagem,id_classe))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    def update_classe_banco(self,id_classe,id_classe_personagem):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """UPDATE classe_personagem
                SET id_classe=%s
                WHERE id_classe_personagem=%s"""
                mycursor.execute(query, (id_classe,id_classe_personagem))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    def carregar_classe_do_banco(self):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """SELECT cp.id_classe, cl.nome_classe,cp.id_classe_personagem
                FROM classe_personagem cp, classe cl
                WHERE cp.id_personagem = %s and cp.id_classe=cl.id_classe;"""
                mycursor.execute(query, (self._id_personagem))
                result = mycursor.fetchone()
                if result:
                    for row in result:
                        self.classe({'id_classe_personagem':row[2],'id_classe':row[0],'nome_classe':row[1]})
                    return True
            return False
        except Exception as e:
            print(e)
            return False
        
    @property
    def classe(self):
        return self._classe

    @classe.setter
    def classe(self, value):
        self._classe.append(value)
        
    def carregar_personagem_banco(self):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """SELECT pr.nome_personagem,rc.nome_raca
                FROM personagem pr,raca rc
                WHERE pr.id_usuario = %s and pr.id_raca=rc.id_raca;"""
                mycursor.execute(query, (self._id))
                result = mycursor.fetchone()
                if result:
                    for row in result:
                        self.nome_personagem=row[0]
                        self.raca=row[1]
                    return True
            return False
        except Exception as e:
            print(e)
            return False
        
    @property
    def nome_personagem(self):
        return self._nome_personagem
        
    @nome_personagem.setter
    def nome_personagem(self,value):
        self._nome_personagem=value
        
    def update_personagem_banco(self,chave,valor):
        try:
            possibilidades_chave=['id_raca','nome_personagem']
            if self._id_personagem and chave in possibilidades_chave:
                mycursor = mydb.cursor()
                query = f"""UPDATE personagem
                SET {chave}=%s
                WHERE id_personagem=%s;"""
                mycursor.execute(query, (valor,self._id_personagem))
                mydb.commit()
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    @property
    def raca(self):
        return self._raca
    
    @raca.setter
    def raca(self,value):
        self._raca=value
#-----------------------------------------------EQUIPAMENTOS-----------------------------------------------

#-----------------------------------------------STATUS_BASE-----------------------------------------------   
    def adicionar_status_base_banco(self,vida=0,xp=0,nivel=0,alinhamento=None,antecendente=None,faccao=None,inspiracao=0,ca=0,iniciativa=0,deslocamento=0,vida_atual=0,vida_temporaria=0):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """INSERT INTO status_base
                (id_personagem,vida,xp,nivel,alinhamento,antecendente,faccao,inspiracao,ca,iniciativa,deslocamento,vida_atual,vida_temporaria) 
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
                mycursor.execute(query, (self._id_personagem,vida,xp,nivel,alinhamento,antecendente,faccao,inspiracao,ca,iniciativa,deslocamento,vida_atual,vida_temporaria))
                mydb.commit()
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    def carregar_status_base_do_banco(self):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """SELECT vida,xp,nivel,alinhamento,antecendente,faccao,inspiracao,ca,iniciativa,deslocamento,vida_atual,vida_temporaria
                FROM status_base
                WHERE id_personagem = %s;"""
                mycursor.execute(query, (self._id_personagem))
                result = mycursor.fetchone()
                if result:
                    for row in result:
                        self.vida=row[0]
                        self.xp=row[1]
                        self.nivel=row[2]
                        self.alinhamento=row[3] 
                        self.antecendente=row[4] 
                        self.faccao=row[5]  
                        self.inspiracao=row[6]
                        self.set_ca=row[7]
                        self.iniciativa[8]
                        self.deslocamento=row[9]
                        self.vida_atual=row[10]
                        self.vida_temporaria=row[11]     
                    return True
            return False
        except Exception as e:
            print(e)
            return False
        
    def update_status_base_banco(self,chave,valor):
        try:
            possibilidades_chave=['vida','xp','nivel','alinhamento','antecendente','faccao','inspiracao','ca','iniciativa','deslocamento','vida_atual','vida_temporaria']
            if self._id_personagem and chave in possibilidades_chave:
                mycursor = mydb.cursor()
                query = f"""UPDATE status_base
                SET {chave}=%s
                WHERE id_personagem=%s;"""
                parametros=(valor,self._id_personagem)
                mycursor.execute(query, parametros)
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    @property
    def nivel(self):
        return self._nivel
    
    @nivel.setter
    def nivel(self,value):
        self._nivel=value
    
    @property
    def alinhamento(self):
        return self._alinhamento
    
    @alinhamento.setter
    def alinhamento(self,value):
        self._alinhamento=value
        
    @property
    def faccao(self):
        return self._faccao        
         
    @faccao.setter
    def faccao(self,value):
        self._faccao=value
        
    @property
    def antecendente(self):
        return self._antecendente        
         
    @antecendente.setter
    def antecendente(self,value):
        self._antecendente=value
    
    @property
    def xp(self):
        return self._xp
                
    @xp.setter
    def xp(self,value):
        self._xp=value
           
    @property
    def deslocamento(self):
        return self._deslocamento
    
    @deslocamento.setter
    def deslocamento(self,value):
        self._deslocamento=value
        
    @property
    def iniciativa(self):
        return self._iniciativa
    
    @iniciativa.setter
    def iniciativa(self,value):
        self._iniciativa=value
    
    @property
    def vida(self):
        return self._vida
    
    @vida.setter
    def vida(self,value):
        self._vida=value
        
    @property
    def vida_atual(self):
        return self._vida_atual
    
    @vida_atual.setter
    def vida_atual(self,value):
        self._vida_atual=value
       
    @property
    def vida_temporaria(self):
        return self._vida_temporaria
    
    @vida_temporaria.setter
    def vida_temporaria(self,value):
        self._vida_temporaria=value
        
    @property
    def inspiracao(self):
        return self._inspiracao
    
    @inspiracao.setter
    def inspiracao(self,value):
        self._inspiracao=value
    
    @property
    def ca(self):
        return self._ca
    
    @ca.setter
    def ca(self,value):
        self._ca=value   
#-----------------------------------------------HABILIDADES----------------------------------------------- 
    def adicionar_feitico_banco(self,id_feitico):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = "INSERT INTO feitico_personagem(id_personagem,id_feitico) VALUES(%s,%s);"
                mycursor.execute(query, (self._id_personagem,id_feitico))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    def carregar_feitico_do_banco(self):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """SELECT fp.id_feitico, ft.nome_feitico, ft.tipo_feitico, td.nome_tipo,fp.id_feitico_personagem
                FROM feitico_personagem fp
                JOIN feitico ft ON fp.id_feitico = ft.id_feitico
                JOIN tipo_dano td ON ft.id_tipo_dano = td.id_tipo_dano
                WHERE fp.id_personagem = %s;"""
                mycursor.execute(query, (self._id_personagem))
                result = mycursor.fetchall()
                if result:
                    for row in result:
                        feitico = {
                            'id_feitico_personagem':row[4],
                            'id_feitico': row[0],
                            'nome_feitico': row[1],
                            'tipo_feitico': row[2],
                            'tipo_dano':row[3]
                        }
                        self.feitico(feitico)               
                    return True
            return False
        except Exception as e:
            print(e)
            return False
        
    def update_feitico_banco(self,novo_feitico,id_feitico_personagem):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """UPDATE feitico_personagem
                SET id_feitico=%s
                WHERE id_feitico_personagem=%s;"""
                mycursor.execute(query, (novo_feitico,id_feitico_personagem))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    @property
    def feitico(self,value):
        return self._feitico[value]
    
    @property
    def feiticos(self):
        return self._feitico  
    
    @feitico.setter
    def feitico(self,value):
        self._feitico.append(value)      
#-----------------------------------------------ATRIBUTOS-----------------------------------------------
    def adicionar_atributos_banco(self,forca,destreza,constituicao,inteligencia,sabedoria,carisma,bonus_proficiencia):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = "INSERT INTO atributos(id_personagem,forca,destreza,constituicao,inteligencia,sabedoria,carisma,bonus_proficiencia) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"
                mycursor.execute(query, (self._id_personagem,forca,destreza,constituicao,inteligencia,sabedoria,carisma,bonus_proficiencia))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    def carregar_atributos_do_banco(self):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """SELECT forca,destreza,constituicao,inteligencia,sabedoria,carisma,bonus_proficiencia 
                FROM atributos WHERE id_personagem = %s"""
                mycursor.execute(query, (self._id_personagem))
                result = mycursor.fetchone() 
                for row in result:
                    self.set_forca(row[0])
                    self.set_destreza(row[1])
                    self.set_constituicao(row[2])
                    self.set_inteligencia(row[3])
                    self.set_sabedoria(row[4])
                    self.set_carisma(row[5])
                    self.bonus_proficiencia(row[6])
                return True
            return False
        except Exception as e:
            print(e)
            return False
    
    def update_atributos_banco(self,chave,valor):
        try:
            possibilidade_chave=['forca','destreza','constituicao','inteligencia','sabedoria','carisma','bonus_proficiencia' ]
            if self._id_personagem and chave in possibilidade_chave:
                mycursor = mydb.cursor()
                query = f"""UPDATE atributos
                SET {chave}=%s
                WHERE id_personagem=%s;"""
                parametros=(valor,self._id_personagem)
                mycursor.execute(query, parametros)
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    @property
    def bonus_proficiencia(self):
        return self._bonus_proficiencia
    
    @bonus_proficiencia.setter
    def bonus_proficiencia(self,value):
        self._bonus_proficiencia=value
    
    @property
    def forca(self):
        if self._atributos['forca'] is None:
            return 0
        return self._atributos['forca']
    
    @property
    def bonus_forca(self):
        return attributes.loc[self._atributos['forca']]
    
    def set_forca(self, value):
        self._atributos['forca'] = value
        
    @property
    def destreza(self):
        if self._atributos['destreza'] is None:
            return 0
        return self._atributos['destreza']
    
    @property
    def bonus_destreza(self):
        return attributes.loc[self._atributos['destreza']]
    
    def set_destreza(self,value):
        self._atributos['destreza']=value
    
    @property
    def constituicao(self):
        if self._atributos['constituicao'] is None:
            return 0
        return self._atributos['constituicao']
    
    @property
    def bonus_constituicao(self):
        return attributes.loc[self._atributos['constituicao']]
           
    def set_constituicao(self,value):
        self._atributos['constituicao']=value
    
    @property
    def inteligencia(self):
        if self._atributos['inteligencia'] is None:
            return 0
        return self._atributos['inteligencia']
    
    @property
    def bonus_inteligencia(self):
        return attributes.loc[self._atributos['inteligencia']]
    
    def set_inteligencia(self,value):
        self._atributos['inteligencia']=value
    
    @property
    def sabedoria(self):
        if self._atributos['sabedoria'] is None:
            return 0
        return self._atributos['sabedoria']
    
    @property
    def bonus_sabedoria(self):
        return attributes.loc[self._atributos['sabedoria']]
     
    def set_sabedoria(self,value):
        self._atributos['sabedoria']=value
    
    @property
    def carisma(self):
        if self._atributos['carisma'] is None:
            return 0
        return self._atributos['carisma']
    
    @property
    def bonus_carisma(self):
        return attributes.loc[self._atributos['carisma']]
    
    def set_carisma(self,value):
        self._atributos['carisma']=value
#-----------------------------------------------CARACTERISTICAS----------------------------------------------- 
    def adicionar_caracteristicas_banco(self,idade,cor_olhos,cor_pele,cor_cabelo,peso,altura,imagem_personagem):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """INSERT INTO caracteristicas_personagem
                (id_personagem,idade,cor_olhos,cor_pele,cor_cabelo,peso,altura,imagem_personagem) 
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"""
                mycursor.execute(query, (self._id_personagem,idade,cor_olhos,cor_pele,cor_cabelo,peso,altura,imagem_personagem))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    def carregar_caracteristicas_do_banco(self):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = "SELECT idade,cor_olhos,cor_pele,cor_cabelo,peso,altura,imagem_personagem FROM caracteristicas_personagem WHERE id_personagem = %s"
                mycursor.execute(query, (self._id_personagem))
                result = mycursor.fetchone() 
                for row in result:
                    self.set_idade=row[0]
                    self.set_cor_olhos=row[1]
                    self.set_cor_pele=row[2]
                    self.set_cor_cabelo=row[3]
                    self.set_peso=row[4]
                    self.set_altura=row[5]
                    self.set_imagem_personagem=row[6]
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    def update_caracteristicas_banco(self,chave,valor):
        try:
            possibilidade_chave=['idade','cor_olhos','cor_pele','cor_cabelo','peso','altura','imagem_personagem']
            if self._id_personagem and chave in possibilidade_chave:
                mycursor = mydb.cursor()
                query = f"""UPDATE caracteristicas_personagem
                SET {chave}=%s
                WHERE id_personagem=%s;"""
                parametros=(valor,self._id_personagem)
                mycursor.execute(query, parametros)
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    def set_idade(self,value):
        self._caracteristicas['idade']=value
    
    @property
    def idade(self):
        self._caracteristicas['idade']
    
    def set_altura(self,value):
        self._caracteristicas['altura']=value
        
    @property
    def altura(self):
        return self._caracteristicas['altura']
    
    def set_peso(self,value):
        self._caracteristicas['peso']=value
    
    @property
    def peso(self):
        return self._caracteristicas['peso']
    
    def set_cor_olhos(self,value):
        self._caracteristicas['cor dos olhos']=value
        
    @property
    def cor_olhos(self):
        return self._caracteristicas['cor dos olhos']
    
    def set_cor_pele(self,value):
        self._caracteristicas['cor da pele']=value
    
    @property
    def cor_pele(self):
        return self._caracteristicas['cor da pele']
    
    def set_cor_cabelo(self,value):
        self._caracteristicas['cor do cabelo']=value
    
    @property
    def cor_cabelo(self):
        return self._caracteristicas['cor do cabelo']  
    
    def set_imagem_personagem(self,value):
        self._caracteristicas['imagem_personagem']=value
        
    @property
    def imagem_personagem(self):
        return self._caracteristicas['imagem_personagem']
#-----------------------------------------------SALVAGUARDAS-----------------------------------------------
    def adicionar_salvaguardas_banco(self,id_salvaguarda):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = "INSERT INTO salvaguarda_personagem(id_personagem,id_salvaguarda) VALUES(%s,%s);"
                mycursor.execute(query, (self._id_personagem,id_salvaguarda))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    def carregar_salvaguardas_do_banco(self):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = "SELECT sp.id_salvaguarda,sp.nome_salvaguarda,sp.id_salvaguarda_personagem FROM salvaguarda_personagem sp,salvaguarda sl WHERE sp.id_personagem = %s and sl.id_salvaguarda=sp.id_salvaguarda"
                mycursor.execute(query, (self._id_personagem))
                result = mycursor.fetchall() 
                for row in result:
                    self.salvaguardas({'id_salvaguarda_personagem':row[2],'id_salvaguarda':row[0],'nome_salvaguarda':row[0]})
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    def update_salvaguardas_banco(self,id_salvaguarda,id_salvaguarda_personagem):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """UPDATE salvaguarda_personagem
                SET id_salvaguarda=%s
                WHERE id_salvaguarda_personagem=%s;"""
                mycursor.execute(query, (id_salvaguarda,id_salvaguarda_personagem))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    @property
    def salvaguardas(self):
        return self._salvaguardas

    @salvaguardas.setter
    def salvaguardas(self, value):
        self._salvaguardas.append(value)

    @property
    def resistencia_forca(self):
        if any(d.get('nome_salvaguarda') == 'forca' for d in self._salvaguardas):
            return self._atributos['forca']+self._bonus_proficiencia
        return self._atributos['forca']
    
    @property
    def resistencia_destreza(self):
        if any(d.get('nome_salvaguarda') == 'destreza' for d in self._salvaguardas):
            return self._atributos['destreza']+self._bonus_proficiencia
        return self._atributos['destreza']
    
    @property
    def resistencia_constituicao(self):
        if any(d.get('nome_salvaguarda') == 'constituicao' for d in self._salvaguardas):
            return self._atributos['constituicao']+self._bonus_proficiencia
        return self._atributos['constituicao']
    
    @property
    def resistencia_inteligencia(self):
        if any(d.get('nome_salvaguarda') == 'inteligencia' for d in self._salvaguardas):
            return self._atributos['inteligencia']+self._bonus_proficiencia
        return self._atributos['inteligencia']
    
    @property
    def resistencia_sabedoria(self):
        if any(d.get('nome_salvaguarda') == 'sabedoria' for d in self._salvaguardas):
            return self._atributos['sabedoria']+self._bonus_proficiencia
        return self._atributos['sabedoria']
    
    @property
    def resistencia_carisma(self):
        if any(d.get('nome_salvaguarda') == 'carisma' for d in self._salvaguardas):
            return self._atributos['carisma']+self._bonus_proficiencia
        return self._atributos['carisma']
#-----------------------------------------------PERICIAS-----------------------------------------------
    def adicionar_pericias_banco(self,id_pericia):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = "INSERT INTO pericia_personagem(id_personagem,id_pericia) VALUES(%s,%s);"
                mycursor.execute(query, (self._id_personagem,id_pericia))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    def carregar_pericias_do_banco(self):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """SELECT pp.id_pericia, pc.nome_pericia, pc.status_uso,pp.id_pericia_personagem 
                FROM pericia_personagem pp 
                JOIN pericia pc ON pp.id_pericia = pc.id_pericia 
                WHERE pp.id_personagem = %s;"""
                mycursor.execute(query, (self._id_personagem,))
                result = mycursor.fetchall() 
                for row in result:
                    self.set_pericias({'id_pericia_personagem':row[3],'id_pericia': row[0], 'nome_pericia': row[1], 'status_uso': row[2]})
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    def update_pericias_banco(self,id_pericia,id_pericia_personagem):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """UPDATE pericia_personagem
                SET id_pericia=%s
                WHERE id_pericia_personagem=%s;"""
                mycursor.execute(query, (id_pericia,id_pericia_personagem))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False

    @property
    def pericias(self):
        return self._pericias

    @pericias.setter
    def pericias(self, value):
        self._pericias.append(value)
        
    @property
    def acrobacia(self):
        if any(d.get('nome_pericia') == 'destreza' for d in self._pericias):
            return self._atributos['destreza'] + self._bonus_proficiencia
        return self._atributos['destreza']

    @property
    def arcanismo(self):
        if any(d.get('nome_pericia') == 'inteligencia' for d in self._pericias):
            return self._atributos['inteligencia'] + self._bonus_proficiencia
        return self._atributos['inteligencia']

    @property
    def atletismo(self):
        if any(d.get('nome_pericia') == 'forca' for d in self._pericias):
            return self._atributos['forca'] + self._bonus_proficiencia
        return self._atributos['forca']

    @property
    def atuacao(self):
        if any(d.get('nome_pericia') == 'carisma' for d in self._pericias):
            return self._atributos['carisma'] + self._bonus_proficiencia
        return self._atributos['carisma']

    @property
    def enganacao(self):
        if any(d.get('nome_pericia') == 'carisma' for d in self._pericias):
            return self._atributos['carisma'] + self._bonus_proficiencia
        return self._atributos['carisma']

    @property
    def furtividade(self):
        if any(d.get('nome_pericia') == 'destreza' for d in self._pericias):
            return self._atributos['destreza'] + self._bonus_proficiencia
        return self._atributos['destreza']

    @property
    def historia(self):
        if any(d.get('nome_pericia') == 'inteligencia' for d in self._pericias):
            return self._atributos['inteligencia'] + self._bonus_proficiencia
        return self._atributos['inteligencia']

    @property
    def intimidacao(self):
        if any(d.get('nome_pericia') == 'carisma' for d in self._pericias):
            return self._atributos['carisma'] + self._bonus_proficiencia
        return self._atributos['carisma']

    @property
    def intuicao(self):
        if any(d.get('nome_pericia') == 'sabedoria' for d in self._pericias):
            return self._atributos['sabedoria'] + self._bonus_proficiencia
        return self._atributos['sabedoria']

    @property
    def investigacao(self):
        if any(d.get('nome_pericia') == 'inteligencia' for d in self._pericias):
            return self._atributos['inteligencia'] + self._bonus_proficiencia
        return self._atributos['inteligencia']

    @property
    def lidar_com_animais(self):
        if any(d.get('nome_pericia') == 'sabedoria' for d in self._pericias):
            return self._atributos['sabedoria'] + self._bonus_proficiencia
        return self._atributos['sabedoria']

    @property
    def medicina(self):
        if any(d.get('nome_pericia') == 'sabedoria' for d in self._pericias):
            return self._atributos['sabedoria'] + self._bonus_proficiencia
        return self._atributos['sabedoria']

    @property
    def natureza(self):
        if any(d.get('nome_pericia') == 'inteligencia' for d in self._pericias):
            return self._atributos['inteligencia'] + self._bonus_proficiencia
        return self._atributos['inteligencia']

    @property
    def percepcao(self):
        if any(d.get('nome_pericia') == 'sabedoria' for d in self._pericias):
            return self._atributos['sabedoria'] + self._bonus_proficiencia
        return self._atributos['sabedoria']

    @property
    def persuasao(self):
        if any(d.get('nome_pericia') == 'carisma' for d in self._pericias):
            return self._atributos['carisma'] + self._bonus_proficiencia
        return self._atributos['carisma']

    @property
    def prestidigitacao(self):
        if any(d.get('nome_pericia') == 'destreza' for d in self._pericias):
            return self._atributos['destreza'] + self._bonus_proficiencia
        return self._atributos['destreza']

    @property
    def religiao(self):
        if any(d.get('nome_pericia') == 'inteligencia' for d in self._pericias):
            return self._atributos['inteligencia'] + self._bonus_proficiencia
        return self._atributos['inteligencia']

    @property
    def sobrevivencia(self):
        if any(d.get('nome_pericia') == 'sabedoria' for d in self._pericias):
            return self._atributos['sabedoria'] + self._bonus_proficiencia
        return self._atributos['sabedoria']