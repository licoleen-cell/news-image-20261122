# RENCANA VARIAN D — news-image-20261122 (draft, 2026-11-23 15:48 WIB)
# Branch: readability-v4 (dari 7da71f0). Tenggat rencana 17:00 WIB.
# Daftar cerita final MENUNGGU daftar fakta dari lek (dikirim sebelum 17:00).

## MASALAH UTAMA C (yang diperbaiki di D)
- C terlalu banyak teks, hampir tidak ada gambar. Top 10 memakai ilustrasi adegan
  berwarna di hampir tiap kartu + peta berpin + timeline UTC + 24-39 cerita.
- 2 KESALAHAN C (dikoreksi lek, dikonfirmasi oyoi 15:48):
  (a) Kotak FRIDAY di IN BRIEF MENIMPA label BEPI COLOMBO — klaim "tidak ada
      tabrakan" di laporan C SALAH. Bukti: crop /tmp/inbrief-C-right.png.
  (b) Strip angka menulis "3 DEAD CIKANDE" dan "24 DEAD NIGERIA" TANPA "at least",
      bertentangan dengan headline "at least three" / "at least 24". Bukti:
      gen_image.py C baris 68-69 vs 93/99.
  Aturan D: (a) tidak ada kotak/tag yang menimpa teks — jarak minimum 4px;
  (b) strip angka dan headline HARUS sama kata dan angkanya ("at least" bila
  sementara).

## TEMUAN LEADERBOARD (dilihat sendiri, 23 Nov 15:47 WIB, top 10)
- Semua top 10 punya kotak DATE CHECK. Yang paling sering dibuang:
  El Chapo Isidro (ranks 1,2,4,5,6,7,10), Kryvyi Rih (1,2,4,6,7,9,10),
  Peru quake (1,3,4,5,6,7,8,9), 400-drone barrage (1,3,4,6,7,9),
  BepiColombo (ranks 1,5 sebagai Sabtu; rank 7 dengan WAKTU "Sat 18:24 UTC";
  rank 10 memasukkannya sebagai cerita, bukan buangan),
  Nvidia (rank 2: SEC probe Fri 20; rank 10: sell-off Fri 20).
  TIDAK ADA kotak date check yang menyebut "Markets" sebagai topik buangan.
- Jumlah cerita: 24 (rank 2) sampai 39 (rank 6). Struktur konsisten:
  baris angka besar, strip timeline UTC, strip wilayah, 3 utama,
  10 kartu menengah, daftar kecil (11-26 item), peta dunia berpin bernomor,
  tag CLAIM/CONFIRMED/REPORTED/PENDING + legenda.
- TIDAK MENYALIN teks atau gambar entri mana pun. Desain D dibuat sendiri.

## KEPUTUSAN TANGGAL PER CERITA (aturan ketat: hanya kejadian Minggu 22 Nov UTC)
| Cerita | Tanggal kejadian | Keputusan | Alasan |
|---|---|---|---|
| Mexico (El Chapo Isidro) | Jumat 20 Nov 2026 | BUANG → date check | CNN + Wikipedia: ditangkap Jumat 20 Nov di Guasave. 7 dari 10 top-10 juga membuangnya. |
| Markets (S&P -3.7%, Nasdaq -5.3%) | Jumat 20 Nov 2026 | BUANG → date check | Data penutupan Jumat; pasar tutup akhir pekan. Tidak ada label Friday. |
| BepiColombo | Sabtu 21 Nov 18:24 UTC | BUANG → date check | ESA konfirmasi Sabtu; rank 7 menulis waktu persis "Sat 18:24 UTC". |
| Sparta II | Sabtu 21 Nov ~06:50 UTC | BUANG → date check | Api mulai Sabtu 06:50 UTC. Status "masih menyala Minggu" adalah perkembangan, bukan kejadian baru. |
| Cikande | Sabtu 21 Nov 2026 malam | **BUANG → date check** (perintah lek 15:52) | Api mulai Sabtu malam. Laporan Minggu hanya perkembangan pencarian. |
| Bolsonaro | Jumat 20 Nov 2026 (masuk RS) | BUANG → date check | Masuk RS Jumat 20 Nov (akut abdomen). "Stable" Minggu hanya update status. Rank 5 menulisnya Sabtu di date check. |
| Nigeria (Bayelsa) | TIDAK PASTI | **JANGAN DIPAKAI** (perintah lek 15:52) | Jangan dipakai sampai lek kasih 2 sumber bertanggal 22 Nov. Pernyataan NEMA 21 Nov + konsensus leaderboard (Jumat 20 Nov) menunjukkan kapal terbalik Jumat. |

Catatan: Cikande dan Nigeria KELUAR dari pool D (Cikande ke date check, Nigeria
ditahan). Daftar final 24-30 cerita bergantung pada daftar fakta lek.

## STRUKTUR D (target 24-30 cerita)
1. Masthead: THE WORLD / SUNDAY 22 NOVEMBER 2026 (paling prominent).
2. Baris angka besar (5-6 angka, >=48pt, dari fakta terverifikasi saja).
3. Timeline jam UTC (strip horizontal: kejadian kunci Minggu 22 Nov per jam UTC).
4. Bar warna wilayah (strip: region per cerita, warna konsisten).
5. 3 UTAMA (headline 32-36pt, sub minimum 18pt, ilustrasi adegan besar).
6. 8-10 MENENGAH (headline 24-28pt, sub minimum 18pt, ilustrasi adegan sedang).
7. DAFTAR KECIL (19pt, 10-16 item, 1 baris per cerita).
   LANTAI FONT (diukur 15:52, Noto Serif, PIL; perintah lek 16:07: sub minimum 18pt,
   list 19pt — 14-17pt TIDAK terbaca): 18pt = x-height 2.93px @300 (borderline);
   19pt = x-height 3.22px @300 (jelas terbaca). 16-17pt (x 2.64px) TIDAK terbaca.
   Hitung cerita: 3 utama + 10 menengah + 11 daftar (19pt, lh 24px, seksi 264px)
   = 24 cerita (minimum). JANGAN kurangi di bawah 24 cerita.
   ATURAN TUNGGAL (perintah lek 16:07): font TIDAK turun, jumlah cerita TIDAK
   di bawah 24, yang dipotong HANYA panjang sub (fewer words).
8. Peta dunia berpin bernomor (pin 1-13, sesuai nomor cerita).
9. Tag: CLAIM (merah, klaim sepihak), CONFIRMED (hijau, 2+ sumber),
   REPORTED (netral, dilaporkan tapi belum terverifikasi penuh).
10. Kotak DATE CHECK (daftar cerita Jumat/Sabtu yang sengaja dibuang + alasan
    tanggalnya). BUKAN label Friday di cerita.
11. Footer: jumlah cerita + PAGE ONE.

## TEMPLATE ILUSTRASI — 4-5 TEMPLATE BERPARAMETER (perintah lek 15:52)
Satu fungsi per template, parameter (warna, simbol, label) yang beda per cerita.
BUKAN gambar unik per cerita. Digambar dengan kode (Pillow), datar + berwarna,
bentuk geometris sederhana. Jangan ulang ikon bola dunia.
1. **API/ASAP** (param: warna api, tinggi asap, ada gedung atau tidak) —
   kebakaran, serangan drone, ledakan, kota terbakar.
2. **KAPAL/LAUT** (param: warna laut, api/asap on-off, jenis kapal) —
   kapal terbakar, pelabuhan, laut, angkatan laut.
3. **GEDUNG/SIMBOL** (param: bentuk gedung, simbol: kotak suara / palu / termometer,
   warna) — pemilu, pengadilan, parlemen, institusi, iklim.
4. **OLAHRAGA/KENDARAAN** (param: lapangan/lintasan, bola/mobil, warna tim, skor) —
   sepak bola, balap, final, transportasi.
5. **MEDIS/DARURAT** (param: simbol: ambulans / monitor ICU / palang, warna) —
   kesehatan, kecelakaan, darurat, rumah sakit.
Aturan: 2-3 warna datar per adegan. Tidak ada foto, tidak ada gambar hasil salin.

## KONSISTENSI TEKS (aturan keras)
- Strip angka dan headline SAMA kata dan angkanya. "at least" bila sementara.
- Tidak ada kotak/tag yang menimpa teks (jarak minimum 4px antar elemen).
- ATURAN TUNGGAL (perintah lek 16:07): font TIDAK turun (sub minimum 18pt,
  list 19pt), jumlah cerita TIDAK di bawah 24, yang dipotong HANYA panjang sub.
  Cek tabrakan visual (jarak 4px) lewat crop 1:1 tiap tingkat.

## ATURAN SUMBER + ZONA WAKTU (perintah lek 16:07)
- Semua sumber "PST" setelah 16:00 itu SUDAH 23 Nov UTC (PST = UTC-8) — jangan
  dipakai sebagai bukti 22 Nov. Contoh yang sudah terkoreksi: KIRO "22 Nov 23:55
  PST" (Zelenskyy) = 23 Nov 07:55 UTC; KIRO "22 Nov 23:40 PST" (Thailand) =
  23 Nov 07:40 UTC; KIRO "22 Nov 17:23 PST" (Cikande) = 23 Nov 01:23 UTC.
  KIRO "22 Nov 08:53 PST" (Dymer) = 22 Nov 16:53 UTC — masih 22 Nov, OK.
- Tiap sumber WAJIB punya tahun 2026 di tanggalnya.

## KETERBACAAN 300px
- Angka besar (>=48pt) dan headline utama (32-36pt) HARUS terbaca di 300px.
- Lapor ukuran font + tinggi huruf (em/cap/x-height) per tingkat.

## PROSES (satu proses, sesi baru, brief pendek, batas looping 3x)
- Branch readability-v4 (dari 7da71f0). Commit per tahap kecil + push ke remote.
- Sesi Qwen BARU (jangan resume sesi lama). Brief pendek (maks 1 halaman).
- Batas looping: snippet yang sama >3x = hentikan + lapor (skrip check-qwen-loop.sh).
- Restart atau macet: lapor saat itu juga.
- Tenggat: rencana 17:00, build selesai 20:00, laporan bukti 21:00.
  Jam 23:00 belum siap: BERHENTI, 7da71f0 tetap kandidat, pindah hidden-spec-cli.

## STATUS (diperbarui 17:28 WIB, batch 1 lek)
- Rencana ini DRAFT. Daftar cerita final menunggu batch 2 lek.
- BATCH 1 — BOLEH DIPAKAI (10 cerita): COP31 (molor 2 hari tanpa kesepakatan),
  Libya Benghazi (suspected, 10 luka ringan), Bahrain (CLAIM IRGC),
  Dymer (at least 3, TANPA CONFIRMED), Liverpool 4-0 Man Utd,
  Barcelona 3-2 Villarreal, Dallas 51-30 Tennessee, KC 34-7 Arizona,
  Buffalo 26-9 Miami, drone Rusia 186/161.
- NUNGGU KEPUTUSAN LEK (JANGAN DIPAKAI dulu): Verstappen, Strathmore California.
- DITAHAN — JANGAN DIPAKAI sampai lek kirim hasil cek: West Bank, Sudan Khartoum,
  South Sudan, California (selain Strathmore).
- Butuh 14-20 cerita lagi dari batch 2 lek untuk mencapai 24-30.

## KANDIDAT TAMBAHAN — DITAHAN (perintah lek 16:07)
JANGAN tambah cerita dari daftar (a)-(r) di bawah ini sebelum lek kasih daftar
fakta final (sebelum 17:00). Daftar ini HANYA referensi riset, bukan untuk dipakai.
Riset oyoi 15:52 WIB — 1 sumber tiap cerita, BUTUH sumber ke-2.
(a) ICJ: Myanmar lakukan genosida terhadap Rohingya — KOREKSI 15:52: putusan ICJ
    tanggal KAMIS 19 Nov 2026 (ReliefWeb 20 Nov; TBS "On 19 November, the ICJ found
    Myanmar responsible"; Asia Daily "On November 19, 2026"). Yang terjadi 22 Nov
    hanya reaksi (Malaysia umumkan penghormatan 22 Nov; Myanmar tolak Jumat).
    → DATE CHECK (Kamis 19 Nov), BUKAN cerita D.
(b) Zelenskyy akui Ukraina di balik serangan kapal perang Rusia di Libya —
    KOREKSI 15:52: konfirmasi Zelenskyy tanggal SENIN 23 Nov 2026 (post X 23 Nov;
    Reuters/CNN "said on Monday"). Serangan itu sendiri Minggu 22 Nov (dini hari)
    dan SUDAH jadi cerita D (Libya, "suspected"). Konfirmasi Senin TIDAK mengubah
    atribusi "suspected" untuk koran 22 Nov. → BUKAN cerita D.
(c) Dymer: 3 tewas, lainnya terkubur (KIRO 22 Nov 08:53 PST) — sudah di C tanpa angka.
(d) Thailand: pengadilan tegakkan vonis pencemaran nama raja — KOREKSI 15:55:
    putusan pengadilan banding tanggal SENIN 23 Nov 2026 (Reuters "on Monday";
    AP "An appeals court Monday upheld the conviction"). Timestamp KIRO
    "22 Nov 23:40 PST" menyesatkan (PST = 23 Nov di Bangkok/UTC).
    → BUKAN cerita D.
(e) Okinawa: aula Kastil Shuri dipulihkan 7 tahun setelah kebakaran (KIRO 22 Nov).
(f) Nepal PM Balendra Shah tiba di Delhi (Minggu 22 Nov) — TERKONFIRMASI 2+ sumber
    (PTI/Nagaland Post "arrived in New Delhi on Sunday"; IANS/Freedom Press
    "arrived in Delhi on Sunday"; Asia Daily "arrive on Sunday"). Pembicaraan
    dengan Modi Senin 23 Nov, tapi KEDATANGAN-nya Minggu. SIAP dipakai.
(g) India-China: pembicaraan militer perbatasan Arunachal (Dainik Jagran 22 Nov).
(h) India vs NZ Test: India deklarasi 720/9, unggul 352 run (Dainik Jagran 22 Nov).
(i) Korea Selatan: pengunduran diri menteri pendidikan diterima (AppiSToS 22 Nov 07:25).
(j) Guatemala: buronan Meksiko ditangkap (AppiSToS 22 Nov 05:18).
(k) Paolo Bulgari meninggal 89 tahun (KIRO/AppiSToS 22 Nov).
(l) Phumzile Mlambo-Ngcuka meninggal 71 tahun (KIRO 22 Nov).
(m) Polandia: puing Kh-101 di tiga lokasi (AppiSToS 22 Nov 20:14).
(n) Sepak bola Minggu 22 Nov: Liverpool 4-0 Man Utd; Barcelona 3-2 Villarreal;
    final Copa Sudamericana Atletico MG 0-2 Boca Juniors — TERKONFIRMASI 2+ sumber
    (LiveScore + FBref + pitchlabstats, semua 22 Nov). SIAP dipakai.
(o) NFL Minggu 22 Nov: Dallas 51-30 Tennessee; Kansas City 34-7 Arizona;
    Buffalo 26-9 Miami — 1 sumber (footballdb). BUTUH sumber ke-2.
(p) Inggris-UE: kesepakatan pasca-Brexit (Open Chronicle 22 Nov).
(q) ICE: protes di Gilroy + agen ICE di bandara Seattle (KPFA 22 Nov).
(r) Eisenkot kutuk serangan pemukim Tepi Barat (Open Chronicle 22 Nov) — perkembangan
    Minggu dari cerita West Bank yang sudah ada.
CATATAN TANGGAL (dari riset 15:52, memperkuat keputusan di atas):
- Nigeria: pernyataan NEMA soal 24 jenazah dikeluarkan 21 Nov (AppiSToS 22 Nov 02:19)
  → mendukung konsensus leaderboard (kapal terbalik Jumat 20 Nov). Menunggu cek fakta lek.
- Cikande: laporan 22 Nov 17:23 PST soal "34 pekerja hilang" masih dicari (KIRO) —
  kebakaran masih berlangsung/dilaporkan Minggu, tapi rank 5 menulis Sabtu. Menunggu cek fakta lek.
- Shenzhen (Trump-Putin-Xi): pertemuan Kamis 19 Nov (date check rank 3,4,8,10) → DATE CHECK,
  bukan cerita D, walau dilaporkan 22 Nov.
- Iran "strikes 3 tankers": kemungkinan insiden Hormuz Jumat/Sabtu yang dilaporkan 22 Nov
  → JANGAN dipakai tanpa verifikasi tanggal kejadian.
