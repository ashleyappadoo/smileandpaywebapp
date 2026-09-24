const content = {
  success: ["Paiement accepté", "Le paiement a bien été validé."],
  refused: ["Paiement refusé", "Le paiement n'a pas été accepté."],
  cancel: ["Paiement annulé", "Le parcours de paiement a été annulé."],
  error: ["Erreur de paiement", "Le paiement n'a pas pu être finalisé."]
};

export default async function PaymentResult({ params, searchParams }) {
  const { status } = await params;
  const query = await searchParams;
  const [title, text] = content[status] || content.error;

  return (
    <main className="wrap">
      <header className="top">
        <div className="brand"><span className="mark">S</span> Smile & Pay</div>
        <span className="pill">WEB PAY</span>
      </header>
      <section className="result">
        <div className="eyebrow">{status.toUpperCase()}</div>
        <h1>{title}</h1>
        <p>{text}</p>
        {query.reason === "configuration" && (
          <div className="notice">La démo est prête. Ajoutez SNP_EPAY_API_KEY dans les variables Vercel pour activer le paiement réel.</div>
        )}
        <a className="btn back" href="/">Retour à la démo</a>
      </section>
    </main>
  );
}
