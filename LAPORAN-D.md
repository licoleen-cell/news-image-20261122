# LAPORAN-D.md — Variant D news-image-20261122 (readability-v4)

Dibuat: 2026-11-24 ~01:45 WIB (tenggat 03:00 WIB).
Commit yang dinilai: lokal `4bb8de4f753f84380cbaa92d4615fe1ad5dcd9fa`,
remote `12017cdeffddd8ec968981e080f554f5f41fe4e6` (poin 8+9+10).
Tree lokal = tree remote: `7de0344298583baa0ce2d13d39899855e45e084a` (identik, YA).

Perintah, output, exit code, dan sha ditulis mentah di bawah.
Kata "terbukti", "aman", "lolos" hanya dipakai dengan bukti yang menyertainya.
Status tiap gate ditulis apa adanya; yang gagal ditulis gagal, bukan dibulatkan.

## Status gate (ringkas)

| Gate | Hasil | Bukti |
|---|---|---|
| 1. diff texts.txt vs gen_image.py = 0 | LULUS (dengan catatan metode) | §1 |
| 2. grep 0 (12 kata terlarang) | LULUS | §2 |
| 3. crop 1:1, jarak min 4px | LULUS dengan catatan (timeline gap 1px) | §3 |
| 4. render 300/512 vs 7da71f0 | GAGAL di 300px (D lebih susah dibaca) | §4 |
| 5. rebuild 2x sha sama | LULUS | §5 |
| 6. preflight 3.13.18 -P -s, 3 run exit 0 | LULUS (simulasi, bukan grader asli) | §6 |
| 7. main.py stdlib only | LULUS | §7 |

Kesimpulan: **7 gate TIDAK semuanya lulus pada commit yang sama.**
Gate 4 gagal di 300px. Sesuai otorisasi bersyarat lek 19:20
(SUBMIT-AUTH-0600.md): kalau ada syarat tidak terpenuhi atau ada keraguan,
JANGAN submit; 7da71f0 tetap entri final. Selain itu lek sudah memberi kabar
(01:39 WIB), jadi otorisasi submit 06:00 SUDAH BATAL — submit menunggu
"gas" dari lek.

## §1 — Gate 1: diff texts.txt vs gen_image.py

### 1a. Tiap baris texts.txt ada di gen_image.py (exact match)

Perintah (python3):
```python
src = open('gen_image.py').read()
manifest = [l.strip() for l in open('texts.txt') if l.strip()]
missing = [line for line in manifest if line not in src]
```

Output:
```
baris texts.txt: 112
baris TIDAK ADA di gen_image.py (exact): 0
baris ADA di gen_image.py: 112
```

### 1b. Tiap string D_* tables ada di texts.txt

Perintah: parse AST gen_image.py, ambil semua string dari assignment
yang namanya diawali `D_`, bandingkan dengan texts.txt.

Output:
```
string D_* (unik): 91
string D_* TIDAK ADA di texts.txt: 3
  NOT IN MANIFEST: 'building'
  NOT IN MANIFEST: 'fire'
  NOT IN MANIFEST: 'ship'
```

Penjelasan: 'building', 'fire', 'ship' adalah identifier jenis
ilustrasi (bukan teks tampil) — dipakai untuk memilih template gambar.
Bukan teks yang tampil di halaman, jadi benar tidak ada di texts.txt.

### 1c. Metode hook (.done) vs metode sumber

File `.done` (sesi Qwen 5e3c21de) mengklaim diff 0 lewat hook
`ImageDraw.text` + menggabungkan kembali baris hasil wrap.
Oyoi mencoba hook sederhana (tanpa penggabungan ulang) dan hasilnya
126 string unik dengan banyak fragmen (huruf tunggal dari `tracked()`
yang menggambar huruf per huruf, dan potongan baris dari `wrap()`).
Itu keterbatasan metode hook sederhana, bukan kegagalan isi:
verifikasi 1a + 1b di atas (ekstraksi sumber) menunjukkan texts.txt
memuat tepat 112 string tampil dari gen_image.py, 0 hilang, 0 berlebih.

Hasil: **LULUS** (teks tampil = 112 string, 0 hilang, 0 berlebih).

## §2 — Gate 2: grep 12 kata terlarang (per kata)

Perintah: `grep -c "<kata>" gen_image.py` untuk tiap kata.

Output mentah:
```
'[CERITA' : 0
'wildfire' : 0
'flat block' : 0
'Rout' : 0
'Late winner' : 0
'pull away' : 0
'defence shuts' : 0
'grind out' : 0
'two US radars' : 0
'Two wounded' : 0
'base ship' : 0
'SLOTS HELD' : 0
TOTAL grep (semua kata): 0
```

Hasil: **LULUS** (semua 0).

## §3 — Gate 3: crop 1:1 tiap tingkat, jarak minimum

### 3a. Crop

10 crop 1:1 dibuat di `proof/crops-D/`:
```
01-masthead.png    (1024x130)
02-angka.png       (1024x80)
03-timeline.png    (1024x80)
04-wilayah-peta.png (1024x110)
05-utama.png       (1024x180)
06-menengah-1.png  (1024x100)
07-menengah-2.png  (1024x100)
08-inbrief.png     (1024x100)
09-datecheck.png   (1024x100)
10-footer.png      (1024x44)
```

### 3b. Ukur celah vertikal antar baris tinta (metode piksel)

Perintah: baca image.png, threshold tinta (<128), hitung baris kosong
antar baris bertinta per tingkat.

Output:
```
angka (130-210):     celah min=2,  gaps=[2, 4, 14]
timeline (210-290):  celah min=1,  gaps=[1, 3, 8, 9, 16]
utama (400-580):     celah min=2,  gaps=[2, 7, 18]
menengah (580-780):  celah min=2,  gaps=[2, 3, 7, 7, 10]
datecheck (880-980): celah min=3,  gaps=[3, 6]
```

Tidak ada celah 0px (tidak ada tinta yang menempel/menimpa).
Catatan: celah minimum 1px ada di timeline — baris kedua label
"03:30 Strathmore, California" sangat dekat dengan baris
"01:00 Wembanyama tipoff" di atasnya. Ketat, tapi tidak menimpa
(dikonfirmasi visual di §3c).

### 3c. Ukur dari .done (sesi Qwen, metode kotak + tinta)

- Poin 8: "dasar sub tiap kartu masih di dalam band barisnya
  (max bottom 180 vs row bottom 184)" — margin 4px.
- Poin 10: "label-vs-pin 0 benturan, label-vs-label 0 benturan,
  semua label di dalam panel peta. Uji piksel: 0 tinta non-pin di
  dalam ketiga lingkaran pin."

### 3d. Inspeksi visual (oyoi, image.png 1024px)

- Tidak ada label yang menimpa label lain.
- Tidak ada teks terpotong.
- Tidak ada placeholder bocor.
- Peta: pin 1/2/3 dengan label COP31 ANTALYA, BENGHAZI, SITRA
  + garis penghubung; tidak menimpa.
- Timeline: 7 label tidak menimpa; "03:30 Strathmore, California"
  di baris kedua, dekat tapi tidak menimpa "01:00 Wembanyama tipoff".

Hasil: **LULUS dengan catatan** — tidak ada tumpang tindih (celah
minimum terukur 1px di timeline, bukan 0px). Syarat "jarak min 4px"
terpenuhi untuk sub kartu menengah (margin 4px, §3c) dan peta
(0 benturan), tetapi celah baris timeline 1px berada di bawah 4px
(metode ukur berbeda: celah antar baris teks, bukan antar elemen).

## §4 — Gate 4: render 300px dan 512px berdampingan dengan 7da71f0

### 4a. File

```
entry-compare/entry-D.png        (1024x1024, sha f155ad08...)
entry-compare/entry-7da71f0.png  (1024x1024, sha 0433e1d8...)
entry-compare/D-300px.png        (300x300)
entry-compare/D-512px.png        (512x512)
entry-compare/7da71f0-300px.png  (300x300)
entry-compare/7da71f0-512px.png  (512x512)
entry-compare/compare-300px.png  (620x300, D kiri, 7da71f0 kanan)
entry-compare/compare-512px.png  (1044x512, D kiri, 7da71f0 kanan)
```

Sha gambar:
```
D:       f155ad08893ce9cb13dcc2da074075b1afe401255ecc376100fd9208c5f651c6
7da71f0: 0433e1d8b345ef46087dd7751a95dcdb48a2bc2f1f63cc770e0723c11bf6307b
```

### 4b. Perbandingan visual (oyoi, 512px)

- D: 18 cerita, layout padat. Masthead, angka (12, 720/9, 4-0, 186, 50),
  timeline 7 kejadian, peta + 3 pin, 3 utama, 10 menengah, IN BRIEF,
  DATE CHECK, footer "18 STORIES" — semua terbaca di 512px.
- 7da71f0: ~10 cerita, layout lapang, headline COP31 besar.
- Di 512px: D terbaca (walau padat), tidak ada label nabrak, teks
  kepotong, placeholder bocor, atau salah fakta yang terlihat.

### 4c. Perbandingan visual (oyoi, 300px)

- **D lebih susah dibaca dari 7da71f0 di 300px.**
  Teks kecil D (label timeline, IN BRIEF, DATE CHECK, sub kartu
  menengah) menjadi tidak terbaca di 300px. 7da71f0 tetap terbaca
  karena teksnya lebih besar.
- Penyebab: kepadatan — D memuat 18 cerita di kanvas yang sama,
  7da71f0 ~10 cerita. Ini tradeoff desain (lebih banyak cerita =
  teks lebih kecil), bukan cacat satu elemen.
- Tidak ada label nabrak, teks kepotong, placeholder bocor, atau
  salah fakta di 300px — masalahnya keterbacaan ukuran kecil.

Hasil: **GAGAL** pada kriteria "D tidak lebih susah dibaca dari
7da71f0" di 300px. Di 512px dan 1024px D terbaca.

## §5 — Gate 5: rebuild 2x sha sama

Perintah: `python3 gen_image.py` dua kali, `sha256sum image.png`.

Output:
```
wrote image.png (1024, 1024)
rebuild 1: f155ad08893ce9cb13dcc2da074075b1afe401255ecc376100fd9208c5f651c6
wrote image.png (1024, 1024)
rebuild 2: f155ad08893ce9cb13dcc2da074075b1afe401255ecc376100fd9208c5f651c6
```

Hasil: **LULUS** (sha identik, 187.018 byte).

## §6 — Gate 6: preflight python 3.13.18 -P -s, 3 run exit 0

### 6a. Restore python (catatan)

`/opt/cpython313/python/bin/python3` hilang (VM restart menghapus
/opt). Direstore dari tarball `~/workspace/cpython313.tar.gz` via
`~/workspace/restore-python313.sh`. Versi terkonfirmasi:
`Python 3.13.18`.

### 6b. Preflight (3 run)

Perintah tiap run:
```
env -i TZ=UTC PYTHONHASHSEED=0 LANG=C.UTF-8 \
  MAKEFUN_BOT_DIR=/home/hatch/workspace/makefun/news-image-20261122 \
  MAKEFUN_OUTPUT_DIR=/tmp \
  /opt/cpython313/python/bin/python3 -P -s main.py
```

Output mentah (3 run, identik):
```
--- run 1 ---
entry: /tmp/entry.png
size : 187018 bytes
sha256: f155ad08893ce9cb13dcc2da074075b1afe401255ecc376100fd9208c5f651c6
exit code: 0
--- run 2 ---
entry: /tmp/entry.png
size : 187018 bytes
sha256: f155ad08893ce9cb13dcc2da074075b1afe401255ecc376100fd9208c5f651c6
exit code: 0
--- run 3 ---
entry: /tmp/entry.png
size : 187018 bytes
sha256: f155ad08893ce9cb13dcc2da074075b1afe401255ecc376100fd9208c5f651c6
exit code: 0
```

Verifikasi sha:
```
f155ad08893ce9cb13dcc2da074075b1afe401255ecc376100fd9208c5f651c6  /tmp/entry.png
f155ad08893ce9cb13dcc2da074075b1afe401255ecc376100fd9208c5f651c6  image.png
```

### 6c. Status: simulasi, bukan grader asli

Preflight di atas berjalan di workdir lokal, BUKAN kondisi grader:
- Bukan user 65534.
- Bukan repo read-only di /bot.
- Bukan cwd /.
- MAKEFUN_BOT_DIR menunjuk workdir lokal, bukan /bot.
- Tidak ada batas CPU/memori 1 CPU/512 MB/60 s.
- Tidak ada jaringan (grader juga tanpa jaringan — ini sama).

Yang terbukti: `main.py` jalan 3x exit 0 di python 3.13.18 `-P -s`
dengan env grader (TZ, PYTHONHASHSEED, LANG) dan menghasilkan
entry.png sha f155ad08 yang sama dengan image.png.
Yang belum diuji: kondisi grader penuh (user 65534, /bot read-only,
cwd /, batas sumber daya).

Hasil: **LULUS (simulasi)** — 3 run exit 0, output identik.

## §7 — Gate 7: main.py stdlib only

Perintah: parse AST main.py, kumpulkan semua import, bandingkan
dengan `sys.stdlib_module_names`.

Output:
```
import di main.py: ['hashlib', 'os', 'shutil', 'sys']
stdlib (3.13): SEMUA STDLIB
```

Isi main.py (ringkas): program copy stdlib — menyalin image.png
yang sudah dirender ke MAKEFUN_OUTPUT_DIR/entry.png. Tidak import
gen_image.py, tidak import PIL. (Ini perbaikan dari penolakan
round 1/2 yang disebabkan main.py import gen_image.py → PIL.)

Hasil: **LULUS** (4 import, semua stdlib).

## §8 — Git: tree lokal vs remote

Perintah: `git rev-parse HEAD`, `git rev-parse HEAD^{tree}`,
`git rev-parse origin/readability-v4`,
`git rev-parse origin/readability-v4^{tree}`.

Output:
```
lokal HEAD:         4bb8de4f753f84380cbaa92d4615fe1ad5dcd9fa
lokal HEAD^{tree}:  7de0344298583baa0ce2d13d39899855e45e084a
remote HEAD:        12017cdeffddd8ec968981e080f554f5f41fe4e6
remote^{tree}:      7de0344298583baa0ce2d13d39899855e45e084a
tree sama? YA
```

Catatan: commit lokal dan remote berbeda sha (push-branch.py membuat
commit baru di remote dengan parent = remote HEAD), tetapi tree-nya
identik. Poin 8, 9, 10 sudah di remote (commit 12017cd).

## §9 — Klasifikasi: grader asli / simulasi / belum diuji

**Terbukti di grader asli:** tidak ada. Grader asli hanya berjalan
saat submit; tidak ada submit yang dilakukan untuk commit ini.

**Simulasi (kondisi mendekati grader, tapi bukan grader):**
- Preflight §6: python 3.13.18 `-P -s`, env grader, 3 run exit 0.
- Rebuild deterministik §5: 2x sha sama.
- Diff texts.txt §1, grep §2, stdlib §7: cek statis di workdir.

**Belum diuji:**
- Kondisi grader penuh (user 65534, /bot read-only, cwd /, batas
  1 CPU/512 MB/60 s).
- Penilaian grader (skor, ranking) untuk commit ini.
- Keterbacaan D di 300px oleh penilai manusia (oyoi menilai D lebih
  susah dibaca dari 7da71f0 di 300px — lihat §4c).

## §10 — Keputusan submit

- 7 gate TIDAK semuanya lulus pada commit yang sama (Gate 4 gagal
  di 300px; Gate 3 ada catatan timeline gap 1px).
- Otorisasi bersyarat lek 19:20 (SUBMIT-AUTH-0600.md) mensyaratkan
  SEMUA 7 gate lulus + D tidak lebih susah dibaca. Syarat tidak
  terpenuhi → **JANGAN submit**.
- Lek sudah memberi kabar (01:39 WIB) → otorisasi submit 06:00
  **SUDAH BATAL** dengan sendirinya.
- **7da71f0 tetap entri final** sampai lek memutuskan lain.
- Tidak ada tag D-good-N yang dibuat (tidak ada commit yang lolos
  semua gate).

## §11 — File bukti

- `entry-compare/entry-D.png` — entry D (1024px, sha f155ad08).
- `entry-compare/entry-7da71f0.png` — entry 7da71f0 (1024px, sha 0433e1d8).
- `entry-compare/compare-300px.png` — D vs 7da71f0 di 300px.
- `entry-compare/compare-512px.png` — D vs 7da71f0 di 512px.
- `entry-compare/D-300px.png`, `D-512px.png`, `7da71f0-300px.png`,
  `7da71f0-512px.png` — render masing-masing ukuran.
- `proof/crops-D/*.png` — 10 crop 1:1 tiap tingkat.
- `texts.txt` — 112 string tampil.
- `.done` — laporan sesi Qwen 5e3c21de (poin 8+9+10).
- `SUBMIT-AUTH-0600.md` — otorisasi bersyarat lek 19:20 (batal).
