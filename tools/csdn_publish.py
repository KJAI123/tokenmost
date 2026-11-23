# -*- coding: utf-8 -*-
"""csdn_publish.py — CSDN 文章发布管线（无头浏览器版）
用法: python3 csdn_publish.py <md文件路径> [md文件2 ...]
依赖: rpa_browser.py (TM_CDP_PORT 默认 9223)
坑位清单见文件内注释（React setter 标题法/DOM 定位/Escape 重开弹窗等）
"""
import json, sys, time
sys.path.insert(0, '.')
from rpa_browser import Tab

TAGS = [('人工智能', '人工智能'), ('语言模型', '语言模型'), ('云计算', '云计算')]


def js_click_label():
    """触发「添加文章标签」按钮（全事件序列 JS click）"""
    return """(function(){
      const cands = [...document.querySelectorAll('*')].filter(el => {
        const t = (el.textContent||'').replace(/\\s+/g,' ').trim();
        const rc = el.getBoundingClientRect();
        return t.includes('添加文章标签') && rc.width > 60 && rc.height > 15;
      });
      if (cands.length) {
        const el = cands[cands.length-1];
        ['pointerdown','mousedown','pointerup','mouseup','click'].forEach(t => el.dispatchEvent(new MouseEvent(t, {bubbles: true, cancelable: true, view: window})));
      }
    })()"""


def js_pick_tag(exact):
    """搜索建议列表中精确点选标签"""
    return """(function(){
      const out = [];
      document.querySelectorAll('*').forEach(el => {
        if (el.children.length) return;
        const t = (el.textContent||'').replace(/\\s+/g,'').trim();
        const rc = el.getBoundingClientRect();
        if (t && t.length <= 10 && rc.width > 15 && rc.height > 12 && rc.y > 50) out.push({t: t, x: Math.round(rc.x+rc.width/2), y: Math.round(rc.y+rc.height/2)});
      });
      const seen = new Set(); const uniq = [];
      for (const o of out) { if (!seen.has(o.t)) { seen.add(o.t); uniq.push(o); } }
      const hit = uniq.find(o => o.t === '%s');
      if (hit) {
        const el = document.elementsFromPoint(hit.x, hit.y).find(e => e.tagName !== 'HTML');
        if (el) { ['pointerdown','mousedown','pointerup','mouseup','click'].forEach(t => el.dispatchEvent(new MouseEvent(t, {bubbles: true, cancelable: true, view: window}))); }
        return 'picked';
      }
      return 'miss';
    })()""" % exact


def set_title_js(title):
    """React 原生 setter 写标题（标题 input 隐藏 w=0 不可聚焦）"""
    import json as _json
    return """(function(){
      const inp = document.querySelector('input.article-bar__title');
      if (!inp) return 'none';
      const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
      setter.call(inp, %s);
      inp.dispatchEvent(new Event('input', {bubbles: true}));
      inp.dispatchEvent(new Event('change', {bubbles: true}));
      return 'set:' + inp.value.slice(0,15);
    })()""" % _json.dumps(title, ensure_ascii=False)


def publish(md_file):
    src = open(md_file, encoding='utf-8').read()
    title_line = src.split('\n', 1)[0].lstrip('# ').strip()
    body = src.split('\n', 1)[1].strip()
    lines = body.split('\n')

    tab = Tab.connect(new_url='https://editor.csdn.net/md/?not_checkout=1&createTime=now', wait=10)
    time.sleep(6)
    # 关模版库（DOM 定位 × / 取消，坐标无关）
    for _ in range(3):
        if tab.ev("document.body.innerText.includes('学习计划模板示例')"):
            tab.ev("""(function(){
              const btns = [...document.querySelectorAll('button')].filter(b => (b.textContent||'').trim()==='取消' && b.getBoundingClientRect().width>0);
              if (btns.length) { btns[btns.length-1].click(); return; }
              const x = [...document.querySelectorAll('[class*=close], [class*=Close], i, svg')].filter(el => {
                const rc = el.getBoundingClientRect();
                return rc.width > 5 && rc.width < 40 && rc.y > 60 && rc.y < 250 && rc.x > 900;
              });
              if (x.length) x[0].click();
            })()""")
            time.sleep(2)
        else:
            break
    # 引导浮层
    if tab.ev("document.body.innerText.includes('我知道了')"):
        tab.ev("""(function(){
          const b = [...document.querySelectorAll('button, div, a')].filter(el => (el.textContent||'').trim()==='我知道了' && el.getBoundingClientRect().width>50);
          if (b.length) b[0].click();
        })()""")
        time.sleep(1.5)
    # 标题：React setter
    r = tab.ev(set_title_js(title_line))
    print(' title:', r)
    # 正文
    r = tab.ev("""(function(){
      const el = document.querySelector('[contenteditable=true].editor__inner');
      if (!el) return 'no-editor';
      el.focus();
      return document.activeElement.getAttribute('contenteditable') === 'true' ? 'focused' : 'fail';
    })()""")
    print(' body:', r)
    if r != 'focused':
        return None
    tab.select_all(); time.sleep(0.4); tab.key('Backspace', 8); time.sleep(0.8)
    prev_list = False
    for line in lines:
        if line.startswith('- ') and prev_list:
            tab.type_text(line[2:])
        elif line.strip():
            tab.type_text(line)
        tab.key('Enter', 13)
        prev_list = line.startswith('- ')
        if len(line) > 60: time.sleep(0.1)
    time.sleep(2)
    g = tab.ev("""(function(){
      const t = document.querySelector('[contenteditable=true].editor__inner').innerText;
      return JSON.stringify({chars: t.length, tm: t.includes('tokenmost.com')});
    })()""")
    gate = json.loads(g)
    print(' gate:', gate)
    # 2026-11-24 新规：CSDN 零提及（tokenmost 提及=营销驳回主因），tm 不再要求
    if gate['chars'] < 500:
        print(' GATE FAILED — abort (draft kept)')
        return None
    # 发布弹窗（AI 面板挡先收起）
    tab.ev("""(function(){
      const col = [...document.querySelectorAll('button, div, span')].filter(el => (el.textContent||'').trim()==='收起' && el.getBoundingClientRect().width>10 && el.getBoundingClientRect().width<80);
      if (col.length) col[col.length-1].click();
    })()""")
    time.sleep(1.5)
    tab.ev("""(function(){
      const b = [...document.querySelectorAll('button')].find(b => (b.textContent||'').includes('发布文章'));
      if (b) b.click();
    })()""")
    time.sleep(4)
    if tab.ev("document.body.innerText.includes('我知道了')"):
        tab.ev("""(function(){
          const b = [...document.querySelectorAll('button, div, a')].filter(el => (el.textContent||'').trim()==='我知道了' && el.getBoundingClientRect().width>50);
          if (b.length) b[0].click();
        })()""")
        time.sleep(1.5)
    # 标签×3
    for q, e in TAGS:
        tab.ev(js_click_label())
        time.sleep(2.5)
        tab.ev("""(function(){
          const inp = [...document.querySelectorAll('input')].find(el => (el.placeholder||'').includes('搜索') || (el.placeholder||'').includes('Enter'));
          if (inp) inp.focus();
        })()""")
        time.sleep(0.5)
        tab.select_all(); time.sleep(0.2); tab.key('Backspace', 8); time.sleep(0.4)
        tab.type_text(q); time.sleep(1.8)
        print(' tag', q, tab.ev(js_pick_tag(e)))
    tab.key('Escape', 27); time.sleep(1.5)
    # Escape 会连弹窗关——重开再发布
    tab.ev("""(function(){
      const b = [...document.querySelectorAll('button')].find(b => (b.textContent||'').includes('发布文章'));
      if (b) b.click();
    })()""")
    time.sleep(3)
    r = tab.ev("""(function(){
      const b = document.querySelector('.modal button.btn-b-red');
      if (!b) return 'no-modal-pub';
      b.click();
      return 'pub-clicked';
    })()""")
    print(' publish:', r)
    d = {'url': ''}
    for i in range(14):
        time.sleep(8)
        st = tab.ev("""JSON.stringify({url: location.href.slice(0,130), loading: document.body.innerText.includes('正在加载中')})""")
        d = json.loads(st)
        if 'creation/success' in d['url']:
            break
        if not d['loading'] and i > 6: break
    return d['url']


if __name__ == '__main__':
    for f in sys.argv[1:]:
        url = publish(f)
        print(f'RESULT {f.split("/")[-1]}: {url}')
        time.sleep(10)
