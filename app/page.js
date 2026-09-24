const demos = [
  { n:"01", title:"E-commerce", text:"Achat d'un produit sur une boutique en ligne.", usecase:"ecommerce" },
  { n:"02", title:"Click & Collect", text:"Commande en ligne puis retrait sur place.", usecase:"click-collect" },
  { n:"03", title:"QR Code", text:"Paiement à table depuis un QR Code.", usecase:"qrcode" }
];

export default function Home() {
  return (
    <main className="wrap">
      <header className="top">
        <div className="brand"><span className="mark">S</span> Smile & Pay</div>
        <span className="pill">PAIEMENT WEB · DEMO</span>
      </header>
      <section className="hero">
        <div className="eyebrow">API PAIEMENT À DISTANCE</div>
        <h1>Les cas d'usages de l'API paiement Web</h1>
        <p>Démonstration des principaux parcours d'intégration du paiement Web Smile & Pay.</p>
      </section>
      <section className="grid">
        {demos.map(d => (
          <article className="card" key={d.usecase}>
            <span className="num">{d.n}</span>
            <h2>{d.title}</h2>
            <p>{d.text}</p>
            <a className="btn" href={"/api/payment/init?usecase="+d.usecase}>
              {d.usecase === "ecommerce" ? "Ouvrir la boutique" : d.usecase === "click-collect" ? "Commander" : "Ouvrir le paiement"}
            </a>
          </article>
        ))}
      </section>
      <footer className="foot">Smile & Pay · Web Pay Demo</footer>
    </main>
  );
}
