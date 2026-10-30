# Makefileの使い方

このMakefileは、`sc1.ipynb`から`sc7.ipynb`までのJupyter NotebookをPDFに変換します。PDFは各Notebookと同じフォルダに作成されます。

## 必要なツール

- Jupyterとnbconvert
- `latex_minted`テンプレート
- `uplatex`
- `dvipdfmx`

## PDFを作成する

Notebookがカレントディレクトリにある場合は、次のコマンドを実行します。

```sh
make
```

Notebookが別のフォルダにある場合は、`NOTEBOOK_DIR`にフォルダを指定します。

```sh
make NOTEBOOK_DIR='../somewhere/notebook_dir/'
```

`NOTEBOOK_DIR`には相対パスまたは絶対パスを指定できます。フォルダ内に`sc1.ipynb`から`sc7.ipynb`までのファイルが必要です。指定を省略すると、カレントディレクトリが使われます。

## 中間ファイルを削除する

```sh
make clean
```

別フォルダを指定して作成した中間ファイルを削除する場合も、作成時と同じ`NOTEBOOK_DIR`を指定します。

```sh
make NOTEBOOK_DIR='../somewhere/notebook_dir/' clean
```

`clean`はNotebookごとのLaTeXファイルやDVIファイルなどの中間ファイルと、Minted・Notebookリソースのフォルダを削除します。作成済みのPDFは削除しません。
