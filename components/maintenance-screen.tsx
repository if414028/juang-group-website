import Image from "next/image";

export function MaintenanceScreen() {
  return (
    <main className="maintenance-page" id="main">
      <div className="maintenance-glow maintenance-glow-left" aria-hidden />
      <div className="maintenance-glow maintenance-glow-right" aria-hidden />

      <section className="maintenance-card" aria-labelledby="maintenance-title">
        <div className="maintenance-brand">
          <Image
            src="/brand/official/juang-group-logo.svg"
            alt="Juang Group"
            width={112}
            height={112}
            priority
          />
        </div>

        <div className="maintenance-status">
          <span aria-hidden />
          Temporarily unavailable
        </div>

        <h1 id="maintenance-title">
          Website access is
          <span>currently on hold.</span>
        </h1>

        <p className="maintenance-lead">
          This website is temporarily unavailable while the final project
          arrangements are being completed. Access will resume once the
          finalization process is complete.
        </p>

        <p className="maintenance-local">
          Website ini sementara dinonaktifkan selama proses penyelesaian akhir
          proyek. Akses akan kembali tersedia setelah seluruh proses finalisasi
          selesai.
        </p>

        <div className="maintenance-divider" aria-hidden>
          <span />
          <i />
          <span />
        </div>

        <footer className="maintenance-footer">
          <strong>Juang Group</strong>
          <span>Purpose · Hospitality · Community</span>
        </footer>
      </section>
    </main>
  );
}
