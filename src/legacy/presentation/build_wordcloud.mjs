import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {spawnSync} from 'node:child_process';
import {Presentation,PresentationFile} from '@oai/artifact-tool';

const dir=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(dir,'../../..');
const out=path.resolve(dir,'../../英文15页_词云版');
await fs.mkdir(out,{recursive:true});
const SKILL='${ORIGINAL_USER_HOME}/.codex/plugins/cache/openai-primary-runtime/presentations/26.1009.11318/skills/presentations';
const {applyPresentationChartFont,finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')));
const PX=4/3;
const fonts={Sans:'Arial',SansB:'Arial',Serif:'Georgia',SerifI:'Georgia',CN:'Microsoft YaHei',CNB:'Microsoft YaHei'};
const ink='#252D2C',teal='#345A60',green='#81968A';
function position(o){return {left:o.x*PX,top:o.y*PX,width:o.w*PX,height:o.h*PX};}
function shape(slide,o,geometry='rect'){
  return slide.shapes.add({geometry,position:position(o),fill:o.color,line:{style:'solid',fill:'none',width:0}});
}
function text(slide,o){
  const s=slide.shapes.add({geometry:'textbox',name:o.source==='single'?'Label':'Editable paragraph',
    position:position(o),fill:'none',line:{style:'solid',fill:'none',width:0}});
  s.text=o.text;
  s.text.style={fontSize:o.size*PX,typeface:fonts[o.font],bold:o.font.endsWith('B'),italic:o.font==='SerifI',
    color:o.color,wrap:o.source==='single'?'none':'square',autoFit:'none',verticalAlignment:'top',
    insets:0,lineSpacing:o.leading/o.size};
  return s;
}
function nativeChart(slide,o,lang){
  const z=lang==='ZH';
  let categories,values,colors;
  if(o.chart==='frequency'){
    categories=[...o.categories];values=[...o.values];colors=values.map((v,i)=>i===0?teal:green);
  }else if(o.chart==='keywords'){
    categories=z?['教室','资金','教学楼','操场','校医室','厕所','玩耍','空间']:
      ['Classroom','Funding','Teaching building','Playground','School clinic','Toilet','Play','Space'];
    values=[7,5,4,3,2,2,2,2];colors=[teal,green,green,green,'#BBC7BC','#BBC7BC','#BBC7BC','#BBC7BC'];
  }else if(o.chart==='audit'){
    categories=z?['基础安全','舒适性','活动支持','照护支持','空间联结']:
      ['Basic safety','Comfort','Activity support','Care support','Spatial connections'];
    values=[3.75,3.44,2.71,3.83,3];colors=[green,green,teal,teal,green];
  }else{
    const labs=z?['学习','就餐','活动','午休','眼保健操','间隙']:
      ['Study','Meals','Activity','Midday rest','Eye exercises','Intervals'];
    const nums=[390,160,90,80,30,120],cols=[teal,green,'#687F72','#ABBBA8','#B5C3B8','#D9DDD4'];
    const chart=slide.charts.add('bar',{
      position:position(o),categories:[z?'每日分钟数':'Scheduled minutes'],
      series:labs.map((name,i)=>({name,values:[nums[i]],fill:cols[i],line:{style:'solid',fill:'none',width:0}})),
      barOptions:{direction:'bar',grouping:'stacked',overlap:100,gapWidth:35},
      hasLegend:true,legend:{position:'bottom',overlay:false,textStyle:{fontSize:11,fill:ink}},
      xAxis:{visible:false,line:{style:'solid',fill:'none',width:0},majorGridlines:null},
      yAxis:{visible:false,min:0,max:870,majorGridlines:null,line:{style:'solid',fill:'none',width:0}},
      dataLabels:{showValue:true,position:'center',numberFormatCode:'0',textStyle:{fontSize:11,fill:'#FFFFFF'}},
      chartFill:'#FFFFFF',chartLine:{style:'solid',fill:'none',width:0},plotAreaFill:'#FFFFFF',plotAreaLine:{style:'solid',fill:'none',width:0}
    });
    applyPresentationChartFont(chart,{fontFamily:z?'Microsoft YaHei':'Arial'});
    return;
  }
  // Office draws horizontal category order from bottom to top.
  categories.reverse();values.reverse();colors.reverse();
  const chart=slide.charts.add('bar',{
    position:position(o),categories,
    series:[{name:z?((o.chart==='keywords'||o.chart==='frequency')?'出现次数':'维度均值'):((o.chart==='keywords'||o.chart==='frequency')?'Occurrences':'Mean score'),values,
      fill:teal,points:colors.map((fill,idx)=>({idx,fill,line:{style:'solid',fill:'none',width:0}}))}],
    barOptions:{direction:'bar',grouping:'clustered',gapWidth:55},hasLegend:false,
    xAxis:{visible:true,textStyle:{fontSize:11,fill:ink},line:{style:'solid',fill:'none',width:0},majorGridlines:null},
    yAxis:{visible:true,min:0,max:(o.chart==='keywords'||o.chart==='frequency')?8:5,majorUnit:(o.chart==='keywords'||o.chart==='frequency')?2:1,
      numberFormatCode:'0',textStyle:{fontSize:10,fill:ink},line:{style:'solid',fill:'none',width:0},
      majorGridlines:{fill:'#E0E6DF',width:.5,style:'solid'}},
    dataLabels:{showValue:true,position:'outEnd',numberFormatCode:(o.chart==='keywords'||o.chart==='frequency')?'0':'0.00',
      textStyle:{fontSize:11,fill:ink}},
    chartFill:'#FFFFFF',chartLine:{style:'solid',fill:'none',width:0},plotAreaFill:'#FFFFFF',plotAreaLine:{style:'solid',fill:'none',width:0}
  });
  applyPresentationChartFont(chart,{fontFamily:z?'Microsoft YaHei':'Arial'});
}
for(const lang of ['EN']){
  const data=JSON.parse(await fs.readFile(path.join(dir,`wordcloud_layout_${lang}.json`),'utf8'));
  const presentation=Presentation.create({slideSize:{width:data.width*PX,height:data.height*PX}});
  for(const [index,item] of data.slides.entries()){
    const slide=presentation.slides.add();slide.background.fill='#FFFFFF';
    for(const o of item.objects){
      if(o.kind==='text')text(slide,o);
      else if(o.kind==='rect'||o.kind==='ellipse')shape(slide,o,o.kind);
      else if(o.kind==='image'){
        slide.images.add({blob:new Uint8Array(await fs.readFile(o.path)),contentType:'image/png',alt:o.alt,
          fit:'contain',position:position(o)});
      }else if(o.kind==='line'||o.kind==='polygon'){
        const xs=o.points.map(p=>p[0]),ys=o.points.map(p=>p[1]),x=Math.min(...xs),y=Math.min(...ys);
        const w=Math.max(...xs)-x,h=Math.max(...ys)-y;
        slide.shapes.add({geometry:'custom',position:{left:x*PX,top:y*PX,width:Math.max(w*PX,.1),height:Math.max(h*PX,.1)},
          fill:o.kind==='polygon'?o.color:'none',line:{style:'solid',fill:o.stroke||o.color,width:o.width*PX,style:o.dash?'dashed':'solid'},
          customPaths:[{width:Math.max(w*PX,.1),height:Math.max(h*PX,.1),
            commands:o.points.map((p,i)=>({[i===0?'moveTo':'lineTo']:{x:(p[0]-x)*PX,y:(p[1]-y)*PX}}))}]});
      }else if(o.kind==='chart')nativeChart(slide,o,lang);
    }
    slide.speakerNotes.text=item.notes || (lang==='ZH'?
      `实地调研、学校访谈与校园设计。参考文献见第11页。`:
      `Field survey, school interviews and campus design. References appear on slide 11.`);
  }
  const candidate=path.join(dir,`wordcloud_candidate_${lang}.pptx`);
  await (await PresentationFile.exportPptx(presentation)).save(candidate);
  const exact=path.join(dir,`wordcloud_exact_${lang}.pptx`);
  const patch=spawnSync('${ORIGINAL_USER_HOME}/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',
    [path.join(root,'patch_ppt_typography.py'),candidate,path.join(dir,`wordcloud_layout_${lang}.json`),exact],{encoding:'utf8'});
  if(patch.status!==0)throw new Error(patch.stderr);
  console.log(patch.stdout.trim());
  console.log('EXPORTED',lang,candidate);
  const final=path.join(out,`Campus_Research_Portfolio_${lang}_15pages_3WordClouds.pptx`);
  const result=await finalizePresentation({
    workspaceDir:root,candidatePath:exact,finalPath:final,
    pythonExecutable:'${ORIGINAL_USER_HOME}/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',
    integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),
    layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),
    layoutArgs:['--expected-slide-size-emu',`${Math.round(data.width*12700)},${Math.round(data.height*12700)}`],
    explicitTotalSlideCount:15,requiredNativeChartOwnerSlides:[4,8],
    materializeLiteralChartWorkbooks:true,
    fontPolicy:{basis:'design',families:['Arial','Georgia','Microsoft YaHei']},
    verifyArtifactToolImport:true,
    receiptPath:path.join(dir,`validation_wordcloud_${lang}.json`)
  });
  console.log('FINALIZED',lang,JSON.stringify(result));
}

