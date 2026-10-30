# 既存の jsarticle / jsbook 文書用: upLaTeX → DVI → dvipdfmx → PDF。
# 実行例: latexmk document.tex（-pdf は pdfLaTeX を選ぶため指定しない）。
# LuaLaTeX への移行には、文書クラスやパッケージの対応も必要。
$pdf_mode = 3;

# %O: latexmk が渡すオプション、%S: 入力ファイル。
# このプロジェクトの minted を使う既存文書に合わせて shell-escape を有効化。
$latex = 'uplatex -kanji=utf8 -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error -shell-escape %O %S';

# UTF-8 の日本語文献と索引。%B: 拡張子を除いた入力名、%D: 出力ファイル。
$bibtex = 'upbibtex -kanji=utf8 %O %B';
$makeindex = 'mendex -U %O -o %D %S';
$dvipdf = 'dvipdfmx %O -o %D %S';
