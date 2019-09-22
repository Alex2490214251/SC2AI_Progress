import sc2
from sc2 import run_game, Race, maps, Difficulty
from sc2.player import Bot, Computer
from Bot_api import Bot_api
from sc2.constants import UnitTypeId, AbilityId

class Bot_Stardust(Bot_api):
    #Main System
    async def on_step(self,iteration):
        await self.distribute_workers()
        await self.train_probe()
        await self.build_pylon()
        await self.build_assimilator()
        await self.build_nexus()
        await self.build_gateway_cyberneticscore()
        await self.build_twilightconcil()
        await self.build_roboticsfacility_roboticsbay()
        await self.build_forge()
        await self.train_stalker()
        await self.train_zealot()
        await self.train_sentry()
        await self.train_immortal()
        await self.train_colossus()
        await self.operation_stalker()
        await self.operation_zealot()
        await self.operation_sentry()
        await self.operation_immortal()
        await self.operation_colossus()
        await self.operation_cyberneticscore()
        await self.operation_twilightconcil()
        await self.operation_forge()

        await self.CONTROLL_ATTACK()

    #Probe
    async def train_probe(self):
        for Nexus in self.units(sc2.UnitTypeId.NEXUS).ready.noqueue:
            if self.can_afford(sc2.UnitTypeId.PROBE) and self.units(sc2.UnitTypeId.PROBE).amount < 60:
                await self.do(Nexus.train(sc2.UnitTypeId.PROBE))

    #Basic Buildings
    async def build_pylon(self):
        if self.supply_left + 8 * self.already_pending(UnitTypeId.PYLON) < \
                ((self.units(sc2.UnitTypeId.GATEWAY).amount+self.units(sc2.UnitTypeId.WARPGATE).amount)*2+(self.units(sc2.UnitTypeId.ROBOTICSFACILITY).amount)*4) and \
                self.supply_cap < 200:
            Nexus = self.units(sc2.UnitTypeId.NEXUS).ready
            if Nexus.exists:
                if self.can_afford(sc2.UnitTypeId.PYLON):
                    await self.build(sc2.UnitTypeId.PYLON,near=Nexus.first.position.towards(self.game_info.map_center, 9.2))
    async def build_assimilator(self):
        for Nexus in self.units(sc2.UnitTypeId.NEXUS).ready:
            Vaspene = self.state.vespene_geyser.closer_than(10.0, Nexus)
            for vaspene in Vaspene:
                if not self.can_afford(sc2.UnitTypeId.ASSIMILATOR) or self.units(sc2.UnitTypeId.GATEWAY).amount == 0 or \
                        self.units(sc2.UnitTypeId.PROBE).amount < self.units(sc2.UnitTypeId.NEXUS).amount * 12 or \
                        self.already_pending(sc2.UnitTypeId.ASSIMILATOR):
                    break
                worker = self.units(sc2.UnitTypeId.PROBE).random
                if worker == None:
                    break
                if not self.units(sc2.UnitTypeId.ASSIMILATOR).closer_than(1.0, vaspene) and \
                        self.units(sc2.UnitTypeId.ASSIMILATOR).amount < self.units(UnitTypeId.NEXUS).ready.amount + self.time//360 + 1:
                    await self.do(worker.build(sc2.UnitTypeId.ASSIMILATOR, vaspene))
    async def build_nexus(self):
        if self.can_afford(sc2.UnitTypeId.NEXUS) and \
                (self.units(sc2.UnitTypeId.PROBE).amount > self.units(sc2.UnitTypeId.NEXUS).amount*(17+self.units(sc2.UnitTypeId.NEXUS).amount) or
                 self.units(sc2.UnitTypeId.NEXUS).amount < self.time//150):
            if not self.already_pending(sc2.UnitTypeId.NEXUS):
                await self.expand_now()
    async def build_gateway_cyberneticscore(self):
        #global Gateway_need_to_be_built
        #Gateway_need_to_be_built = int(self.units(sc2.UnitTypeId.NEXUS).ready.amount * (self.time / 195))
        if self.units(sc2.UnitTypeId.PYLON).ready.exists:
            pylon = self.units(sc2.UnitTypeId.PYLON).ready.random
            if self.units(sc2.UnitTypeId.GATEWAY).ready.exists:
                if not self.units(sc2.UnitTypeId.CYBERNETICSCORE):
                    if self.can_afford(sc2.UnitTypeId.CYBERNETICSCORE) and not self.already_pending(sc2.UnitTypeId.CYBERNETICSCORE):
                        await self.build(sc2.UnitTypeId.CYBERNETICSCORE, near=pylon) #Build Cyberneticscore
            if (not self.units(sc2.UnitTypeId.CYBERNETICSCORE) or
                    ((self.units(sc2.UnitTypeId.GATEWAY).amount + self.units(sc2.UnitTypeId.WARPGATE).amount < int(self.units(sc2.UnitTypeId.NEXUS).ready.amount*((self.time / 360)+0.75)) and
                      self.units(sc2.UnitTypeId.CYBERNETICSCORE).ready.exists and
                     self.units(sc2.UnitTypeId.GATEWAY).amount < self.units(sc2.UnitTypeId.NEXUS).ready.amount * 2))): #Less than 3 GateWay per Nexus
                if self.can_afford(sc2.UnitTypeId.GATEWAY) and (not self.already_pending(sc2.UnitTypeId.GATEWAY)):
                    await self.build(sc2.UnitTypeId.GATEWAY, near=pylon)
    async def build_twilightconcil(self):
        if self.units(sc2.UnitTypeId.PYLON).ready.exists:
            pylon = self.units(sc2.UnitTypeId.PYLON).ready.random
            if self.units(UnitTypeId.CYBERNETICSCORE).ready.exists:
                if not self.units(UnitTypeId.TWILIGHTCOUNCIL):
                    if self.can_afford(UnitTypeId.TWILIGHTCOUNCIL) and not self.already_pending(UnitTypeId.TWILIGHTCOUNCIL):
                        await self.build(UnitTypeId.TWILIGHTCOUNCIL, near=pylon)
    async def build_roboticsfacility_roboticsbay(self):
        if self.units(sc2.UnitTypeId.CYBERNETICSCORE).ready.exists and self.units(sc2.UnitTypeId.PYLON).ready.exists:
            pylon = self.units(sc2.UnitTypeId.PYLON).ready.random
            if self.units(sc2.UnitTypeId.ROBOTICSFACILITY).ready.amount >= 2:
                if not self.units(sc2.UnitTypeId.ROBOTICSBAY):
                    if self.can_afford(sc2.UnitTypeId.ROBOTICSBAY) and not self.already_pending(sc2.UnitTypeId.ROBOTICSBAY):
                        await self.build(sc2.UnitTypeId.ROBOTICSBAY, near=pylon) #Build Roboticsbay
            if self.units(sc2.UnitTypeId.ROBOTICSFACILITY).amount < self.units(sc2.UnitTypeId.NEXUS).ready.amount:
                if self.can_afford(sc2.UnitTypeId.ROBOTICSFACILITY) and not self.already_pending(sc2.UnitTypeId.ROBOTICSFACILITY): #Build Roboticsfacility
                    await self.build(sc2.UnitTypeId.ROBOTICSFACILITY, near=pylon)
    async def build_forge(self):
        if self.units(sc2.UnitTypeId.PYLON).ready.exists:
            pylon = self.units(sc2.UnitTypeId.PYLON).ready.random
            if self.units(UnitTypeId.TWILIGHTCOUNCIL).ready.exists or self.units(UnitTypeId.ROBOTICSFACILITY).ready.exists or self.units(UnitTypeId.STARGATE).ready.exists:
                if self.units(UnitTypeId.FORGE).amount < (self.time//600 + 1):
                    if self.can_afford(UnitTypeId.FORGE) and not self.already_pending(UnitTypeId.FORGE):
                        await self.build(UnitTypeId.FORGE, near=pylon)

    #Train Troops
    async def train_zealot(self):
        for gateway in self.units(sc2.UnitTypeId.GATEWAY).ready.noqueue:
            if self.can_afford(sc2.UnitTypeId.ZEALOT) and self.supply_left > 1 and \
                    ((self.units(sc2.UnitTypeId.STALKER).amount) + 1) / (
                    (self.units(sc2.UnitTypeId.ZEALOT).amount) + 1) >= 6.0 or \
                    self.units(sc2.UnitTypeId.ASSIMILATOR).amount == 0 and \
                    warp == False:
                await self.train(UnitTypeId.ZEALOT, gateway)
        if self.units(sc2.UnitTypeId.PYLON).ready.exists:
            for pylon in self.units(sc2.UnitTypeId.PYLON).ready:
                for warpgate in self.units(sc2.UnitTypeId.WARPGATE).ready.idle:
                    if self.supply_left > 1 and \
                            ((self.units(sc2.UnitTypeId.STALKER).amount) + 1)/((self.units(sc2.UnitTypeId.ZEALOT).amount) + 1) >= 6.0 and \
                            self.can_afford(UnitTypeId.ZEALOT) and \
                            await self.has_ability(AbilityId.WARPGATETRAIN_ZEALOT, warpgate):
                        await self.warp_in(UnitTypeId.ZEALOT, warpgate, pylon.position)
    async def train_stalker(self):
        for gateway in self.units(sc2.UnitTypeId.GATEWAY).ready.noqueue:
            if self.supply_left > 1 and \
                    self.units(sc2.UnitTypeId.CYBERNETICSCORE).ready.exists and \
                    self.units(UnitTypeId.STALKER).ready.amount < 40 - (self.time//42) and \
                    warp == False:
                await self.train(UnitTypeId.STALKER, gateway)
        if self.units(sc2.UnitTypeId.PYLON).ready.exists:
            for pylon in self.units(sc2.UnitTypeId.PYLON).ready:
                for warpgate in self.units(sc2.UnitTypeId.WARPGATE).ready.idle:
                    if self.supply_left > 1 and self.can_afford(UnitTypeId.STALKER) and \
                            self.units(sc2.UnitTypeId.CYBERNETICSCORE).ready.exists and \
                            self.units(UnitTypeId.STALKER).ready.amount < 40 - (self.time // 42) and \
                            await self.has_ability(AbilityId.WARPGATETRAIN_STALKER, warpgate):
                        await self.warp_in(UnitTypeId.STALKER, warpgate, pylon.position)
    async def train_sentry(self):
        for gateway in self.units(sc2.UnitTypeId.GATEWAY).ready.noqueue:
            if self.supply_left > 1 and \
                    self.units(sc2.UnitTypeId.CYBERNETICSCORE).ready.exists and \
                    self.units(UnitTypeId.SENTRY).ready.amount <= int((await self.troop_size())*0.02) and \
                    warp == False:
                await self.train(UnitTypeId.SENTRY, gateway)
        if self.units(sc2.UnitTypeId.PYLON).ready.exists:
            for pylon in self.units(sc2.UnitTypeId.PYLON).ready:
                for warpgate in self.units(sc2.UnitTypeId.WARPGATE).ready.idle:
                    if self.supply_left > 1 and \
                            self.units(sc2.UnitTypeId.CYBERNETICSCORE).ready.exists and \
                            self.units(UnitTypeId.SENTRY).ready.amount <= int((await self.troop_size()) * 0.02) and \
                            await self.has_ability(AbilityId.WARPGATETRAIN_SENTRY, warpgate):
                        await self.warp_in(UnitTypeId.SENTRY, warpgate, pylon.position)

    async def train_immortal(self):
        for roboticsfacility in self.units(sc2.UnitTypeId.ROBOTICSFACILITY).ready.noqueue:
            if self.supply_left > 3 and self.units(UnitTypeId.IMMORTAL).ready.amount < 5*(self.units(UnitTypeId.COLOSSUS).amount+1):
                await self.train(UnitTypeId.IMMORTAL, roboticsfacility)
    async def train_colossus(self):
        for roboticsfacility in self.units(sc2.UnitTypeId.ROBOTICSFACILITY).ready.noqueue:
            if self.supply_left > 5 and \
                    self.units(sc2.UnitTypeId.ROBOTICSBAY).ready.exists:
                await self.train(UnitTypeId.COLOSSUS, roboticsfacility)
    async def train_observer(self):
        for roboticfacility in self.units(sc2.UnitTypeId.ROBOTICSFACILITY).ready.noqueue:
            if self.supply_left > 0 and \
                    self.units(UnitTypeId.OBSERVER).ready.amount < 3:
                await self.train(UnitTypeId.OBSERVER, roboticfacility)
    async def train_warpprism(self):
        for roboticsfacility in self.units(sc2.UnitTypeId.ROBOTICSFACILITY).ready.noqueue:
            if self.supply_left > 1 and \
                    not self.units(sc2.UnitTypeId.WARPPRISM):
                await self.train(UnitTypeId.WARPPRISM, roboticsfacility)

    #Troops Micro AI
    async def operation_zealot(self):
        known_enemy_troops = self.known_enemy_units - self.known_enemy_structures
        for zealot in self.units(sc2.UnitTypeId.ZEALOT):
            if self.units(sc2.UnitTypeId.ZEALOT).amount > 0 and len(known_enemy_troops) > 0 and attack_history == False:
                await self.do(zealot.attack(known_enemy_troops[-1]))
            elif attack == True:
                await self.macro_attack(zealot)
            elif attack == False:
                await self.do(zealot.move(self.units(sc2.UnitTypeId.PYLON).ready.closest_to(self.game_info.map_center).position.towards(self.game_info.map_center, 10)))
    async def operation_stalker(self):
        known_enemy_troops = self.known_enemy_units - self.known_enemy_structures
        for stalker in self.units(sc2.UnitTypeId.STALKER):
            if self.units(sc2.UnitTypeId.STALKER).amount > 0 and len(known_enemy_troops) > 0 and attack_history == False:
                await self.do(stalker.attack(known_enemy_troops[-1]))
            elif attack == True :
                await self.macro_attack(stalker)
            elif attack == False :
                await self.do(stalker.move(self.units(sc2.UnitTypeId.PYLON).ready.closest_to(self.game_info.map_center).position.towards(self.game_info.map_center, 10)))
            if await self.has_ability(AbilityId.EFFECT_BLINK_STALKER, stalker):
                if stalker.shield_percentage <= 0.4:
                    await self.do(stalker(AbilityId.EFFECT_BLINK_STALKER, stalker.position.towards(self.start_location, 4)))
    async def operation_sentry(self):
        known_enemy_troops = self.known_enemy_units - self.known_enemy_structures
        for sentry in self.units(sc2.UnitTypeId.SENTRY):
            if self.units(sc2.UnitTypeId.SENTRY).amount > 0 and len(known_enemy_troops) > 0 and attack_history == False:
                await self.do(sentry.attack(known_enemy_troops[-1]))
            elif attack == True:
                await self.macro_attack(sentry)
            elif attack == False:
                await self.do(sentry.move(self.units(sc2.UnitTypeId.PYLON).ready.closest_to(self.game_info.map_center).position.towards(self.game_info.map_center, 10)))
            if await self.has_ability(AbilityId.FORCEFIELD_FORCEFIELD, sentry):
                if len(known_enemy_troops) > 0 and not await self.has_ability(AbilityId.FORCEFIELD_CANCEL, sentry):
                    await self.do(sentry(AbilityId.FORCEFIELD_FORCEFIELD, known_enemy_troops[await self.random(0,len(known_enemy_troops))].position.towards(self.start_location, 0.5)))

    async def operation_immortal(self):
        known_enemy_troops = self.known_enemy_units - self.known_enemy_structures
        for immortal in self.units(sc2.UnitTypeId.IMMORTAL):
            if self.units(sc2.UnitTypeId.IMMORTAL).amount > 0 and len(known_enemy_troops) > 0 and attack_history == False:
                await self.do(immortal.attack(known_enemy_troops[-1]))
            elif attack == True:
                await self.macro_attack(immortal)
            elif attack == False:
                await self.do(immortal.move(self.units(sc2.UnitTypeId.PYLON).ready.closest_to(self.game_info.map_center).position.towards(self.game_info.map_center, 10)))
    async def operation_colossus(self):
        known_enemy_troops = self.known_enemy_units - self.known_enemy_structures
        for colossus in self.units(sc2.UnitTypeId.COLOSSUS):
            if self.units(sc2.UnitTypeId.COLOSSUS).amount > 0 and len(known_enemy_troops) > 0 and attack_history == False:
                await self.do(colossus.attack(known_enemy_troops[-1]))
            elif attack == True and colossus.shield_percentage >= 0.3:
                await self.macro_attack(colossus)
            elif attack == False or colossus.shield_percentage < 0.3:
                await self.do(colossus.move(self.units(sc2.UnitTypeId.PYLON).ready.closest_to(self.game_info.map_center).position.towards(self.game_info.map_center, 10)))

    async def operation_warpprism(self):
        Troop = self.units(UnitTypeId.STALKER)+self.units(UnitTypeId.SENTRY)+self.units(UnitTypeId.IMMORTAL)+self.units(UnitTypeId.COLOSSUS)
        for prism in self.units(UnitTypeId.WARPPRISM):
            for troop in Troop:
                if troop.shield_percentage <= 0.025 and troop.health_percentage <= 0.8:
                    await self.do(prism(AbilityId.LOAD_WARPPRISM, troop))
            if prism.has_cargo:
                await self.do(prism(AbilityId.UNLOADALLAT_WARPPRISM, self.units(UnitTypeId.STALKER).closest_to(self.game_info.map_center).position.towards(self.game_info.map_center, -2)))
            else:
                await self.do(prism.move(self.units(UnitTypeId.STALKER).closest_to(self.game_info.map_center).position.towards(self.game_info.map_center, -2)))
    async def operation_observer(self):
        for observer in self.units(UnitTypeId.OBSERVER):
            await self.do(observer.move(self.units(UnitTypeId.STALKER).closest_to(self.enemy_start_locations[0]).position.towards(self.start_location,6)))

    #Buildings Micro AI
    async def operation_cyberneticscore(self):
        global warp
        warp = False
        for cyberneticscore in self.units(sc2.UnitTypeId.CYBERNETICSCORE).ready.noqueue:
            if self.can_afford(sc2.AbilityId.RESEARCH_WARPGATE) and await self.has_ability(AbilityId.RESEARCH_WARPGATE, cyberneticscore):
                await self.do(cyberneticscore(sc2.AbilityId.RESEARCH_WARPGATE))
            elif not await self.has_ability(AbilityId.RESEARCH_WARPGATE, cyberneticscore):
                warp = True
    async def operation_twilightconcil(self):
        for twilightconcil in self.units(UnitTypeId.TWILIGHTCOUNCIL).ready.noqueue:
            if await self.has_ability(AbilityId.RESEARCH_BLINK, twilightconcil):
                if self.can_afford(AbilityId.RESEARCH_BLINK):
                    await self.do(twilightconcil(sc2.AbilityId.RESEARCH_BLINK))
            #else:
            #    if self.can_afford(AbilityId.RESEARCH_CHARGE) and await self.has_ability(AbilityId.RESEARCH_CHARGE, twilightconcil):
            #        await self.do(twilightconcil(sc2.AbilityId.RESEARCH_CHARGE))
    async def operation_forge(self):
        for forge in self.units(UnitTypeId.FORGE).ready.noqueue:
            if self.can_afford(AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL1) and await self.has_ability(AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL1, forge):
                await self.do(forge(sc2.AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL1))
            elif self.can_afford(AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL1) and await self.has_ability(AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL1, forge):
                await self.do(forge(sc2.AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL1))
            elif self.can_afford(AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL2) and await self.has_ability(AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL2, forge):
                await self.do(forge(sc2.AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL2))
            elif self.can_afford(AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL1) and await self.has_ability(AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL1, forge):
                await self.do(forge(sc2.AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL1))
            elif self.can_afford(AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL3) and await self.has_ability(AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL3, forge):
                await self.do(forge(sc2.AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL3))
            elif self.can_afford(AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL2) and await self.has_ability(AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL2, forge):
                await self.do(forge(sc2.AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL2))
            elif self.can_afford(AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL2) and await self.has_ability(AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL2, forge):
                await self.do(forge(sc2.AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL2))
            elif self.can_afford(AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL3) and await self.has_ability(AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL3, forge):
                await self.do(forge(sc2.AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL3))
            elif self.can_afford(AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL3) and await self.has_ability(AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL3, forge):
                await self.do(forge(sc2.AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL3))

    #System
    async def CONTROLL_ATTACK(self):
        global attack
        global attack_history
        attack = False
        if self.time < 1:
            attack_history = False
        if self.units(UnitTypeId.STALKER).ready.exists:
            if await self.has_ability(AbilityId.EFFECT_BLINK_STALKER, self.units(UnitTypeId.STALKER).first):
                attack_history = True
        if attack_history == True:
            if await self.troop_size() >= 74:
                attack = True


sc2.run_game(sc2.maps.get("ProximaStationLE"), [
    #Player,
    Bot(Race.Protoss, Bot_Stardust()),
    Computer(Race.Protoss, difficulty=Difficulty.VeryHard)
], realtime=False, save_replay_as="AI13.SC2Replay")
