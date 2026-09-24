const mem=globalThis.__snpOrders||(globalThis.__snpOrders=new Map());
const url=process.env.KV_REST_API_URL; const token=process.env.KV_REST_API_TOKEN;
async function redis(cmd){if(!url||!token)return null;const r=await fetch(url,{method:"POST",headers:{Authorization:"Bearer "+token,"Content-Type":"application/json"},body:JSON.stringify(cmd),cache:"no-store"});if(!r.ok)throw new Error("KV "+r.status);return (await r.json()).result}
export async function putOrder(o){mem.set(o.id,o);if(url&&token)await redis(["SET","order:"+o.id,JSON.stringify(o),"EX","86400"]);return o}
export async function getOrder(id){if(url&&token){const v=await redis(["GET","order:"+id]);if(v)return typeof v==="string"?JSON.parse(v):v}return mem.get(id)||null}
export async function patchOrder(id,p){const o=await getOrder(id);if(!o)return null;return putOrder({...o,...p,updatedAt:new Date().toISOString()})}