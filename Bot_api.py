import sc2
from sc2 import run_game, Race, maps, Difficulty
from sc2.player import Bot, Computer
from sc2 import position, Race
from sc2.constants import UnitTypeId, AbilityId, UpgradeId

# TO DO
# Defending attack the structures
# Attack enemy troops when exists

class Bot_api(sc2.BotAI):

    async def macro_attack(self, attack_unit):
        known_enemy_troops = self.enemy_units
        enemy_in_range = await self.enemy_in_range(known_enemy_troops,attack_unit)
        if len(known_enemy_troops) > 0:
            if attack_unit.weapon_cooldown != 0 or len(enemy_in_range) == 0:
                self.do(attack_unit.move(self.enemy_units.closest_to(attack_unit.position).position.towards(
                    attack_unit.position,attack_unit.ground_range+2
                )))
            else:
                self.do(attack_unit.attack(self.enemy_units.closest_to(attack_unit.position)))
        elif len(self.enemy_structures) > 0:
            self.do(attack_unit.attack(self.enemy_structures.closest_to(attack_unit.position)))
        else:
            self.do(attack_unit.attack(self.enemy_start_locations[0]))

    async def macro_defend(self, attack_unit):
        half_map = self.start_location.position.distance_to(self.enemy_start_locations[0].position)
        enemy_attack = self.enemy_units.filter(lambda unit:unit.distance_to(self.start_location) < 0.4*half_map) + \
                       self.enemy_structures.filter(lambda unit:unit.distance_to(self.start_location) < 0.4*half_map)
        rally_position = self.structures(sc2.UnitTypeId.PYLON).ready.closest_to(self.game_info.map_center).position.towards(
            self.game_info.map_center, 10)
        if len(enemy_attack) > 0:
            if attack_unit.weapon_cooldown != 0:
                if self.enemy_units.exists:
                    self.do(attack_unit.move(self.enemy_units.closest_to(attack_unit.position).position.towards(
                        attack_unit.position,attack_unit.ground_range+1
                    )))
                else:
                    self.do(attack_unit.move(self.enemy_structures.closest_to(attack_unit.position).position.towards(
                        attack_unit.position, attack_unit.ground_range + 1
                    )))
            else:
                if self.enemy_units.exists:
                    self.do(attack_unit.attack(self.enemy_units.closest_to(attack_unit.position)))
                else:
                    self.do(attack_unit.attack(self.enemy_structures.closest_to(attack_unit.position)))
        else:
            if attack_unit.distance_to(rally_position) > 8:
                self.do(attack_unit.move(rally_position))

    async def attack_control(self, attack_unit, attack):
        if attack == True:
            await self.macro_attack(attack_unit)
        else:
            await self.macro_defend(attack_unit)

    async def has_ability(self, ability, unit):
        unit_ability = await self.get_available_abilities(unit)
        if ability in unit_ability:
            return True
        else:
            return False

    async def train(self, unit, building):
        if self.can_afford(unit):
            self.do(building.train(unit))

    async def warp_in(self, unit, building, position_point):
        import random
        x = random.randrange(-8,8)
        y = random.randrange(-8,8)
        placement = sc2.position.Point2((position_point.x+x,position_point.y+y))
        if self.can_afford(unit):
            self.do(building.warp_in(unit, placement))

    async def troop_size(self):
        supply_troop = self.supply_used - self.units(sc2.UnitTypeId.PROBE).ready.amount
        return supply_troop

    async def enemy_in_range(self, known_enemy_list, unit):
        enemy_in_range_list = []
        for enemy in known_enemy_list:
            if unit.distance_to(enemy) <= max(unit.ground_range,unit.air_range)+2:
                enemy_in_range_list.append(enemy)
        return enemy_in_range_list

    def has_order(self, orders, unit):
        if type(orders) != list:
            orders = [orders]
        count = 0
        if len(unit.orders) >= 1 and unit.orders[0].ability.id in orders:
            count += 1
        return count

    async def order(self, units, order, target=None, silent=True):
        if type(units) != list:
            unit = units
            self.do(unit(order, target=target))
        else:
            for unit in units:
                self.do(unit(order, target=target))

    async def random(self, min, max):
        import random
        output = random.randrange(min, max)
        return output

    async def zealot_ratio(self):
        race = self.enemy_race
        if race == Race.Protoss:
            return 6.0
        elif race == Race.Terran:
            return 1.2
        elif race == Race.Zerg:
            return 1.4
        else:
            return 2.0





