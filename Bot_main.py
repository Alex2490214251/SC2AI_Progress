import sc2
from sc2 import run_game, Race, maps, Difficulty
from sc2.player import Bot, Computer
from Bot_api import Bot_api
from sc2.constants import UnitTypeId, AbilityId, BuffId

# TO DO
# Fix sentry Forcefield Ability Use
# Probe defence
# Stalker strike air units first

class Bot_Stardust(Bot_api):
    #Main System
    send1 = False
    send2 = False
    async def on_step(self,iteration):
        if iteration % 2 == 1:
            await self.distribute_workers()
            await self.train_probe()
            await self.build_pylon()
            await self.build_assimilator()
            await self.build_nexus()
            await self.build_gateway_cyberneticscore()
            await self.build_twilightconcil()
            await self.build_roboticsfacility_roboticsbay()
            await self.build_forge()
            #await self.build_shieldbattery()

            await self.train_stalker()
            await self.train_zealot()
            await self.train_sentry()
            await self.train_immortal()
            await self.train_colossus()
            await self.train_observer()

            await self.operation_zealot()
            await self.operation_sentry()
            await self.operation_stalker()
            await self.operation_immortal()
            await self.operation_colossus()
            await self.operation_cyberneticscore()
            await self.operation_twilightconcil()
            await self.operation_forge()
            await self.operation_roboticsbay()
            await self.operation_observer()
            await self.operation_nexus()

        await self.CONTROLL_ATTACK()
        await self.scout()
        await self.chat()

        if iteration == 1:
            await self.chat_send('Greetings I am a rookie protoss player XD(probe)')

        #if iteration % 1200 == 1:
            #await self.log()

    #Probe
    async def train_probe(self):
        for Nexus in self.structures(sc2.UnitTypeId.NEXUS).ready.idle:
            if self.can_afford(sc2.UnitTypeId.PROBE) and self.units(sc2.UnitTypeId.PROBE).amount < min(self.structures(sc2.UnitTypeId.NEXUS).amount*20,60):
                await self.train(UnitTypeId.PROBE,Nexus)

    #Basic Buildings
    async def build_pylon(self):
        if self.supply_left + 8 * self.already_pending(UnitTypeId.PYLON) < \
                ((self.structures(sc2.UnitTypeId.GATEWAY).amount+self.structures(sc2.UnitTypeId.WARPGATE).amount)*2+(self.structures(sc2.UnitTypeId.ROBOTICSFACILITY).amount)*4)+2 and \
                self.supply_cap < 200:
            Nexus = self.structures(sc2.UnitTypeId.NEXUS).ready
            if Nexus.exists:
                if self.can_afford(sc2.UnitTypeId.PYLON):
                    await self.build(sc2.UnitTypeId.PYLON,near=Nexus.random.position.towards(self.game_info.map_center, 9.2))
    async def build_assimilator(self):
        for Nexus in self.structures(sc2.UnitTypeId.NEXUS).ready:
            Vaspene = self.vespene_geyser.closer_than(10.0, Nexus)
            for vaspene in Vaspene:
                if not self.can_afford(sc2.UnitTypeId.ASSIMILATOR) or self.structures(sc2.UnitTypeId.GATEWAY).amount == 0 or \
                        self.units(sc2.UnitTypeId.PROBE).amount < min(self.structures(sc2.UnitTypeId.NEXUS).amount * 12,62):
                    break
                worker = self.units(sc2.UnitTypeId.PROBE).random
                if worker == None:
                    break
                if self.structures(sc2.UnitTypeId.ASSIMILATOR).amount+self.already_pending(UnitTypeId.ASSIMILATOR) < self.structures(UnitTypeId.NEXUS).ready.amount + self.time//370 or \
                        self.minerals > self.vespene+250:
                    self.do(worker.build(UnitTypeId.ASSIMILATOR,vaspene))
    async def build_nexus(self):
        if self.can_afford(sc2.UnitTypeId.NEXUS) and \
                (self.units(sc2.UnitTypeId.PROBE).amount > self.structures(sc2.UnitTypeId.NEXUS).amount*(16+self.structures(sc2.UnitTypeId.NEXUS).amount) or
                 self.structures(sc2.UnitTypeId.NEXUS).amount < self.time//130):
            if not self.already_pending(sc2.UnitTypeId.NEXUS):
                await self.expand_now()
    async def build_gateway_cyberneticscore(self):
        if self.structures(sc2.UnitTypeId.PYLON).ready.exists:
            pylon = self.structures(sc2.UnitTypeId.PYLON).ready.random
            if self.structures(sc2.UnitTypeId.GATEWAY).ready.exists:
                if not self.structures(sc2.UnitTypeId.CYBERNETICSCORE):
                    if self.can_afford(sc2.UnitTypeId.CYBERNETICSCORE) and not self.already_pending(sc2.UnitTypeId.CYBERNETICSCORE):
                        await self.build(sc2.UnitTypeId.CYBERNETICSCORE, near=pylon) #Build Cyberneticscore
            if (not self.structures(sc2.UnitTypeId.CYBERNETICSCORE) or
                    ((self.structures(sc2.UnitTypeId.GATEWAY).amount + self.structures(sc2.UnitTypeId.WARPGATE).amount < int(self.structures(sc2.UnitTypeId.NEXUS).ready.amount*((self.time / 360)+0.75)) and
                      self.structures(sc2.UnitTypeId.CYBERNETICSCORE).ready.exists and
                      (self.structures(sc2.UnitTypeId.GATEWAY).amount+self.structures(sc2.UnitTypeId.WARPGATE).amount) < self.structures(sc2.UnitTypeId.NEXUS).ready.amount * 2))): #Less than 3 GateWay per Nexus
                if self.can_afford(sc2.UnitTypeId.GATEWAY) and (not self.already_pending(sc2.UnitTypeId.GATEWAY)):
                    await self.build(sc2.UnitTypeId.GATEWAY, near=pylon)
    async def build_twilightconcil(self):
        if self.structures(sc2.UnitTypeId.PYLON).ready.exists:
            pylon = self.structures(sc2.UnitTypeId.PYLON).ready.random
            if self.structures(UnitTypeId.CYBERNETICSCORE).ready.exists:
                if not self.structures(UnitTypeId.TWILIGHTCOUNCIL):
                    if self.can_afford(UnitTypeId.TWILIGHTCOUNCIL) and not self.already_pending(UnitTypeId.TWILIGHTCOUNCIL):
                        await self.build(UnitTypeId.TWILIGHTCOUNCIL, near=pylon)
    async def build_roboticsfacility_roboticsbay(self):
        if self.structures(sc2.UnitTypeId.TWILIGHTCOUNCIL).ready.exists and self.structures(sc2.UnitTypeId.PYLON).ready.exists:
            pylon = self.structures(sc2.UnitTypeId.PYLON).ready.random
            if self.structures(sc2.UnitTypeId.ROBOTICSFACILITY).amount > 2:
                if not self.structures(sc2.UnitTypeId.ROBOTICSBAY):
                    if self.can_afford(sc2.UnitTypeId.ROBOTICSBAY) and not self.already_pending(sc2.UnitTypeId.ROBOTICSBAY):
                        await self.build(sc2.UnitTypeId.ROBOTICSBAY, near=pylon) #Build Roboticsbay
            if self.structures(sc2.UnitTypeId.ROBOTICSFACILITY).amount < self.structures(sc2.UnitTypeId.NEXUS).ready.amount-min(1,max(0,300-self.time)):
                if self.can_afford(sc2.UnitTypeId.ROBOTICSFACILITY) and not self.already_pending(sc2.UnitTypeId.ROBOTICSFACILITY): #Build Roboticsfacility
                    await self.build(sc2.UnitTypeId.ROBOTICSFACILITY, near=pylon)
    async def build_forge(self):
        if self.structures(sc2.UnitTypeId.PYLON).ready.exists:
            pylon = self.structures(sc2.UnitTypeId.PYLON).ready.random
            if self.structures(UnitTypeId.TWILIGHTCOUNCIL).ready.exists and self.structures(UnitTypeId.ROBOTICSFACILITY).ready.exists:
                if self.structures(UnitTypeId.FORGE).amount < (self.time//600 + 1):
                    if self.can_afford(UnitTypeId.FORGE) and not self.already_pending(UnitTypeId.FORGE):
                        await self.build(UnitTypeId.FORGE, near=pylon)

    async def build_shieldbattery(self):
        if self.structures(sc2.UnitTypeId.PYLON).ready.exists:
            pylon = self.structures(UnitTypeId.PYLON).ready.closest_to(self.game_info.map_center)
            if self.structures(sc2.UnitTypeId.SHIELDBATTERY).ready.amount < (self.supply_army//8) or \
                    self.minerals >= 500:
                if self.can_afford(UnitTypeId.SHIELDBATTERY) and not self.already_pending(UnitTypeId.SHIELDBATTERY):
                    await self.build(UnitTypeId.SHIELDBATTERY, near=pylon)



    #Train Troops
    async def train_zealot(self):
        for gateway in self.structures(sc2.UnitTypeId.GATEWAY).ready.idle:
            if self.can_afford(sc2.UnitTypeId.ZEALOT) and self.supply_left > 1 and \
                    ((self.units(sc2.UnitTypeId.STALKER).amount) + 1) / (
                    (self.units(sc2.UnitTypeId.ZEALOT).amount) + 1) >= await self.zealot_ratio() or \
                    self.structures(sc2.UnitTypeId.ASSIMILATOR).amount == 0 and \
                    warp == False:
                await self.train(UnitTypeId.ZEALOT, gateway)
        if self.structures(sc2.UnitTypeId.PYLON).ready.exists:
            for pylon in self.structures(sc2.UnitTypeId.PYLON).ready:
                for warpgate in self.structures(sc2.UnitTypeId.WARPGATE).ready.idle:
                    if self.supply_left > 1 and \
                            ((self.units(sc2.UnitTypeId.STALKER).amount) + 1)/((self.units(sc2.UnitTypeId.ZEALOT).amount) + 1) >= await self.zealot_ratio() and \
                            self.can_afford(UnitTypeId.ZEALOT) and \
                            await self.has_ability(AbilityId.WARPGATETRAIN_ZEALOT, warpgate):
                        await self.warp_in(UnitTypeId.ZEALOT, warpgate, pylon.position)
    async def train_stalker(self):
        for gateway in self.structures(sc2.UnitTypeId.GATEWAY).ready.idle:
            if self.supply_left > 1 and \
                    self.structures(sc2.UnitTypeId.CYBERNETICSCORE).ready.exists and \
                    self.units(UnitTypeId.STALKER).ready.amount < 30 - (self.time//42) and \
                    self.units(UnitTypeId.STALKER).ready.amount < int(3.3 * (
                    self.units(UnitTypeId.IMMORTAL).ready.amount + 1) + 2) and \
                    warp == False:
                await self.train(UnitTypeId.STALKER, gateway)
        if self.structures(sc2.UnitTypeId.PYLON).ready.exists:
            for pylon in self.structures(sc2.UnitTypeId.PYLON).ready:
                for warpgate in self.structures(sc2.UnitTypeId.WARPGATE).ready.idle:
                    if self.supply_left > 1 and self.can_afford(UnitTypeId.STALKER) and \
                            self.structures(sc2.UnitTypeId.CYBERNETICSCORE).ready.exists and \
                            self.units(UnitTypeId.STALKER).ready.amount < 40 - (self.time // 42) and \
                            self.units(UnitTypeId.STALKER).ready.amount < int(3.3 * (
                            self.units(UnitTypeId.IMMORTAL).ready.amount + 1) + 2) and \
                            await self.has_ability(AbilityId.WARPGATETRAIN_STALKER, warpgate):
                        await self.warp_in(UnitTypeId.STALKER, warpgate, pylon.position)
    async def train_sentry(self):
        for gateway in self.structures(sc2.UnitTypeId.GATEWAY).ready.idle:
            if self.supply_left > 1 and \
                    self.structures(sc2.UnitTypeId.CYBERNETICSCORE).ready.exists and \
                    self.units(UnitTypeId.SENTRY).ready.amount <= int((await self.troop_size())*0.02)-1 and \
                    warp == False:
                await self.train(UnitTypeId.SENTRY, gateway)
        if self.structures(sc2.UnitTypeId.PYLON).ready.exists:
            for pylon in self.structures(sc2.UnitTypeId.PYLON).ready:
                for warpgate in self.structures(sc2.UnitTypeId.WARPGATE).ready.idle:
                    if self.supply_left > 1 and \
                            self.structures(sc2.UnitTypeId.CYBERNETICSCORE).ready.exists and \
                            self.units(UnitTypeId.SENTRY).ready.amount <= int((await self.troop_size()) * 0.02)-1 and \
                            await self.has_ability(AbilityId.WARPGATETRAIN_SENTRY, warpgate):
                        await self.warp_in(UnitTypeId.SENTRY, warpgate, pylon.position)

    async def train_immortal(self):
        for roboticsfacility in self.structures(sc2.UnitTypeId.ROBOTICSFACILITY).ready.idle:
            if self.supply_left > 3 and self.units(UnitTypeId.IMMORTAL).ready.amount < 4*(self.units(UnitTypeId.COLOSSUS).amount+1):
                await self.train(UnitTypeId.IMMORTAL, roboticsfacility)
    async def train_colossus(self):
        for roboticsfacility in self.structures(sc2.UnitTypeId.ROBOTICSFACILITY).ready.idle:
            if self.supply_left > 5 and \
                    self.structures(sc2.UnitTypeId.ROBOTICSBAY).ready.exists:
                await self.train(UnitTypeId.COLOSSUS, roboticsfacility)
    async def train_observer(self):
        for roboticfacility in self.structures(sc2.UnitTypeId.ROBOTICSFACILITY).ready.idle:
            if self.supply_left > 0 and \
                    self.units(UnitTypeId.OBSERVER).amount < 2:
                await self.train(UnitTypeId.OBSERVER, roboticfacility)
    async def train_warpprism(self):
        for roboticsfacility in self.structures(sc2.UnitTypeId.ROBOTICSFACILITY).ready.idle:
            if self.supply_left > 1 and \
                    not self.units(sc2.UnitTypeId.WARPPRISM):
                await self.train(UnitTypeId.WARPPRISM, roboticsfacility)

    #Troops Micro AI
    async def operation_zealot(self):
        for zealot in self.units(sc2.UnitTypeId.ZEALOT):
            await self.attack_control(zealot, attack)

    async def operation_stalker(self):
        known_enemy_troops = self.enemy_units - self.enemy_structures
        for stalker in self.units(sc2.UnitTypeId.STALKER):
            enemy_in_range = await self.enemy_in_range(known_enemy_troops, stalker)
            await self.attack_control(stalker, attack)
            if await self.has_ability(AbilityId.EFFECT_BLINK_STALKER, stalker):
                if stalker.shield_percentage <= 0.4 and len(enemy_in_range) != 0:
                    self.do(stalker(AbilityId.EFFECT_BLINK_STALKER, self.enemy_units.closest_to(stalker.position).position.towards(
                    stalker.position,14
                )))

    async def operation_sentry(self):
        half_map = self.start_location.position.distance_to(self.enemy_start_locations[0].position)
        enemy_attack = self.enemy_units.filter(lambda unit: unit.distance_to(self.start_location) < 0.4 * half_map)
        for sentry in self.units(sc2.UnitTypeId.SENTRY):
            await self.attack_control(sentry, attack)
            if await self.has_ability(AbilityId.FORCEFIELD_FORCEFIELD, sentry):
                if len(enemy_attack) > 0 and not await self.has_ability(AbilityId.FORCEFIELD_CANCEL, sentry):
                    self.do(sentry(AbilityId.FORCEFIELD_FORCEFIELD, self.enemy_units.closest_to(sentry).position.towards(self.start_location, -0.5)))

    async def operation_immortal(self):
        for immortal in self.units(sc2.UnitTypeId.IMMORTAL):
            await self.attack_control(immortal, attack)

    async def operation_colossus(self):
        for colossus in self.units(sc2.UnitTypeId.COLOSSUS):
            await self.attack_control(colossus, attack)

    async def operation_warpprism(self):
        Troop = self.units(UnitTypeId.STALKER)+self.units(UnitTypeId.SENTRY)+self.units(UnitTypeId.IMMORTAL)+self.units(UnitTypeId.COLOSSUS)
        for prism in self.units(UnitTypeId.WARPPRISM):
            for troop in Troop:
                if troop.shield_percentage <= 0.025 and troop.health_percentage <= 0.8:
                    self.do(prism(AbilityId.LOAD_WARPPRISM, troop))
            if prism.has_cargo:
                self.do(prism(AbilityId.UNLOADALLAT_WARPPRISM, self.units(UnitTypeId.STALKER).closest_to(self.game_info.map_center).position.towards(self.game_info.map_center, -2)))
            else:
                self.do(prism.move(self.units(UnitTypeId.STALKER).closest_to(self.game_info.map_center).position.towards(self.game_info.map_center, -2)))
    async def operation_observer(self):
        for observer in self.units(UnitTypeId.OBSERVER).idle:
            if self.units(UnitTypeId.STALKER).ready.exists:
                self.do(observer.move(self.units(UnitTypeId.STALKER).closest_to(self.enemy_start_locations[0]).position.towards(self.start_location,6)))

    #Buildings Micro AI
    async def operation_cyberneticscore(self):
        global warp
        warp = False
        for cyberneticscore in self.structures(sc2.UnitTypeId.CYBERNETICSCORE).ready.idle:
            if self.can_afford(sc2.AbilityId.RESEARCH_WARPGATE) and await self.has_ability(AbilityId.RESEARCH_WARPGATE, cyberneticscore):
                self.do(cyberneticscore(sc2.AbilityId.RESEARCH_WARPGATE))
            elif not await self.has_ability(AbilityId.RESEARCH_WARPGATE, cyberneticscore):
                warp = True
    async def operation_twilightconcil(self):
        for twilightconcil in self.structures(UnitTypeId.TWILIGHTCOUNCIL).ready.idle:
            if await self.has_ability(AbilityId.RESEARCH_BLINK, twilightconcil):
                if self.can_afford(AbilityId.RESEARCH_BLINK):
                    self.do(twilightconcil(sc2.AbilityId.RESEARCH_BLINK))
            if await self.has_ability(AbilityId.RESEARCH_CHARGE, twilightconcil) and self.enemy_race != Race.Protoss:
                if self.can_afford(AbilityId.RESEARCH_CHARGE):
                    self.do(twilightconcil(sc2.AbilityId.RESEARCH_CHARGE))
    async def operation_forge(self):
        for forge in self.structures(UnitTypeId.FORGE).ready.idle:
            if self.can_afford(AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL1) and await self.has_ability(AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL1, forge):
                self.do(forge(sc2.AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL1))
            elif self.can_afford(AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL1) and await self.has_ability(AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL1, forge):
                self.do(forge(sc2.AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL1))
            elif self.can_afford(AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL2) and await self.has_ability(AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL2, forge):
                self.do(forge(sc2.AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL2))
            elif self.can_afford(AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL1) and await self.has_ability(AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL1, forge):
                self.do(forge(sc2.AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL1))
            elif self.can_afford(AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL3) and await self.has_ability(AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL3, forge):
                self.do(forge(sc2.AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL3))
            elif self.can_afford(AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL2) and await self.has_ability(AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL2, forge):
                self.do(forge(sc2.AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL2))
            elif self.can_afford(AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL2) and await self.has_ability(AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL2, forge):
                self.do(forge(sc2.AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL2))
            elif self.can_afford(AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL3) and await self.has_ability(AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL3, forge):
                self.do(forge(sc2.AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL3))
            elif self.can_afford(AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL3) and await self.has_ability(AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL3, forge):
                self.do(forge(sc2.AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL3))
    async def operation_roboticsbay(self):
        for roboticsbay in self.structures(UnitTypeId.ROBOTICSBAY).ready.idle:
            if await self.has_ability(AbilityId.RESEARCH_EXTENDEDTHERMALLANCE, roboticsbay):
                if self.can_afford(AbilityId.RESEARCH_EXTENDEDTHERMALLANCE):
                    self.do(roboticsbay(sc2.AbilityId.RESEARCH_EXTENDEDTHERMALLANCE))

    async def operation_nexus(self):
        structures = \
            self.structures(UnitTypeId.GATEWAY)+ \
            self.structures(UnitTypeId.ROBOTICSFACILITY)+ \
            self.structures(UnitTypeId.WARPGATE)+ \
            self.structures(UnitTypeId.CYBERNETICSCORE)
        idle_structures = \
            self.structures(UnitTypeId.GATEWAY).idle + \
            self.structures(UnitTypeId.ROBOTICSFACILITY).idle + \
            self.structures(UnitTypeId.WARPGATE).idle + \
            self.structures(UnitTypeId.CYBERNETICSCORE).idle
        working_structures = structures-idle_structures
        for nexus in self.structures(UnitTypeId.NEXUS).ready:
            if await self.has_ability(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST,nexus):
                if len(working_structures) > 0:
                    for a in range(len(working_structures)):
                        if not working_structures[a].has_buff(BuffId.CHRONOBOOSTENERGYCOST):
                            self.do(nexus(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST,working_structures[a]))


    #System
    async def CONTROLL_ATTACK(self):
        global attack
        global attack_history
        if self.time < 1:
            attack_history = False
            attack = False
        if self.units(UnitTypeId.STALKER).ready.exists:
            if await self.has_ability(AbilityId.EFFECT_BLINK_STALKER, self.units(UnitTypeId.STALKER).first):
                attack_history = True
        if attack_history == True:
            if await self.troop_size() >= 96:
                attack = True

    async def scout(self):
        import random
        units_to_ignore = [UnitTypeId.DRONE, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.EGG, UnitTypeId.LARVA, UnitTypeId.OVERLORD, UnitTypeId.OVERSEER, UnitTypeId.OBSERVER]
        detect_units = [UnitTypeId.OBSERVER, UnitTypeId.PHOTONCANNON, UnitTypeId.OVERSEER, UnitTypeId.RAVEN,
                        UnitTypeId.MISSILETURRET, UnitTypeId.SPORECRAWLER, UnitTypeId.SPORECANNON]
        if self.units(UnitTypeId.PROBE).ready.amount > 22:
            scout_worker = None
            for worker in self.workers:
                if self.has_order([AbilityId.PATROL], worker):
                    scout_worker = worker
            if not scout_worker:
                random_exp_location = random.choice(list(self.expansion_locations.keys()))
                scout_worker = self.workers.closest_to(self.start_location)
                if not scout_worker:
                    return
                await self.order(scout_worker, AbilityId.PATROL, random_exp_location)
                return
            nearby_enemy_units = self.enemy_units.filter(lambda unit: unit.type_id not in units_to_ignore).closer_than(10, scout_worker)
            if nearby_enemy_units.exists:
                await self.order(scout_worker, AbilityId.PATROL, self.game_info.map_center)
                return
            target = (scout_worker.orders[0].target.x,scout_worker.orders[0].target.y)
            if scout_worker.distance_to(target) < 10:
                random_exp_location = random.choice(list(self.expansion_locations.keys()))
                await self.order(scout_worker, AbilityId.PATROL, random_exp_location)
                return

        if self.units(UnitTypeId.OBSERVER).ready.amount > 1:
            scout = None
            for observer in self.units(UnitTypeId.OBSERVER):
                if self.has_order([AbilityId.PATROL], observer):
                    scout = observer
            if not scout:
                random_exp_location = random.choice(list(self.expansion_locations.keys()))
                scout = self.units(UnitTypeId.OBSERVER).closest_to(self.start_location)
                if not scout:
                    return
                await self.order(scout, AbilityId.PATROL, random_exp_location)
                return
            if self.enemy_units.filter(lambda unit: unit.type_id in detect_units).closer_than(10, scout):
                await self.order(scout, AbilityId.PATROL, self.game_info.map_center)
                return
            target = (scout.orders[0].target.x,scout.orders[0].target.y)
            if scout.distance_to(target) < 10:
                random_exp_location = random.choice(list(self.expansion_locations.keys()))
                await self.order(scout, AbilityId.PATROL, random_exp_location)
                return

    async def log(self):
        zealot = self.units(UnitTypeId.ZEALOT).ready.amount
        stalker = self.units(UnitTypeId.STALKER).ready.amount
        sentry = self.units(UnitTypeId.SENTRY).ready.amount
        immortal = self.units(UnitTypeId.IMMORTAL).ready.amount
        colossus = self.units(UnitTypeId.COLOSSUS).ready.amount
        data = '- '+str(zealot)+', '+str(stalker)+', '+str(sentry)+', '+str(immortal)+', '+str(colossus)

    async def chat(self):
        if self.supply_army > 100 and self.send1 == False:
            await self.chat_send('hope this time I can win :)')
            self.send1 = True
        if self.units(UnitTypeId.PROBE).ready.amount < 5 and self.send2 == False:
            await self.chat_send('Why you treat me like this... I am just a Rookie TAT')
            self.send2 = True



