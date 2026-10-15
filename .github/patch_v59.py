from pathlib import Path
p=Path('index.html')
s=p.read_text()
s=s.replace('BOOK LAB v5.8 WEBGL','BOOK LAB v5.9 WEBGL')
old="""void main(){
  bool staticPage = uMode < 0.5;
  bool front = staticPage ? true : !gl_FrontFacing;
  if(!staticPage && !front && uFlip < 0.48) discard;
  vec2 uv=front?vUV:vec2(1.0-vUV.x,vUV.y);
  vec4 c=front?samplePage(uFront,uv,uFrontOpacity,uFrontMat):samplePage(uBack,uv,uBackOpacity,uBackMat);
"""
new="""void main(){
  bool staticPage = uMode < 0.5;
  // Symmetric timing in both directions: never expose the target/back page before the fold crosses the spine.
  bool front = staticPage ? true : (uFlip < 0.5);
  vec2 uv=front?vUV:vec2(1.0-vUV.x,vUV.y);
  vec4 c=front?samplePage(uFront,uv,uFrontOpacity,uFrontMat):samplePage(uBack,uv,uBackOpacity,uBackMat);
"""
if old not in s: raise SystemExit('fragment flip anchor not found')
s=s.replace(old,new,1)
anchor="function setupGL(){gl.enable(gl.DEPTH_TEST);gl.depthFunc(gl.LEQUAL);gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);gl.disable(gl.CULL_FACE)}\n"
insert="""function setupGL(){gl.enable(gl.DEPTH_TEST);gl.depthFunc(gl.LEQUAL);gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);gl.disable(gl.CULL_FACE)}
function underPage(s,side){
  if(side<0)return pageAt(s*2-3);
  return pageAt(s*2+2);
}
function drawStatic(p,side,s,z=0){
  if(!p)return;
  if(p.material==='tracing'){
    const under=underPage(s,side);
    if(under)drawMesh(under,under,{mode:0,side,z:z-.02});
  }
  drawMesh(p,p,{mode:0,side,z});
}
"""
if anchor not in s: raise SystemExit('setup anchor not found')
s=s.replace(anchor,insert,1)
old_scene="""function drawScene(s=spread,flipState=null){fitCanvas(false);gl.viewport(0,0,canvas.width,canvas.height);gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);if(!pages.length){updateIndicator();return}setupGL();const P=pair(s);if(!flipState){if(P.l)drawMesh(P.l,P.l,{mode:0,side:-1});if(P.r)drawMesh(P.r,P.r,{mode:0,side:1});}else{const {dir,t,from,to}=flipState,A=pair(from),B=pair(to);if(dir>0){
    if(A.l)drawMesh(A.l,A.l,{mode:0,side:-1});
    if(B.r)drawMesh(B.r,B.r,{mode:0,side:1,z:-.012});
    if(A.r||B.l)drawMesh(A.r,B.l,{mode:1,dir:1,flip:t,curl:.95,z:.004});
  }else{
    if(B.l)drawMesh(B.l,B.l,{mode:0,side:-1,z:-.012});
    if(A.r)drawMesh(A.r,A.r,{mode:0,side:1});
    if(A.l||B.r)drawMesh(A.l,B.r,{mode:1,dir:-1,flip:t,curl:.95,z:.004});
  }}updateIndicator()}
"""
new_scene="""function drawScene(s=spread,flipState=null){fitCanvas(false);gl.viewport(0,0,canvas.width,canvas.height);gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);if(!pages.length){updateIndicator();return}setupGL();const P=pair(s);if(!flipState){drawStatic(P.l,-1,s);drawStatic(P.r,1,s);}else{const {dir,t,from,to}=flipState,A=pair(from),B=pair(to);if(dir>0){
    drawStatic(A.l,-1,from);
    drawStatic(B.r,1,to,-.012);
    if(A.r||B.l)drawMesh(A.r,B.l,{mode:1,dir:1,flip:t,curl:.95,z:.004});
  }else{
    drawStatic(B.l,-1,to,-.012);
    drawStatic(A.r,1,from);
    if(A.l||B.r)drawMesh(A.l,B.r,{mode:1,dir:-1,flip:t,curl:.95,z:.004});
  }}updateIndicator()}
"""
if old_scene not in s: raise SystemExit('scene anchor not found')
s=s.replace(old_scene,new_scene,1)
p.write_text(s)
