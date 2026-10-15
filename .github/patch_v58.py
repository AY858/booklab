from pathlib import Path
p=Path('index.html')
s=p.read_text()

s=s.replace('BOOK LAB v5.7 WEBGL','BOOK LAB v5.8 WEBGL')

old='uniform float uMode;\nout vec2 vUV;out float vShade;out float vEdge;'
new='uniform float uMode;\nuniform float uZOffset;\nout vec2 vUV;out float vShade;out float vEdge;'
if old not in s: raise SystemExit('VS uniform anchor not found')
s=s.replace(old,new,1)

old='  vUV=aUV;vEdge=smoothstep(.0,.08,ux)*(1.0-smoothstep(.9,1.0,ux));\n  gl_Position=uMVP*vec4(p,1.0);'
new='  p.z += uZOffset;\n  vUV=aUV;vEdge=smoothstep(.0,.08,ux)*(1.0-smoothstep(.9,1.0,ux));\n  gl_Position=uMVP*vec4(p,1.0);'
if old not in s: raise SystemExit('VS position anchor not found')
s=s.replace(old,new,1)

old="['uMVP','uFlip','uDir','uSide','uCurl','uMode','uFrontOpacity','uBackOpacity','uFrontMat','uBackMat','uFront','uBack']"
new="['uMVP','uFlip','uDir','uSide','uCurl','uMode','uZOffset','uFrontOpacity','uBackOpacity','uFrontMat','uBackMat','uFront','uBack']"
if old not in s: raise SystemExit('uniform list anchor not found')
s=s.replace(old,new,1)

old='gl.uniform1f(U.uMode,opt.mode??0);gl.uniform1f(U.uFrontOpacity'
new='gl.uniform1f(U.uMode,opt.mode??0);gl.uniform1f(U.uZOffset,opt.z??0);gl.uniform1f(U.uFrontOpacity'
if old not in s: raise SystemExit('drawMesh uniform anchor not found')
s=s.replace(old,new,1)

old='if(B.r)drawMesh(B.r,B.r,{mode:0,side:1});\n    if(A.r||B.l)drawMesh(A.r,B.l,{mode:1,dir:1,flip:t,curl:.95});'
new='if(B.r)drawMesh(B.r,B.r,{mode:0,side:1,z:-.012});\n    if(A.r||B.l)drawMesh(A.r,B.l,{mode:1,dir:1,flip:t,curl:.95,z:.004});'
if old not in s: raise SystemExit('forward layering anchor not found')
s=s.replace(old,new,1)

old='if(B.l)drawMesh(B.l,B.l,{mode:0,side:-1});\n    if(A.r)drawMesh(A.r,A.r,{mode:0,side:1});\n    if(A.l||B.r)drawMesh(A.l,B.r,{mode:1,dir:-1,flip:t,curl:.95});'
new='if(B.l)drawMesh(B.l,B.l,{mode:0,side:-1,z:-.012});\n    if(A.r)drawMesh(A.r,A.r,{mode:0,side:1});\n    if(A.l||B.r)drawMesh(A.l,B.r,{mode:1,dir:-1,flip:t,curl:.95,z:.004});'
if old not in s: raise SystemExit('reverse layering anchor not found')
s=s.replace(old,new,1)

p.write_text(s)
