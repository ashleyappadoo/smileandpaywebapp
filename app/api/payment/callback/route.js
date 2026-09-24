export async function POST(request) {
  let payload = {};
  try {
    payload = await request.json();
  } catch {}

  console.log("Smile & Pay Web Pay callback", JSON.stringify(payload));

  return Response.json({ received: true }, { status: 200 });
}
