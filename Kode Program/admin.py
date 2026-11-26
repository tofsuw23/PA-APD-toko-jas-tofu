from auth import wajib_admin
from data import (seluruh_sewa, riwayat_hapus, katalog_jas, pengguna, sesi,
                  jenis_jas, ukuran_jas)
from tampilan import (judul_halaman, pesan_error, pesan_sukses, pesan_info,
                      tampilkan_pilihan, tampilkan_tabel_katalog, tampilkan_tabel_ganda,
                      tampilkan_tabel_riwayat, tampilkan_tabel_akun)
from utils import (minta_input_wajib, minta_pilihan, minta_konfirmasi,
                   input_angka_positif, input_id)


def menu_ganda():
    wajib_admin()
    judul_halaman("PEMERIKSAAN DATA GANDA")
    pesan_info("Data akan dianggap ganda jika nama, tanggal, dan kategori sama.\n")
    pasangan = []
    daftar_id = list(seluruh_sewa.keys())
    for i in range(len(daftar_id)):
        for j in range(i + 1, len(daftar_id)):
            id_a = daftar_id[i]
            id_b = daftar_id[j]
            a = seluruh_sewa[id_a]
            b = seluruh_sewa[id_b]
            if (a["nama"].lower() == b["nama"].lower()
                    and a["tanggal"] == b["tanggal"]
                    and a["kategori"] == b["kategori"]):
                pasangan.append((id_a, id_b, a))
    if len(pasangan) == 0:
        pesan_sukses("Tidak ditemukan data ganda.")
    else:
        tampilkan_tabel_ganda(pasangan)
        print(f"\nDitemukan {len(pasangan)} pasangan data ganda.")
        print("Hapus salah satunya melalui menu Hapus data sewa.")


def menu_riwayat():
    wajib_admin()
    judul_halaman("RIWAYAT PENGHAPUSAN DATA")
    if len(riwayat_hapus) == 0:
        pesan_info("Belum ada data yang dihapus.")
        return
    tampilkan_tabel_riwayat()


def menu_katalog():
    wajib_admin()
    judul_halaman("KELOLA KATALOG JAS & STOK")
    tampilkan_tabel_katalog()
    print("\n1. Tambah jas")
    print("2. Ubah stok")
    print("3. Ubah harga per hari")
    print("4. Kembali")
    sub = minta_pilihan("Pilih: ", ("1", "2", "3", "4"), "Pilihan tidak valid, ulangi (1-4)!")
    if sub == "4":
        return
    if sub == "1":
        nama = minta_input_wajib("Nama jas: ", "Nama jas")
        tampilkan_pilihan("JENIS JAS", jenis_jas)
        kode_jenis = minta_pilihan("Pilih jenis: ", jenis_jas, "Pilihan jenis tidak valid!")
        tampilkan_pilihan("UKURAN JAS", ukuran_jas)
        kode_ukuran = minta_pilihan("Pilih ukuran: ", ukuran_jas, "Pilihan ukuran tidak valid!")
        harga = input_angka_positif("Harga sewa per hari (Rp): ", "Harga")
        stok = input_angka_positif("Stok: ", "Stok", boleh_nol=True)
        id_baru = max(katalog_jas) + 1 if katalog_jas else 1
        katalog_jas[id_baru] = {
            "nama": nama,
            "jenis": jenis_jas[kode_jenis],
            "ukuran": ukuran_jas[kode_ukuran],
            "harga_per_hari": harga,
            "stok": stok,
        }
        pesan_sukses(f"\nJas berhasil ditambahkan dengan ID {id_baru}.")
        return
    if len(katalog_jas) == 0:
        pesan_info("Katalog masih kosong.")
        return
    id_jas = input_id("Masukkan ID jas: ", katalog_jas)
    if sub == "2":
        katalog_jas[id_jas]["stok"] = input_angka_positif("Stok baru: ", "Stok", boleh_nol=True)
        pesan_sukses("\nStok berhasil diubah.")
    else:
        katalog_jas[id_jas]["harga_per_hari"] = input_angka_positif("Harga baru per hari (Rp): ", "Harga")
        pesan_sukses("\nHarga berhasil diubah.")


def menu_kelola():
    wajib_admin()
    judul_halaman("KELOLA AKUN")
    tampilkan_tabel_akun()
    print("\n1. Hapus akun")
    print("2. Kembali")
    sub = minta_pilihan("Pilih: ", ("1", "2"), "Pilihan tidak valid, ulangi (1/2)!")
    if sub == "2":
        return
    target = input("Masukkan username yang akan dihapus: ").strip()
    try:
        role_target = pengguna[target]["role"]
    except KeyError:
        pesan_error("Username tidak ditemukan!")
        return
    if target == sesi["username"]:
        pesan_error("Tidak dapat menghapus akun yang sedang dipakai!")
    elif role_target == "Administrator":
        pesan_error("Akun administrator tidak dapat dihapus!")
    elif minta_konfirmasi(f"Yakin hapus akun {target}? (Ya/Tidak): "):
        del pengguna[target]
        pesan_sukses("Akun berhasil dihapus.")
    else:
        pesan_info("Penghapusan dibatalkan.")