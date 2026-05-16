// web/script.js
let currentPenerima = [];
let currentParams = {};

// Daftar kampus di Indonesia untuk simulasi instansi
const daftarKampus = [
    "Institut Teknologi Kalimantan",
    "Institut Teknologi Bandung",
    "Universitas Indonesia",
    "Universitas Gadjah Mada",
    "Institut Teknologi Sepuluh Nopember",
    "Universitas Mulawarman",
    "Universitas Airlangga",
    "Universitas Diponegoro",
    "Universitas Brawijaya",
    "Institut Teknologi Sumatera"
];

// Inisialisasi data saat aplikasi dibuka
async function init() {
    const data = await eel.ambil_data_awal()();
    document.getElementById('info_kandidat').innerText = `Terdapat ${data.length} kandidat dalam database lokal.`;
}

async function prosesSeleksi() {
    const params = {
        min_ipk: parseFloat(document.getElementById('in_min_ipk').value),
        max_ukt: parseInt(document.getElementById('in_max_ukt').value),
        kuota: parseInt(document.getElementById('in_kuota').value),
        anggaran: parseInt(document.getElementById('in_anggaran').value),
        bobot: parseInt(document.getElementById('in_bobot').value)
    };
    currentParams = params;

    const res = await eel.jalankan_seleksi(params.min_ipk, params.max_ukt, params.kuota, params.anggaran, params.bobot)();
    currentPenerima = res.penerima;

    const tbody = document.getElementById('table_body');
    tbody.innerHTML = '';

    const nimLolos = new Set(res.penerima.map(p => p.nim));
    const kandidatUrut = res.kandidat.sort((a, b) => (b.skor_akhir || 0) - (a.skor_akhir || 0));

    kandidatUrut.forEach((m) => {
        const lolos = nimLolos.has(m.nim);
        const tidakIpk = m.ipk < params.min_ipk;
        const tidakUkt = m.ukt > params.max_ukt;

        // Pilih kampus secara acak tapi konsisten menggunakan NIM sebagai seed
        const seed = parseInt(m.nim) || 0;
        const instansi = daftarKampus[seed % daftarKampus.length];

        let bgClass = "bg-white";
        let badge = `<span class="bg-slate-100 text-slate-500 px-3 py-1 rounded-lg text-[9px] font-bold">TIDAK LOLOS</span>`;

        if (lolos) {
            bgClass = "bg-emerald-50/40 hover:bg-emerald-50 transition-colors";
            badge = `<span class="bg-emerald-500 text-white px-3 py-1 rounded-lg text-[9px] font-bold shadow-sm shadow-emerald-100">✓ LOLOS</span>`;
        } else if (tidakIpk) {
            bgClass = "bg-orange-50/50 hover:bg-orange-50 transition-colors";
            badge = `<span class="bg-orange-500 text-white px-3 py-1 rounded-lg text-[9px] font-bold">IPK < ${params.min_ipk}</span>`;
        } else if (tidakUkt) {
            bgClass = "bg-rose-50/50 hover:bg-rose-50 transition-colors";
            badge = `<span class="bg-rose-500 text-white px-3 py-1 rounded-lg text-[9px] font-bold">UKT > LIMIT</span>`;
        }

        const skor = m.skor_akhir ? m.skor_akhir.toFixed(2) : '-';
        const rank = lolos ? (res.penerima.findIndex(p => p.nim === m.nim) + 1) : '-';

        tbody.innerHTML += `
            <tr class="border-b border-slate-50 ${bgClass} group">
                <td class="px-6 py-4 font-bold text-slate-400 group-hover:text-blue-500">${rank}</td>
                <td class="px-6 py-4 font-bold text-slate-700">${m.nama}</td>
                <td class="px-6 py-4 text-slate-400 font-mono text-xs">${m.nim}</td>
                <td class="px-6 py-4 text-slate-600 italic text-xs">${instansi}</td>
                <td class="px-6 py-4 text-slate-500">${m.prodi}</td>
                <td class="px-6 py-4 text-center font-mono font-bold text-slate-700">${m.ipk.toFixed(2)}</td>
                <td class="px-6 py-4 text-slate-500 font-mono text-xs">Rp ${m.ukt.toLocaleString('id-ID')}</td>
                <td class="px-6 py-4 text-center font-mono font-bold text-blue-600">${skor}</td>
                <td class="px-6 py-4 text-center">${badge}</td>
            </tr>
        `;
    });

    const terpakai = res.terpakai || 0;
    const sisa = params.anggaran - terpakai;
    document.getElementById('status_badge').innerText = `Lolos: ${res.penerima.length}/${params.kuota} | Dana Terpakai: Rp ${terpakai.toLocaleString('id-ID')}`;
    document.getElementById('status_badge').className = "bg-blue-600 text-white px-5 py-2.5 rounded-full font-bold text-[10px] uppercase tracking-widest shadow-lg shadow-blue-100 animate-pulse";
}

async function importData() {
    const res = await eel.import_data()();
    if (res.status === "success") {
        alert(`Impor Berhasil! ${res.count} data baru telah dimuat.`);
        init();
        prosesSeleksi();
    }
}

async function eksporCSV() {
    if (currentPenerima.length === 0) return alert("Belum ada hasil seleksi untuk diekspor!");
    const res = await eel.ekspor_csv(currentPenerima)();
    if (res) alert(res);
}

async function unduhTXT() {
    if (currentPenerima.length === 0) return alert("Belum ada hasil seleksi untuk diunduh!");
    const res = await eel.unduh_txt(
        currentPenerima, currentParams.min_ipk, currentParams.max_ukt,
        currentParams.kuota, currentParams.anggaran, 0, currentParams.bobot
    )();
    alert(res);
}

document.getElementById('in_bobot').oninput = function() {
    document.getElementById('val_bobot').innerText = this.value + '%';
};

// Jalankan pengambilan data saat halaman siap
init();