import { NextResponse } from "next/server";

const scenarios = {
  ecommerce: { amount: 10, description: "DEMO ECOMMERCE" },
  "click-collect": { amount: 20, description: "DEMO CLICK AND COLLECT" },
  qrcode: { amount: 30, description: "DEMO QR CODE" }
};

export async function GET(request) {
  const currentUrl = new URL(request.url);
  const usecase = currentUrl.searchParams.get("usecase") || "ecommerce";
  const scenario = scenarios[usecase] || scenarios.ecommerce;
  const apiKey = process.env.SNP_EPAY_API_KEY;
  const endpoint = process.env.SNP_EPAY_ENDPOINT || "https://extranet-api.smileandpay.com/public/api/v1/web-payment/init";

  if (!apiKey) {
    return NextResponse.redirect(new URL("/payment/error?reason=configuration", request.url));
  }

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": apiKey
      },
      body: JSON.stringify({
        amount: scenario.amount,
        description: scenario.description
      }),
      cache: "no-store"
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok || !data.paymentUrl) {
      console.error("Smile & Pay init error", response.status, data);
      return NextResponse.redirect(new URL("/payment/error?reason=api", request.url));
    }

    return NextResponse.redirect(data.paymentUrl);
  } catch (error) {
    console.error("Smile & Pay init exception", error);
    return NextResponse.redirect(new URL("/payment/error?reason=network", request.url));
  }
}
