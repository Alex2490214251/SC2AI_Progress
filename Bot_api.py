import sc2
from sc2 import run_game, Race, maps, Difficulty
from sc2.player import Bot, Computer
from sc2 import position
from sc2.constants import UnitTypeId, AbilityId, UpgradeId

class Bot_api(sc2.BotAI):

    async def macro_attack(self, attack_unit):
        known_enemy_troops = self.known_enemy_units+self.units(UnitTypeId.PHOTONCANNON)
        enemy_in_range = await self.enemy_in_range(known_enemy_troops, attack_unit)

        if len(enemy_in_range) > 0:
            if attack_unit.weapon_cooldown != 0:
                if len(known_enemy_troops) >= 1.5*self.units(UnitTypeId.STALKER).ready.amount and \
                        attack_unit != UnitTypeId.COLOSSUS:
                    await self.do(attack_unit.move(self.known_enemy_units.closest_to(attack_unit.position).position.towards(
                        attack_unit.position,attack_unit.ground_range
                    )))
                else:
                    await self.do(attack_unit.move(self.known_enemy_units.closest_to(attack_unit.position).position))
            else:
                await self.do(attack_unit.attack(self.known_enemy_units.closest_to(attack_unit.position)))
        elif len(self.known_enemy_structures) > 0:
            await self.do(attack_unit.attack(self.known_enemy_structures[-1]))
        else:
            await self.do(attack_unit.attack(self.enemy_start_locations[0]))

    async def has_ability(self, ability, unit):
        unit_ability = await self.get_available_abilities(unit)
        if ability in unit_ability:
            return True
        else:
            return False

    async def train(self, unit, building):
        if self.can_afford(unit):
            await self.do(building.train(unit))

    async def warp_in(self, unit, building, position_point):
        import random
        x = random.randrange(-8,8)
        y = random.randrange(-8,8)
        placement = sc2.position.Point2((position_point.x+x,position_point.y+y))
        if self.can_afford(unit):
            await self.do(building.warp_in(unit, placement))

    async def troop_size(self):
        supply_troop = self.supply_used - self.units(sc2.UnitTypeId.PROBE).ready.amount
        return supply_troop

    async def enemy_in_range(self, known_enemy_list, unit):
        enemy_in_range_list = []
        for enemy in known_enemy_list:
            if unit.target_in_range(enemy):
                enemy_in_range_list.append(enemy)
        return enemy_in_range_list

    async def random(self, min, max):
        import random
        output = random.randrange(min, max)
        return output


