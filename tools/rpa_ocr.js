#!/usr/bin/env osascript -l JavaScript
// Vision OCR：读图片文件 → 输出 JSON {n, lines:[{text,x,y,w,h}]}（坐标=像素，原点左上；DPR 换算由调用方处理）
// 用法：osascript -l JavaScript tools/rpa_ocr.js <png路径> [图像宽px] [图像高px]
// 已知边界（2026-11-14 实测）：本机 Vision CJK 模型未下载，中文行会输出拉丁形近串——
//   拉丁关键词（tokenmost/Login/URL/复选框文字）定位与验证=准，中文内容验证改用多模态读图。
ObjC.import('Vision');
ObjC.import('Foundation');

function run(argv) {
  const path = argv[0];
  const imgW = argv[1] ? parseInt(argv[1], 10) : null;
  const imgH = argv[2] ? parseInt(argv[2], 10) : null;

  const nsPath = $.NSString.alloc.initWithUTF8String(path);
  const url = $.NSURL.fileURLWithPath(nsPath);
  // ObjC 选择器 initWithURL:options: → JXA initWithURLOptions
  const handler = $.VNImageRequestHandler.alloc.initWithURLOptions(url, $.NSDictionary.dictionary);
  const req = $.VNRecognizeTextRequest.alloc.init;
  req.recognitionLevel = 1; // accurate
  req.revision = 3;         // 新版模型（CJK 就绪时生效）
  req.automaticallyDetectsLanguage = false;
  req.recognitionLanguages = $(['zh-Hans', 'en-US']);
  req.usesLanguageCorrection = true;

  const err = Ref();
  const ok = handler.performRequestsError($.NSArray.arrayWithObject(req), err);
  if (!ok) {
    return JSON.stringify({ error: (err[0] && err[0].localizedDescription) ? String(err[0].localizedDescription.js) : 'perform failed' });
  }
  const out = [];
  const obs = req.results;   // NSArray：用 .count 不是 .length
  for (let i = 0; i < obs.count; i++) {
    const o = obs.objectAtIndex(i);
    const cands = o.topCandidates(1);
    if (cands.count === 0) continue;
    const t = String(cands.objectAtIndex(0).string.js);
    const bb = o.boundingBox; // 归一化，原点左下
    const entry = { text: t };
    if (imgW && imgH) {
      entry.x = Math.round(bb.origin.x * imgW);
      entry.y = Math.round((1 - bb.origin.y - bb.size.height) * imgH);
      entry.w = Math.round(bb.size.width * imgW);
      entry.h = Math.round(bb.size.height * imgH);
    }
    out.push(entry);
  }
  return JSON.stringify({ n: out.length, lines: out });
}
