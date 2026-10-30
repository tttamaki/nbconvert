## Makefileのみで外部Notebookフォルダを変換する

### 方針

`kyoritsu.md` の `make`、`make NOTEBOOK_DIR=...`、`make clean` を維持します。変更は `Makefile` のみに限定し、`latexmkrc` とテンプレートは既存のものを使います。

### 実装

- Makefile自身の場所からプロジェクトの絶対パスを取得し、`NOTEBOOK_DIR` へ移動して内部ビルドを実行します。相対パス・絶対パス・末尾の `/`・空白を含む指定を扱います。
- 対象は従来どおり `sc1.ipynb`〜`sc7.ipynb`。内部ではファイル名だけをターゲットにし、Notebookごとの更新判定を維持します。
- Pythonはプロジェクトの `.venv/bin/python` があれば使用し、なければ `python3` を使用します。プロジェクトのコードを `PYTHONPATH`、`share/templates` をテンプレート検索先に明示し、外部フォルダからこのコンバータを利用できるようにします。Pythonのバイトコード生成も抑止します。
- nbconvertは `latex_minted` エクスポータを使い、出力先を作業フォルダに指定します。既存の `jsbook`・`uplatex`・`dvipdfmx`・`tombow` への置換を維持し、置換用のバックアップファイルは作りません。
- 直接の `uplatex`・`dvipdfmx` 呼び出しを `latexmk` に置き換えます。`-norc -r <プロジェクトのlatexmkrc絶対パス>` で設定を明示し、既存の用紙指定 `260mm,348mm` はMakefileからdvipdfmxのオプションとして引き継ぎます。
- `.tex`、画像リソース、LaTeXの中間ファイル、SyncTeX、latexmk管理ファイル、mintedのキャッシュ・補助ファイル、PDFはすべて `NOTEBOOK_DIR` 内に生成します。
- Notebook、Makefile、latexmkrc、使用テンプレートの更新を再生成条件にします。失敗時は後続処理を停止し、不完全なPDFを更新済みとして扱わせません。
- `clean` も同じフォルダで実行します。`latexmk -c` と生成物に限定した補完削除で中間ファイル・mintedキャッシュ・Notebookリソースを除去し、NotebookとPDFは保持します。

### 検証

- 一時フォルダに日本語、Pythonコード、画像出力、相対パス画像を含むNotebookを用意し、7冊の変換を確認します。
- 相対パス、絶対パス、末尾 `/`、空白・日本語を含むフォルダ名で実行します。未指定の `NOTEBOOK_DIR=.` も確認します。
- PDF・各種中間ファイル・minted生成物の保存先を確認し、プロジェクト側に変換生成物が増えないことを確認します。
- 再実行時の更新判定、Notebook・設定更新時の再生成、コンパイル失敗の伝播を確認します。
- `clean` 後にPDF・Notebook・利用者が置いた画像が残り、対象の生成物が削除されることを確認します。最後に変更差分がMakefileだけであることを確認します。

---

## 全Notebookの変換と生成先の分離

### 仕様

- 変更対象は `Makefile` のみ。既存の `latexmkrc`・テンプレート・説明ファイルは変更しません。
- `NOTEBOOK_DIR` 直下の `*.ipynb` をすべて変換します。サブフォルダは探索しません。
- `NOTEBOOK_DIR` は省略時 `.`。生成先 `ARTIFACT_DIR` は指定必須とし、未指定・入力フォルダと同一の場合はエラーにします。
- PDFも含むすべての変換生成物を `ARTIFACT_DIR` に保存します。

```sh
make NOTEBOOK_DIR='../notebooks' ARTIFACT_DIR='../output'
make clean NOTEBOOK_DIR='../notebooks' ARTIFACT_DIR='../output'
```

### 実装

- 両フォルダの相対パスをmake起動時の作業ディレクトリ基準で解決します。絶対パス、末尾 `/`、空白・日本語を含むパスに対応します。生成先がなければ作成します。
- Notebookはファイルとして存在するものを列挙し、0件なら明示的にエラーにします。固定の `sc1`〜`sc7` は廃止します。
- nbconvertとlatexmkの作業ディレクトリを生成先に統一します。`.tex`、抽出画像、`*_files/`、aux・dvi・log、SyncTeX、latexmk管理ファイル、mintedのキャッシュ・補助ファイル、PDFをそこに集約します。
- Pythonはプロジェクトの `.venv/bin/python` を優先し、なければ `python3` を使用します。プロジェクトのコードとテンプレートを絶対パスで参照し、Pythonのバイトコード生成を抑止します。
- `latex_minted` エクスポータを使い、既存の `jsbook`・`uplatex`・`dvipdfmx`・`tombow` への置換を維持します。Notebook内の相対画像参照は入力フォルダを基準に解決できるよう、TeXの検索パスにも入力フォルダを追加します。
- `latexmk -norc -r <プロジェクトのlatexmkrc絶対パス>` でコンパイルし、既存のdvipdfmxの用紙指定 `260mm,348mm` を維持します。
- Notebook、Makefile、latexmkrc、使用テンプレートの更新時に再生成します。変換は順次実行し、失敗時は停止して、不完全なPDFを更新済みとして扱いません。
- `clean` は生成先の対象Notebookに対応する中間ファイル・抽出リソース・minted生成物を削除します。PDF、元Notebook、元画像は保持します。生成先フォルダ自体の一括削除は行いません。

### 検証

- 任意名・空白・日本語を含む複数のNotebookが対象になり、サブフォルダ内のNotebookは対象外になることを確認します。
- 日本語、minted、埋め込み画像、入力フォルダにある相対パス画像を含むPDFを生成します。
- 入力・生成先の相対パス、絶対パス、末尾 `/`、空白・日本語を含む指定を確認します。
- 入力フォルダとプロジェクトに変換生成物が増えず、全生成物が指定先に収まることを確認します。
- 生成先未指定・入力先と同一・Notebookなし・コンパイル失敗のエラーを確認します。
- 更新判定と `clean` 後のPDF・元データの保持を確認し、変更差分がMakefileだけであることを検証します。
