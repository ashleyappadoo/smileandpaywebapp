# Smile & Pay — Web Pay Demo

Démo Vercel / Next.js.

- E-commerce : 0,10 €
- Click & Collect : 0,20 €
- QR Code : 0,30 €

## Variables Vercel

- `SNP_EPAY_API_KEY` : clé API Smile & Pay.
- `SNP_EPAY_ENDPOINT` : optionnelle. Par défaut : `https://extranet-api.smileandpay.com/public/api/v1/web-payment/init`.

## Routes portail Smile & Pay

- Success : `/payment/success`
- Error : `/payment/error`
- Refused : `/payment/refused`
- Cancel : `/payment/cancel`
- Callback : `/api/payment/callback`
