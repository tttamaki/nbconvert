# Makefileの使い方

このプロジェクトをコンバータとして使い、別フォルダで作成したJupyter NotebookをPDFに変換します。`NOTEBOOK_DIR` 直下の `*.ipynb` がすべて対象です。ファイル名の指定は不要で、サブフォルダ内のNotebookは対象外です。

コンパイルには、このプロジェクトの `latexmkrc` を読み込んだ `latexmk` を使い、upLaTeXとdvipdfmxでPDFを生成します。Notebookのセルは実行せず、保存済みの出力を変換します。

## 必要なツール

- `make`
- Python 3と、このプロジェクトのnbconvertが必要とする依存パッケージ
- `pandoc`（Markdownの変換用）
- TeX環境：`latexmk`、`uplatex`、`dvipdfmx`、`upbibtex`、`mendex`、`minted`などの必要なパッケージ
- mintedの外部処理に必要なツール（利用するmintedのバージョンに対応する `latexminted` やPygmentsなど）

Pythonはプロジェクト内の `.venv/bin/python` があれば優先して使い、なければ `python3` を使います。別のPython環境を使う場合は `PYTHON='/path/to/python'` をmakeの引数に追加します。変換にはこのプロジェクトのコードと `share/templates` 内の `latex_minted` テンプレートを使います。

## PDFを作成する

プロジェクトのルートフォルダで、Notebookのあるフォルダと生成先を指定します。

```sh
make NOTEBOOK_DIR='../notebooks' ARTIFACT_DIR='../output'
```

| 変数 | 意味 |
| --- | --- |
| `NOTEBOOK_DIR` | 入力Notebookのフォルダ。Makefile上の既定値は空で、省略時はmakeを実行したカレントディレクトリを使います。 |
| `ARTIFACT_DIR` | PDFと中間生成物の保存先。Makefile上の既定値は空のため指定必須です。入力フォルダと同じ場所は指定できません。存在しなければ作成します。 |

どちらも相対パス・絶対パスを指定できます。相対パスはmakeを実行したカレントディレクトリが基準です。末尾の `/` は省略できます。空白を含むパスは引用符で囲みます。

```sh
make NOTEBOOK_DIR='../日本語のノート' ARTIFACT_DIR='../PDF 出力'
```

カレントディレクトリのNotebookを変換する場合も、生成先は指定します。

```sh
make ARTIFACT_DIR='../output'
```

Notebookのあるフォルダから実行する場合は、`-f` でこのプロジェクトのMakefileを指定できます。

```sh
make -f /path/to/nbconvert/Makefile ARTIFACT_DIR='../output'
```

`ARTIFACT_DIR` の未指定、入力と生成先が同じ場所、入力フォルダが存在しない場合、対象のNotebookが0件の場合はエラーになります。

## 生成物の保存先

完成したPDFは `ARTIFACT_DIR/<Notebook名>.pdf` に保存します。中間生成物は、同じ生成先の隠しフォルダ `.nbconvert/` 以下にNotebookごとに分けて保存します。

```text
notebooks/
  chapter1.ipynb
  chapter2.ipynb
  image.png
output/
  chapter1.pdf
  chapter2.pdf
  .nbconvert/
    <Notebookのbasename>-<Notebookのパスから算出したID>/
      document.tex
      document.aux
      document.dvi
      document.log
      document.synctex.gz
      document.fls
      document.fdb_latexmk
      document.pdf
      document_files/
      _minted/
      .tmp/
      ...
```

画像リソース、mintedのキャッシュ・補助ファイル、一時ファイルもこの中に作成します。入力Notebookと元画像は変更しません。Notebook内の相対パス画像は、入力フォルダを基準に参照します。

再実行時はNotebook、Makefile、`latexmkrc`、テンプレートの更新を確認します。参照画像などの変更はlatexmkが確認し、必要な処理を再実行します。コンパイルに失敗すると、その時点で処理を停止します。失敗したNotebookの生成先直下のPDFは削除され、次回実行時に再変換します。

## 中間ファイルを削除する

変換時と同じ入力フォルダ・生成先を指定して実行します。

```sh
make clean NOTEBOOK_DIR='../notebooks' ARTIFACT_DIR='../output'
```

`clean` は、現在の入力フォルダにあるNotebookに対応する `.nbconvert/<Notebookのbasename>-<ID>/` を削除します。LaTeXの中間ファイル、抽出画像、mintedキャッシュ、一時ファイルが削除されます。生成先直下のPDF、元Notebook、元画像、その他のファイルは保持します。

入力Notebookを移動・削除した場合、そのNotebookに対応する以前の中間フォルダは `clean` の対象外です。
