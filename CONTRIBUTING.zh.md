# 参与贡献

中文 · [English](CONTRIBUTING.md)

发现了 bug，有个想法，或者想改点什么？这一页告诉你怎么做，几分钟就能读完。Camomile（洋甘菊）是给不写代码的人用的，所以一句说得清楚的话，和一个能用的补丁一样有价值。

**维护者：** Cota。**在哪儿聊：** 仓库的 Issue（问题反馈页），在 [GitHub](https://github.com/xcota/pos/issues) 或者 [Gitee](https://gitee.com/cotya/pos-starter/issues) 上都行，哪个能打开用哪个。没有别的联系渠道（没有邮箱，也没有聊天群）。用中文、English 或者 Русский 写都可以。

## 反馈问题

新建一个 Issue（在 GitHub 上选“Bug report”），把下面这些写清楚：

- **你的电脑：** Mac 还是 Linux，系统是什么版本（Mac 上：屏幕左上角的苹果图标 →“关于本机”）。
- **Claude Code 的版本：** 在终端（输入命令的那个窗口）里打 `claude --version`。
- **操作步骤：** 从打开文件夹开始，你打了什么字、点了什么，按先后顺序写。
- **你原本期望的结果**，和**实际发生的结果**。出现了报错，就把报错那几行原样复制过来。
- 只有问题跟“按意思搜索”或者“保存”有关时，才需要再附上 `python3 --version` 和 `git --version` 的输出。

**请不要贴出或上传你的个人记录。** 存着你记录的那些文件夹（`daily/`、`knowledge/`、`memory/`、`state/`、`reports/`、`inbox/`），还有 `HOME.md`、`MEMORY.md`、`context/identity.md` 这几个文件，都是私人的，而 Issue 是公开的。用你自己的话把问题讲清楚就行；如果某一行记录确实关键，先把里面的名字和细节换成占位符（比如“某某”），再贴。

## 提改进建议

新建一个 Issue（在 GitHub 上选“Feature request”）。先说**你遇到的问题**，别急着说办法：你当时在做什么，什么地方卡住了，还有谁可能会碰到。然后再写你的想法（有的话）。

符合下面几条的想法最容易被接受，因为这几条是 README 对使用者的承诺：

- 所有东西都是存在使用者自己硬盘上的普通文件——没有账号，也没有我们的服务器；
- 不瞒着使用者做任何事——要动手之前，助手先问一声；
- 用大白话说就能办成，不用学术语，也不用背命令；
- Claude Code 仍然是使用者唯一要付钱的东西。

不符合其中某一条的想法也可以聊，在 Issue 里把理由说明白就行。

## 提交 PR（Pull Request，把你改好的东西交给我们看）

错别字、小问题，直接提 PR 就行。大一点的改动，请先开一个 Issue 说一声，咱们先对一下方向，免得你白费功夫。

1. Fork（在你自己的账号下复制一份）仓库，在一个新分支上改，然后向 `main` 分支提 PR。
2. **改动要小：** 一个 PR 只做一件事。不相干的修改，分成几个 PR。
3. **助手自己读的文件（引擎）用英文写：** `CLAUDE.md`、`AGENTS.md`、`.claude/`（里面的技能 skills 和钩子 hooks）、`rules/`、`context/`、`scripts/`、`modules/`、`_templates/`。助手对使用者说话时用的是使用者自己的语言，那是它自己会处理的事。`AGENTS.md` 是给 Claude Code 以外的 AI 程序看的另一张说明书，靠人手动跟 `CLAUDE.md` 保持一致：你改了其中一个里的规矩，请看一眼另一个。
4. **给人看的文字有三种语言**——英文、中文、俄文：`README.md`、`README.zh.md`、`docs/ru/README.md`，以及 `docs/en/`、`docs/zh/`、`docs/ru/` 里的 `.md` 文件。你只改了其中一种语言也行，不用自己去翻译，但请在 PR 里写明：其他语言的哪些文件还需要做同样的修改。只改 `.md` 就行，`docs/` 里的网页（`.html`）由维护者重新生成。
5. **文件名**只用 `a-z`、`0-9`、`_` 和 `-`（见 `rules/naming-convention.md`）。
6. **别带任何个人信息：** 真实的个人记录、姓名、邮箱、你电脑上的路径，文件里、提交说明里、截图里都不要有。

提 PR 之前，在文件夹的根目录运行这两项检查：

```bash
python3 scripts/vault_sensors.py
for f in .claude/hooks/*.sh; do bash -n "$f" || echo "syntax error: $f"; done
```

第一项只会报告情况（退出码永远是 0），所以要自己看它打印了什么：开工前跑一次，改完再跑一次，确认你的改动没有让输出多出新的提示。第二项在所有钩子都没问题时什么也不打印；如果你还改了别的 `.sh` 文件，也用 `bash -n` 检查一下。

**往哪儿提：** GitHub 的 `main` 分支。Gitee 上的仓库是镜像：它的 `master` 分支在维护者每次发布时都会由 `main` 重新生成，所以直接在 Gitee 上合并的改动会被覆盖。在 Gitee 上提 PR 也欢迎——被采纳的改动，维护者会手动合进 `main`。

维护者有空时会看 PR，也许会请你再改改；合并哪些，由维护者决定。

## 你提交内容的许可

Camomile 使用 [AGPL-3.0](LICENSE) 许可。你提交的内容，也按同一个许可发布。请只提交你自己写的，或者你有权按这个许可发布的东西。

## 在哪儿聊

Issue 是唯一的地方——[GitHub](https://github.com/xcota/pos/issues) 或者 [Gitee](https://gitee.com/cotya/pos-starter/issues)：反馈 bug、提想法、问怎么用 Camomile（[使用说明](docs/zh/guide.md)能回答大部分问题）、问某个 PR 的事，都在这儿。维护者 Cota 有空就回，不承诺多久回复。
