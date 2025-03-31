class Personage:
    def __init__(self, personage_name, hp = 100, mana = 100, stamina = 100,physic_damage = 10, magic_damage=5):
        '''Основной класс персонажа. Создаёт персонажа, с набором параметров (hp, mana, stamina).'''
        self.name = personage_name
        self.hp = hp
        self.mana = mana
        self.stamina = stamina
        self.physic_damage = physic_damage
        self.magic_damage = magic_damage
        self.can_used_perks = []  # Перки, которые можно активировать
        self.active_perks = []    # Активные перки

    def change_param(self, param, value=0, percent=0):
        """Обновляет параметр персонажа с учетом процента или абсолютного значения"""
        if value != 0 and percent != 0:
            raise ValueError('Нельзя одновременно передавать и процент и скалярное значение.')
        if not isinstance(value, (int, float)) or not isinstance(percent, (int, float)):
            raise TypeError('Одно из значений percent или value не является числом.')

        current_value = getattr(self, param)

        if percent != 0:
            new_value = current_value * (1 + percent / 100)
        else:
            new_value = current_value + value

        self.param_update(param, new_value)

    def param_update(self, param, new_value):
        """Непосредственно обновляет параметр и выводит информацию об изменении"""
        old_value = getattr(self, param)
        setattr(self, param, new_value)
        print(f'Параметр {param} обновлён с {old_value} на {new_value}')

    def add_perk(self, perk):
        """Добавляет перк в список доступных перков"""
        if not isinstance(perk, Perk):
            raise TypeError("Можно добавлять только объекты класса Perk")
        self.can_used_perks.append(perk)
        print(f"Перк '{perk.get_name()}' добавлен в список доступных")

    def activate(self, perk):
        """Активирует перк, перемещая его в active_perks и применяя эффект"""
        if perk not in self.can_used_perks:
            raise ValueError("Этот перк не найден в списке доступных")
        
        self.can_used_perks.remove(perk)
        self.active_perks.append(perk)
        perk.apply_effect(self)  # Применяем эффект перка
        print(f"Перк '{perk.get_name()}' активирован")

    def deactivate(self, perk):
        """Деактивирует перк, перемещая его обратно в can_used_perks и отменяя эффект"""
        if perk not in self.active_perks:
            raise ValueError("Этот перк не найден в списке активных")
        
        self.active_perks.remove(perk)
        self.can_used_perks.append(perk)
        perk.remove_effect(self)  # Отменяем эффект перка
        print(f"Перк '{perk.get_name()}' деактивирован")

    def get_use_perk(self):
        """Возвращает список доступных перков"""
        return self.can_used_perks

    def get_active_perks(self):
        """Возвращает список активных перков"""
        return self.active_perks


class Perk:
    def __init__(self):
        self._name = ""
        self._description = ""
        self._effect_param = None
        self._effect_value = 0
        self._is_percent = False
        self._effect_type = "add"  # или "multiply" для мультипликативных эффектов

    def name(self, name):
        self._name = name
        return self  # Возвращаем self для возможности цепочки вызовов

    def description(self, description):
        self._description = description
        return self

    def get_name(self):
        return self._name
    
    def get_description(self):
        return self._description
    
    def effect(self, param_name, effect_type, value, is_percent=True):
        """Устанавливает эффект перка"""
        self._effect_param = param_name
        self._effect_value = value
        self._is_percent = is_percent
        self._effect_type = effect_type
        return self

    def apply_effect(self, personage):
        """Применяет эффект перка к персонажу через change_param"""
        print(f"Эффект перка '{self._name}' применяется к параметру {self._effect_param}")
        if not self._effect_param:
            return

        if self._effect_type == "add":
            if self._is_percent:
                personage.change_param(self._effect_param, percent=self._effect_value*100)
            else:
                personage.change_param(self._effect_param, value=self._effect_value)
        elif self._effect_type == "multiply":
            # Для мультипликативного эффекта используем процентное изменение
            personage.change_param(self._effect_param, percent=(self._effect_value-1)*100)


    def remove_effect(self, personage):
        """Отменяет эффект перка, возвращая параметр к исходному значению"""
        print(f"Эффект перка '{self._name}' отменяется для параметра {self._effect_param}")
        if not self._effect_param:
            return

        if self._effect_type == "add":
            if self._is_percent:
                personage.change_param(self._effect_param, percent=-self._effect_value*100)
            else:
                personage.change_param(self._effect_param, value=-self._effect_value)
        elif self._effect_type == "multiply":
            # Для мультипликативного эффекта используем процентное изменение
            personage.change_param(self._effect_param, percent=-(self._effect_value-1)*100)
