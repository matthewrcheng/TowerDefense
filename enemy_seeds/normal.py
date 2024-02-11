from Enemy import Pirate, Bandit, Thug, Brute, PirateGunner, Ghost, Paratrooper, Phantom, PirateMate, PirateCaptain, DreadPirate, Hooligan, Marauder, Juggernaut, Smuggler, Raider

seed = {
    1: [(Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60)],
    2: [(Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60)],
    3: [(Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60)],
    4: [(Bandit, 60), (Bandit, 60), (Bandit, 60), (Bandit, 60)],
    5: [(Bandit, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Bandit, 60), (Bandit, 60), (Bandit, 60)],
    6: [(Thug, 60), (Thug, 60), (Thug, 60), (Thug, 60), (Thug, 60)],
    7: [(Thug, 60), (Thug, 60), (Thug, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Bandit, 60), (Bandit, 60), (Bandit, 60)],
    8: [(Brute, 30)],
    9: [(Thug, 60), (Thug, 60), (Brute, 30), (Bandit, 60)],
    10: [(Bandit, 60), (Bandit, 60), (Bandit, 60), (Bandit, 60), (Bandit, 60), (PirateGunner, 30), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60)],
    11: [(Brute, 30), (Brute, 30), (Brute, 30), (Brute, 30), (PirateGunner, 30), (Pirate, 15), (Pirate, 15), (Pirate, 15), (Pirate, 15)],
    12: [(Bandit, 15), (Bandit, 15), (Bandit, 15), (Bandit, 15), (Bandit, 15), (Bandit, 15), (Bandit, 15), (Bandit, 15), (Bandit, 15), (Bandit, 15), (Bandit, 15), (Bandit, 15), (PirateGunner, 30), (PirateGunner, 30)],
    13: [(Ghost, 20), (Ghost, 20), (Ghost, 20), (Ghost, 20), (Ghost, 20), (Ghost, 20)],
    14: [(Ghost, 20), (Ghost, 20), (Ghost, 20), (PirateGunner, 45), (Brute, 60), (Brute, 30), (Brute, 30), (Brute, 30), (Brute, 30), (Brute, 30), (Brute, 30), (Brute, 30), (Brute, 30), (Brute, 30), (Paratrooper, 90)],
    15: [(Ghost, 20), (Ghost, 20), (Ghost, 20), (Phantom, 10), (PirateGunner, 45), (PirateGunner, 45), (PirateGunner, 45)],
    16: [(PirateGunner, 30), (PirateGunner, 30), (PirateGunner, 30), (PirateGunner, 30), (PirateGunner, 30), (PirateGunner, 30), (PirateGunner, 30), (PirateMate, 60)],
    17: [(PirateMate, 30), (PirateMate, 30), (PirateMate, 30), (Phantom, 20), (Phantom, 20), (Phantom, 20), (Phantom, 20), (Juggernaut, 30)],
    18: [(Paratrooper, 10), (Paratrooper, 10), (Paratrooper, 10), (Paratrooper, 10), (Paratrooper, 10), (Hooligan, 10), (Hooligan, 10), (Hooligan, 10), (Hooligan, 10), (Hooligan, 10), (Hooligan, 10), (Hooligan, 10), (Hooligan, 10), (Hooligan, 10), (Hooligan, 10), (Juggernaut, 30), (Juggernaut, 30), (Juggernaut, 30)],
    19: [(Marauder, 30), (Marauder, 30), (Marauder, 30), (Marauder, 30), (Marauder, 30), (PirateMate, 30), (PirateMate, 30), (PirateMate, 30), (PirateMate, 30), (PirateMate, 30), (Phantom, 10), (Phantom, 10), (Phantom, 10), (Phantom, 10), (Phantom, 10), (Phantom, 10), (Phantom, 10), (Phantom, 10), (Phantom, 10), (Phantom, 10), (Phantom, 10)],
    20: [(Pirate, 30), (PirateGunner, 30), (PirateMate, 30), (PirateCaptain, 30), (PirateMate, 30), (PirateMate, 30), (PirateGunner, 30), (PirateGunner, 30), (PirateGunner, 30), (PirateGunner, 30), (Pirate, 30), (Pirate, 30), (Pirate, 30), (Pirate, 30), (Pirate, 30), (Pirate, 30), (Pirate, 30), (Pirate, 30)],
    21: [(PirateCaptain, 30), (PirateCaptain, 10), (PirateCaptain, 10), (Juggernaut, 30), (Phantom, 10), (Juggernaut, 10), (Phantom, 10), (Juggernaut, 10), (Phantom, 10), (Juggernaut, 10), (Phantom, 10), (Juggernaut, 10), (Phantom, 10), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5)],
    22: [(Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10)],
    23: [(Smuggler, 3), (Smuggler, 3), (Smuggler, 3), (Smuggler, 3), (Smuggler, 3), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10)],
    24: [(Raider, 5), (Raider, 5), (Raider, 5), (Raider, 5), (Raider, 5), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (Smuggler, 3), (Smuggler, 3), (Smuggler, 3), (Smuggler, 3), (Smuggler, 3)],
    25: [(Pirate, 90), (PirateGunner, 30), (PirateMate, 30), (PirateCaptain, 30), (DreadPirate, 30)]
}