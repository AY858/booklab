from pathlib import Path

p = Path('index.html')
s = p.read_text()

s = s.replace('BOOK LAB v5.6 WEBGL', 'BOOK LAB v5.7 WEBGL')
s = s.replace('拖图片到这里 · 导入文件夹保留读取顺序', '拖图片到这里 · 按源文件名前缀页码排序')

old_sort = "function uid(){return crypto.randomUUID?crypto.randomUUID():Date.now().toString(36)+Math.random().toString(36).slice(2)}function sortN(a,b){return a.name.localeCompare(b.name,undefined,{numeric:true,sensitivity:'base'})}"
new_sort = """function uid(){return crypto.randomUUID?crypto.randomUUID():Date.now().toString(36)+Math.random().toString(36).slice(2)}
function sourcePageSort(a,b){
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
function sortN(a,b){return sourcePageSort(a,b)}"""
if old_sort not in s:
    raise SystemExit('sort anchor not found')
s = s.replace(old_sort, new_sort)

old_add = "async function addFiles(fs,preserveOrder=false){const arr=[...fs].filter(f=>f.type.startsWith('image/'));if(!preserveOrder)arr.sort(sortN);"
new_add = "async function addFiles(fs,preserveOrder=false){const arr=[...fs].filter(f=>f.type.startsWith('image/')).map((f,i)=>{f.__sourceIndex=i;return f});arr.sort(sourcePageSort);"
if old_add not in s:
    raise SystemExit('addFiles anchor not found')
s = s.replace(old_add, new_add)

# Remove accidental duplicate source-name block if present twice in a row.
block = "const fn=document.createElement('div');fn.style.cssText='margin-top:4px;font-size:10px;color:#b7bdc7;white-space:nowrap;overflow:hidden;text-overflow:ellipsis';fn.textContent=p.sourceName||p.name;fn.title=p.sourcePath||p.sourceName||p.name;d.appendChild(fn);"
s = s.replace(block + block, block)

p.write_text(s)
