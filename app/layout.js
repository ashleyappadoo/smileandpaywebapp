import "./globals.css";

export const metadata = {
  title: "Smile & Pay — Paiement Web",
  description: "Démonstration API Paiement Web Smile & Pay"
};

export default function RootLayout({ children }) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}
