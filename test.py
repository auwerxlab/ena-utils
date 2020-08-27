import os
import click
import pandas as pd
from click.testing import CliRunner
import pytest
import gzip
from ena_utils.__main__ import cli

# Requires the ENA_UTILS_USER and ENA_UTILS_PASSWORD environment variables
# Run the tests with `$ pytest test.py -s`

@pytest.mark.parametrize('test_input',
  ['study-table', 'run-table', 'experiment-table', 'sample-table'])
def test_template(test_input):
  runner = CliRunner()
  test_fp = 'tmp/test.txt'
  cmd = ['write-template',
    test_input,
    '-t', test_fp,
    '-v']
  result = runner.invoke(cli, cmd)
  print('command: ' + ' '.join(cmd))
  print('output: ' + result.output)
  assert result.exit_code == 0
  assert os.path.exists(test_fp)
  os.remove(test_fp)
  assert 'Template table writen to ' + test_fp in result.output

# def test_upload():
#   runner = CliRunner()
#   test_fp = 'tmp/test.txt'
#   open(test_fp, 'a')
#   cmd = ['upload',
#     '--user', os.environ['ENA_UTILS_USER'],
#     '--password', os.environ['ENA_UTILS_PASSWORD'],
#     '--file_path', test_fp,
#     '-v']
#   result = runner.invoke(cli, cmd)
#   print('command: ' + ' '.join(cmd))
#   print('output: ' + result.output)
#   assert result.exit_code == 0
#   assert 'Transfer complete' in result.output

@pytest.mark.parametrize('test_input',
  [['study',
  '-a', 'test_alias',
  '-t', 'Test project.',
  '-d', 'Test description.',
  '--study_xml', 'tmp/test_project.xml'],
  ['experiment',
  '--study', 'test_study',
  '--sample', 'test_sample',
  '--alias', 'test_alias',
  '--center', 'test_center',
  '--title', 'Test title.',
  '--design', 'Test design.',
  '--lib_name', 'test_lib_name',
  '--lib_strategy', 'AMPLICON',
  '--lib_source', 'METAGENOMIC',
  '--lib_selection', 'PCR',
  '--lib_length', '311',
  '--lib_protocol', 'Test lib protocol.',
  '--instrument', 'Illumina MiSeq',
  '--experiment_xml', 'tmp/test_experiment.xml'
  ],
  ['run',
  '--experiment', 'test_experiment',
  '--alias', 'test_alias',
  '--center', 'test_center',
  '--filename', 'tmp/test_R1.fastq.gz,tmp/test_R2.fastq.gz',
  '--filetype', 'fastq,fastq',
  '--run_xml', 'tmp/test_run.xml'],
  ['sample',
  '--alias', 'test_alias',
  '--title', 'Test title.',
  '--taxon_id', '10090',
  '--scientific_name', 'Mus musculus',
  '--common_name', 'house mouse',
  '--attributes', '{"age":"2 weeks","strain":"C57BL/6"}',
  '--sample_xml', 'tmp/test_sample.xml']])
def test_submit(test_input):
  runner = CliRunner()
  for tf in ['tmp/test_R1.fastq.gz', 'tmp/test_R2.fastq.gz']:
    with gzip.open(tf, 'wb') as f:
      f.write('This is a test file.'.encode('utf-8'))
  cmd = ['submit',
    '--user', os.environ['ENA_UTILS_USER'],
    '--password', os.environ['ENA_UTILS_PASSWORD'],
    '--submission_xml', 'tmp/test_submission.xml'
    ]
  cmd.extend(test_input)
  cmd.append('-v')
  result = runner.invoke(cli, cmd)
  print('command: ' + ' '.join(cmd))
  print('output: ' + result.output)
  assert (
      'success="true"' in result.output
      and '<INFO>Submission has been committed.</INFO>' in result.output
    ) or (
      'success="false"' in result.output
      and any(e in result.output for e in [
        'The object being added already exists',
        'Failed to find referenced',
        'does not exist in the upload area'
        ])
    )

@pytest.mark.parametrize('test_input',
  ['study', 'experiment', 'run', 'sample'])
def test_submit_set(test_input):
  runner = CliRunner()
  # Create a table from template
  table_fp = 'tmp/' + test_input + '_table.txt'
  runner.invoke(cli, ['write-template',
    test_input + '-table',
    '-t', table_fp])
  if test_input == 'run':
    # Create mock files from table
    files_list = []
    for i, row in pd.read_table(table_fp).iterrows():
      files_list.extend(dict(row)['filename'].split(','))
    for tf in files_list:
      with gzip.open(tf, 'wb') as f:
        f.write('This is a test file.'.encode('utf-8'))
  cmd = ['submit',
    '--user', os.environ['ENA_UTILS_USER'],
    '--password', os.environ['ENA_UTILS_PASSWORD'],
    '--submission_xml', 'tmp/test_submission.xml',
    test_input + '-set',
    '--table', table_fp,
    '--' + test_input + '_xml', 'tmp/test_' + test_input + '.xml',
    '-v'
    ]
  result = runner.invoke(cli, cmd)
  print('command: ' + ' '.join(cmd))
  print('output: ' + result.output)
  assert (
      'success="true"' in result.output
      and '<INFO>Submission has been committed.</INFO>' in result.output
    ) or (
      'success="false"' in result.output
      and any(e in result.output for e in [
        'The object being added already exists',
        'Failed to find referenced',
        'does not exist in the upload area'
        ])
    )
