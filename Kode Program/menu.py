from admin import menu_ganda, menu_katalog, menu_kelola, menu_riwayat
from auth import AksesDitolakError, proses_logout
from data import khusus_admin, khusus_user, sesi
from pengunjung import (
    menu_hapus,
    menu_kembali,
    menu_lihat,
    menu_tambah,
    menu_ubah,
)
from tampilan import (
    clear_screen,
    pesan_error,
    pesan_info,
    tampilkan_menu,
)

DAFTAR_AKSI = {
    "tambah": menu_tambah,
    "lihat": menu_lihat,
    "ubah": menu_ubah,
    "hapus": menu_hapus,
    "kembali": menu_kembali,
    "ganda": menu_ganda,
    "riwayat": menu_riwayat,
    "katalog": menu_katalog,
    "kelola": menu_kelola,
}

FITUR_ADMIN = {"ubah", "hapus", "ganda", "riwayat", "katalog", "kelola"}


def jeda():
    input("\nTekan Enter untuk kembali ke menu...")


def jalankan_menu_utama():
    while True:
        clear_screen()
        is_admin = sesi["role"] == "Administrator"
        menu_aktif = khusus_admin if is_admin else khusus_user

        tampilkan_menu("TOKO JAS 'TOFU'", menu_aktif)
        pilihan = input("Pilih menu: ").strip()

        if pilihan not in menu_aktif:
            pesan_error("Pilihan menu tidak valid! Masukkan nomor yang tersedia.")
            jeda()
            continue

        tujuan = menu_aktif[pilihan]["tujuan"]

        if tujuan == "logout":
            proses_logout()
            pesan_info("Anda berhasil logout.")
            jeda()
            break

        try:
            if tujuan in FITUR_ADMIN and not is_admin:
                raise AksesDitolakError("Menu ini hanya dapat diakses oleh Administrator.")
            aksi = DAFTAR_AKSI[tujuan]
            aksi()
        except AksesDitolakError as e:
            pesan_error(f"\n[AKSES DITOLAK] {e}")
        except KeyError:
            pesan_error(f"\nFitur '{tujuan}' belum terdaftar di sistem.")
        except Exception as e:
            pesan_error(f"\nTerjadi kesalahan tak terduga: {e}")
        finally:
            jeda()