import os
from prettytable import PrettyTable, HRuleStyle, VRuleStyle
from data import pengguna, riwayat_hapus, katalog_jas
def pesan_sukses(teks):
    print(teks)
def pesan_error(teks):
    print(teks)
def pesan_info(teks):
    print(teks)
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
def judul_halaman(judul):
    clear_screen()
    print(f"=== {judul} ===")
def format_rupiah(angka):
    return "Rp " + f"{angka:,}".replace(",", ".")
def buat_tabel(judul, kolom, rata_kiri=True):
    tabel = PrettyTable()
    tabel.title = judul
    tabel.field_names = kolom
    if rata_kiri:
        tabel.align = "l"
    tabel.max_width = 34
    tabel.hrules = HRuleStyle.ALL
    tabel.vrules = VRuleStyle.ALL
    return tabel
def tampilkan_pilihan(judul, daftar):
    """daftar: dict {kode: teks}"""
    tabel = buat_tabel(judul, ["No", "Pilihan"])
    for kode, teks in daftar.items():
        tabel.add_row([kode, teks])
    print(tabel)
def tampilkan_menu(judul, menu):
    """menu: dict {nomor: {"nama": ..., "tujuan": ...}}"""
    tabel = buat_tabel(judul, ["No", "Menu"])
    for nomor, isi in menu.items():
        tabel.add_row([nomor, isi["nama"]])
    print(tabel)
def tampilkan_detail(data):
    tabel = buat_tabel("DETAIL PENYEWAAN", ["Keterangan", "Isi"])
    tabel.add_row(["Nama penyewa", data["nama"]])
    tabel.add_row(["Telepon", data["telepon"]])
    tabel.add_row(["Tanggal sewa", data["tanggal"]])
    tabel.add_row(["Jas", data["jas"]])
    tabel.add_row(["Jenis", data["kategori"]])
    tabel.add_row(["Durasi", f"{data['durasi']} hari"])
    tabel.add_row(["Total biaya", format_rupiah(data["total"])])
    tabel.add_row(["Tanggal kembali", data["tgl_kembali"]])
    tabel.add_row(["Status", data["status"]])
    print()
    print(tabel)
def tampilkan_tabel(hasilnya):
    tabel = buat_tabel(
        "DATA PENYEWAAN JAS",
        ["ID", "Penyewa", "Tgl Sewa", "Jas", "Jenis", "Durasi", "Total",
         "Tgl Kembali", "Status"],
    )
    for id_sewa, d in hasilnya.items():
        tabel.add_row([id_sewa, d["nama"], d["tanggal"], d["jas"], d["kategori"],
                       f"{d['durasi']} hari", format_rupiah(d["total"]),
                       d["tgl_kembali"], d["status"]])
    print(tabel)
    print(f"\nTotal: {len(hasilnya)} Data")
def tampilkan_tabel_ganda(pasangan):
    tabel = buat_tabel("DATA GANDA", ["ID A", "ID B", "Penyewa", "Tgl Sewa", "Jas"])
    for id_a, id_b, d in pasangan:
        tabel.add_row([id_a, id_b, d["nama"], d["tanggal"], d["jas"]])
    print(tabel)
def tampilkan_tabel_riwayat():
    tabel = buat_tabel(
        "RIWAYAT PENGHAPUSAN DATA",
        ["ID", "Penyewa", "Tanggal", "Alasan", "Oleh", "Waktu Hapus"],
    )
    for r in riwayat_hapus.values():
        tabel.add_row([r["id_sewa"], r["nama"], r["tanggal"],
                       r["alasan"], r["dihapus_oleh"], r["waktu"]])
    print(tabel)
    print(f"\nTotal: {len(riwayat_hapus)} data dihapus")
def tampilkan_tabel_katalog():
    tabel = buat_tabel(
        "KATALOG JAS",
        ["ID", "Nama Jas", "Jenis", "Ukuran", "Harga/Hari", "Stok"],
    )
    for id_jas, j in katalog_jas.items():
        tabel.add_row([id_jas, j["nama"], j["jenis"], j["ukuran"],
                       format_rupiah(j["harga_per_hari"]), j["stok"]])
    print(tabel)
def tampilkan_tabel_akun():
    tabel = buat_tabel("DAFTAR AKUN", ["No", "Username", "Role"])
    for nomor, (nama_user, info) in enumerate(pengguna.items(), start=1):
        tabel.add_row([nomor, nama_user, info["role"]])
    print(tabel)
def tampilkan_header_utama():
    clear_screen()
    print("=" * 42)
    print("          SISTEM PENYEWAAN JAS")
    print("=" * 42)
def tampilkan_penutup():
    clear_screen()
    print("=" * 68)
    print("")
    print(" Sebelum pulang kerja, pastikan semua jas sudah tertata rapi ♥♥♥")
    print("")
    print("JANGAN LUPA ISTIRAHAT YANG CUKUP ♥♥♥".center(68, " "))
    print("")
    print("=" * 68)