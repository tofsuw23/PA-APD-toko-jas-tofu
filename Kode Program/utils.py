"""utils.py - Fungsi bantu: konversi, validasi, dan pengambilan input."""
from datetime import datetime, date, timedelta

from data import hari_per_bulan, nama_tiap_bulan
from tampilan import pesan_error, pesan_info


def ambil_waktu_sekarang():
    return datetime.now().strftime("%d-%m-%Y %H:%M")


def ke_angka(teks, nama="Input"):
    try:
        return int(teks)
    except ValueError:
        raise ValueError(f"{nama} harus berupa angka!") from None


# ---------- Validasi tanggal ----------
def tahun_kabisat(tahun):
    return tahun % 400 == 0 or (tahun % 4 == 0 and tahun % 100 != 0)


def jumlah_hari(bulan, tahun):
    hari = hari_per_bulan[bulan]
    if bulan == 2 and tahun_kabisat(tahun):
        hari = 29
    return hari


def validasi_tanggal(tanggal, bulan, tahun):
    """Return teks tanggal berformat '13 November 2026'."""
    if tahun < 2000 or tahun > 2100:
        raise ValueError("Masukkan tahun hanya antara 2000 - 2100")
    if bulan < 1 or bulan > 12:
        raise ValueError("Masukkan bulan hanya antara 1 - 12")
    mentok_hari = jumlah_hari(bulan, tahun)
    if tanggal < 1 or tanggal > mentok_hari:
        raise ValueError(f"Tanggal tidak valid! (bulan {bulan} hanya sampai tanggal {mentok_hari})")
    return f"{tanggal} {nama_tiap_bulan[bulan]} {tahun}"


def hitung_tgl_kembali(tanggal_sewa, durasi):
    """Tanggal kembali = tanggal sewa + durasi hari.
    Contoh: ("13 November 2026", 3) -> "16 November 2026"."""
    hari, nama_bulan, tahun = tanggal_sewa.split()
    bulan = [no for no, nama in nama_tiap_bulan.items() if nama == nama_bulan][0]
    hasil = date(int(tahun), bulan, int(hari)) + timedelta(days=durasi)
    return f"{hasil.day} {nama_tiap_bulan[hasil.month]} {hasil.year}"


# ---------- Input berulang sampai valid ----------
def minta_input_wajib(pesan, label):
    teks = input(pesan).strip()
    if len(teks) == 0:
        pesan_error(f"{label} tidak boleh kosong!")
        return minta_input_wajib(pesan, label)
    return teks


def minta_pilihan(pesan, daftar_valid, pesan_salah, boleh_kosong=False):
    pilihan = input(pesan).strip()
    if boleh_kosong and pilihan == "":
        return ""
    if pilihan in daftar_valid:
        return pilihan
    pesan_error(pesan_salah)
    return minta_pilihan(pesan, daftar_valid, pesan_salah, boleh_kosong)


def minta_konfirmasi(pesan):
    jawaban = input(pesan).strip().lower()
    if jawaban == "ya":
        return True
    if jawaban == "tidak":
        return False
    return minta_konfirmasi("Masukkan hanya Ya atau Tidak: ")


def input_angka_positif(pesan, nama="Input", boleh_nol=False):
    """Input angka bulat > 0 (dipakai untuk lama sewa / tambah hari).
    boleh_nol=True: angka 0 juga diterima (dipakai untuk stok)."""
    while True:
        try:
            angka = ke_angka(input(pesan).strip(), nama)
            if boleh_nol and angka < 0:
                raise ValueError(f"{nama} tidak boleh kurang dari 0!")
            if not boleh_nol and angka <= 0:
                raise ValueError(f"{nama} harus lebih dari 0!")
        except ValueError as e:
            pesan_error(e)
        else:
            return angka


BATAS_TELEPON = 12


def input_telepon(pesan, boleh_batal=False):
    """Nomor telepon: hanya angka, maksimal BATAS_TELEPON digit.
    boleh_batal=True: input kosong mengembalikan None."""
    while True:
        teks = input(pesan).strip()
        if boleh_batal and teks == "":
            return None
        try:
            if teks == "":
                raise ValueError("Nomor telepon tidak boleh kosong!")
            if not (teks.isascii() and teks.isdigit()):
                raise ValueError("Nomor telepon hanya boleh berisi angka!")
            if len(teks) > BATAS_TELEPON:
                raise ValueError(f"Nomor telepon maksimal {BATAS_TELEPON} angka!")
        except ValueError as e:
            pesan_error(e)
        else:
            return teks


def input_id(pesan, daftar_data):
    """Input ID berupa angka yang ada di daftar_data. Return ID (int)."""
    while True:
        try:
            id_input = ke_angka(input(pesan).strip(), "ID")
            if id_input not in daftar_data:
                raise ValueError("ID tidak ditemukan!")
        except ValueError as e:
            pesan_error(e)
        else:
            return id_input


def input_tanggal(boleh_batal=False):
    while True:
        if boleh_batal:
            pesan_info("\nMasukkan tanggal sewa (kosongkan semua kolom untuk membatalkan):")
        else:
            pesan_info("Masukkan tanggal, bulan, dan tahun secara terpisah di bawah ini:")
        teks_tanggal = input("Masukkan tanggal: ").strip()
        teks_bulan = input("Masukkan bulan: ").strip()
        teks_tahun = input("Masukkan tahun: ").strip()
        if boleh_batal and teks_tanggal == "" and teks_bulan == "" and teks_tahun == "":
            return None
        try:
            tanggal = ke_angka(teks_tanggal, "Tanggal")
            bulan = ke_angka(teks_bulan, "Bulan")
            tahun = ke_angka(teks_tahun, "Tahun")
            hasil = validasi_tanggal(tanggal, bulan, tahun)
        except ValueError as e:
            pesan_error(e)
        else:
            return hasil