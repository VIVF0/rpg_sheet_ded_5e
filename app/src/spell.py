import asyncio
from src import Db

class Spell:
    def __init__(self, spell_id = None, attribute_use = None, side_dice = None, description_spell = None, spell_name = None, type_damage_id = None, amount_dice = None, spell_level = None, add_per_level = None):
        self._spell_id = spell_id or []
        self._attribute_use = attribute_use or []
        self._spell_name = spell_name or []
        self._spell_level = spell_level or []
        self._type_damage_name = []
        self._amount_dice = amount_dice or []
        self._side_dice = side_dice or []
        self._add_per_level = add_per_level or [] 
        self._description_spell = description_spell or []
        self.__character_has_spell = []
        self.__type_damage_id = type_damage_id
        
    async def load_character_spells(self, character_id):
        try:
            if character_id:
                query = """SELECT sp.spell_id, sp.attribute_use, sp.spell_name, sp.spell_level, td.type_damage_name, sp.amount_dice, sp.side_dice, sp.add_per_level, sp.description_spell, CASE WHEN cs.character_spell_id IS NOT NULL THEN TRUE ELSE FALSE END AS has
                FROM spell sp
                INNER JOIN type_damage td ON sp.type_damage_id = td.type_damage_id
                LEFT JOIN character_spell cs ON sp.spell_id = cs.spell_id AND cs.character_id = %s;"""
                parameters = (character_id,)
                db = Db()
                await db.connection_db()
                result = await db.select(query=query, parameters=parameters)
                if result:
                    for row in result:
                        self._spell_id.append(row[0])
                        self._attribute_use.append(row[1])
                        self._spell_name.append(row[2])
                        self._spell_level.append(row[3])
                        self._type_damage_name.append(row[4])
                        self._amount_dice.append(row[5])
                        self._side_dice.append(row[6])
                        self._add_per_level.append(row[7])
                        self._description_spell.append(row[8])
                        self.__character_has_spell.append(row[9])              
                    return True
            return False
        except Exception as e:
            print(e)
            return False
        
    @property
    async def spells(self):
        if (type(self._spell_id) is list and len(self._spell_id)<=0) or (self._spell_id is None):
            await self.load_spells()
        spells = []
        for spell_id, attribute_use, spell_name, spell_level, type_damage_name, amount_dice, side_dice, add_per_level, description_spell, character_has_spell in zip(self._spell_id, self._attribute_use, self._spell_name, self._spell_level, self._type_damage_name, self._amount_dice, self._side_dice, self._add_per_level, self._description_spell, self.__character_has_spell):
            spells.append({
                'spell_id': spell_id, 
                'attribute_use': attribute_use, 
                'spell_name': spell_name, 
                'spell_level': spell_level, 
                'type_damage_name': type_damage_name, 
                'amount_dice': amount_dice, 
                'side_dice': side_dice, 
                'add_per_level': add_per_level, 
                'description_spell': description_spell,
                'character_has': character_has_spell 
            })
        return spells
    
    @property
    async def spell(self):
        if self._spell_id is None:
            await self.load_spell()
        spell = {
            'spell_id': self.spell_id, 
            'attribute_use': self.attribute_use, 
            'spell_name': self.spell_name, 
            'spell_level': self.spell_level, 
            'type_damage_name': self.type_damage_name, 
            'amount_dice': self.amount_dice, 
            'side_dice': self.side_dice, 
            'add_per_level': self.add_per_level, 
            'description_spell': self.description_spell
        }
        return spell
   
    async def load_spells(self):
        try:
            query = """SELECT sp.spell_id, sp.attribute_use, sp.spell_name, sp.spell_level, td.type_damage_name, sp.amount_dice, sp.side_dice, sp.add_per_level, sp.description_spell 
            FROM spell sp, type_damage td
            WHERE SP.type_damage_id = td.type_damage_id
            ;"""
            db = Db()
            await db.connection_db()
            result = await db.select(query=query)
            if result:
                for row in result:
                    self._spell_id.append(row[0])
                    self._attribute_use.append(row[1])
                    self._spell_name.append(row[2])
                    self._spell_level.append(row[3])
                    self._type_damage_name.append(row[4])
                    self._amount_dice.append(row[5])
                    self._side_dice.append(row[6])
                    self._add_per_level.append(row[7])
                    self._description_spell.append(row[8])
                return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def load_spell(self):
        try:
            query = "SELECT spell_id, attribute_use, spell_name, spell_level, type_damage_name, amount_dice, side_dice, add_per_level, description_spell FROM spell WHERE spell_id=%s;"
            parameters = (self._spell_id,)
            db = Db()
            await db.connection_db()
            result = await db.select(query=query, parameters=parameters, all=False)
            if result:
                self._spell_id = result[0]
                self._attribute_use = result[1]
                self._spell_name = result[2]
                self._spell_level = result[3]
                self._type_damage_name = result[4]
                self._amount_dice = result[5]
                self._side_dice = result[6]
                self._add_per_level = result[7]
                self._description_spell = result[8]
                return True
            return False
        except Exception as e:
            print(e)
            return False

    async def insert_spell(self):
        try:
            query = "INSERT INTO spell (attribute_use, spell_name, spell_level, type_damage_id, amount_dice, side_dice, add_per_level, description_spell) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING spell_id;;"
            parameters = (self.attribute_use, self.spell_name, self.spell_level, self.type_damage_id, self.amount_dice, self.side_dice, self.add_per_level, self.description_spell)
            db = Db()
            await db.connection_db()
            self.character_spell_id = await db.insert(query=query, parameters=parameters)  
            return True
        except Exception as e:
            print(e)
            return False

    async def delete_spell(self):
        try:
            if self.spell_id:
                query = """DELETE from spell
                WHERE spell_id=%s;"""
                parameters = (self._spell_id,)
                db = Db()
                await db.connection_db()
                return await db.delete(query=query, parameters=parameters)  
            return False
        except Exception as e:
            print(e)
            return False
        
    async def update_spell(self, key, value):
        try:
            possible_key = ['spell_id', 'attribute_use', 'spell_name', 'spell_level', 'type_damage_id', 'amount_dice', 'side_dice', 'add_per_level', 'description_spell']
            if key in possible_key:
                query = f"""UPDATE habilidade SET {key}=%s WHERE spell_id=%s;"""
                parameters = (value, self._spell_id)
                db = Db()
                await db.connection_db()
                return await db.update(query=query, parameters=parameters) 
            return False
        except Exception as e:
            print(e)
            return False 
        
    @property
    def spell_name(self):
        return self._spell_name
    
    @spell_name.setter
    def spell_name(self, value):
        self._spell_name = value
        
    @property
    def attribute_use(self):
        return self._attribute_use
    
    @attribute_use.setter
    def attribute_use(self, value):
        self._attribute_use = value
    
    @property
    def spell_id(self):
        return self._spell_id
    
    @spell_id.setter
    def spell_id(self, value):
        self._spell_id = value
        
    @property
    def type_damage_name(self):
        return self._type_damage_name
    
    @type_damage_name.setter
    def type_damage_name(self, value):
        self._type_damage_name = value
        
    @property
    def amount_dice(self):
        return self._amount_dice
    
    @amount_dice.setter
    def amount_dice(self, value):
        self._amount_dice = value 
    
    @property
    def side_dice(self):
        return self._side_dice
    
    @side_dice.setter
    def side_dice(self, value):
        self._side_dice = value
        
    @property
    def add_per_level(self):
        return self._add_per_level
    
    @add_per_level.setter
    def add_per_level(self, value):
        self._add_per_level = value
        
    @property
    def description_spell(self):
        return self._description_spell
    
    @description_spell.setter
    def description_spell(self, value):
        self._description_spell = value
        
    @property
    def spell_level(self):
        return self._spell_level
    
    @spell_level.setter
    def spell_level(self, value):
        self._spell_level = value
        
    @property
    def type_damage_id(self):
        return self.__type_damage_id