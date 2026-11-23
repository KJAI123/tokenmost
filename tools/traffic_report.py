"""Aggregate TokenMost access logs for complete Beijing days. Only aggregate counts leave the process."""
import argparse
from collections import Counter
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, unquote, urlsplit

BJ = dt.timezone(dt.timedelta(hours=8))
LINE = re.compile(r'^(\S+) \S+ \S+ \[([^]]+)\] "([A-Z]+) ([^ ]+) HTTP/[^"]+" (\d{3}) [\d-]+ "([^"]*)" "([^"]*)"')
BOT = re.compile(r'bot|spider|crawler|headless|lighthouse|selenium|playwright|puppeteer|preview|monitor|curl|wget|python|go-http|httpclient|httpx|scrapy|slurp|facebookexternalhit|prerender|bytespider|petalbot',re.I)
QA = {'month-check','release','acceptance','__qa','qa'}
SITES = {'tokenmost.com','www.tokenmost.com'}
EVENTS = {'claim','share','rss'}
SURFACES = {'home','directory','comparison','platform','guide'}


def summarize(files, pages, end, days):
    start = end - dt.timedelta(days=days)
    lo = dt.datetime.combine(start, dt.time(), BJ).timestamp()
    hi = dt.datetime.combine(end, dt.time(), BJ).timestamp()
    by_day = {str(start+dt.timedelta(days=n)):Counter() for n in range(days)}
    refs, landings, action_counts, activity = Counter(),Counter(),Counter(),[]
    seen_dates = set()
    for path in files:
        reader = gzip.open if str(path).endswith('.gz') else open
        with reader(path,'rt',errors='replace') as log:
            for line in log:
                m = LINE.match(line)
                if not m:
                    continue
                addr,stamp,method,target,status,ref,ua = m.groups()
                if method not in ('GET','HEAD') or status not in ('200','304') or not ('Mozilla/' in ua and not BOT.search(ua)):
                    continue
                try:
                    url = urlsplit(target)
                    page = unquote(url.path)
                    if page == '/index.html': page = '/'
                    if page not in pages and page != '/assets/interaction.txt':
                        continue
                    query = parse_qs(url.query,keep_blank_values=True)
                    if QA.intersection(query) or addr in ('127.0.0.1','::1'):
                        continue
                    instant = dt.datetime.strptime(stamp,'%d/%b/%Y:%H:%M:%S %z').timestamp()
                    host = (urlsplit(ref).hostname or '').lower()
                except (ValueError, OverflowError):
                    continue
                date = str(dt.datetime.fromtimestamp(instant,BJ).date())
                seen_dates.add(date)
                if not lo-1800 <= instant < hi: continue
                if page == '/assets/interaction.txt':
                    event = query.get('event',[''])[0]
                    surface = query.get('surface',[''])[0]
                    if instant >= lo and method == 'HEAD' and event in EVENTS and surface in SURFACES:
                        action_counts[surface+'/'+event] += 1
                    continue
                if method != 'GET': continue
                client = hashlib.sha256((addr+'\0'+ua).encode()).digest()
                tags = {'share':'shared-link','verified_rss':'verified-rss','github_readme':'github-project','github_dataset':'github-dataset'}
                tag = query.get('utm_source',[''])[0]
                source = tags.get(tag) or ('internal' if host in SITES else host or 'direct/unknown')
                activity.append((instant,client,page,source,date))
    previous = {}
    for instant,client,page,source,date in sorted(activity):
        gap = instant-previous.get(client,0)
        previous[client] = instant
        if instant < lo: continue
        by_day[date]['pageviews'] += 1
        if gap >= 1800:
            by_day[date]['sessions'] += 1
            refs[source] += 1
            landings[page] += 1
    return {'start':str(start),'through':str(end-dt.timedelta(days=1)), 'timezone':'Asia/Shanghai',
            'sessions':sum(v['sessions'] for v in by_day.values()), 'pageviews':sum(v['pageviews'] for v in by_day.values()),
            'daily':by_day, 'entry_sources':dict(refs.most_common(30)), 'landing_pages':dict(landings.most_common(30)),
            'interaction_requests':action_counts,'observed_dates_in_window':sorted(k for k in seen_dates if k in by_day)}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path, default=Path('/www/wwwroot/tokenmost'))
    parser.add_argument('--end',help='Exclusive end date in Beijing time')
    parser.add_argument('--days',type=int,default=7)
    parser.add_argument('--baseline',type=Path,help='Fixed seven-day baseline report')
    parser.add_argument('--archive',type=Path,help='Private directory for dated aggregate reports')
    parser.add_argument('logs',nargs='*')
    args=parser.parse_args()
    end=dt.datetime.strptime(args.end,'%Y-%m-%d').date() if args.end else dt.datetime.now(BJ).date()
    pages={'/','/platform/','/guides/','/en.html','/free-cloud-servers.html','/free-ai-api.html'}
    for folder in ['platform','guides']:
        pages.update('/'+folder+'/'+p.name for p in (args.root/folder).glob('*.html'))
    files = args.logs or [str(p) for p in Path('/www/wwwlogs').glob('tokenmost.com.log*') if p.is_file()]
    if not files or args.days < 1: parser.error('No logs or invalid day count')
    report = summarize(files,pages,end,args.days)
    if args.baseline:
        baseline = json.loads(args.baseline.read_text())
        if baseline['timezone'] != report['timezone'] or len(baseline['daily']) != args.days or baseline['sessions'] <= 0:
            parser.error('Baseline and measurement windows must be comparable')
        report['baseline_sessions'] = baseline['sessions']
        report['target_sessions'] = baseline['sessions'] * 100
        report['multiple'] = (round(report['sessions']/baseline['sessions'],3)
                              if len(report['observed_dates_in_window']) == args.days else None)
    body = json.dumps(report,ensure_ascii=False,indent=2)+'\n'
    if args.archive:
        import os, tempfile
        with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=str(args.archive),delete=False) as f:
            f.write(body)
        os.replace(f.name,str(args.archive/(report['through']+'.json')))
    else:
        print(body,end='')
