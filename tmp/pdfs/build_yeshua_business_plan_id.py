from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, PageBreak, Table, TableStyle, Image, HRFlowable)
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output/pdf/rencana-bisnis-yeshua-cafe-versi-indonesia.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)
W, H = A4

HIJAU = colors.HexColor("#123D32")
HIJAU_2 = colors.HexColor("#006B4F")
KREM = colors.HexColor("#F2F0EB")
EMAS = colors.HexColor("#CBA258")
TINTA = colors.HexColor("#16201D")
ABU = colors.HexColor("#5F6B67")
GARIS = colors.HexColor("#D9DDD9")
PUTIH = colors.white

ss = getSampleStyleSheet()
ss.add(ParagraphStyle(name="Label", fontName="Helvetica-Bold", fontSize=8, leading=10,
                      textColor=HIJAU_2, spaceAfter=4, tracking=1.2))
ss.add(ParagraphStyle(name="Judul", fontName="Helvetica-Bold", fontSize=30, leading=33,
                      textColor=HIJAU, spaceAfter=10))
ss.add(ParagraphStyle(name="H1id", fontName="Helvetica-Bold", fontSize=22, leading=25,
                      textColor=HIJAU, spaceAfter=10))
ss.add(ParagraphStyle(name="H2id", fontName="Helvetica-Bold", fontSize=14, leading=17,
                      textColor=HIJAU, spaceBefore=5, spaceAfter=6))
ss.add(ParagraphStyle(name="Isi", fontName="Helvetica", fontSize=9.3, leading=14,
                      textColor=TINTA, spaceAfter=6))
ss.add(ParagraphStyle(name="Kecil", fontName="Helvetica", fontSize=7.5, leading=10,
                      textColor=ABU, spaceAfter=3))
ss.add(ParagraphStyle(name="Putih", fontName="Helvetica", fontSize=10, leading=15,
                      textColor=PUTIH, spaceAfter=6))
ss.add(ParagraphStyle(name="PutihBesar", fontName="Helvetica-Bold", fontSize=28, leading=31,
                      textColor=PUTIH, spaceAfter=10))
ss.add(ParagraphStyle(name="Metrik", fontName="Helvetica-Bold", fontSize=18, leading=20,
                      textColor=HIJAU, alignment=TA_CENTER))
ss.add(ParagraphStyle(name="MetrikLabel", fontName="Helvetica", fontSize=7.2, leading=9,
                      textColor=ABU, alignment=TA_CENTER))
ss.add(ParagraphStyle(name="TH", fontName="Helvetica-Bold", fontSize=7.3, leading=9,
                      textColor=PUTIH))
ss.add(ParagraphStyle(name="TD", fontName="Helvetica", fontSize=7.2, leading=9.5,
                      textColor=TINTA))


def p(teks, gaya="Isi"):
    return Paragraph(teks, ss[gaya])


def rupiah(n):
    if abs(n) >= 1_000_000_000:
        return f"Rp {n/1_000_000_000:.2f} miliar"
    return f"Rp {n/1_000_000:.1f} juta"


def kepala(no, judul, sub=None):
    isi = [p(f"{no}  /  RENCANA BISNIS", "Label"), p(judul, "H1id")]
    if sub:
        isi.append(p(sub))
    isi.append(HRFlowable(width="100%", thickness=.6, color=GARIS, spaceAfter=10))
    return isi


def poin(teks):
    return p(f"<font color='#006B4F'>&#9679;</font>&nbsp;&nbsp;{teks}")


def tabel(header, baris, lebar):
    data = [[p(x, "TH") for x in header]] + [[p(str(x), "TD") for x in r] for r in baris]
    t = Table(data, colWidths=lebar, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), HIJAU), ("TEXTCOLOR", (0,0), (-1,0), PUTIH),
        ("GRID", (0,0), (-1,-1), .35, GARIS), ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [PUTIH, colors.HexColor("#F7F8F6")]),
        ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    return t


def sorotan(judul, teks):
    t = Table([[p(judul, "Label"), p(teks)]], colWidths=[42*mm, 122*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#EAF3EF")),
        ("BOX", (0,0), (-1,-1), .6, HIJAU_2), ("LINEBEFORE", (0,0), (0,-1), 3, HIJAU_2),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))
    return t


def metrik(items):
    cells = [[p(v, "Metrik"), p(l, "MetrikLabel")] for v,l in items]
    t = Table([cells], colWidths=[164*mm/len(items)]*len(items), rowHeights=[22*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F7F8F6")),
        ("BOX", (0,0), (-1,-1), .5, GARIS), ("INNERGRID", (0,0), (-1,-1), .5, GARIS),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ]))
    return t


def foto(rel, tinggi=68*mm):
    im = Image(str(ROOT / rel), width=164*mm, height=tinggi)
    im.hAlign = "CENTER"
    return im


class Kanvas(canvas.Canvas):
    def __init__(self, *a, **k):
        super().__init__(*a, **k); self.states=[]
    def showPage(self):
        self.states.append(dict(self.__dict__)); self._startPage()
    def save(self):
        total=len(self.states)
        for s in self.states:
            self.__dict__.update(s)
            if self._pageNumber > 1:
                self.setFont("Helvetica", 7); self.setFillColor(ABU)
                self.drawString(23*mm, 12*mm, "YESHUA CAFE  /  DRAF DISKUSI INVESTOR")
                self.drawRightString(W-23*mm, 12*mm, f"{self._pageNumber} / {total}")
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)


def latar_sampul(c, d):
    c.saveState(); c.setFillColor(HIJAU); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(colors.HexColor("#194F41")); c.circle(W*.9,H*.15,80*mm,fill=1,stroke=0)
    c.setFillColor(EMAS); c.rect(0,H-8*mm,W,8*mm,fill=1,stroke=0); c.restoreState()


def latar(c, d):
    c.saveState(); c.setFillColor(KREM); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(HIJAU); c.rect(0,H-5*mm,W,5*mm,fill=1,stroke=0); c.restoreState()


doc=BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=23*mm, rightMargin=23*mm,
                    topMargin=20*mm, bottomMargin=20*mm, title="Rencana Bisnis Yeshua Cafe")
frame=Frame(23*mm,20*mm,164*mm,252*mm,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
doc.addPageTemplates([PageTemplate(id="Sampul",frames=frame,onPage=latar_sampul),
                      PageTemplate(id="Isi",frames=frame,onPage=latar)])
s=[]

# Sampul
s += [Spacer(1,27*mm)]
logo=Image(str(ROOT/"public/brand/official/yeshua-cafe-logo.png"),38*mm,38*mm); logo.hAlign="LEFT"
s += [logo,Spacer(1,12*mm),p("DRAF DISKUSI INVESTOR","Label"),p("Yeshua Cafe","PutihBesar"),
      p("Hospitalitas inklusif, operasi yang disiplin, dan sebuah kafe yang dirancang untuk menciptakan pekerjaan yang bermakna.","Putih"),
      Spacer(1,68*mm),p("RENCANA BISNIS + STRATEGI PEMASARAN","Putih"),
      p("Kajian lokasi pilot: Pejaten, Jakarta Selatan<br/>Opsi ekspansi: Jakarta Utara","Putih"),
      Spacer(1,8*mm),p("Disiapkan untuk Juang Group  |  2 Agustus 2026","Putih"),PageBreak()]
doc.handle_nextPageTemplate("Isi")

# Catatan dan isi
s += kepala("00","Cara menggunakan dokumen ini","Dokumen pengambilan keputusan untuk pembahasan pendiri dan investor, bukan jaminan keuntungan.")
s += [sorotan("STATUS DOKUMEN","Rencana ini disusun berdasarkan materi konsep yang tersedia dan sejumlah asumsi kerja yang dinyatakan secara terbuka. Penawaran sewa, denah, quotation pemasok, asesmen tenaga kerja, serta skema pendanaan wajib divalidasi sebelum penandatanganan investasi."),Spacer(1,8)]
daftar=[("01","Ringkasan eksekutif"),("02","Tesis investasi dan konsep"),("03","Pasar dan strategi lokasi"),("04","Model ketenagakerjaan inklusif"),("05","Produk dan sumber pendapatan"),("06","Operasional dan teknologi"),("07","Strategi pemasaran"),("08","Model keuangan"),("09","Kebutuhan investasi dan sewa"),("10","Roadmap, tata kelola, dan risiko"),("11","Daftar uji tuntas investor")]
s += [p("Peta dokumen","H2id"),tabel(["BAGIAN","ISI"],daftar,[24*mm,140*mm]),Spacer(1,8),p("Catatan nama merek","H2id"),p("Website saat ini menggunakan nama Yeshua Cafe sebagai bagian dari Juang Group. Jika nama komersial akan kembali menjadi Juang Coffee, nama badan usaha, merek, izin, signage, kanal digital, dan materi investor harus diselaraskan sebelum pembukaan."),PageBreak()]

# Ringkasan
s += kepala("01","Ringkasan eksekutif","Satu gerai pilot untuk membuktikan kelayakan komersial dan sistem kerja inklusif.")
s += [metrik([("1 gerai","Skala pembukaan"),("60 kursi","Asumsi kapasitas"),("Rp2,35 M","Dana awal ilustratif"),("15-18 bln","Periode validasi")]),Spacer(1,9)]
s += [p("Peluang usaha","H2id"),p("Yeshua Cafe diposisikan sebagai kafe komunitas yang mudah diakses, memiliki menu khas, layanan berbasis teknologi, serta membuka kesempatan kerja terstruktur bagi orang dengan Down syndrome. Bisnis harus tetap bersaing melalui kualitas produk, keramahtamahan, kenyamanan, kecepatan, dan konsistensi. Misi sosial memperkuat merek, tetapi tidak boleh menggantikan disiplin komersial dan praktik ketenagakerjaan yang adil.")]
s += [p("Rekomendasi utama","H2id"),poin("Buka satu gerai pilot di Pejaten setelah penilaian lokasi dan negosiasi sewa."),poin("Tempatkan Jakarta Utara sebagai fase kedua sampai area mikro dan propertinya divalidasi."),poin("Gunakan asesmen individu, pendamping kerja, SOP visual, pembagian tugas, dan upah yang adil."),poin("Bangun permintaan berulang melalui komunitas, kantor, kampus, acara, CRM, delivery, dan catering."),poin("Terapkan dashboard mingguan dan laporan investor bulanan sejak hari pertama.")]
s += [sorotan("GERBANG INVESTASI","Jangan menandatangani sewa cabang kedua sebelum gerai pilot mencatat EBITDA positif selama enam bulan berturut-turut, akurasi pesanan di atas 98%, rating pelanggan minimal 4,5/5, dan retensi pegawai minimal 85%."),PageBreak()]

# Tesis dan konsep
s += kepala("02","Tesis investasi dan konsep pelanggan","Nilai bisnis harus dibuktikan dengan data operasional, bukan hanya cerita yang menarik.")
tesis=[("Proposisi berbeda","Hospitalitas inklusif dan program komunitas menciptakan daya ingat.","Buktikan kunjungan ulang dan rekomendasi."),("Permintaan multi-waktu","Kopi, makanan, kerja, keluarga, acara, dan komunitas menyebarkan transaksi.","Buktikan penjualan per jam dan margin kategori."),("Kontrol digital","QR, kasir, dapur, dan stok terhubung mengurangi salah input serta meningkatkan keterlacakan.","Buktikan kestabilan dan disiplin pencatatan."),("Model dapat direplikasi","SOP visual dan modul pelatihan mendukung ekspansi.","Buktikan di satu gerai terlebih dahulu."),("Dampak terukur","Pekerjaan, jam kerja, kompetensi, retensi, dan kepuasan dapat dilaporkan.","Gunakan persetujuan dan lindungi martabat pegawai.")]
s += [tabel(["PENDORONG NILAI","ALASAN","BUKTI YANG DIBUTUHKAN"],tesis,[38*mm,65*mm,61*mm]),Spacer(1,8),p("Janji pelanggan","H2id")]
janji=[("Produk","Kopi, minuman, hidangan nasi, meat pie, shawarma, comfort food, dan dessert yang konsisten."),("Tempat","Ruang hangat untuk belajar, bekerja, rapat santai, keluarga, dan komunitas."),("Manusia","Tim campuran, termasuk orang dengan Down syndrome pada peran yang sesuai kesiapan dan kekuatannya."),("Proses","Pemesanan QR dan data terintegrasi untuk kecepatan, akurasi, serta transparansi."),("Komunitas","Workshop, open mic, acara keluarga, dan kolaborasi dengan organisasi lokal.")]
s += [tabel(["PILAR","JANJI"],janji,[35*mm,129*mm]),PageBreak()]

# Pasar lokasi
s += kepala("03","Pasar dan strategi lokasi","Pejaten direkomendasikan sebagai titik awal; Jakarta Utara menunggu penentuan area mikro.")
s += [foto("public/images/juang-cafe/target-communities.webp"),Spacer(1,7)]
seg=[("Mahasiswa dan anak muda","Belajar, Wi-Fi, makan terjangkau, tugas kelompok","Paket makan, jam belajar, ambassador kampus"),("Profesional dan pekerja jarak jauh","Kopi, ruang kerja, pertemuan informal","Paket pagi/siang dan kerja sama kantor"),("Keluarga","Tempat nyaman dan cerita bermakna","Program akhir pekan dan paket keluarga"),("Komunitas dan kreator","Tempat berkumpul, workshop, open mic","Paket acara dan kalender kolaboratif"),("Perusahaan dan institusi","Catering, CSR, employee engagement","Pesanan rapat dan program kemitraan")]
s += [tabel(["SEGMEN","KEBUTUHAN","PENAWARAN"],seg,[42*mm,59*mm,63*mm]),Spacer(1,7),p("Riset wajib sebelum sewa","H2id"),p("Data BPS dapat menjadi dasar profil wilayah, tetapi tidak dapat menggantikan studi area tangkapan gerai. Sebelum menyewa, lakukan hitung lalu lintas pejalan kaki selama tiga hari, pemetaan kompetitor dalam radius 1-3 km, wawancara calon pelanggan, penilaian akses kendaraan, parkir, delivery, serta pengumpulan quotation sewa."),PageBreak()]

s += kepala("03A","Perbandingan lokasi","Keputusan harus dibuat berdasarkan alamat dan properti, bukan hanya nama wilayah.")
lok=[("Kejelasan pasar","Campuran hunian, pendidikan, kantor, dan komunitas cukup jelas.","Sangat berbeda antara Kelapa Gading, Pluit, PIK, Koja, dan area lainnya."),("Kelayakan pilot","Lebih tinggi untuk menguji frekuensi kunjungan lingkungan.","Menarik, tetapi sangat bergantung pada klaster dan harga sewa."),("Kecocokan merek","Kafe komunitas, belajar, bekerja, dan keluarga.","Bisa menjadi lifestyle atau destination cafe sesuai lokasi."),("Risiko utama","Kemacetan, parkir, frontage, dan kenaikan sewa.","Over-rent, ketergantungan destinasi, dan area pertama belum jelas."),("Rekomendasi","Pilih tiga properti untuk dinilai.","Pilih dua area mikro, lalu cari properti.")]
s += [tabel(["KRITERIA","PEJATEN","JAKARTA UTARA"],lok,[39*mm,63*mm,62*mm]),Spacer(1,8),p("Bobot penilaian properti","H2id")]
skor=[("Sewa dan service charge","20%","Biaya okupansi maksimal 12% dari omzet matang"),("Lalu lintas dan visibilitas","20%","Penghitungan per jam hari kerja dan akhir pekan"),("Akses dan parkir","15%","Drop-off aman dan pintu masuk mudah diakses"),("Potensi area tangkapan","15%","Hunian, sekolah, kantor, dan komunitas"),("Dapur dan utilitas","10%","Listrik, exhaust, air, grease trap, limbah"),("Kompetitor dan tenant sekitar","10%","Ada permintaan tanpa perang harga langsung"),("Fleksibilitas kontrak","10%","Masa fit-out, kenaikan, break clause")]
s += [tabel(["FAKTOR","BOBOT","SYARAT"],skor,[58*mm,22*mm,84*mm]),PageBreak()]

# Inklusif
s += kepala("04","Model ketenagakerjaan inklusif","Pekerjaan harus terstruktur, dibayar, aman, dan sesuai kemampuan individu, bukan sekadar materi promosi.")
s += [foto("public/images/juang-cafe/inclusive-employment.webp"),Spacer(1,7)]
peran=[("Penyambutan tamu","Menyapa, menjelaskan menu, memberi nomor meja","Kartu skrip, buddy, prosedur eskalasi"),("Dukungan meja","Mengantar, membersihkan, menata ulang","Kode warna/nomor dan latihan rute"),("Pengemasan","Label, alat makan, pemeriksaan takeaway","Checklist bergambar dan verifikasi"),("Dukungan minuman","Tugas terukur yang aman","Bahan terukur dan urutan visual"),("Stok dan kebersihan","Menghitung, menata, jadwal pembersihan","Papan tugas, APD, persetujuan supervisor")]
s += [tabel(["KELOMPOK PERAN","CONTOH TUGAS","AKOMODASI"],peran,[36*mm,63*mm,65*mm]),Spacer(1,7)]
s += [p("Prinsip pelaksanaan","H2id"),poin("Asesmen individual dan partisipasi sukarela; tidak menyamaratakan kemampuan."),poin("Upah setara untuk jenis pekerjaan dan tanggung jawab yang sama."),poin("Fasilitas mudah diakses, akomodasi yang layak, pengaduan, dan perlindungan."),poin("Pendamping kerja atau mentor shift, SOP visual, jadwal terprediksi, dan sertifikasi tugas."),poin("Pegawai boleh menolak foto atau cerita publik tanpa konsekuensi terhadap pekerjaannya."),PageBreak()]

s += kepala("04A","Perjalanan pegawai dan pengukuran dampak","Jalur berulang dari rekrutmen sampai kemandirian menjalankan tugas.")
alur=[("1. Mitra","Yayasan, sekolah, keluarga, layanan ketenagakerjaan disabilitas, dan tenaga profesional."),("2. Asesmen","Preferensi, komunikasi, transportasi, kebutuhan sensorik, dan kesiapan tugas."),("3. Persiapan","Pelatihan berbayar dua minggu menggunakan simulasi dan SOP visual."),("4. Penempatan","Peran yang didukung buddy dan akomodasi tertulis."),("5. Perkembangan","Evaluasi mingguan saat masa percobaan, lalu bulanan; sertifikasi per tugas."),("6. Keberlanjutan","Jadwal adil, umpan balik, jenjang kerja, komunikasi keluarga dengan persetujuan.")]
s += [tabel(["TAHAP","KEWAJIBAN OPERASIONAL"],alur,[37*mm,127*mm]),Spacer(1,8)]
dampak=[("Pekerjaan","Jumlah pegawai; jam kerja berbayar; retensi"),("Kemampuan","Tugas tersertifikasi; jam pelatihan; kemandirian"),("Kualitas","Akurasi pesanan; pemulihan layanan; rating"),("Kesejahteraan","Masukan pegawai; keluarga dengan persetujuan; insiden"),("Keadilan","Kesetaraan upah; stabilitas jadwal; promosi")]
s += [p("Dashboard dampak","H2id"),tabel(["DIMENSI","UKURAN"],dampak,[38*mm,126*mm]),Spacer(1,7),sorotan("TARGET TAHUN PERTAMA","Target awal: 4-6 pegawai dengan Down syndrome, minimal 80 jam pelatihan berbayar per peserta, retensi 85%, dan minimal tiga kelompok tugas tersertifikasi. Target final menunggu asesmen mitra dan kandidat."),PageBreak()]

# Produk operasi
s += kepala("05","Produk dan sumber pendapatan","Menu pembukaan harus fokus agar kecepatan, kualitas, margin, dan pelatihan tetap terjaga.")
s += [foto("public/images/juang-cafe/menu-concept-real-menu.webp"),Spacer(1,7)]
pend=[("Makan di tempat dan takeaway","70-75%","Sumber utama; bundling dan add-on meningkatkan nilai transaksi"),("Delivery","12-15%","Jangkauan tambahan; kendalikan komisi dan kemasan"),("Acara komunitas","5-8%","Sewa ruang, paket makanan, workshop, open mic"),("Catering dan perusahaan","5-8%","Nampan pre-order, rapat, CSR, dan institusi"),("Produk ritel masa depan","0-5%","Kopi, cokelat, produk kemasan setelah operasi stabil")]
s += [tabel(["SUMBER","BAURAN MATANG","LOGIKA"],pend,[50*mm,26*mm,88*mm]),Spacer(1,7),p("Aturan rekayasa menu","H2id"),poin("Luncurkan maksimal 25-30 SKU inti ditambah produk musiman terbatas."),poin("Setiap SKU memiliki resep, porsi, alergen, biaya, waktu produksi, margin, dan standar foto."),poin("Target COGS gabungan 33-35%; evaluasi produk berpenjualan rendah setiap bulan."),poin("Produk khas memberi pembeda; produk familiar mengurangi hambatan mencoba."),PageBreak()]

s += kepala("06","Operasional dan teknologi terintegrasi","Setiap pesanan dan pergerakan stok harus menghasilkan jejak data.")
s += [foto("public/images/juang-cafe/connected-operations.webp"),Spacer(1,7)]
flow=[("1. QR meja","Pelanggan membuka menu, memberi catatan, dan mengirim pesanan."),("2. POS dan pembayaran","Pesanan masuk dengan nomor meja, item, diskon, pembayaran, dan audit trail."),("3. Tampilan dapur","Stasiun menerima tiket dengan waktu dan status."),("4. Pelayanan","Runner menerima notifikasi dan mengantar ke meja."),("5. Inventaris","Resep mengurangi stok; waste, void, dan transfer memakai kode alasan."),("6. Manajemen","Pendiri dan investor menerima dashboard sesuai hak akses.")]
s += [tabel(["ALUR","KONTROL"],flow,[38*mm,126*mm]),Spacer(1,7),p("Dashboard wajib","H2id"),poin("Penjualan, transaksi, AOV, bauran kategori, diskon, void, dan refund."),poin("Waktu tiket, akurasi, ketersediaan menu, waste, dan selisih stok."),poin("Jam kerja, produktivitas, kehadiran, pelatihan, dan insiden."),poin("Rekonsiliasi kas, utang, runway, dan laporan investor."),PageBreak()]

# Marketing
s += kepala("07","Strategi pemasaran","Komunitas sebelum kampanye: bangun mesin permintaan lokal, bukan bergantung pada ramai saat pembukaan.")
s += [foto("public/images/juang-cafe/marketing-ecosystem.webp"),Spacer(1,7)]
kanal=[("Milik sendiri","Website, Google Business, Instagram, TikTok, WhatsApp CRM","Penemuan dan retensi"),("Lokal","Kompleks hunian, sekolah, kantor, gereja, komunitas","Kepercayaan dan kunjungan rutin"),("Kemitraan","Kampus, yayasan, perusahaan, kreator, penyelenggara acara","Berbagi audiens dan program"),("Berbayar","Iklan radius, pencarian, peta, retargeting","Menangkap niat tinggi"),("Publisitas","PR, kisah pendiri, edukasi pekerjaan inklusif","Kredibilitas dengan persetujuan pegawai")]
s += [tabel(["MESIN","TAKTIK","PERAN"],kanal,[30*mm,81*mm,53*mm]),Spacer(1,7),sorotan("URUTAN PESAN","Utamakan kualitas dan keramahtamahan. Dukung dengan kemudahan dan komunitas. Jelaskan inklusi melalui cerita faktual tentang pekerjaan berbayar, keterampilan, dan kesempatan, bukan komunikasi yang mengundang rasa kasihan."),PageBreak()]

s += kepala("07A","Funnel pelanggan dan rencana 90 hari","Jalur terukur dari mengenal, mencoba, kembali, sampai merekomendasikan.")
fun=[("Kesadaran","SEO peta, PR lokal, preview kreator, audiens mitra","Jangkauan, view peta, pencarian merek"),("Pertimbangan","Menu, harga, lokasi, review, cerita pegawai","Kunjungan web, petunjuk arah, simpan"),("Kunjungan pertama","Penawaran pembukaan, bundling, acara, sampling","Pelanggan baru dan biaya akuisisi"),("Kunjungan kedua","QR pada struk, opt-in WhatsApp, penawaran kembali","Repeat rate 30 hari"),("Kebiasaan","Program waktu, loyalitas, pre-order, kalender komunitas","Frekuensi dan AOV"),("Advokasi","Review, UGC, referral, cerita kemitraan","NPS, rating, referral")]
s += [tabel(["TAHAP","AKTIVASI","KPI"],fun,[31*mm,85*mm,48*mm]),Spacer(1,8)]
hari=[("H-60 sampai H-30","Membangun","Kemitraan, cerita pembangunan, waitlist, profil Google"),("H-30 sampai H-7","Preview","Tasting komunitas, preview tetangga dan kreator"),("Minggu pembukaan","Pengalaman","Reservasi terkendali dan evaluasi harian"),("Hari 8-30","Perbaikan","Perbaiki menu, waktu tiket, stok, review, dan iklan radius"),("Hari 31-90","Retensi","CRM, penawaran waktu kerja, acara, catering, referral")]
s += [p("Rencana 90 hari","H2id"),tabel(["PERIODE","TUJUAN","AKSI"],hari,[31*mm,31*mm,102*mm]),PageBreak()]

s += kepala("07B","Rencana kerja dan anggaran pemasaran","Pemasaran harus menghasilkan permintaan dan pembelajaran, bukan hanya unggahan.")
ang=[("Produksi konten","Rp3,0 juta","Foto/video, persetujuan pegawai, aset menu"),("Iklan berbayar","Rp3,5 juta","Peta, pencarian, dan radius 3-5 km"),("Komunitas dan acara","Rp2,5 juta","Host, peralatan, sampling, materi mitra"),("CRM dan loyalitas","Rp1,0 juta","WhatsApp, penawaran, kebersihan data"),("PR / kreator","Rp1,0 juta","Seeding selektif"),("Cadangan eksperimen","Rp1,0 juta","Tes kanal dan penawaran")]
s += [tabel(["POS","PER BULAN","KEGUNAAN"],ang,[48*mm,29*mm,87*mm]),Spacer(1,8),p("Ritme konten mingguan","H2id"),poin("Dua konten produk: menu, proses, nilai, dan waktu konsumsi."),poin("Satu cerita manusia dan proses dengan persetujuan."),poin("Satu konten komunitas, acara, mitra, atau panduan lingkungan."),poin("Informasi harian: jam buka, ketersediaan, acara, arah, dan balasan."),poin("Bukti bulanan: dampak, masukan pelanggan, perbaikan, dan hasil mitra."),PageBreak()]

# Keuangan
s += kepala("08","Model keuangan: asumsi dasar","Seluruh angka merupakan ilustrasi sebelum pajak dan harus diganti dengan quotation serta kontrak sewa nyata.")
asum=[("Format pilot","120 m2, sekitar 60 kursi, satu gerai"),("Hari operasi","30 hari per bulan"),("Transaksi matang","125 transaksi per hari"),("Nilai transaksi rata-rata","Rp75.000"),("Pendapatan tambahan","Rp28,75 juta per bulan"),("COGS gabungan","35% dari pendapatan"),("Opex tetap/semi-tetap","Rp148 juta per bulan"),("Target okupansi","Sewa + service charge maksimal 12% omzet matang"),("Ramp-up","6-9 bulan menuju kondisi matang")]
s += [tabel(["ASUMSI","NILAI KERJA"],asum,[64*mm,100*mm]),Spacer(1,8),sorotan("CATATAN PENTING","Rp2,35 miliar adalah estimasi kebutuhan awal, bukan nilai kontrak sewa 10 tahun dan bukan jaminan bahwa bisnis akan mencapai proyeksi. Faktor paling sensitif adalah transaksi per hari, AOV, COGS, sewa, dan payroll."),PageBreak()]

s += kepala("08A","Estimasi kebutuhan dana awal","Ilustrasi satu gerai pilot; tidak termasuk pembelian tanah maupun seluruh sewa 10 tahun.")
cap=[("Renovasi dan MEP",720_000_000),("Peralatan dapur dan kopi",360_000_000),("Furnitur, signage, smallwares",190_000_000),("POS, QR, KDS, jaringan, CCTV",70_000_000),("Perizinan, profesional, pre-opening",80_000_000),("Rekrutmen dan pelatihan inklusif",100_000_000),("Deposit / uang muka sewa awal",300_000_000),("Stok pembukaan",70_000_000),("Cadangan modal kerja",310_000_000),("Kontingensi",150_000_000)]
tot=sum(v for _,v in cap)
s += [tabel(["PENGGUNAAN DANA","NILAI","PORSI"],[(k,rupiah(v),f"{v/tot*100:.1f}%") for k,v in cap]+[("TOTAL",rupiah(tot),"100%")],[87*mm,48*mm,29*mm]),Spacer(1,7)]
s += [p("Asal angka","H2id"),p("Estimasi dibangun secara bottom-up dari asumsi luas 120 m2, renovasi sekitar Rp6 juta/m2, peralatan komersial kelas menengah, sistem teknologi, biaya pre-opening, deposit sewa awal, dan cadangan kas. Angka ini bukan berasal dari quotation vendor atau penawaran properti Pejaten tertentu."),PageBreak()]

s += kepala("08B","Sewa 10 tahun: ditampilkan terpisah","Komitmen kontrak tidak selalu sama dengan uang tunai yang dibayar di muka.")
sewa=[]; nilai=300_000_000; total_sewa=0
for tahun in range(1,11):
    sewa.append((f"Tahun {tahun}",rupiah(nilai))); total_sewa+=nilai; nilai*=1.05
s += [tabel(["PERIODE","ILUSTRASI SEWA"],sewa+[("TOTAL NOMINAL 10 TAHUN",rupiah(total_sewa))],[82*mm,82*mm]),Spacer(1,8)]
s += [metrik([("Rp2,35 M","Dana awal ilustratif"),("Rp3,77 M","Sewa 10 tahun ilustratif"),("Rp6,12 M","Gabungan nominal kasar")]),Spacer(1,8)]
s += [sorotan("JANGAN SALAH BACA","Ilustrasi memakai sewa tahun pertama Rp300 juta dengan kenaikan 5% per tahun. Total Rp3,77 miliar bukan quotation dan tidak harus dibayar sekaligus apabila kontrak dibayar tahunan. Gabungan Rp6,12 miliar bersifat kasar dan dapat mengandung perbedaan waktu pembayaran serta perlakuan deposit."),Spacer(1,7)]
s += [p("Struktur sewa yang lebih aman","H2id"),poin("Kontrak pilot 3 tahun dengan opsi perpanjangan 2+5 tahun."),poin("Pembayaran tahunan, bukan 10 tahun di muka."),poin("Masa bebas sewa 2-4 bulan untuk fit-out."),poin("Batas kenaikan, hak perpanjangan, pengalihan, dan break clause yang jelas."),PageBreak()]

s += kepala("08C","Unit economics bulanan saat matang","Skenario dasar setelah gerai mencapai operasi stabil.")
omzet=310_000_000; cogs=108_500_000; gross=201_500_000; opex=148_000_000; ebitda=53_500_000
eco=[("Pendapatan inti",rupiah(281_250_000),"90,7%"),("Pendapatan tambahan",rupiah(28_750_000),"9,3%"),("Total pendapatan",rupiah(omzet),"100%"),("COGS",rupiah(-cogs),"35%"),("Laba kotor",rupiah(gross),"65%"),("Biaya operasional",rupiah(-opex),"47,7%"),("EBITDA gerai",rupiah(ebitda),"17,3%")]
s += [tabel(["POS","BULANAN","% OMZET"],eco,[86*mm,48*mm,30*mm]),Spacer(1,9),metrik([("Rp310 jt","Omzet matang"),("Rp53,5 jt","EBITDA gerai"),("17,3%","Margin EBITDA"),("~44 bln","Simple payback")]),Spacer(1,8)]
s += [p("Titik impas","H2id"),p("Dengan margin kontribusi 65% dan biaya tetap/semi-tetap Rp148 juta per bulan, omzet impas diperkirakan sekitar Rp228 juta per bulan. Pada AOV Rp75.000 serta pendapatan tambahan Rp20 juta, dibutuhkan kurang lebih 93 transaksi per hari."),PageBreak()]

s += kepala("08D","Analisis skenario","Keputusan investasi harus mempertimbangkan kemampuan bertahan pada kondisi buruk.")
sken=[("Konservatif","80","Rp65 rb","Rp171 jt","37%","-Rp22 jt","Negatif"),("Dasar","125","Rp75 rb","Rp310 jt","35%","Rp53,5 jt","17,3%"),("Optimistis","155","Rp82 rb","Rp416 jt","33%","Rp108,7 jt","26,1%")]
s += [tabel(["SKENARIO","TRX/HARI","AOV","OMZET","COGS","EBITDA","MARGIN"],sken,[31*mm,21*mm,21*mm,26*mm,19*mm,27*mm,19*mm]),Spacer(1,9)]
tahun=[("Tahun 1","Rp2,55 M","Rp0,08 M","3%","Pembukaan dan ramp-up"),("Tahun 2","Rp3,55 M","Rp0,48 M","13,5%","Optimasi setahun penuh"),("Tahun 3","Rp3,90 M","Rp0,65 M","16,7%","Gerai matang; keputusan ekspansi")]
s += [p("Ilustrasi tiga tahun","H2id"),tabel(["TAHUN","OMZET","EBITDA","MARGIN","CATATAN"],tahun,[24*mm,30*mm,28*mm,21*mm,61*mm]),Spacer(1,8),sorotan("PERINGATAN","Angka ini bukan proyeksi yang diaudit. Pajak, depresiasi, bunga, kompensasi pemilik, komisi platform, serta overhead kantor pusat masih harus dimasukkan ke model spreadsheet final."),PageBreak()]

# Investasi roadmap risiko
s += kepala("09","Struktur investasi dan penggunaan dana","Dana sebaiknya dicairkan berdasarkan milestone dengan tata kelola dan hak informasi yang jelas.")
opsi=[("Ekuitas","Investor memiliki saham perusahaan","Keselarasan jangka panjang","Valuasi dan dilusi perlu dinegosiasikan"),("Instrumen konversi","Utang berubah menjadi saham pada pemicu tertentu","Menunda pembahasan valuasi","Butuh dokumen hukum dan batas konversi"),("Bagi hasil","Imbal hasil mengikuti performa gerai","Logika komersial sederhana","Berisiko menekan kas dan memicu sengketa"),("SPV proyek","Gerai pilot berada pada entitas khusus","Ekonomi gerai dan governance lebih jelas","Administrasi lebih banyak")]
s += [tabel(["OPSI","MEKANISME","KELEBIHAN","CATATAN"],opsi,[30*mm,51*mm,41*mm,42*mm]),Spacer(1,8)]
s += [p("Perlindungan investor yang disarankan","H2id"),poin("Persetujuan atas utang baru, sewa kedua, transaksi pihak berelasi, dan capex besar."),poin("Laporan manajemen bulanan dan laporan dampak kuartalan."),poin("Dual-control bank di atas batas tertentu dan pengadaan terdokumentasi."),poin("Komitmen pendiri, kepemilikan IP, dan keterbukaan pihak berelasi."),poin("Kebijakan dividen dan reinvestasi yang disepakati."),PageBreak()]

s += kepala("10","Roadmap dan gerbang keputusan","Ekspansi dilakukan setelah bukti, sistem, dan tim siap.")
road=[("0-2 bulan","Validasi","Model bisnis, lokasi, wawancara, MoU mitra, quotation","Persetujuan komite investasi"),("2-4 bulan","Pengamanan","Sewa, desain, izin, vendor, teknologi, rekrutmen","Uji tuntas teknis dan hukum"),("4-7 bulan","Pembangunan","Fit-out, SOP, uji menu, perekrutan, pelatihan","Audit kesiapan"),("7-9 bulan","Peluncuran","Soft opening dan perbaikan harian","Evaluasi stabilisasi 90 hari"),("9-15 bulan","Optimasi","Menu, CRM, catering, produktivitas, dampak","Tren KPI positif 6 bulan"),("15-24 bulan","Keputusan","Kajian area dan properti Jakarta Utara","Go/no-go gerai kedua")]
s += [tabel(["WAKTU","FASE","PEKERJAAN","GERBANG"],road,[25*mm,27*mm,71*mm,41*mm]),Spacer(1,9),metrik([(">=15%","Margin EBITDA"),(">=98%","Akurasi pesanan"),(">=4,5","Rating pelanggan"),(">=85%","Retensi pegawai")]),Spacer(1,7),p("Tambahan syarat ekspansi: arus kas operasional positif, selisih stok di bawah 2%, biaya okupansi di bawah 12%, calon manajer tersedia, dan laporan enam bulan bersih."),PageBreak()]

s += kepala("10A","Risiko dan mitigasi","Rencana yang kuat mengakui kemungkinan kegagalan sebelum investor menanyakannya.")
ris=[("Trafik di bawah target","Tinggi","Hitung lapangan, sewa konservatif, kemitraan, funnel mingguan"),("Tekanan sewa","Tinggi","Batas okupansi, kenaikan, masa fit-out, hak keluar"),("Layanan tidak konsisten","Tinggi","Soft opening, SOP visual, coaching, menu terbatas"),("Inklusi tokenistik / safeguarding","Tinggi","Mitra, persetujuan, pengaduan, mentor, protokol insiden"),("Keamanan pangan","Tinggi","Kontrol suhu, FIFO/FEFO, vendor, pelatihan, audit"),("Kebocoran kas / stok","Menengah-tinggi","Hak akses POS, CCTV, cycle count, dual approval"),("Ketergantungan pada pendiri","Menengah-tinggi","Delegasi, manajer, SOP, dewan, succession plan"),("Gangguan teknologi","Menengah","Prosedur offline, backup, SLA, kontrol akses"),("Risiko reputasi","Menengah","Pesan bermartabat, koreksi terbuka, privasi"),("Keterlambatan izin","Menengah","Checklist, ahli, jalur halal, syarat dalam kontrak")]
s += [tabel(["RISIKO","TINGKAT","MITIGASI"],ris,[48*mm,26*mm,90*mm]),Spacer(1,7),p("Irama tata kelola","H2id"),p("Briefing toko harian; evaluasi operasi mingguan; laporan keuangan dan dampak bulanan; rapat investor kuartalan; evaluasi strategi dan remunerasi tahunan."),PageBreak()]

s += kepala("10B","Legal dan kepatuhan","Gunakan nasihat profesional untuk hukum, pajak, tenaga kerja, aksesibilitas, dan keamanan pangan.")
patuh=[("Badan usaha","Dokumen perusahaan, perjanjian pemegang saham, pajak, beneficial ownership"),("Perizinan","NIB dan KBLI melalui OSS; lokasi dan persyaratan bangunan"),("Pangan dan minuman","Sanitasi, alergen, pemasok, food safety, jalur sertifikasi halal"),("Ketenagakerjaan","Kontrak, upah, BPJS, jam, cuti, kesetaraan, akomodasi, pengaduan"),("Aksesibilitas","Pintu masuk, sirkulasi, toilet, signage, keadaan darurat"),("Data dan teknologi","Persetujuan pelanggan, CRM, hak akses, backup, kontrak vendor"),("Merek dan IP","Pencarian merek, kepemilikan logo, domain, rahasia resep"),("Sewa","Peruntukan, signage, fit-out, utilitas, pemulihan, kenaikan, perpanjangan")]
s += [tabel(["AREA","PEMERIKSAAN MINIMAL"],patuh,[47*mm,117*mm]),Spacer(1,8),sorotan("PERLU PERHATIAN","BPJPH menyatakan perluasan kewajiban sertifikasi halal produk makanan dan minuman berlaku pada Oktober 2026. Pendiri harus mengonfirmasi kategori serta jadwal yang berlaku sebelum pembukaan."),PageBreak()]

# DD dan sumber
s += kepala("11","Daftar uji tuntas investor","Data yang dibutuhkan untuk mengubah draf ini menjadi rencana yang siap didanai.")
dd=[("Pendiri dan badan usaha","CV, dokumen perusahaan, cap table, kewajiban, pihak berelasi"),("Pendanaan","Dana yang dicari, kontribusi pendiri, instrumen, valuasi/imbal hasil"),("Properti","Alamat, denah, sewa, service charge, deposit, masa, kenaikan, utilitas"),("Pasar","Peta area, hitung trafik, audit harga/menu kompetitor, wawancara"),("Menu","SKU, harga, recipe cost, quotation pemasok, waktu produksi, alergen"),("Manusia","Struktur, payroll, mitra inklusi, asesmen, biaya coaching"),("Operasi","Jam buka, kapasitas, peralatan, SOP, food safety, insiden"),("Teknologi","Vendor, biaya, integrasi, SLA, hak akses"),("Keuangan","Model 36-60 bulan, modal kerja, pajak, depresiasi, sensitivitas"),("Dampak","Target, persetujuan, data, safeguarding, umpan balik")]
s += [tabel(["BIDANG","DOKUMEN / JAWABAN"],dd,[44*mm,120*mm]),Spacer(1,8),p("Agenda pertemuan berikutnya","H2id"),poin("Konfirmasi merek komersial: Yeshua Cafe atau Juang Coffee."),poin("Setujui strategi satu pilot dan scorecard lokasi."),poin("Konfirmasi kebutuhan investasi dan kontribusi modal pendiri."),poin("Tetapkan penanggung jawab dan tenggat uji tuntas."),poin("Mulai kajian properti, costing menu, dan model finansial spreadsheet."),PageBreak()]

s += kepala("LAMPIRAN","Sumber, definisi, dan keterbatasan","Disusun dari sumber publik resmi dan materi konsep Juang Group.")
src=[("BPS Jakarta Selatan","Kota Jakarta Selatan Dalam Angka 2025","https://jakselkota.bps.go.id"),("BPS Jakarta Utara","Kota Jakarta Utara Dalam Angka 2025","https://jakutkota.bps.go.id"),("Pemerintah RI","UU No. 8 Tahun 2016 tentang Penyandang Disabilitas","https://peraturan.bpk.go.id/Details/37251/uu-no-8-tahun-2016"),("ILO","Inclusive employment services in Indonesia","https://www.ilo.org/resource/news/indonesia-paves-way-inclusive-employment-services"),("OSS","Referensi KBLI kafe dan penyediaan makanan","https://oss.go.id/id/kbli"),("BPJPH","Informasi wajib sertifikasi halal Oktober 2026","https://bpjph.halal.go.id")]
s += [tabel(["SUMBER","REFERENSI","URL"],src,[34*mm,61*mm,69*mm]),Spacer(1,8),p("Keterbatasan","H2id"),p("Belum tersedia kunjungan lokasi, quotation sewa, wawancara pelanggan, quotation pemasok, laporan keuangan, kajian pajak/hukum, asesmen profesional disabilitas, serta ketentuan investasi pendiri. Semua angka adalah asumsi perencanaan dalam rupiah dan tidak boleh dipresentasikan sebagai jaminan keuntungan."),Spacer(1,8),sorotan("TAHAP BERIKUTNYA","Setelah data uji tuntas terkumpul, lanjutkan menjadi: model finansial 5 tahun yang dapat diedit, pitch deck 12-15 slide, ringkasan investasi satu halaman, dan rencana bisnis final dengan asumsi yang telah disetujui."),PageBreak()]

s += [Spacer(1,45*mm),p("BERAWAL DARI VISI,<br/>DIBANGUN DENGAN DISIPLIN.","Judul"),Spacer(1,8*mm),p("Yeshua Cafe dirancang untuk membangun usaha hospitalitas yang berkelanjutan secara komersial sekaligus menciptakan pekerjaan bermakna. Langkah berikutnya bukan membuat janji lebih besar, melainkan mengumpulkan bukti yang lebih kuat."),Spacer(1,55*mm),HRFlowable(width="100%",thickness=2,color=EMAS),Spacer(1,6*mm),p("Disiapkan untuk Juang Group","H2id"),p("Draf diskusi investor  |  Agustus 2026","Kecil")]

doc.build(s, canvasmaker=Kanvas)
print(OUT)
