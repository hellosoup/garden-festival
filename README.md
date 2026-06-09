# 🌿 Garden Festival 🍎

A simple, family-friendly web game. Move your character left/right, catch falling
fruit & vegetables for points, dodge the junk food, and don't let good food hit the
ground. 3 lives. Build a catch streak for a points multiplier (up to ×10).

Works on **desktop** (arrow keys) and **phone/tablet** (drag to move).

---

## Play it now

Just open `index.html` in a browser. It runs immediately with placeholder art and a
local-only leaderboard — no setup needed to try it.

For phones, you'll want to host it (see **Hosting** below) so everyone can reach it.

---

## Artwork

**Falling items now render as emoji**, defined in the `EMOJI` map in `index.html` — no
image files needed for fruit/veg/junk. (The old item PNGs are still in `assets/` but
unused; you can delete them later.) To tweak an item's emoji, edit that map. Lives, the
falling-heart pickup, and the lose-a-life burst all use heart emoji (❤️ / 💔).

Item set: **1pt** apple banana orange watermelon grapes tomato carrot pear · **3pt** mango
bok choy strawberry avocado pineapple broccoli corn peach · **5pt** cherries blueberries
kiwi coconut · **junk** burger fries ice cream chocolate donut pizza soda lollipop.

**Characters still use PNGs** auto-loaded from `assets/`:

- **Format:** PNG with a transparent background, ~128×128 px, feet near the bottom edge.
- **Frames per character:** `popo_1..6` and `gonggong_1..6` — 1&2 walk, 3&4 eating, 5&6 yuck.

---

## Shared leaderboard (Supabase)

By default scores are saved only in the player's own browser. To share one leaderboard
across the family:

1. In your Supabase project, open **SQL Editor → New query**, paste the contents of
   [`supabase-setup.sql`](supabase-setup.sql), and click **Run**. This creates the
   `scores` table with insert+read-only access.
2. Go to **Project Settings → API** and copy your **Project URL** and **anon public key**.
3. Open `index.html`, find these two lines near the top of the `<script>` block, and
   paste your values:
   ```js
   const SUPABASE_URL = 'YOUR_SUPABASE_URL';
   const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';
   ```

That's it — the game will now read/write the shared Top 10.

---

## Hosting (so the family can play on their phones)

Any static host works. Easiest free options:
- **Netlify Drop** — drag the project folder onto https://app.netlify.com/drop
- **GitHub Pages** — push the folder to a repo, enable Pages
- **Cloudflare Pages / Vercel** — connect the repo

No build step — it's plain HTML/JS.

---

## Audio

- Background music (`assets/bg_music.mp3`) loops continuously, starting on the first
  click/tap (browsers block audio until the user interacts with the page).
- Button clicks, catching produce, catching junk, and dropping produce all play short
  synthesized sounds (Web Audio — no sound files needed). The collect sound rises in
  pitch as your streak multiplier climbs.
- The 🔊/🔇 button in the top-left corner mutes/unmutes **all** sound (music + SFX) and
  remembers the setting between visits. To replace the music, drop a new MP3 at
  `assets/bg_music.mp3`.

## Gameplay rules

- Catch fruit/veg → points × current multiplier (tier 1 = 1, tier 2 = 3, tier 3 = 5).
- Catch in a row → multiplier +1 each catch, capped at ×10.
- Catch junk food → lose a life **and** the streak resets.
- Let fruit/veg hit the floor → lose a life **and** the streak resets.
- Junk food hitting the floor → harmless (dodging is the right move!).
- It gets faster and busier the longer you survive. 3 lives total.
