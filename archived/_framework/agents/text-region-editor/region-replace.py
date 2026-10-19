#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""region-replace.py — 局部区域文本修改（标记模式）

框架组件 _framework/agents/text-region-editor/ 的配套脚本。
只改标记范围内的区域，区域外字节原样不动；任何参数错误都 fail-fast，绝不改动文件。

标记 = 行首匹配的唯一字符串（整行以该字符串开头）。新内容从 stdin 读入，
或用 --content-file 指定（优先级更高）；内容内部用 LF 换行即可，落盘时自动
转换为文件的 EOL（CRLF/LF 自动检测保留）。

用法示例：
  # 替换两标记之间的区域（两标记行保留）
  python region-replace.py --file qa.md \
      --from-marker "## Q11" --to-marker "## Q12" --replace < new.md

  # 连起点标记行一起替换（--include-to 同理）
  python region-replace.py --file qa.md \
      --from-marker "## Q11" --to-marker "## Q12" --include-from --replace < new.md

  # 在标记行之后插入一段内容（--insert-before 同理，插到标记行之前）
  python region-replace.py --file qa.md --insert-after "**来源**: 查资料" < add.md

  # 预览（只打印将改动的区域，不写盘）
  python region-replace.py --file qa.md \
      --from-marker "## Q11" --to-marker "## Q12" --dry-run

  # 防呆：区域行数与预期不符（如被并发修改）即失败、不改文件
  python region-replace.py --file qa.md \
      --from-marker "## Q11" --to-marker "## Q12" --expect-lines 23 --replace < new.md
"""
import argparse
import io
import sys


def _force_utf8():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def read_text(path):
    # newline=""：读入不翻译换行，保留 CRLF 供 EOL 检测
    with io.open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def load_content(args):
    if args.content_file:
        return read_text(args.content_file)
    if sys.stdin.isatty():
        fail("需要新内容：从 stdin 管道输入，或用 --content-file 指定")
    return sys.stdin.buffer.read().decode("utf-8")


def fail(msg):
    sys.stderr.write("region-replace: 错误: %s\n" % msg)
    sys.exit(1)


def find_marker(lines, marker, start, end):
    """在 [start, end) 内找行首匹配 marker 的行；缺失/不唯一即 fail。返回 0-based 行号。"""
    hits = [i for i in range(start, end) if lines[i].startswith(marker)]
    if not hits:
        fail("标记未找到: %r（行首匹配；文件共 %d 行）" % (marker, len(lines)))
    if len(hits) > 1:
        fail("标记不唯一: %r 命中 %d 行: %s"
             % (marker, len(hits), ", ".join(str(h + 1) for h in hits)))
    return hits[0]


def show_region(lines, start, end):
    for i in range(start, end):
        sys.stdout.write("  %5d | %s\n" % (i + 1, lines[i]))


def main():
    _force_utf8()
    ap = argparse.ArgumentParser(
        description="局部区域文本修改（标记模式，区域外字节不动）",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", required=True, help="目标文件路径")
    ap.add_argument("--from-marker", help="区域起点标记（行首匹配）")
    ap.add_argument("--to-marker", help="区域终点标记（行首匹配）")
    ap.add_argument("--replace", action="store_true",
                    help="替换模式：两标记之间的区域替换为新内容（stdin 或 --content-file）")
    ap.add_argument("--insert-after", metavar="MARKER", help="插入模式：在标记行之后插入新内容")
    ap.add_argument("--insert-before", metavar="MARKER", help="插入模式：在标记行之前插入新内容")
    ap.add_argument("--include-from", action="store_true", help="替换区域包含起点标记行")
    ap.add_argument("--include-to", action="store_true", help="替换区域包含终点标记行")
    ap.add_argument("--content-file", help="新内容文件（默认从 stdin 读）")
    ap.add_argument("--dry-run", action="store_true", help="只打印将改动的区域，不写盘")
    ap.add_argument("--expect-lines", type=int,
                    help="防呆：替换区域的行数必须与此值一致，否则 fail-fast 不改文件（仅 --replace）")
    args = ap.parse_args()

    text = read_text(args.file)
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = [l.rstrip("\r") for l in text.split("\n")]

    if (args.dry_run and not (args.replace or args.insert_after or args.insert_before)
            and args.from_marker and args.to_marker):
        args.replace = True  # dry-run 只带标记 = 预览替换区域

    modes = sum([args.replace,
                 args.insert_after is not None,
                 args.insert_before is not None])
    if modes != 1:
        fail("必须且只能指定一种模式：--replace / --insert-after / --insert-before")
    if args.replace and not (args.from_marker and args.to_marker):
        fail("--replace 需要同时给出 --from-marker 与 --to-marker")
    if (args.include_from or args.include_to) and not args.replace:
        fail("--include-from/--include-to 仅用于 --replace 模式")
    if args.expect_lines is not None and not args.replace:
        fail("--expect-lines 仅用于 --replace 模式")

    if args.replace:
        a = find_marker(lines, args.from_marker, 0, len(lines))
        b = find_marker(lines, args.to_marker, a + 1, len(lines))
        start = a if args.include_from else a + 1
        end = b + 1 if args.include_to else b
        if args.expect_lines is not None and (end - start) != args.expect_lines:
            fail("区域大小不符：预期 %d 行，实际 %d 行（第 %d–%d 行）——文件可能被并发修改，请重新核对标记与区域后重试"
                 % (args.expect_lines, end - start, start + 1, end))
        if args.dry_run:
            new_part = []
        else:
            content = load_content(args)
            # 空内容 = 删除区域（"" split 成 [""] 会留一个空行，需特殊处理）
            new_part = [] if content == "" else [l.rstrip("\r") for l in content.split("\n")]
        action = "替换"
        if start < end:
            span = "第 %d–%d 行" % (start + 1, end)
        else:
            span = "第 %d 行之后（区域为空，等效插入）" % start
    else:
        marker = args.insert_after if args.insert_after is not None else args.insert_before
        i = find_marker(lines, marker, 0, len(lines))
        new_part = [] if args.dry_run else [l.rstrip("\r") for l in load_content(args).split("\n")]
        # 插入模式：内容末尾的换行只是行终止符，不产生额外空行
        if new_part and new_part[-1] == "" and not args.dry_run:
            new_part.pop()
        action = "插入"
        if args.insert_after is not None:
            start, end = i + 1, i + 1
            span = "第 %d 行之后" % (i + 1)
        else:
            start, end = i, i
            span = "第 %d 行之前" % (i + 1)

    if args.dry_run:
        sys.stdout.write("region-replace: dry-run（未写盘）\n")
        sys.stdout.write("  文件: %s（%s，%d 行）\n"
                         % (args.file, "CRLF" if nl == "\r\n" else "LF", len(lines)))
        sys.stdout.write("  操作: %s %s\n" % (action, span))
        sys.stdout.write("  新内容: %s\n"
                         % ("（dry-run 不读 stdin）" if args.dry_run else "%d 行" % len(new_part)))
        sys.stdout.write("  将改动的区域：\n")
        show_region(lines, start, end)
        return

    out = lines[:start] + new_part + lines[end:]
    with io.open(args.file, "w", encoding="utf-8", newline="") as f:
        f.write(nl.join(out))
    sys.stdout.write("region-replace: OK — %s %s（%d 行 → %d 行，%s）\n"
                     % (action, span, len(lines), len(out), args.file))


if __name__ == "__main__":
    main()
