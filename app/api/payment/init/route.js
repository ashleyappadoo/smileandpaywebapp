import {NextResponse} from "next/server";
const demos={ecommerce:{amount:10,description:"DEMO ECOMMERCE"},"click-collect":{amount:20,description:"DEMO CLICK AND COLLECT"},qrcode:{amount:30,description:"DEMO QR CODE"}};
export async function GET(request){
  const u=new URL(request.url);
  const usecase=u.searchParams.get("usecase");
  const demo=demos[usecase];
  if(!demo)return NextResponse.redirect(new URL("/payment/error?reason=usecase",request.url));
  const key=process.env.SNP_EPAY_API_KEY;
  const endpoint=process.env.SNP_EPAY_ENDPOINT||"https://extranet-api.smileandpay.com/public/api/v1/web-payment/init";
  if(!key)return NextResponse.redirect(new URL("/payment/error?reason=configuration",request.url));
  try{
    const r=await fetch(endpoint,{method:"POST",headers:{"Content-Type":"application/json","X-API-Key":key},body:JSON.stringify(demo),cache:"no-store"});
    const d=await r.json().catch(()=>({}));
    if(!r.ok||!d.paymentUrl){console.error("SmilePay init",r.status,d);return NextResponse.redirect(new URL("/payment/error?reason=api",request.url))}
    return NextResponse.redirect(d.paymentUrl);
  }catch(e){console.error("SmilePay network",e);return NextResponse.redirect(new URL("/payment/error?reason=network",request.url))}
}