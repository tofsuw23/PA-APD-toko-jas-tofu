pengguna = {
    "tofu": {"password": "admin123", "role": "Administrator"},
    "izhar": {"password": "aturaja", "role": "User"},
}

katalog_jas = {
    1: {"nama": "Jas Hitam Classic", "jenis": "Jas Pernikahan", "ukuran": "L",
        "harga_per_hari": 150000, "stok": 3},
    2: {"nama": "Tuxedo Navy Slim Fit", "jenis": "Tuxedo", "ukuran": "M",
        "harga_per_hari": 250000, "stok": 2},
    3: {"nama": "Jas Abu Formal", "jenis": "Jas Formal", "ukuran": "XL",
        "harga_per_hari": 100000, "stok": 4},
    4: {"nama": "Jas Wisuda Hitam", "jenis": "Jas Wisuda", "ukuran": "M",
        "harga_per_hari": 90000, "stok": 5},
}

seluruh_sewa = {
    1: {
        "nama": "Muhammad Abdul Aziz",
        "telepon": "081256484756",
        "tanggal": "13 November 2026",
        "id_jas": 1,
        "jas": "Jas Hitam Classic (L)",
        "kategori": "Jas Pernikahan",
        "durasi": 3,
        "total": 450000,
        "tgl_kembali": "16 November 2026",
        "status": "Masih disewa",
    },
    2: {
        "nama": "Muhammad Arya Dhamanullah",
        "telepon": "082198765432",
        "tanggal": "10 November 2026",
        "id_jas": 2,
        "jas": "Tuxedo Navy Slim Fit (M)",
        "kategori": "Tuxedo",
        "durasi": 2,
        "total": 500000,
        "tgl_kembali": "12 November 2026",
        "status": "Sudah dikembalikan",
    },
    3: {
        "nama": "Muhammad Arsyad",
        "telepon": "085611122233",
        "tanggal": "12 November 2026",
        "id_jas": 3,
        "jas": "Jas Abu Formal (XL)",
        "kategori": "Jas Formal",
        "durasi": 1,
        "total": 100000,
        "tgl_kembali": "13 November 2026",
        "status": "Masih disewa",
    },
}
riwayat_hapus = {}
sesi = {"username": "", "role": ""}
khusus_admin = {
    "1": {"nama": "Tambah transaksi sewa", "tujuan": "tambah"},
    "2": {"nama": "Lihat / cari data sewa", "tujuan": "lihat"},
    "3": {"nama": "Ubah data sewa", "tujuan": "ubah"},
    "4": {"nama": "Hapus data sewa", "tujuan": "hapus"},
    "5": {"nama": "Cek data ganda", "tujuan": "ganda"},
    "6": {"nama": "Riwayat penghapusan", "tujuan": "riwayat"},
    "7": {"nama": "Kelola katalog jas & stok", "tujuan": "katalog"},
    "8": {"nama": "Kelola akun petugas", "tujuan": "kelola"},
    "9": {"nama": "Logout", "tujuan": "logout"},
}
khusus_user = {
    "1": {"nama": "Tambah transaksi sewa", "tujuan": "tambah"},
    "2": {"nama": "Lihat / cari data sewa", "tujuan": "lihat"},
    "3": {"nama": "Proses pengembalian jas", "tujuan": "kembali"},
    "4": {"nama": "Logout", "tujuan": "logout"},
}
hari_per_bulan = {
    1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
    7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31,
}
nama_tiap_bulan = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember",
}

jenis_jas = {
    "1": "Jas Pernikahan",
    "2": "Tuxedo",
    "3": "Jas Formal",
    "4": "Jas Wisuda",
    "5": "Jas Pesta",
    "6": "Jas Anak",
}
ukuran_jas = {
    "1": "S",
    "2": "M",
    "3": "L",
    "4": "XL",
    "5": "XXL",
}
alasan_hapus = {
    "1": "Data ganda (double)",
    "2": "Penyewa fiktif / batal",
    "3": "Salah data",
}
dlm_lihat = {
    "1": "Semua data",
    "2": "Berdasarkan jenis jas",
    "3": "Berdasarkan tanggal sewa",
    "4": "Berdasarkan nama penyewa",
    "5": "Yang masih disewa (belum kembali)",
    "6": "Yang sudah dikembalikan",
}
kolom_admin = {
    "1": {"nama": "Nama penyewa", "kunci": "nama"},
    "2": {"nama": "Nomor telepon", "kunci": "telepon"},
    "3": {"nama": "Tanggal sewa", "kunci": "tanggal"},
    "4": {"nama": "Jenis jas", "kunci": "kategori"},
    "5": {"nama": "Durasi sewa (hari)", "kunci": "durasi"},
    "6": {"nama": "Tanggal kembali", "kunci": "tgl_kembali"},
}
