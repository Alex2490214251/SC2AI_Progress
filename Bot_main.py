import sc2
from sc2 import run_game, Race, maps, Difficulty
from sc2.player import Bot, Computer

class Bot1(sc2.BotAI):

    async def on_step(self,iteration):
        await self.distribute_workers()
        await self.train_probe()
        await self.build_pylon()
        await self.build_assimilator()
        await self.build_nexus()
        await self.build_gateway_cyberneticscore()
        await self.train_stalker()
        await self.attack_stalker()
        await self.train_zealot()
        await self.attack_zealot()
        await self.CONTROLL_ATTACK()
        #await self.build_forge()

    async def train_probe(self):
        for nexus in self.units(sc2.UnitTypeId.NEXUS).ready.noqueue:
            if self.can_afford(sc2.UnitTypeId.PROBE) and self.units(sc2.UnitTypeId.PROBE).amount < 66:
                await self.do(nexus.train(sc2.UnitTypeId.PROBE))

    async def build_pylon(self):
        if self.supply_left < (self.units(sc2.UnitTypeId.GATEWAY).amount * 2)+2 and not self.already_pending(sc2.UnitTypeId.PYLON):
            Nexus = self.units(sc2.UnitTypeId.NEXUS).ready
            if Nexus.exists:
                if self.can_afford(sc2.UnitTypeId.PYLON):
                    await self.build(sc2.UnitTypeId.PYLON,near=Nexus.first.position.towards(self.game_info.map_center, 10))

    async def build_assimilator(self):
        for Nexus in self.units(sc2.UnitTypeId.NEXUS).ready:
            Vaspene = self.state.vespene_geyser.closer_than(10.0, Nexus)
            for vaspene in Vaspene:
                if not self.can_afford(sc2.UnitTypeId.ASSIMILATOR) or self.units(sc2.UnitTypeId.CYBERNETICSCORE).amount == 0 or \
                        self.units(sc2.UnitTypeId.PROBE).amount < self.units(sc2.UnitTypeId.NEXUS).amount * 12:
                    break
                worker = self.select_build_worker(vaspene.position)
                if worker == None:
                    break
                if not self.units(sc2.UnitTypeId.ASSIMILATOR).closer_than(1.0, vaspene):
                    await self.do(worker.build(sc2.UnitTypeId.ASSIMILATOR, vaspene))

    async def build_nexus(self):
        if self.can_afford(sc2.UnitTypeId.NEXUS) and \
                (self.units(sc2.UnitTypeId.PROBE).amount > self.units(sc2.UnitTypeId.NEXUS).amount * 16 or
                 self.units(sc2.UnitTypeId.NEXUS).amount < self.time//120):
            await self.expand_now()

    async def build_gateway_cyberneticscore(self):
        if self.units(sc2.UnitTypeId.PYLON).ready.exists:
            pylon = self.units(sc2.UnitTypeId.PYLON).ready.random
            if self.units(sc2.UnitTypeId.GATEWAY).ready.exists:
                if not self.units(sc2.UnitTypeId.CYBERNETICSCORE):
                    if self.can_afford(sc2.UnitTypeId.CYBERNETICSCORE) and not self.already_pending(sc2.UnitTypeId.CYBERNETICSCORE):
                        await self.build(sc2.UnitTypeId.CYBERNETICSCORE, near=pylon)
            if (not self.units(sc2.UnitTypeId.CYBERNETICSCORE) and not self.already_pending(sc2.UnitTypeId.GATEWAY)) or \
                    ((self.units(sc2.UnitTypeId.GATEWAY).amount < self.units(sc2.UnitTypeId.NEXUS).amount * (self.time // 150) and self.units(sc2.UnitTypeId.CYBERNETICSCORE).ready.exists and
                     self.units(sc2.UnitTypeId.GATEWAY).amount < 6)): # Less than 6 GateWay
                if self.can_afford(sc2.UnitTypeId.GATEWAY):# and not self.already_pending(sc2.UnitTypeId.GATEWAY):
                    await self.build(sc2.UnitTypeId.GATEWAY, near=pylon)

    async def train_stalker(self):
        for gateway in self.units(sc2.UnitTypeId.GATEWAY).ready.noqueue:
            if self.can_afford(sc2.UnitTypeId.STALKER) and self.supply_left > 1:
                await self.do(gateway.train(sc2.UnitTypeId.STALKER))

    async def attack_stalker(self):
        for stalker in self.units(sc2.UnitTypeId.STALKER).idle:
            if self.units(sc2.UnitTypeId.STALKER).amount > 5 and len(self.known_enemy_units) > 0:
                await self.do(stalker.attack(self.known_enemy_units[0]))
            elif len(self.known_enemy_units) == 0 and attack == True:
                await self.do(stalker.attack(self.enemy_start_locations[0]))
            elif attack == False:
                await self.do(stalker.move(self.start_location))

    async def train_zealot(self):
        for gateway in self.units(sc2.UnitTypeId.GATEWAY).ready.noqueue:
            if self.can_afford(sc2.UnitTypeId.ZEALOT) and self.supply_left > 1 and \
                    ((self.units(sc2.UnitTypeId.STALKER).amount)+1) / ((self.units(sc2.UnitTypeId.ZEALOT).amount)+1) >= 2.0 or \
                    self.units(sc2.UnitTypeId.ASSIMILATOR).amount == 0:
                await self.do(gateway.train(sc2.UnitTypeId.ZEALOT))

    async def attack_zealot(self):
        for zealot in self.units(sc2.UnitTypeId.ZEALOT).idle:
            if self.units(sc2.UnitTypeId.ZEALOT).amount > 3 and len(self.known_enemy_units) > 0:
                await self.do(zealot.attack(self.known_enemy_units[0]))
            elif len(self.known_enemy_units) == 0 and attack == True:
                await self.do(zealot.attack(self.enemy_start_locations[0]))
            elif attack == False:
                await self.do(zealot.move(self.start_location))

    async def CONTROLL_ATTACK(self):
        global attack
        attack = False
        if (self.units(sc2.UnitTypeId.ZEALOT).amount +
            self.units(sc2.UnitTypeId.STALKER).amount) >= 30:
            attack = True
        else:
            attack = False


    #async def build_forge(self):

run_game(maps.get('ProximaStationLE'),[
    Bot(Race.Protoss, Bot1()),
    Computer(Race.Random, Difficulty.Hard)
], realtime=True)