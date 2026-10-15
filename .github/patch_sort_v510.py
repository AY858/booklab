from pathlib import Path
p=Path('index.html')
s=p.read_text()
s=s.replace('BOOK LAB v5.9 WEBGL','BOOK LAB v5.10 WEBGL')
old="""function sourcePageSort(a,b){
  const A=(a.name||'').normalize('NFKC'),B=(b.name||'').normalize('NFKC');
  const ma=A.match(/^(\\d+)/),mb=B.match(/^(\\d+)/);
  if(ma&&mb){
    const na=Number(ma[1]),nb=Number(mb[1]);
    if(na!==nb)return na-nb;
    if(ma[1].length!==mb[1].length)return mb[1].length-ma[1].length;
    return (a.__sourceIndex??0)-(b.__sourceIndex??0);
  }
  if(ma&&!mb)return -1;
  if(!ma&&mb)return 1;
  const al=A.toLowerCase(),bl=B.toLowerCase();
  return al<bl?-1:al>bl?1:(a.__sourceIndex??0)-(b.__sourceIndex??0);
}
"""
new="""const fileNameCollator=new Intl.Collator('zh-CN',{numeric:true,sensitivity:'base',ignorePunctuation:false});
function sourcePageSort(a,b){
  const A=(a.name||'').normalize('NFKC'),B=(b.name||'').normalize('NFKC');
  const ma=A.match(/^(\\d+)/),mb=B.match(/^(\\d+)/);
  if(ma&&mb){
    const na=Number(ma[1]),nb=Number(mb[1]);
    if(na!==nb)return na-nb;
    if(ma[1].length!==mb[1].length)return mb[1].length-ma[1].length;
    const ra=A.slice(ma[1].length),rb=B.slice(mb[1].length);
    const ha=(ra.match(/^-+/)||[''])[0].length,hb=(rb.match(/^-+/)||[''])[0].length;
    if((ha>0)!=(hb>0))return ha>0?1:-1;
    if(ha!==hb)return ha-hb;
    const c=fileNameCollator.compare(ra,rb);
    if(c)return c;
    return A<B?-1:A>B?1:0;
  }
  if(ma&&!mb)return -1;
  if(!ma&&mb)return 1;
  const la=(A.match(/^[A-Za-z]+/)||[''])[0],lb=(B.match(/^[A-Za-z]+/)||[''])[0];
  if(la&&lb&&la[0].toLowerCase()===lb[0].toLowerCase()&&la.length!==lb.length)return lb.length-la.length;
  return fileNameCollator.compare(A,B);
}
"""
if old not in s: raise SystemExit('sort block not found')
s=s.replace(old,new,1)
p.write_text(s)
