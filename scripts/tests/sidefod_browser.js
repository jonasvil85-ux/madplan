// Sidefodens elementer skal være mindst 44 px høje på 390 px, uden vandret scroll (kræver playwright + Chromium).
// Kør: node scripts/tests/sidefod_browser.js
const {chromium}=require('playwright');const http=require('http'),fs=require('fs'),path=require('path');
const rod=path.resolve(__dirname,'../..');
const srv=http.createServer((q,r)=>{let f=path.join(rod,q.url.split('?')[0]);if(f.endsWith('/'))f+='index.html';fs.readFile(f,(e,d)=>{if(e){r.writeHead(404);r.end();}else r.end(d);});}).listen(0,async()=>{
  const b=await chromium.launch();const p=await b.newPage({viewport:{width:390,height:844}});
  await p.route(/^https?:\/\/(?!localhost|127\.0\.0\.1)/,r=>r.abort());
  await p.addInitScript(()=>localStorage.setItem('madplan-intro','1'));
  await p.goto('http://localhost:'+srv.address().port+'/index.html');await p.waitForTimeout(1500);
  const fejl=await p.evaluate(()=>{const f=[];if(document.documentElement.scrollWidth>innerWidth)f.push('vandret scroll');
    document.querySelectorAll('.fod summary,.fod a,.fod-knap').forEach(e=>{if(e.offsetParent&&e.getBoundingClientRect().height<44)f.push(e.textContent.trim()+' '+e.getBoundingClientRect().height+' px');});return f;});
  console.log('FEJL',JSON.stringify(fejl));await b.close();srv.close();process.exit(fejl.length?1:0);});
