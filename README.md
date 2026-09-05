# Floating Islands Obby (Roblox)

Obby 10 stage di pulau melayang, sunset skybox. Buka di Roblox Studio, publish, main.

## Isi
- `obby.rbxlx` — place file (buka via File → Open dari File)
- `generate.py` — generator (stdlib only), jalankan `python3 generate.py` untuk regen
- `ObbyLogic.lua` — script server (checkpoints, kill, pads, movers, win)

## Stage
1. Jump gaps — platform lintang 4 gap
2. Kill strips — neon merah di lantai
3. Moving platform — slider antar jurang
4. Spinner — balok berputar
5. Jump pads — 3 tingkat naik
6. Balance beam — jalur sempit
7. Conveyor pushback — lantai dorong balik
8. Truss climb — panjat ke ledge
9. Zigzag stairs — tangga siku + kill brick
10. Final gauntlet — 2 spinner + WinPad (timer leaderboard `Time`)

## Mekanik (script `ObbyLogic` di ServerScriptService)
- Checkpoint sentuh → simpan stage, respawn ke checkpoint
- Kill part sentuh → mati
- Launch pad → dorong ke atas (power via StringValue `Launch`)
- Spinner / slider / conveyor via StringValue (`Spin`, `Slide`, `Conveyor`)
- leaderstats: `Stage` + `Time` (speedrun)

## Pakai
1. Roblox Studio → File → Open from File → `obby.rbxlx`
2. Test (Play) — checkpoint + kill jalan
3. Publish: File → Publish to Roblox

Regen dunia: edit `generate.py`, `python3 generate.py`.
