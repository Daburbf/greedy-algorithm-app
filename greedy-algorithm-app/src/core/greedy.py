# src/core/greedy.py

def seleksi_greedy(mahasiswa_list, min_ipk, max_ukt, kuota, total_anggaran, bobot_ipk_persen):
    """
    Algoritma Greedy dengan Sistem Bobot (Scoring System).
    Menghitung Skor Akhir berdasarkan bobot IPK dan UKT.
    """
    bobot_ukt_persen = 100 - bobot_ipk_persen
    kandidat = []

    # Evaluasi dan hitung skor masing-masing kandidat
    for m in mahasiswa_list:
        if m["ipk"] >= min_ipk and m["ukt"] <= max_ukt:
            # Hitung Skor IPK (Maksimal 100)
            skor_ipk = (m["ipk"] / 4.0) * 100

            # Hitung Skor UKT (Semakin kecil UKT, semakin mendekati 100)
            if max_ukt > 0:
                skor_ukt = ((max_ukt - m["ukt"]) / max_ukt) * 100
            else:
                skor_ukt = 0

            # Hitung Skor Akhir berdasarkan persentase slider
            skor_akhir = (skor_ipk * bobot_ipk_persen / 100) + (skor_ukt * bobot_ukt_persen / 100)

            # Salin data asli dan tambahkan nilai skor akhir
            m_copy = m.copy()
            m_copy["skor_akhir"] = skor_akhir
            kandidat.append(m_copy)

    # Urutkan secara greedy: Skor Akhir tertinggi yang diambil duluan!
    kandidat.sort(key=lambda x: x["skor_akhir"], reverse=True)

    penerima = []
    anggaran_terpakai = 0

    # Masukkan ke daftar penerima selama kuota dan anggaran masih muat
    for m in kandidat:
        if len(penerima) >= kuota:
            break

        if anggaran_terpakai + m["ukt"] <= total_anggaran:
            penerima.append(m)
            anggaran_terpakai += m["ukt"]

    return penerima, kandidat, anggaran_terpakai