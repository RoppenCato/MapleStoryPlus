# Travel

Every way of travelling in the game that costs something or takes time, with its price and duration. Read from the server's scripts on 2026-10-10. **Not tested in the game.** Walking through ordinary map portals is not listed.

This is step `T-3` in the [Implementation list](../Docs/Implementation-List.md).

## How ride times work

Scheduled rides (boats, trains and so on) run on a timetable: the gate opens, closes, and the ride leaves. All of those times are divided by the `travel_rate` setting, which is **10** right now. So a 10 minute boat ride takes 1 minute today.

To get rides of about 3 minutes, `travel_rate` would be about 3 for the Ellinia boat (10 minutes originally) but the other rides (5 minutes originally) would then take under 2 minutes. One number scales all of them.

## Scheduled rides

Buy a ticket, wait at the platform, ride. "Now" is with `travel_rate` 10.

| Route | Ticket | Sold by | Ride (original) | Ride (now) | Leaves every (original) |
|-------|--------|---------|-----------------|------------|-------------------------|
| Ellinia ↔ Orbis (boat) | 5,000 from Ellinia, 5,000 from Orbis | Joel (Ellinia), ticket seller at Orbis Station | 10 min | 1 min | 15 min |
| Orbis ↔ Ludibrium (train) | 6,000 | Orbis Station seller, Ludibrium seller | 5 min | 30 s | 10 min |
| Orbis ↔ Leafre (cabin) | 30,000 | Orbis Station seller, Leafre seller | 5 min | 30 s | 10 min |
| Orbis ↔ Ariant (genie) | 6,000 | Orbis Station seller, Ariant seller | 5 min | 30 s | 10 min |
| Kerning City ↔ New Leaf City (subway) | 5,000 | Bell | 4 min | 24 s | 5 min |
| Kerning City ↔ Singapore (plane) | 5,000 | Irene (Kerning), Shalon (Singapore) | 1 min | 6 s | 10 min |
| Orbis ↔ Mu Lung (crane) | 1,500 | Crane | 1 min | 6 s | on demand |
| Ludibrium ↔ Korean Folk Town (Helios Tower elevator) | free | none | 1 min | 6 s | 2 min |

The Ellinia ↔ Orbis boat can be attacked by Crog (Balrog ship) during the ride.

## Taxis and instant travel

Pay and arrive at once.

| From | To | Cost | NPC |
|------|----|------|-----|
| Henesys, Ellinia, Perion, Kerning City, Lith Harbor, Nautilus | Any of the other Victoria towns | 800 to 1,000 (one tenth for beginners) | Regular Cab |
| Lith Harbor, Ellinia (and other VIP cabs) | Ant Tunnel Park (Sleepywood) | 10,000 (1,000 for beginners) | VIP Cab |
| El Nath | Ice Valley II | 10,000 | Danger Zone Taxi |
| Ludibrium | Path of Time | 25,000 | Danger Zone Taxi |
| Omega Sector | Ludibrium | 25,000 | Danger Zone Taxi |
| Leafre | Entrance to Dragon Forest | 65,000 | Danger Zone Taxi |
| Ariant ↔ Magatia | | 1,500 | Camel Cab |
| Mu Lung ↔ Herb Town | | 500 | Crane |
| Aquarium → The Sharp Unknown | | 1,000 | Dolphin |
| Aquarium ↔ Herb Town | | 10,000 | Dolphin |
| Ariant | A random Victoria town | 10,000 | Karcasa |
| New Leaf City ↔ Haunted House | | 15,000 | NLC Taxi |
| Lith Harbor, Orbis, Ludibrium | Florina Beach | 1,500 / 2,000 / 1,800, or a VIP ticket | Pason, Shuri, Nara |
| Maple Island | Lith Harbor | 150 | Shanks |
| Ellinia ↔ Ereve, Orbis ↔ Ereve | | 1,000 | Kiriru, Kiru |
| Lith Harbor ↔ Rien | | 800 | Puro |
| Any town with Spinel | Mushroom Shrine (Japan) | 3,000 | Spinel (World Tour) |
| Any town with Spinel | Second World Tour destination | 10,000 | Spinel (World Tour) |
| Singapore (CBD) | Trend Zone Metropolis (Malaysia) | 42,000 | Audrey |
| Trend Zone Metropolis | Kampung Village | 10,000 | Audrey |
| Kerning City subway | Construction site B1 to B3 | 1,000 | Ticket seller |

## Towers

Changed on 2026-10-10 (`T-2`): the tower stones cost mesos instead of a rock scroll. The scrolls were not sold or dropped anywhere on our server, so the stones could not be used before.

| Tower | From and to | Cost | NPC |
|-------|-------------|------|-----|
| Orbis Tower | 20th floor and 1st floor | 5,000 mesos | Orbis Magic Spot (NPCs 2012014, 2012015) |
| Eos Tower | 100th, 71st, 41st and 1st floor, one step at a time | 5,000 mesos per jump | Eos Rock (NPCs 2040024 to 2040027) |

The price is the line `var teleportCost = 5000;` at the top of each of the six scripts in `Server/scripts/npc/`.

## Not covered

- Mystic Door, town scrolls, teleport rocks and the VIP teleport rock from the Cash Shop.
- Quest-only transport and party quest entrances.
- The exact timetable wording in NPC dialogue, which still quotes the original times.
