# Usage: make NOTEBOOK_DIR='../notebooks' ARTIFACT_DIR='../output'
# Only PDFs are published at ARTIFACT_DIR's top level. All intermediate files,
# including minted caches and temporary files, live in .nbconvert/<name>-<source-id>/.
NOTEBOOK_DIR ?=
ARTIFACT_DIR ?=
CONVERTER_MAKEFILE := $(abspath $(lastword $(MAKEFILE_LIST)))
CONVERTER_DIR := $(dir $(CONVERTER_MAKEFILE))
PYTHON ?= $(if $(wildcard $(CONVERTER_DIR).venv/bin/python),$(CONVERTER_DIR).venv/bin/python,python3)
export NOTEBOOK_DIR ARTIFACT_DIR CONVERTER_MAKEFILE
export PYTHONDONTWRITEBYTECODE := 1

.DEFAULT_GOAL := all
.PHONY: all clean
.NOTPARALLEL:

# Keep orchestration here so paths with spaces do not become Make word lists.
# subprocess argument lists also keep notebook names out of shell commands.
define CONVERT_NOTEBOOKS
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    source = Path(os.environ['NOTEBOOK_DIR']).resolve()
    output_arg = os.environ.get('ARTIFACT_DIR', '')
    if not output_arg.strip():
        raise ValueError('ARTIFACT_DIR is required')
    output = Path(output_arg).resolve()
    if source == output:
        raise ValueError('ARTIFACT_DIR must differ from NOTEBOOK_DIR')
    if not source.is_dir():
        raise ValueError('NOTEBOOK_DIR is not a directory: ' + str(source))
    notebooks = sorted(p for p in source.glob('*.ipynb') if p.is_file())
    if not notebooks:
        raise ValueError('No *.ipynb files in NOTEBOOK_DIR: ' + str(source))

    makefile = Path(os.environ['CONVERTER_MAKEFILE']).resolve()
    project = makefile.parent
    rc = project / 'latexmkrc'
    templates = project / 'share' / 'templates'
    dependencies = [makefile, rc, *[p for p in templates.rglob('*') if p.is_file()]]
    env = os.environ.copy()
    env['PYTHONPATH'] = str(project) + os.pathsep + env.get('PYTHONPATH', '')
    # The trailing separator retains TeX's standard search path.
    for variable in ('TEXINPUTS', 'BIBINPUTS', 'BSTINPUTS'):
        env[variable] = '.' + os.pathsep + str(source) + os.pathsep + env.get(variable, '')
    build_root = output / '.nbconvert'

    for notebook in notebooks:
        identifier = hashlib.sha256(os.fsencode(notebook)).hexdigest()
        work = build_root / f'{notebook.stem}-{identifier}'
        pdf = output / (notebook.stem + '.pdf')
        if sys.argv[1] == 'clean':
            if work.exists():
                shutil.rmtree(work)
                print('Cleaned: ' + notebook.name, flush=True)
            continue

        work.mkdir(parents=True, exist_ok=True)
        temporary = work / '.tmp'
        temporary.mkdir(exist_ok=True)
        job_env = dict(env, TMPDIR=str(temporary), TMP=str(temporary), TEMP=str(temporary))
        tex = work / 'document.tex'
        exported = work / '.exported'
        try:
            regenerate = (not tex.exists() or not exported.exists() or
                          any(p.stat().st_mtime_ns > exported.stat().st_mtime_ns
                              for p in [notebook, *dependencies]))
            if regenerate:
                exported.unlink(missing_ok=True)
                print('Converting: ' + notebook.name, flush=True)
                subprocess.run([
                    sys.executable, '-m', 'nbconvert', '--to', 'latex_minted',
                    '--template', 'latex_minted',
                    '--TemplateExporter.extra_template_basedirs=' + str(templates),
                    '--output-dir=.', '--output=document', str(notebook),
                ], cwd=work, env=job_env, check=True)
                content = tex.read_text(encoding='utf-8')
                original = r'\documentclass[11pt,dvipdfmx]{jsarticle}'
                if original not in content:
                    raise ValueError('Expected jsarticle declaration missing: ' + str(tex))
                tex.write_text(content.replace(
                    original, r'\documentclass[uplatex,dvipdfmx,tombow]{jsbook}', 1
                ), encoding='utf-8')
                exported.touch()

            # latexmk also checks referenced images and bibliography dependencies.
            subprocess.run([
                'latexmk', '-norc', '-r', str(rc), '-pdfdvi',
                '-e', '$$dvipdf = "dvipdfmx -p 260mm,348mm %O -o %D %S";',
                *(['-g'] if regenerate else []), 'document.tex',
            ], cwd=work, env=job_env, check=True)
            built_pdf = work / 'document.pdf'
            if not pdf.exists() or built_pdf.stat().st_mtime_ns > pdf.stat().st_mtime_ns:
                shutil.copy2(built_pdf, pdf)
            print('PDF: ' + str(pdf), flush=True)
        except BaseException:
            # A failed build must be retried even if an intermediate PDF exists.
            exported.unlink(missing_ok=True)
            pdf.unlink(missing_ok=True)
            raise

    if sys.argv[1] == 'clean' and build_root.is_dir() and not any(build_root.iterdir()):
        build_root.rmdir()


try:
    main()
except (ValueError, OSError, subprocess.CalledProcessError) as error:
    print('Error: ' + str(error), file=sys.stderr)
    sys.exit(1)
endef
export CONVERT_NOTEBOOKS

all clean:
	@"$(PYTHON)" -c "$$CONVERT_NOTEBOOKS" "$@"
