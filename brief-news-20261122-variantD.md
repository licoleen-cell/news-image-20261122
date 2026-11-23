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

## DAFTAR CERITA (batch 1 lek 17:28 — BOLEH DIPAKAI, 10 cerita)
COP31 (molor 2 hari tanpa kesepakatan), Libya Benghazi (suspected, 10 luka ringan),
Bahrain (CLAIM IRGC), Dymer (at least 3, TANPA CONFIRMED), Liverpool 4-0 Man Utd,
Barcelona 3-2 Villarreal, Dallas 51-30 Tennessee, KC 34-7 Arizona,
Buffalo 26-9 Miami, drone Rusia 186/161.
NUNGGU KEPUTUSAN LEK (JANGAN DIPAKAI dulu): Verstappen, Strathmore California.
DITAHAN (JANGAN DIPAKAI sampai lek kirim hasil cek): West Bank, Sudan Khartoum,
South Sudan, California (selain Strathmore).
KANDIDAT (a)-(r) DITAHAN (perintah lek 16:07): JANGAN tambah cerita dari daftar
(a)-(r) sebelum lek kasih daftar fakta final. Lihat
plan-news-20261122-variantD.md untuk referensi riset saja.
JANGAN tulis texts.txt sebelum batch 2 lek tiba.

## PROSES
- Hanya ubah gen_image.py + texts.txt. main.py JANGAN disentuh (stdlib-only copy).
- Commit SETIAP selesai satu tahap kecil. Jangan tunggu semua beres.
- 1024x1024 PNG <=1 MiB, deterministik (rebuild 2x sha sama).
- Ukur SATU kali per hal. Snippet yang sama >3x = BERHENTI, tulis .done apa adanya.
- Bukti ke proof/: crop 1:1 tiap tingkat, crop tag, render 300px + 512px
  berdampingan dengan 7da71f0, .done (sha, ukuran, pt tiap tingkat, tinggi huruf
  300px, daftar cerita final).
- Jangan submit apa pun. Hanya build + verifikasi.
