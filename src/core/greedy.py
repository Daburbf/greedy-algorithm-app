# src/core/greedy.py

def seleksi_greedy(mahasiswa_list, min_ipk, max_ukt, kuota):
    """
    Algoritma Greedy untuk seleksi beasiswa.
    Prioritas: IPK tertinggi, dengan syarat UKT <= max_ukt dan IPK >= min_ipk.
    """
    # Filter berdasarkan kriteria minimum
    kandidat = [
        m for m in mahasiswa_list
        if m["ipk"] >= min_ipk and m["ukt"] <= max_ukt
    ]

    # Urutkan secara greedy: IPK tertinggi dulu, jika sama pilih UKT terendah
    kandidat.sort(key=lambda m: (-m["ipk"], m["ukt"]))

    # Ambil sesuai kuota
    penerima = kandidat[:kuota]

    return penerima, kandidat