// BFT live face for an ordinals inscription. Self-contained, no imports. DISPLAY CONVENTION, not the standard.
// bftLive(h, arrivedAt, now, estimated) is pure: the date, hour and 10-minute step come from the height, the
// clock only measures seconds since the block arrived. Holds at 9:59 past 600 s, skew reads 0, no arrival: "HH:M-:--".
// bftWatch(render) polls /r/blockheight and records the moment THIS viewer first saw each new height (an inscription
// cannot call out: the ord CSP blocks it, so viewer first-seen is the only arrival it can know). On a cold load, before
// any change has been seen, it asks /r/blockinfo/<h> for the header time, clamps the age into [0, 599] s and marks the
// face estimated. The header time is never used otherwise.
const bftLive=(h,a,n,est=false)=>{const N=x=>typeof x=="number"&&isFinite(x),p=(v,w)=>String(v).padStart(w,"0"),E=!!est;
if(!Number.isSafeInteger(h)||h<0)return{known:false,text:"----.--.-- --:--:-- a₿",hour:null,minute:null,second:null,elapsed:null,holding:false,lateBy:0,skewed:false,estimated:E};
const d=Math.floor(h/144),b=h%144,o=d%364,hr=Math.floor(b/6),st=b%6*10,
D=p(Math.floor(d/364),4)+"."+p(Math.floor(o/28)+1,2)+"."+p(o%28+1,2)+" "+p(hr,2)+":";
if(!N(a)||!N(n))return{known:true,text:D+st/10+"-:-- a₿",hour:hr,minute:null,second:null,elapsed:null,holding:false,lateBy:0,skewed:false,estimated:E};
const r=Math.floor(n-a),e=Math.max(0,r),H=e>=600,s=H?599:e,m=st+Math.floor(s/60),c=s%60;
return{known:true,text:D+p(m,2)+":"+p(c,2)+" a₿",hour:hr,minute:m,second:c,elapsed:e,holding:H,lateBy:H?e-600:0,skewed:r<0,estimated:E}};
const bftWatch=(render,env={})=>{const f=env.fetch||fetch,now=env.now||(()=>Date.now()/1000);let h=null,a=null,est=false;
const poll=async()=>{try{const v=Number((await(await f("/r/blockheight")).text()).trim());if(!Number.isSafeInteger(v)||v<0)return;
if(h===null){h=v;try{const t=(await(await f("/r/blockinfo/"+v)).json()).timestamp,k=now();a=Number.isFinite(t)?k-Math.min(599,Math.max(0,k-t)):null;est=a!==null}catch(x){a=null}}
else if(v!==h){h=v;a=now();est=false}}catch(x){}};
const draw=()=>{if(h!==null)render(bftLive(h,a,now(),est),h)};
if(!env.manual){poll();setInterval(poll,5e3);setInterval(draw,1e3)}return{poll,draw}};
