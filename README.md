# Smile & Pay — Web Pay Demo

Démo Vercel pour 3 cas d'usage : e-commerce (0,10 €), click & collect (0,20 €), QR code (0,30 €).

## Variables Vercel
- SNP_EPAY_ENDPOINT : endpoint unique EPay
- SNP_EPAY_API_KEY : clé si nécessaire

## URLs à configurer dans le portail client
- /payment/success
- /payment/error
- /payment/refused
- /payment/cancel
- Callback : /api/payment/callback
