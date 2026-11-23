# DO NOT SUBMIT — branch readability-v3

Branch ini BERISI STATE LAMA (pre-fix) dan BELUM BOLEH DISUBMIT.

Isi saat ini (checkpoint 7a5fc64, dipush sebagai cf3e2ca3):
- Cerita HORMUZ masih ada (sudah DIBUANG — peristiwa Sabtu 21 Nov, bukan 22 Nov).
- Cerita UKRAINE PEACE / Kushner masih ada (sudah DIBUANG — paling lemah).
- Headline Sparta II masih "drone-hit" sebagai fakta (sudah DIBUANG — penyebab hanya klaim).
- Tag CONFIRMED masih menempel di Cikande dan Nigeria (sudah DIBUANG — angka sementara).
- Sub Sparta II masih versi lama.

Branch ini baru BOLEH dipakai submit SETELAH:
1. Fix round selesai (sesi 9222d3df) — 16 cerita, semua koreksi diterapkan.
2. Grep string buangan lolos (0 kemunculan): "drone-hit", "after two days of
   firefighting", "radar" (Houthis), "Hormuz", "Kushner".
3. texts.txt sinkron dengan gambar (diff 0) dan rebuild 2x sha sama.
4. Preflight python 3.13.18 -P -s 3 run exit 0, main.py stdlib-only.
5. lek memberi izin submit eksplisit ("gas submit news-image-20261122").

Kandidat yang sudah SCORED dan aman sebagai cadangan: main 7da71f0 (97.66%).
File ini TIDAK ikut push entry (tidak ada di daftar FILES push script).
Hapus file ini setelah branch dinyatakan layak submit.
