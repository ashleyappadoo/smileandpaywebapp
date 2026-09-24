const demos = [
  { n:"01", title:"E-commerce", text:"Achat d'un produit sur une boutique en ligne.", price:"0,10 €", usecase:"ecommerce" },
  { n:"02", title:"Click & Collect", text:"Commande en ligne puis retrait sur place.", price:"0,20 €", usecase:"click-collect" },
  { n:"03", title:"QR Code", text:"Paiement à table depuis un QR Code.", price:"0,30 €", usecase:"qrcode" }
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
        <h1>3 parcours.<br/>Un seul paiement Web.</h1>
        <p>Démonstration des principaux parcours d'intégration du paiement Web Smile & Pay.</p>
      </section>
      <section className="grid">
        {demos.map(d => (
          <article className="card" key={d.usecase}>
            <span className="num">{d.n}</span>
            <h2>{d.title}</h2>
            <p>{d.text}</p>
            <div className="price">{d.price}</div>
            <a className="btn" href={"/api/payment/init?usecase="+d.usecase}>Payer {d.price}</a>
          </article>
        ))}
      </section>
      <footer className="foot">Smile & Pay · Web Pay Demo</footer>
    </main>
  );
}
