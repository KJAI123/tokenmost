#!/usr/bin/env python3
"""Offline regression tests; fixtures, credentials and output stay in temporary directories."""
import contextlib
import gzip
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import zlib

import harvest
import harvest_diff
import notify_hourly as notify
import sync
import datetime


HTML = "<p>新用户免费 2000 万 Tokens，每天 1000 次。</p>"
CREDS = ("offline-app", "offline-secret", "offline-owner")


def entries(n):
    return [{"id": str(i), "name": str(i), "url": f"https://example.invalid/{i}",
             "status": "ok", "findings": []} for i in range(n)]


class PipelineTests(unittest.TestCase):
    def use(self, manager):
        result = manager.__enter__()
        self.addCleanup(manager.__exit__, None, None, None)
        return result

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.use(patch("urllib.request.urlopen", side_effect=AssertionError("network forbidden")))
        self.use(patch.object(notify, "CFG", self.root / "missing-config.json"))
        self.use(patch.object(notify.time, "sleep", return_value=None))
        self.use(contextlib.redirect_stdout(io.StringIO()))
        self.use(contextlib.redirect_stderr(io.StringIO()))

    def test_entry_health_is_deduplicated_and_independent_of_verification(self):
        rows = [dict(id=i,url=url,published=True,verify_status="verified")
                for i,url in [("a","https://example.org/claim/"),("b","https://example.org/claim"),
                              ("watched","https://example.org/rules"),("old","https://example.org/old")]]
        rows[-1]["verify_status"] = "expired"
        sources = [{"deals":["watched"]}]
        now = datetime.datetime.now(datetime.timezone.utc)
        state, calls = {}, []
        def denied(url):
            calls.append(url)
            raise urllib.error.HTTPError(url,403,"restricted",{},None)
        for hours in (0,1,24,48):
            sync.check_entry_links(rows,sources,state,now+datetime.timedelta(hours=hours),denied)
        self.assertEqual(len(calls),3)
        entry, = state["entry_links"].values()
        self.assertEqual((entry["status"],entry["fail_streak"],entry["deals"]),("access_limited",3,["a","b"]))
        self.assertEqual(len(sync.review_items([],{},state["entry_links"])),1)
        def success(url):
            calls.append(url)
            return 200
        for days in (3,4,9,10):
            sync.check_entry_links(rows,sources,state,now+datetime.timedelta(days=days),success)
        self.assertEqual(len(calls),5)
        self.assertEqual(sync.review_items([],{},state["entry_links"]),[])
        self.assertEqual(rows[0]["verify_status"],"verified")

    def harvest_setup(self, fetch):
        cfg = self.root / "sources.json"
        cfg.write_text(json.dumps({"sources": entries(3)}), encoding="utf-8")
        for name, value in (("SOURCES", cfg), ("OUTDIR", self.root), ("fetch", fetch),
                            ("fetch_md", lambda _: ""), ("robots_allows", lambda *_: True)):
            self.use(patch.object(harvest, name, value))

    def test_decoding_compressed_text(self):
        raw = HTML.encode()
        compressor = zlib.compressobj(wbits=-zlib.MAX_WBITS)
        deflated = compressor.compress(raw) + compressor.flush()
        for data, encoding in ((raw, None), (gzip.compress(raw), None),
                               (gzip.compress(raw), "gzip"), (zlib.compress(raw), "deflate"),
                               (deflated, "deflate"), (gzip.compress(zlib.compress(raw)), "deflate, gzip")):
            with self.subTest(encoding=encoding):
                decoded = harvest.decode_payload(data, encoding)
                self.assertEqual(decoded, HTML)
                self.assertTrue(harvest.extract(harvest.load_text(decoded), harvest.DEFAULT_PATTERNS))

    def test_unknown_or_broken_encoding_never_becomes_evidence(self):
        for payload, encoding in ((b"free 2000 tokens", "br"), (b"free 2000 tokens", "zstd"),
                                  (b"free 2000 tokens", "gzip"), (b"\x1f\x8b", None)):
            with self.subTest(encoding=encoding):
                with self.assertRaises(harvest.UnreadablePayload):
                    harvest.decode_payload(payload, encoding)
        self.harvest_setup(lambda _: harvest.decode_payload(b"free 2000 tokens", "br"))
        results, _ = harvest.run("0")
        self.assertEqual(results[0]["status"], "binary")
        self.assertEqual(results[0]["findings"], [])

    def test_binary_text_is_excluded(self):
        self.harvest_setup(lambda _: "\x00\x01\x02" * 100 + "免费 2000 tokens")
        results, _ = harvest.run("0")
        self.assertEqual(results[0]["status"], "binary")
        self.assertEqual(results[0]["findings"], [])

    def test_binary_response_keeps_request_pacing(self):
        self.harvest_setup(lambda _: "\x00\x01\x02" * 100 + "免费 2000 tokens")
        with patch.object(harvest.time, "sleep") as delay:
            harvest.run("0")
        delay.assert_called_once_with(harvest.DELAY)

    def test_only_preserves_full_json_and_report(self):
        self.harvest_setup(lambda _: HTML)
        report = harvest.save(entries(3))
        before = {p.name: p.read_bytes() for p in (report, self.root / "latest.json")}
        self.assertEqual(harvest.main(["--only", "1"]), 0)
        for name, content in before.items():
            self.assertEqual((self.root / name).read_bytes(), content)
        partial = json.loads((self.root / "latest-partial.json").read_text())
        self.assertEqual(partial["scope"], "--only 1")
        self.assertEqual([r["id"] for r in partial["results"]], ["1"])

    def test_no_match_and_empty_save_preserve_snapshot(self):
        self.harvest_setup(lambda _: HTML)
        harvest.save(entries(3))
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        self.assertEqual(harvest.main(["--only", "missing"]), 1)
        with self.assertRaises(ValueError):
            harvest.save([])
        self.assertEqual({p.name: p.read_bytes() for p in self.root.iterdir()}, before)

    def diff_setup(self, current, previous=None):
        (self.root / "latest.json").write_text(json.dumps(current), encoding="utf-8")
        if previous is not None:
            (self.root / "prev.json").write_text(json.dumps(previous), encoding="utf-8")

    def assert_diff_refused(self, baseline):
        self.assertEqual(harvest_diff.run_diff(self.root)[0], 1)
        prev = self.root / "prev.json"
        self.assertEqual(prev.read_bytes() if prev.exists() else None, baseline)
        self.assertEqual(list(self.root.glob("alert-*.md")), [])

    def test_partial_scope_refused_before_initializing_baseline(self):
        self.diff_setup({"scope": "--only 1", "results": entries(8)})
        self.assert_diff_refused(None)

    def test_partial_scope_refused_even_above_count_threshold(self):
        self.diff_setup({"scope": "--only 1", "results": entries(8)}, {"results": entries(12)})
        self.assert_diff_refused((self.root / "prev.json").read_bytes())

    def test_legacy_count_collapse_preserves_baseline(self):
        self.diff_setup({"results": entries(1)}, {"results": entries(12)})
        self.assert_diff_refused((self.root / "prev.json").read_bytes())

    def test_empty_or_invalid_snapshot_preserves_baseline(self):
        for current in ({"results": []}, {"results": None}, []):
            with self.subTest(current=current):
                self.diff_setup(current, {"results": entries(3)})
                self.assert_diff_refused((self.root / "prev.json").read_bytes())
        (self.root / "latest.json").write_text("{broken", encoding="utf-8")
        self.assert_diff_refused((self.root / "prev.json").read_bytes())

    def test_normal_changes_and_legacy_initialization_still_work(self):
        self.diff_setup({"results": entries(2)})
        self.assertEqual(harvest_diff.run_diff(self.root)[0], 0)
        current = entries(2)
        current[0]["findings"] = [{"match": "免费额度", "context": "new evidence"}]
        self.diff_setup({"scope": "full", "results": current})
        self.assertEqual(harvest_diff.run_diff(self.root)[0], 0)
        self.assertEqual(len(list(self.root.glob("alert-*.md"))), 1)
        self.assertIn("no change", harvest_diff.run_diff(self.root)[1])

    def transport(self, tokens, message):
        self.calls = {"token": 0, "message": 0, "uuids": []}

        def call(url, body, headers, timeout=15):
            if url == notify.FEISHU_TOKEN_URL:
                i = self.calls["token"]
                self.calls["token"] += 1
                response = tokens[min(i, len(tokens) - 1)]
            else:
                self.calls["message"] += 1
                self.calls["uuids"].append(body["uuid"])
                response = message
            if isinstance(response, Exception):
                raise response
            return response
        return call

    def test_token_non_2xx_cannot_authorize_message_post(self):
        for status in (None, 302, 502):
            with self.subTest(status=status):
                call = self.transport([(status, {"code": 0, "tenant_access_token": "fake"})],
                                      (200, {"code": 0}))
                self.assertEqual(notify.send("offline", call, CREDS)[0], "token_failed")
                self.assertEqual(self.calls["message"], 0)

    def test_token_definitive_rejection_has_no_retry_or_message(self):
        for response in ((403, {"code": 0, "tenant_access_token": "fake"}),
                         (200, {"code": 10003, "msg": "invalid app"})):
            with self.subTest(response=response):
                call = self.transport([response], (200, {"code": 0}))
                with self.assertRaises(RuntimeError):
                    notify.send("offline", call, CREDS)
                self.assertEqual(self.calls["token"], 1)
                self.assertEqual(self.calls["message"], 0)

    def test_only_token_stage_can_retry(self):
        for first in (TimeoutError("token timeout"), (502, {"code": 0, "tenant_access_token": "fake"})):
            with self.subTest(first=first):
                call = self.transport([first, (200, {"code": 0, "tenant_access_token": "fake"})],
                                      (200, {"code": 0}))
                self.assertEqual(notify.send("offline", call, CREDS)[0], "ok")
                self.assertEqual(self.calls["token"], 2)
                self.assertEqual(self.calls["message"], 1)

    def test_ambiguous_message_results_never_retry(self):
        for response in (TimeoutError("response lost"), (502, {"code": 0}), (200, None),
                         (None, {"code": 0})):
            with self.subTest(response=response):
                call = self.transport([(200, {"code": 0, "tenant_access_token": "fake"})], response)
                self.assertEqual(notify.send("offline", call, CREDS)[0], "unknown")
                self.assertEqual(self.calls["message"], 1)

    def test_cli_outbox_and_exit_codes_without_real_config(self):
        for scenario, expected in (("ok", 0), ("fail", 1), ("net", 3), ("token_rej", 2)):
            with self.subTest(scenario=scenario):
                outbox = self.root / (scenario + ".md")
                notify._mock_reset()
                rc = notify.main(["--text", "offline original", "--mock", scenario, "--outbox", str(outbox)])
                self.assertEqual(rc, expected)
                self.assertLessEqual(notify.MOCK_STATS["msg_posts"], 1)
                if expected in (1, 3):
                    saved = outbox.read_text()
                    self.assertIn("offline original", saved)
                    self.assertIn("uuid", saved)
                    if expected == 3:
                        self.assertIn("人工", saved.replace("手动", "人工"))
                        self.assertIn("unknown", saved)
                else:
                    self.assertFalse(outbox.exists())

    def test_http_error_retains_status_even_if_body_says_success(self):
        error = urllib.error.HTTPError("https://example.invalid", 502, "gateway", {},
                                       io.BytesIO(b'{"code": 0}'))
        with patch("urllib.request.urlopen", side_effect=error):
            self.assertEqual(notify._real_transport("https://example.invalid", {}, {}), (502, {"code": 0}))

    def test_outbox_write_failure_preserves_unknown_exit_code(self):
        notify._mock_reset()
        with patch.object(notify, "_save_outbox", side_effect=OSError("disk full")):
            self.assertEqual(notify.main(["--text", "offline", "--mock", "net"]), 3)
        self.assertEqual(notify.MOCK_STATS["msg_posts"], 1)

    def test_incomplete_config_exits_cleanly_without_sending(self):
        notify.CFG.write_text(json.dumps({"channels": {"feishu": {"dms": {}}}}))
        self.assertEqual(notify.main(["--text", "offline"]), 2)

    def test_stable_request_id_reused_without_duplicate_post_in_one_call(self):
        call = self.transport([(200, {"code": 0, "tenant_access_token": "fake"})],
                              TimeoutError("response lost"))
        for text in ("same", "same", "different"):
            self.assertEqual(notify.send(text, call, CREDS)[0], "unknown")
        a, b, c = self.calls["uuids"]
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertLessEqual(len(a), 50)
        self.assertEqual(self.calls["message"], 3)


if __name__ == "__main__":
    unittest.main()
