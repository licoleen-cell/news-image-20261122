# BRIEF — Varian D, news-image-20261122 (SESI BARU, singkat, maks 1 halaman)
# Branch: readability-v4 (dari 7da71f0). DAFTAR CERITA final diisi dari daftar fakta lek.
# Tenggat build 20:00 WIB. Baca brief ini SEKALI. Jangan baca ulang. Jangan ukur berulang.

## TUJUAN
Bangun koran THE WORLD, Minggu 22 November 2026, 24-30 cerita. HANYA kejadian
Minggu 22 Nov (UTC) dengan 2 sumber bertanggal 22 Nov. Desain sendiri — jangan
salin teks atau gambar entri mana pun.

## STRUKTUR (atas ke bawah, 1024x1024)
1. Masthead THE WORLD + SUNDAY 22 NOVEMBER 2026 (paling prominent, 138pt).
2. Baris angka besar (5-6 angka, >=48pt, dari fakta terverifikasi saja).
3. Timeline jam UTC (strip horizontal kejadian kunci Minggu 22 Nov per jam UTC).
4. Bar warna wilayah (strip region, warna konsisten per wilayah).
5. 3 UTAMA (headline 32-36pt, sub minimum 18pt, ilustrasi adegan BESAR).
6. 8-10 MENENGAH (headline 24-28pt, sub minimum 18pt, ilustrasi adegan SEDANG).
7. DAFTAR KECIL (19pt, 10-16 item, 1 baris per cerita).
8. Peta dunia berpin bernomor (pin 1-13, sesuai nomor cerita).
9. Tag: CLAIM (merah, klaim sepihak), CONFIRMED (hijau, 2+ sumber),
   REPORTED (netral, dilaporkan tapi belum terverifikasi penuh).
10. Kotak DATE CHECK (cerita Jumat/Sabtu yang sengaja dibuang + tanggalnya).
11. Footer: jumlah cerita + PAGE ONE.

## ILUSTRASI (PRIORITAS — 4-5 TEMPLATE BERPARAMETER, perintah lek 15:52)
Satu fungsi per template, parameter (warna, simbol, label) beda per cerita.
BUKAN gambar unik per cerita. Digambar dengan kode (Pillow), datar + berwarna.
1. API/ASAP (warna api, tinggi asap, gedung on-off) — kebakaran, serangan, ledakan.
2. KAPAL/LAUT (warna laut, api/asap on-off, jenis kapal) — kapal, pelabuhan, laut.
3. GEDUNG/SIMBOL (bentuk gedung, simbol: kotak suara/palu/termometer, warna) —
   pemilu, pengadilan, parlemen, institusi, iklim.
4. OLAHRAGA/KENDARAAN (lapangan/lintasan, bola/mobil, warna tim, skor) —
   sepak bola, balap, final, transportasi.
5. MEDIS/DARURAT (simbol: ambulans/monitor ICU/palang, warna) —
   kesehatan, kecelakaan, darurat, rumah sakit.

## ATURAN TANGGAL (ketat)
- Jumat/Sabtu DIBUANG → masuk DATE CHECK, BUKAN dilabeli Friday.
  Mexico (Jumat 20 Nov), Markets (Jumat 20 Nov), BepiColombo (Sabtu 21 Nov 18:24 UTC),
  Sparta II (api Sabtu 21 Nov 06:50 UTC), Bolsonaro (masuk RS Jumat 20 Nov),
  Cikande (api Sabtu 21 Nov malam — perintah lek 15:52).
- Nigeria: JANGAN DIPAKAI sampai lek kasih 2 sumber bertanggal 22 Nov.
- ICJ Myanmar = Kamis 19 Nov → DATE CHECK. Konfirmasi Zelenskyy = Senin 23 Nov → BUKAN D.

## ATURAN TEKS (keras — perintah lek 16:07)
- Strip angka dan headline SAMA kata dan angkanya ("at least" bila sementara).
- TIDAK ADA kotak/tag yang menimpa teks (jarak minimum 4px antar elemen).
  Cek tabrakan visual lewat crop 1:1 tiap tingkat.
- ATURAN TUNGGAL: font TIDAK turun (sub minimum 18pt, list 19pt), jumlah cerita
  TIDAK di bawah 24, yang dipotong HANYA panjang sub (fewer words).
  14-17pt TIDAK terbaca (terukur: x-height 2.64px @300px).

## ATURAN SUMBER + ZONA WAKTU (perintah lek 16:07)
- Sumber "PST" setelah 16:00 = SUDAH 23 Nov UTC (PST = UTC-8). Jangan dipakai
  sebagai bukti 22 Nov.
- Tiap sumber WAJIB punya tahun 2026 di tanggalnya.
  Total cerita JANGAN di bawah 24 (3 utama + 10 menengah + 11 daftar = 24).

## KETERBACAAN 300px
- Angka besar (>=48pt) dan headline utama (32-36pt) HARUS terbaca di 300px.
- Tulis ukuran font + tinggi huruf (em/cap/x-height) per tingkat di .done.

## DAFTAR CERITA (batch 1+2+4 + keputusan lek 17:53 — 17 cerita)
BERSIH (14): COP31 (molor 2 hari tanpa kesepakatan), Libya Benghazi (suspected,
10 luka ringan), Bahrain (CLAIM IRGC), Dymer (at least 3, TANPA CONFIRMED),
Liverpool 4-0 Man Utd, Barcelona 3-2 Villarreal, Dallas 51-30 Tennessee,
KC 34-7 Arizona, Buffalo 26-9 Miami, drone Rusia 186/161, West Bank (REPORTED:
pemukim serang beberapa desa semalam menuju Minggu 22 Nov, sedikitnya
12 kendaraan dibakar — residents said, Eisenkot mengecam, TANPA angka korban),
India vs NZ Test 1 Wellington hari ke-4 (India declare 720/9 — Pant 128,
Rahul 136 — unggul 352, NZ 119/2), Paus Leo XIV (makan siang dengan sekitar
1.300 orang miskin di Aula Paulus VI Vatikan, Minggu 22 Nov, Hari Orang Miskin
Sedunia ke-10), Hong Kong (pemilihan subsektor Komite Pemilihan 2026 ditutup
18:00 HKT, 5.640 dari 5.709 pemilih, partisipasi 98,79% — REPORTED),
Nepal (PM Balendra Shah tiba di New Delhi Minggu 22 Nov untuk kunjungan
kenegaraan 2 hari, kunjungan bilateral pertamanya sejak menjabat Maret 2026,
bertemu Menlu Jaishankar — JANGAN pertemuan dengan Modi, itu Senin 23 Nov).
DIPAKAI (keputusan lek 17:53, 3): Verstappen, Strathmore California,
Wembanyama (50 poin, 18 rebound, 5 blok, Spurs 114-91 Pelicans,
tipoff 01:00 UTC Minggu 22 Nov). Tulis JAM UTC-nya, JANGAN kata "Saturday".
DITAHAN (JANGAN DIPAKAI sampai lek kirim hasil cek): Sudan Khartoum,
South Sudan, California (selain Strathmore).
LANTAI CERITA: 20. SLOT PLACEHOLDER = 20 - 18 = 2 slot. (Satu angka: 2.)
CHECKPOINT 19:30 WIB: satu render kerangka layout (png, kasar gak papa,
pakai placeholder) + commit/push. Kalau belum ada, lapor jam itu juga.
POLISH TEMPLATE 1+2 DIBATALIN (perintah lek 17:40) — pakai yang ada.
PERBAIKAN KECIL TEMPLATE 3+4 SELESAI (commit 573276f).
SEBELUM BUILD FINAL: grep "[CERITA" HARUS 0 hasil (tempel outputnya).
PERBAIKAN LAYOUT 4 HAL (perintah lek 18:10, WAJIB):
1) STRIP ANGKA: label JANGAN nimpa digit, jarak min 4px, label SAMA PERSIS
   dengan kata headline (contoh: "AT LEAST 12 CARS BURNED").
2) TIMELINE: label gak boleh ketimpa penanda, teks min 11px, kurangi jadi
   6-8 kejadian.
3) HAPUS dari timeline: "06-11 Dymer strike", "00-05 West Bank", "IRGC 04:46".
   ATURAN: jam gak ada di sumber = gak boleh ditaruh. JAM AMAN: Wembanyama
   01:00 UTC, India declare ~01:00 UTC, Hong Kong tutup 10:00 UTC,
   Barcelona 13:00 UTC, Liverpool 16:30 UTC, NFL 18:00 UTC. BOLEH DITAMBAH:
   Strathmore ~03:30 UTC, Verstappen finish ~05:50 UTC.
4) ESTONIA → DATE CHECK (keputusan Jumat 20 Nov, diumumkan Minggu 15 Nov,
   efektif 1 Des).
CHECKPOINT 20:00 WIB: satu render halaman penuh.
KANDIDAT (a)-(r) DITAHAN (perintah lek 16:07): JANGAN tambah cerita dari daftar
(a)-(r) sebelum lek kasih daftar fakta final. Lihat
plan-news-20261122-variantD.md untuk referensi riset saja.
JANGAN tulis texts.txt final sebelum batch berikutnya lek tiba — layout pakai
placeholder dulu.

## PROSES
- Hanya ubah gen_image.py + texts.txt. main.py JANGAN disentuh (stdlib-only copy).
- Commit SETIAP selesai satu tahap kecil. Jangan tunggu semua beres.
- 1024x1024 PNG <=1 MiB, deterministik (rebuild 2x sha sama).
- Ukur SATU kali per hal. Snippet yang sama >3x = BERHENTI, tulis .done apa adanya.
- Bukti ke proof/: crop 1:1 tiap tingkat, crop tag, render 300px + 512px
  berdampingan dengan 7da71f0, .done (sha, ukuran, pt tiap tingkat, tinggi huruf
  300px, daftar cerita final).
- Jangan submit apa pun. Hanya build + verifikasi.
