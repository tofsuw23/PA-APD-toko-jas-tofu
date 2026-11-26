import json
import os

from auth import proses_login, proses_register
from data import katalog_jas, pengguna, riwayat_hapus, seluruh_sewa
from menu import jalankan_menu_utama
from tampilan import (
    pesan_error,
    pesan_info,
    pesan_sukses,
    tampilkan_header_utama,
    tampilkan_penutup,
    tampilkan_pilihan,
)

FILE_DATA = "data_tofu.json"

MENU_AWAL = {
    "1": "Login",
    "2": "Register",
    "3": "Keluar",
}


def muat_data_eksternal():
    if not os.path.exists(FILE_DATA):
        return
    try:
        with open(FILE_DATA, "r") as file:
            isi = json.load(file)
        if "pengguna" in isi:
            pengguna.clear()
            pengguna.update(isi["pengguna"])
        if "katalog_jas" in isi:
            katalog_jas.clear()
            katalog_jas.update({int(k): v for k, v in isi["katalog_jas"].items()})
        if "seluruh_sewa" in isi:
            seluruh_sewa.clear()
            seluruh_sewa.update({int(k): v for k, v in isi["seluruh_sewa"].items()})
        if "riwayat_hapus" in isi:
            riwayat_hapus.clear()
            riwayat_hapus.update({int(k): v for k, v in isi["riwayat_hapus"].items()})
    except (OSError, json.JSONDecodeError, ValueError) as e:
        pesan_error(f"Gagal memuat file {FILE_DATA} ({e}). Menggunakan data bawaan.")


def simpan_data_eksternal():
    paket_data = {
        "pengguna": pengguna,
        "katalog_jas": katalog_jas,
        "seluruh_sewa": seluruh_sewa,
        "riwayat_hapus": riwayat_hapus,
    }
    try:
        with open(FILE_DATA, "w") as file:
            json.dump(paket_data, file, indent=4, ensure_ascii=False)
    except OSError as e:
        pesan_error(f"Gagal menyimpan data ke {FILE_DATA}: {e}")
    else:
        pesan_sukses(f"Data berhasil disinkronkan ke {FILE_DATA}.")


def main():
    muat_data_eksternal()
    try:
        while True:
            tampilkan_header_utama()
            tampilkan_pilihan("TOKO JAS 'TOFU'", MENU_AWAL)
            opsi = input("Pilih menu: ").strip()

            if opsi == "1":
                if proses_login():
                    jalankan_menu_utama()
                    simpan_data_eksternal()
                else:
                    input("\nTekan Enter untuk mencoba lagi...")
            elif opsi == "2":
                proses_register()
                simpan_data_eksternal()
                input("\nTekan Enter untuk kembali ke menu awal...")
            elif opsi == "3":
                simpan_data_eksternal()
                tampilkan_penutup()
                break
            else:
                pesan_error("Pilihan menu tidak valid! Masukkan angka 1, 2, atau 3.")
                input("\nTekan Enter untuk melanjutkan...")
    except KeyboardInterrupt:
        print()
        pesan_info("Program dihentikan oleh pengguna. Menyimpan data...")
        simpan_data_eksternal()


if __name__ == "__main__":
    main()

    #mantap