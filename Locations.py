import typing

from BaseClasses import Location
from .Names import LocationName, ItemName, RegionName
from .Subclasses import LocationData
from .Regions import PSYREGIONS

# eventid matches Randomizer Seed index in table
CA_Checks = {
    LocationName.BehindFurnitureCard: LocationData(1),
    LocationName.StaircaseLedgesCard: LocationData(2),
    LocationName.UpperLedgeFossil: LocationData(3),
    LocationName.TopofGPCCard: LocationData(4),
    LocationName.UnderGPCCard: LocationData(5),
    LocationName.MountainLionLogBridgeCard: LocationData(6),
    LocationName.AboveEntranceLakeCard: LocationData(7),
    LocationName.RockWallBehindTreeCard: LocationData(8),
    LocationName.RockWallTopPirateScope: LocationData(9),
    LocationName.TreeNearFenceCard: LocationData(10),
    LocationName.TreeNearGeyserCard: LocationData(11),
    LocationName.FenceBehindGPCCard: LocationData(12),
    LocationName.NeartheBearCard: LocationData(13),
    LocationName.RockyPlatformsBehindGPCRightCard: LocationData(14),
    LocationName.RockyPlatformsBehindGPCLeftCard: LocationData(15),
    LocationName.TopofLogFlumeCard: LocationData(16),
    LocationName.RidetheLogFlumeCard: LocationData(17),
    LocationName.BottomofLogFlumeCard: LocationData(18),
    LocationName.BigRockNearFordCard: LocationData(19),
    LocationName.RuinedCabinChallengeMarker: LocationData(20),
    LocationName.BranchSwingingCourseStartCard: LocationData(21),
    LocationName.BranchSwingingCourseMidCard: LocationData(22),
    LocationName.BranchSwingingCourseEndChallengeMarker: LocationData(23),
    LocationName.BranchAboveSquirrelCard: LocationData(24),
    LocationName.CreekGrateGlassEye: LocationData(25),
    LocationName.SquirrelsAcornGoldenAcorn: LocationData(26),
    LocationName.GeyserMinersSkull: LocationData(27),
    LocationName.FenceNearKidsCabinsCard: LocationData(28),
    LocationName.UnderLodgeFrontStepsCard: LocationData(29),
    LocationName.BehindTreeNearLodgeCard: LocationData(30),
    LocationName.UndertheLodgeGoldDoubloon: LocationData(31),
    LocationName.Loudspeaker1PlatformCard: LocationData(32),
    LocationName.UnderLodgeMetalRoofCard: LocationData(33),
    LocationName.LoudspeakerTightropeWalkCard: LocationData(34),
    LocationName.Loudspeaker2PlatformCard: LocationData(35),
    LocationName.LodgeRoofChallengeMarker: LocationData(36),
    LocationName.MetalRoofOutcroppingCard: LocationData(37),
    LocationName.LoudspeakerAboveStumpCard: LocationData(38),
    LocationName.TreePlatformLeftCard: LocationData(39),
    LocationName.TreePlatformRightEagleClaw: LocationData(40),
    LocationName.RockWallTopCard: LocationData(41),
    LocationName.ParkingLotArchCard: LocationData(42),
    LocationName.ParkingLotSmallLogCard: LocationData(43),
    LocationName.OleandersCarCard: LocationData(44),
    LocationName.ParkingLotBasketballHoopCard: LocationData(45),
    LocationName.ParkingLotHistoryBoardCard: LocationData(46),
    LocationName.ParkingLotOuthouseCard: LocationData(47),
    LocationName.RockNearBenchCard: LocationData(48),    
    LocationName.GrindingontheRootsCard: LocationData(49),
    LocationName.UnderStairsCard: LocationData(50),
    LocationName.TopotheLoudspeakerCard: LocationData(51),
    LocationName.CabinRoof1Card: LocationData(52),
    LocationName.TrampolineAboveOuthouseCard: LocationData(53),
    LocationName.TrampolinePlatformChallengeMarker: LocationData(54),
    LocationName.CabinsOuthouseCard: LocationData(55),
    LocationName.BehindCabinCard: LocationData(56),
    LocationName.RoofofCabin2Card: LocationData(57),
    LocationName.CaveEntranceCard: LocationData(58),
    LocationName.DeepCavePathCard: LocationData(59),
    LocationName.DeepCaveLadderCard: LocationData(60),
    LocationName.HighUpTightropeCard: LocationData(61),
    LocationName.CaveRefrigeratorTurkeySandwich: LocationData(62),
    LocationName.GraveyardBearCard: LocationData(63), 
    LocationName.NearBeehiveCard: LocationData(64),
    LocationName.MineshaftTrailerEntranceCard: LocationData(65),
    LocationName.TightropeStartCard: LocationData(66), 
    LocationName.TightropeEndCard: LocationData(67), 
    LocationName.RocksNearTrailerCard: LocationData(68), 
    LocationName.FireplaceTreeLowerCard: LocationData(69), 
    LocationName.FireplaceTreeRockCard: LocationData(70), 
    LocationName.SwampSkinnyPolesCard: LocationData(71), 
    LocationName.BigLogPlatformCard: LocationData(72), 
    LocationName.AboveWaterfallLeftCard: LocationData(73), 
    LocationName.AboveWaterfallRightCard: LocationData(74), 
    LocationName.BehindtheWaterfallCard: LocationData(75), 
    LocationName.WeirdTreeLeftCherryWoodPipe: LocationData(76), 
    LocationName.WeirdTreeRightCard: LocationData(77), 
    LocationName.LogHillTopCard: LocationData(78),
    LocationName.LogHillBehindCard: LocationData(79), 
    LocationName.MineshaftGrindRailCard: LocationData(80), 
    LocationName.MineshaftUpperEntranceCard: LocationData(81), 
    LocationName.MineshaftAboveUpperEntranceCard: LocationData(82), 
    LocationName.InsideMineshaftCard: LocationData(83), 
    LocationName.MineshaftBearCard: LocationData(84), 
    LocationName.SwampBirdsNestCondorEgg: LocationData(85), 
    LocationName.CollapsedCaveChallengeMarker: LocationData(86), 
    LocationName.FireplaceTreeTopDinosaurBone: LocationData(87), 
    LocationName.HornetNestFertilityIdol: LocationData(88),
    LocationName.UndertheFirstBridgeCard: LocationData(89), 
    LocationName.BehindStumpCard: LocationData(90), 
    LocationName.LeftofEntranceRockWallCard: LocationData(91), 
    LocationName.PolesonLakeCard: LocationData(92), 
    LocationName.BathysphereRoofCard: LocationData(93), 
    LocationName.BathysphereDockCard: LocationData(94),
    LocationName.MetalRoofAboveFordCard: LocationData(95), 
    LocationName.AboveFordRopesCard: LocationData(96), 
    LocationName.AboveFordCabinPlatformCard: LocationData(97), 
    LocationName.OutsideCougarCaveCard: LocationData(98), 
    LocationName.InsideCougarCaveDiversHelmet: LocationData(99), 
    LocationName.BulletinBoardBushesCard: LocationData(100), 
    LocationName.PinkTreesPlatformLeftCard: LocationData(101), 
    LocationName.PinkTreesPlatformRightCard: LocationData(102), 
    LocationName.RockWallUpperCard: LocationData(103), 
    LocationName.LakeShoreCard: LocationData(104), 
    LocationName.TinyIslandCard: LocationData(105), 
    LocationName.RockWallGapPsychonautsComic1: LocationData(106), 
    LocationName.TopofBigRockChallengeMarker: LocationData(107), 
    LocationName.MainLodgeRaftersVoodooDoll: LocationData(108), 
    LocationName.TopofSanctuaryCard: LocationData(109), 
    LocationName.BottomofSanctuaryCard: LocationData(110), 
}

Rank_Checks = {
    LocationName.PSIRank05: LocationData(111), 
    LocationName.PSIRank10: LocationData(112), 
    LocationName.PSIRank15: LocationData(113),
    LocationName.PSIRank20: LocationData(114), 
    LocationName.PSIRank25: LocationData(115), 
    LocationName.PSIRank30: LocationData(116), 
    LocationName.PSIRank35: LocationData(117), 
    LocationName.PSIRank40: LocationData(118), 
    LocationName.PSIRank45: LocationData(119), 
    LocationName.PSIRank50: LocationData(120), 
    LocationName.PSIRank55: LocationData(121), 
    LocationName.PSIRank60: LocationData(122), 
    LocationName.PSIRank65: LocationData(123), 
    LocationName.PSIRank70: LocationData(124), 
    LocationName.PSIRank75: LocationData(125), 
    LocationName.PSIRank80: LocationData(126), 
    LocationName.PSIRank85: LocationData(127), 
    LocationName.PSIRank90: LocationData(128), 
    LocationName.PSIRank95: LocationData(129), 
    LocationName.PSIRank101: LocationData(130), 
}

AS_Checks = {
    LocationName.RockWallBottom: LocationData(131), 
    LocationName.RockWallLadder: LocationData(132), 
    LocationName.OutsideFrontGate: LocationData(133),
    LocationName.PillarAboveGate: LocationData(134), 
    LocationName.FountainTop: LocationData(135), 
    LocationName.HedgeAlcove: LocationData(136), 
    LocationName.AsylumDoorsRight: LocationData(137), 
    LocationName.AsylumDoorsLeft: LocationData(138), 
    LocationName.CornerNearFence: LocationData(139), 
    LocationName.LedgeBeforeGloria: LocationData(140),
    LocationName.AboveElevator: LocationData(141), 
    LocationName.CrowsBasket: LocationData(142), 
    LocationName.LedgeAboveFredLeft: LocationData(143), 
    LocationName.LedgeAboveFredRight: LocationData(144), 
    LocationName.LedgeOppositeElevator: LocationData(145), 
    LocationName.EdgarsRoom: LocationData(146), 
    LocationName.BehindElevator: LocationData(147), 
    LocationName.JunkCorner: LocationData(148), 
    LocationName.AboveEdgar: LocationData(149),
    LocationName.BehindMattressWall: LocationData(150), 
    LocationName.CheckeredBathroom: LocationData(151), 
    LocationName.RoomNearCheckeredBathroom: LocationData(152), 
    LocationName.ElevatorShaft: LocationData(153), 
    LocationName.RoomLeftOfPipeSlide: LocationData(154), 
    LocationName.FloatingInHole: LocationData(155), 
    LocationName.NextToHole: LocationData(156), 
    LocationName.CrumblingOuterWallPlanks: LocationData(157), 
    LocationName.CrumblingOuterWallPillar: LocationData(158), 
    LocationName.CrumblingOuterWallBelowPlatform: LocationData(159), 
    LocationName.CrumblingOuterWallPlatform: LocationData(160), 
    LocationName.RoomAboveTiltedStairs: LocationData(161), 
    LocationName.AcidRoomFloor: LocationData(162), 
    LocationName.AcidRoomTable: LocationData(163), 
    LocationName.AcidRoomWindow: LocationData(164), 
    LocationName.AcidRoomOverhang: LocationData(165), 
    LocationName.SmallWindowsLedge: LocationData(166), 
    LocationName.RoundWoodPlatform: LocationData(167),
    LocationName.GrateClimbBottom: LocationData(168), 
    LocationName.GrateClimbMid: LocationData(169), 
    LocationName.SinkPlatformLeft: LocationData(170), 
    LocationName.SinkPlatformRight: LocationData(171), 
    LocationName.PipesBelowChairDoor: LocationData(172),
    LocationName.RoomOppositeChairDoor: LocationData(173), 
    LocationName.PipeSlideNearChairDoor: LocationData(174), 
    LocationName.RaftersAboveChairDoor: LocationData(175),
    LocationName.LabCagedCrowLeft: LocationData(176), 
    LocationName.LabCagedCrowRight: LocationData(177), 
    LocationName.NextToPokeylope: LocationData(178), 
    LocationName.LabTopRailingLeft1: LocationData(179), 
    LocationName.LabTopRailingLeft2: LocationData(180),
    LocationName.LabTopElevator: LocationData(181), 
    LocationName.LabTopRailingRight: LocationData(182), 
    LocationName.TeaRoom: LocationData(183),

}

BB_Checks = {
    LocationName.JumpingTutorial1: LocationData(184), 
    LocationName.JumpingTutorial2: LocationData(185), 
    LocationName.PoleClimbingTutorialFloor: LocationData(186), 
    LocationName.BelowTheTripleTrampolines: LocationData(187),
    LocationName.GiantSoldierCutOut: LocationData(188), 
    LocationName.DodgingBullets1: LocationData(189), 
    LocationName.DodgingBullets2: LocationData(190), 
    LocationName.MachineGunTurret: LocationData(191), 
    LocationName.PoleSwingingTutorial: LocationData(192), 
    LocationName.TrapezeCobweb: LocationData(193),
    LocationName.TrapezePlatform: LocationData(194), 
    LocationName.InsidePlaneWreckage: LocationData(195),
    LocationName.EndOfObstacleCourseLeft: LocationData(196), 
    LocationName.EndOfObstacleCourseRight: LocationData(197), 
    LocationName.BasicBrainingComplete: LocationData(198),
}

SA_Checks = {
    LocationName.OnTheBed: LocationData(199), 
    LocationName.OnThePillow: LocationData(200), 
    LocationName.BuildingBlocksLeft: LocationData(201), 
    LocationName.BuildingBlocksBelow: LocationData(202), 
    LocationName.BuildingBlocksRight: LocationData(203),
    LocationName.TopOfBedFrame: LocationData(204), 
    LocationName.RoundPlatformsBottom: LocationData(205), 
    LocationName.RoundPlatformsNearValve: LocationData(206),
    LocationName.RoundPlatformsFarFromValve: LocationData(207),  
    LocationName.SideOfCubeFace3: LocationData(208), 
    LocationName.BottomOfShoeboxLadder: LocationData(209), 
    LocationName.ShoeboxPedestal: LocationData(210), 
    LocationName.ShoeboxTowerTop: LocationData(211), 
    LocationName.FlameTowerSteps: LocationData(212), 
    LocationName.FlameTowerTop1: LocationData(213), 
    LocationName.FlameTowerTop2: LocationData(214), 
    LocationName.SashasShootingGalleryComplete: LocationData(215),    

}

MI_Checks = {
    LocationName.IntroRingsTutorial: LocationData(216), 
    LocationName.DancingCamperPlatform1: LocationData(217), 
    LocationName.DemonRoom: LocationData(218), 
    LocationName.WindyLadderBottom: LocationData(219), 
    LocationName.PinballPlunger: LocationData(220), 
    LocationName.PlungerPartyLedge: LocationData(221), 
    LocationName.GrindrailRings: LocationData(222), 
    LocationName.CensorHallway: LocationData(223), 
    LocationName.PinkBowlBottom: LocationData(224), 
    LocationName.PinkBowlSmallPlatform: LocationData(225), 
    LocationName.BubblyFanBottom: LocationData(226), 
    LocationName.BubblyFanPlatform: LocationData(227), 
    LocationName.BubblyFanTop: LocationData(228), 
    LocationName.MillasPartyRoom: LocationData(229), 
    LocationName.MillasDancePartyComplete: LocationData(230),
}

NI_Checks = {
    LocationName.OutsideCaravan: LocationData(231), 
    LocationName.BehindTheEgg: LocationData(232), 
    LocationName.ShadowMonsterPath: LocationData(233),
    LocationName.ShadowMonsterBlueMushrooms: LocationData(234), 
    LocationName.LedgeBehindShadowMonster: LocationData(235), 
    LocationName.BelowTheSteepLedge: LocationData(236), 
    LocationName.ForestPathBlueMushrooms: LocationData(237), 
    LocationName.ForestBlueLedge: LocationData(238), 
    LocationName.ForestHighPlatform: LocationData(239), 
    LocationName.ForestPathThorns: LocationData(240), 
    LocationName.BehindThornTowerLeft: LocationData(241), 
    LocationName.BehindThornTowerMid: LocationData(242), 
    LocationName.BehindThornTowerRight: LocationData(243),
    LocationName.BrainTumblerExperimentComplete: LocationData(244), 
    
}

LO_Checks = {
    LocationName.SkyscraperStart: LocationData(245), 
    LocationName.CornerNearJail: LocationData(246), 
    LocationName.SkyscraperBeforeDam: LocationData(247), 
    LocationName.BehindLasersLeft1: LocationData(248), 
    LocationName.BehindLasersLeft2: LocationData(249), 
    LocationName.BehindLasersRight: LocationData(250), 
    LocationName.BlimpHop: LocationData(251), 
    LocationName.EndOfDam: LocationData(252), 
    LocationName.EndOfDamPlatform: LocationData(253), 
    LocationName.SkyscraperAfterDam: LocationData(254), 
    LocationName.NearBattleships: LocationData(255), 
    LocationName.OnTheBridge: LocationData(256), 
    LocationName.GroundAfterBridge: LocationData(257), 
    LocationName.SkyscraperAfterBridge: LocationData(258), 
    LocationName.TunnelSuitcaseTag: LocationData(259), 
    LocationName.FinalSkyscrapersLeft: LocationData(260), 
    LocationName.FinalSkyscrapersRight: LocationData(261),
    LocationName.KochamaraIntroLeft: LocationData(262),
    LocationName.KochamaraIntroRight: LocationData(263),
    LocationName.LungfishopolisComplete: LocationData(264),

}

MM_Checks = {
    LocationName.BoydsFridgeClv: LocationData(265), 
    LocationName.FirstHouseDufflebagTag: LocationData(266), 
    LocationName.SecondHouseRollingPin: LocationData(267), 
    LocationName.CarTrunk1StopSign: LocationData(268),
    LocationName.RoofAfterRoadCrewPurseTag: LocationData(269), 
    LocationName.CarTrunk2HedgeTrimmers: LocationData(270), 
    LocationName.CarHouseBackyardSteamertrunkTag: LocationData(271),
    LocationName.InsideWebbedGarageHatbox: LocationData(272),
    LocationName.GraveyardPatioVault: LocationData(273), 
    LocationName.GraveyardBehindTreeOneUp: LocationData(274), 
    LocationName.BehindGraveyardDufflebag: LocationData(275), 
    LocationName.HedgeMazeFlowers: LocationData(276), 
    LocationName.CarTrunk3WateringCan: LocationData(277), 
    LocationName.PostOfficeRoofOneUp: LocationData(278),
    LocationName.PostOfficeLobbySuitcase: LocationData(279),
    LocationName.PostOfficeBasementPlunger: LocationData(280),
    LocationName.LandscapersHouseBackyardSuitcaseTag: LocationData(281), 
    LocationName.LandscapersHouseTablePurse: LocationData(282),
    LocationName.LandscapersHouseKitchenAmmoUp: LocationData(283), 
    LocationName.PowerlineIslandSandboxHatboxTag: LocationData(284), 
    LocationName.PowerlineIslandLeftMemoryVault: LocationData(285), 
    LocationName.PowerlineIslandRightMaxLives: LocationData(286),
    LocationName.BehindBookDepositorySteamerTrunk: LocationData(287),   
    LocationName.MilkmanComplete: LocationData(288), 

}

TH_Checks = {
    LocationName.NearTheCriticPurse: LocationData(289),
    LocationName.InTheAudienceAmmoUp: LocationData(290),
 
    LocationName.BelowTheSpotlightSteamertrunkTag: LocationData(291), 
    LocationName.BehindStagePurseTag: LocationData(292),
    LocationName.BehindStageCobwebSuitcase: LocationData(293),
    LocationName.StorageRoomFloorVault: LocationData(294), 
    LocationName.StorageRoomLeftSteamertrunk: LocationData(295), 
    LocationName.StorageRoomRightLowerSuitcaseTag: LocationData(296), 
    LocationName.StorageRoomRightUpperCandle1: LocationData(297), 
    LocationName.BonitasRoom: LocationData(298),
    LocationName.DoghouseSlicersDufflebagTag: LocationData(299), 
    LocationName.BigPlatform1Hatbox: LocationData(300), 
    LocationName.BigPlatform2Vault: LocationData(301), 
    LocationName.BigPlatform3OneUp: LocationData(302), 
    LocationName.BigPlatformAboveHatboxTag: LocationData(303), 
    LocationName.NextToOatmealDufflebag: LocationData(304), 
    LocationName.CandleBasketCandle2: LocationData(305), 
    LocationName.CurtainSlideConfusionAmmoUp: LocationData(306),
    LocationName.GloriasTheaterComplete: LocationData(307),

}

WW_Checks = {
    LocationName.FredsRoomHatboxTag: LocationData(308), 
    LocationName.TheFireplacePricelessCoin: LocationData(309), 
    LocationName.GameBoardSuitcaseTag: LocationData(310),
    LocationName.CarpentersRoofVault: LocationData(311),
    LocationName.TightropeRoomDufflebag: LocationData(312),
    LocationName.OutsideVillager1HouseOneUp: LocationData(313), 
    LocationName.SmallArchTopMaxLives: LocationData(314), 
    LocationName.SmallArchBelowPurseTag: LocationData(315), 
    LocationName.TopOfVillager2sHouseDufflebagTag: LocationData(316),
    LocationName.TopOfVillager3sHouseAmmoUp: LocationData(317), 
    LocationName.TopOfKnightsHouseConfusionAmmoUp: LocationData(318),
    LocationName.CastleTowerOneUp: LocationData(319), 
    LocationName.CastleInsideVault: LocationData(320), 
    LocationName.CastleWallSteamertrunk: LocationData(321),
    LocationName.UnderTheGuillotineSuitcase: LocationData(322), 
    LocationName.FredsHouseBasementHatbox: LocationData(323), 

    LocationName.BlacksmithsLeftBuildingPurse: LocationData(324),
    LocationName.BlacksmithsRightBuildingSteamertrunkTag: LocationData(325), 
    LocationName.BlacksmithsHaybaleTheMusket: LocationData(326), 
    LocationName.HelpTheCarpenter: LocationData(327),
    LocationName.HelpVillager1: LocationData(328), 
    LocationName.HelpTheKnight: LocationData(329), 
    LocationName.HelpVillager2: LocationData(330), 
    LocationName.HelpVillager3: LocationData(331),
    LocationName.WaterlooWorldComplete: LocationData(332), 

}

BV_Checks = {
    LocationName.ClubStreetLadySteamertrunk: LocationData(333), 
    LocationName.ClubStreetMetalBalconyDufflebagTag: LocationData(334), 
    LocationName.HeartStreetHIGHBalconyAmmoUp: LocationData(335),
    LocationName.AlleywaysLedgeHatboxTag: LocationData(336), 
    LocationName.SewersMainVault: LocationData(337),
    LocationName.ClubStreetGatedSteamerTrunkTag: LocationData(338), 
    LocationName.BurnTheLogsDufflebag: LocationData(339), 

    LocationName.TheGardenVault: LocationData(340), 
    LocationName.NearDiegosHouseMaxLives: LocationData(341), 
    LocationName.DiegosBedSuitcaseTag: LocationData(342), 
    LocationName.DiegosRoomHatbox: LocationData(343), 
    LocationName.DiegosHouseGrindrailSuitcase: LocationData(344), 
    LocationName.GrindrailBalconyConfusionAmmoUp: LocationData(345),
    LocationName.SanctuaryBalconyPurseTag: LocationData(346), 

    LocationName.SanctuaryGroundPurse: LocationData(347), 
    LocationName.TigerWrestler: LocationData(348), 
    LocationName.DragonWrestler: LocationData(349),
    LocationName.EagleWrestler: LocationData(350), 
    LocationName.CobraWrestler: LocationData(351), 
    LocationName.BlackVelvetopiaComplete: LocationData(352), 

}

MC_Checks = {
    LocationName.EntranceAwningSteamertrunkTag: LocationData(353), 
    LocationName.CrumblingPathSteamertrunk: LocationData(354), 
    LocationName.CrumblingPathEndRightHatboxTag: LocationData(355), 
    LocationName.CrumblingPathEndLeftConfusionAmmoUp: LocationData(356),
    LocationName.OllieEscortFloorSuitcaseTag: LocationData(357), 
    LocationName.OllieEscortMiddleHatbox: LocationData(358), 
    LocationName.OllieEscortTopLeftVault: LocationData(359), 
    LocationName.OllieEscortTopRightPurseTag: LocationData(360), 
    LocationName.TunnelOfLoveStartPurse: LocationData(361), 
    LocationName.TunnelOfLoveCornerSuitcase: LocationData(362), 
    LocationName.TunnelOfLoveRailDufflebagTag: LocationData(363), 
    LocationName.NextToTheFatLadyDufflebag: LocationData(364),
        
}

all_locations = {
    **CA_Checks
    **Rank_Checks
    **AS_Checks
    **BB_Checks
    **SA_Checks
    **MI_Checks
    **NI_Checks
    **LO_Checks
    **MM_Checks
    **TH_Checks
    **WW_Checks
    **BV_Checks
    **MC_Checks
}