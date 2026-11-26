from auth import wajib_admin
from data import (seluruh_sewa, riwayat_hapus, katalog_jas, sesi, jenis_jas,
                  alasan_hapus, dlm_lihat, kolom_admin)
from tampilan import (clear_screen, judul_halaman, pesan_error, pesan_sukses, pesan_info,
                      tampilkan_detail, tampilkan_tabel, tampilkan_pilihan,
                      tampilkan_tabel_katalog)
from utils import (ke_angka, ambil_waktu_sekarang, minta_input_wajib, minta_pilihan,
                   minta_konfirmasi, input_tanggal, input_angka_positif, input_id,
                   input_telepon, hitung_tgl_kembali)


def buat_id_baru():
    id_baru = 1
    for id_sewa in seluruh_sewa:
        if id_sewa >= id_baru:
            id_baru = id_sewa + 1
    for catatan in riwayat_hapus.values():
        if catatan["id_sewa"] >= id_baru:
            id_baru = catatan["id_sewa"] + 1
    return id_baru


def cari_sewa(teks_id):
    id_angka = ke_angka(teks_id.strip(), "ID")
    return id_angka, seluruh_sewa[id_angka]


def cocok_filter(pilihan, data, kata_kunci):
    if pilihan == "1":
        return True
    if pilihan == "2":
        return data["kategori"] == kata_kunci
    if pilihan == "3":
        return data["tanggal"] == kata_kunci
    if pilihan == "4":
        return kata_kunci in data["nama"].lower()
    if pilihan == "5":
        return data["status"] == "Masih disewa"
    if pilihan == "6":
        return data["status"] == "Sudah dikembalikan"
    return False


def _ubah_stok(id_jas, selisih):
    """Tambah/kurangi stok jas di katalog (selisih bisa negatif)."""
    jas = katalog_jas.get(id_jas)
    if jas is not None:
        jas["stok"] += selisih


def _ambil_sewa_dari_input(sumber=None):
    """Tampilkan data sewa dulu, lalu minta ID sewa.
    sumber: dict sewa yang boleh dipilih (default: semua).
    Input kosong = batal. ID salah diminta ulang. Return (id, data) atau None."""
    if sumber is None:
        sumber = seluruh_sewa
    if len(sumber) == 0:
        pesan_info("Belum ada data sewa." if sumber is seluruh_sewa
                   else "Anda belum memiliki transaksi sewa yang bisa diproses.")
        return None
    tampilkan_tabel(sumber)
    print()
    while True:
        teks = input("Masukkan ID sewa (kosongkan untuk batal): ").strip()
        if teks == "":
            pesan_info("Dibatalkan.")
            return None
        try:
            id_sewa, data = cari_sewa(teks)
            if id_sewa not in sumber:
                raise KeyError(id_sewa)
            return id_sewa, data
        except ValueError as e:
            pesan_error(e)
        except KeyError:
            pesan_error("ID tidak ditemukan atau bukan transaksi Anda!"
                        if sumber is not seluruh_sewa else "ID tidak ditemukan!")


def menu_tambah():
    judul_halaman("TAMBAH TRANSAKSI SEWA")
    if len(katalog_jas) == 0:
        pesan_info("Katalog jas masih kosong.")
        return
    if not any(j["stok"] > 0 for j in katalog_jas.values()):
        pesan_error("Semua jas sedang habis stok, transaksi tidak dapat dibuat.")
        return
    nama = minta_input_wajib("Nama penyewa: ", "Nama")
    telepon = input_telepon("Nomor telepon (maks. 12 angka): ")
    print("")
    tanggal_sewa = input_tanggal()
    print("-" * 45)
    print(f"Tanggal sewa : {tanggal_sewa}")
    print("-" * 45)
    pesan_info(f"{nama} menyewa jas berikut:")
    tampilkan_tabel_katalog()
    while True:
        id_jas = input_id("Masukkan ID jas: ", katalog_jas)
        jas = katalog_jas[id_jas]
        if jas["stok"] > 0:
            break
        pesan_error(f"Stok {jas['nama']} ({jas['ukuran']}) habis, pilih jas lain!")
    durasi = input_angka_positif("Lama sewa (hari): ", "Lama sewa")
    new_id = buat_id_baru()
    seluruh_sewa[new_id] = {
        "nama": nama,
        "telepon": telepon,
        "tanggal": tanggal_sewa,
        "id_jas": id_jas,
        "jas": f"{jas['nama']} ({jas['ukuran']})",
        "kategori": jas["jenis"],
        "durasi": durasi,
        "total": jas["harga_per_hari"] * durasi,
        "tgl_kembali": hitung_tgl_kembali(tanggal_sewa, durasi),
        "status": "Masih disewa",
        "dibuat_oleh": sesi["username"],
    }
    jas["stok"] -= 1
    pesan_sukses(f"\nTransaksi sewa berhasil ditambahkan dengan ID {new_id}.")
    pesan_info(f"Sisa stok {jas['nama']} ({jas['ukuran']}): {jas['stok']}")


def menu_lihat():
    judul_halaman("LIHAT DATA SEWA")
    tampilkan_pilihan("CARI BERDASARKAN", dlm_lihat)
    pilihan = input("Pilih kategori data: ").strip()
    if pilihan not in dlm_lihat:
        pesan_error("Pilihan kategori data tidak valid!")
        return
    kata_kunci = ""
    if pilihan == "2":
        clear_screen()
        tampilkan_pilihan("JENIS JAS", jenis_jas)
        pil_jenis = input("Pilih jenis jas: ").strip()
        if pil_jenis not in jenis_jas:
            pesan_error("Pilihan jenis jas tidak valid!")
            return
        kata_kunci = jenis_jas[pil_jenis]
    elif pilihan == "3":
        clear_screen()
        kata_kunci = input_tanggal(boleh_batal=True)
        if kata_kunci is None:
            pesan_info("Pencarian dibatalkan.")
            return
    elif pilihan == "4":
        clear_screen()
        kata_kunci = input("Masukkan nama (boleh sebagian): ").strip().lower()
        if len(kata_kunci) == 0:
            pesan_error("Nama tidak boleh kosong!")
            return
    hasilnya = {}
    for id_sewa, data in seluruh_sewa.items():
        if cocok_filter(pilihan, data, kata_kunci):
            hasilnya[id_sewa] = data
    print()
    if len(hasilnya) == 0:
        pesan_info("Tidak ada data yang sesuai kriteria.")
    else:
        clear_screen()
        tampilkan_tabel(hasilnya)


def menu_kembali():
    judul_halaman("PROSES PENGEMBALIAN JAS")
    if sesi["role"] == "Administrator":
        sumber = seluruh_sewa
    else:  # User biasa hanya boleh mengembalikan transaksi buatannya sendiri
        sumber = {i: d for i, d in seluruh_sewa.items()
                  if d.get("dibuat_oleh") == sesi["username"]}
    hasil = _ambil_sewa_dari_input(sumber)
    if hasil is None:
        return
    id_cari, data = hasil
    if data["status"] == "Sudah dikembalikan":
        pesan_info("Jas pada transaksi ini sudah dikembalikan.")
        return
    tampilkan_detail(data)
    print()
    if not minta_konfirmasi("Proses pengembalian jas ini? (Ya/Tidak): "):
        pesan_info("Pengembalian dibatalkan.")
        return
    data["status"] = "Sudah dikembalikan"
    _ubah_stok(data["id_jas"], 1)
    pesan_sukses("Jas berhasil dikembalikan, stok jas bertambah 1.")


def menu_ubah():
    wajib_admin()
    judul_halaman("UBAH DATA SEWA")
    if len(seluruh_sewa) == 0:
        pesan_info("Belum ada data sewa.")
        return
    hasil = _ambil_sewa_dari_input()
    if hasil is None:
        return
    id_ubah, data = hasil
    tampilkan_detail(data)
    print()
    tampilkan_pilihan("DATA YANG INGIN DIUBAH", {k: v["nama"] for k, v in kolom_admin.items()})
    pilih_kolom = input("Pilih: ").strip()
    if pilih_kolom not in kolom_admin:
        pesan_error("Pilihan tidak valid!")
        return
    kunci = kolom_admin[pilih_kolom]["kunci"]
    if kunci == "nama":
        nama_baru = input("Masukkan nama baru. (Jika bagian ini kosong, perubahan akan dibatalkan): ").strip()
        if len(nama_baru) == 0:
            pesan_info("Perubahan nama dibatalkan.")
        else:
            data["nama"] = nama_baru
            pesan_sukses("\nNama penyewa berhasil diubah.")
    elif kunci == "telepon":
        telepon_baru = input_telepon("Nomor telepon baru (maks. 12 angka, kosong = batal): ",
                                     boleh_batal=True)
        if telepon_baru is None:
            pesan_info("Perubahan nomor telepon dibatalkan.")
        else:
            data["telepon"] = telepon_baru
            pesan_sukses("\nNomor telepon berhasil diubah.")
    elif kunci == "tanggal":
        tanggal_baru = input_tanggal(boleh_batal=True)
        if tanggal_baru is None:
            pesan_info("Perubahan tanggal dibatalkan.")
        else:
            data["tanggal"] = tanggal_baru
            data["tgl_kembali"] = hitung_tgl_kembali(tanggal_baru, data["durasi"])
            pesan_sukses("\nTanggal sewa berhasil diubah.")
    elif kunci == "kategori":
        tampilkan_pilihan("JENIS JAS", jenis_jas)
        kode = minta_pilihan("Pilih jenis jas baru (Jika bagian ini kosong, perubahan akan dibatalkan): ",
                             jenis_jas, "Pilihan jenis jas tidak valid!", boleh_kosong=True)
        if kode == "":
            pesan_info("Perubahan jenis jas dibatalkan.")
            return
        pilihan_jas = {i: j for i, j in katalog_jas.items() if j["jenis"] == jenis_jas[kode]}
        if len(pilihan_jas) == 0:
            pesan_error("Belum ada jas dengan jenis tersebut di katalog!")
            return
        tampilkan_pilihan("JAS", {i: f"{j['nama']} ({j['ukuran']}) - stok {j['stok']}"
                                  for i, j in pilihan_jas.items()})
        id_baru = input_id("Masukkan ID jas: ", pilihan_jas)
        jas = katalog_jas[id_baru]
        # Stok hanya berpindah jika jas masih dipinjam dan jasnya benar-benar berganti
        if data["status"] == "Masih disewa" and id_baru != data["id_jas"]:
            if jas["stok"] <= 0:
                pesan_error("Stok jas tersebut habis, perubahan dibatalkan!")
                return
            _ubah_stok(data["id_jas"], 1)
            jas["stok"] -= 1
        data["id_jas"] = id_baru
        data["jas"] = f"{jas['nama']} ({jas['ukuran']})"
        data["kategori"] = jas["jenis"]
        data["total"] = jas["harga_per_hari"] * data["durasi"]
        pesan_sukses("\nJenis jas berhasil diubah.")
    elif kunci == "durasi":
        durasi_baru = input_angka_positif("Durasi baru (hari): ", "Durasi")
        data["durasi"] = durasi_baru
        data["total"] = katalog_jas[data["id_jas"]]["harga_per_hari"] * durasi_baru
        data["tgl_kembali"] = hitung_tgl_kembali(data["tanggal"], durasi_baru)
        pesan_sukses("\nDurasi sewa berhasil diubah.")
    else:
        tgl_baru = input_tanggal(boleh_batal=True)
        if tgl_baru is None:
            pesan_info("Perubahan tanggal kembali dibatalkan.")
        else:
            data["tgl_kembali"] = tgl_baru
            pesan_sukses("\nTanggal kembali berhasil diubah.")


def menu_hapus():
    wajib_admin()
    judul_halaman("HAPUS DATA SEWA")
    if len(seluruh_sewa) == 0:
        pesan_info("Belum ada data sewa.")
        return
    hasil = _ambil_sewa_dari_input()
    if hasil is None:
        return
    id_hapus, data = hasil
    tampilkan_detail(data)
    print()
    tampilkan_pilihan("ALASAN PENGHAPUSAN", alasan_hapus)
    kode = minta_pilihan("Pilih alasan: ", alasan_hapus, "Pilihan alasan tidak valid!")
    alasan = alasan_hapus[kode]
    if minta_konfirmasi("\nApakah anda yakin ingin menghapus data ini? (Ya/Tidak): "):
        nomor_riwayat = len(riwayat_hapus) + 1
        riwayat_hapus[nomor_riwayat] = {
            "id_sewa": id_hapus,
            "nama": data["nama"],
            "tanggal": data["tanggal"],
            "alasan": alasan,
            "dihapus_oleh": sesi["username"],
            "waktu": ambil_waktu_sekarang(),
        }
        if data["status"] == "Masih disewa":
            _ubah_stok(data["id_jas"], 1)  # transaksi dibatalkan, jas kembali ke stok
        del seluruh_sewa[id_hapus]
        pesan_sukses("Data berhasil dihapus dan dicatat di riwayat penghapusan.")
    else:
        pesan_info("Penghapusan ini dibatalkan.")