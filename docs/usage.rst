File upload
-----------

The ``ena-utils upload`` command.

Uploading files to a Webin user file upload area is needed prior to files submission.
See the associated `ENA documentation <https://ena-docs.readthedocs.io/en/latest/submit/fileprep/upload.html>`_ for details.

:Example:

::

    $ ena-utils upload --file_path <path/to/sequences/files.gz>

Submissions
-----------

The ``ena-utils submit`` command.

The ``ena-utils submit`` command has specific sub-commands for each type of object:

- Study (ex: ``ena-utils submit study``)
- Sample (ex: ``ena-utils submit sample``)
- Experiment (ex: ``ena-utils submit experiment``)
- Run (ex: ``ena-utils submit run``)

In addition, all these sub-commands come in two flavors:

- Unique object submission (ex: ``ena-utils submit study``).
- Multiple objects submission using a submission file (ex: ``ena-utils submit study-set``).

The ``ena-utils submit`` sub-commands allow to define some submission metadata. The possible metadata fields and values are specified in the `ENA schema <https://ena-docs.readthedocs.io/en/latest/submit/general-guide/programmatic.html>`_ (also available in this documentation :ref:`here <ena_xml_schema>`). Check the sub-commands specific documentation to see which metadata fields are supported by your ``ena-utils`` version.

Template files for multiple objects submission can be created using the ``ena-utils create-template`` command, then edited to the specific needs of each submission.

By default, ``ena-utils submit`` sub-commands submit objects to the ENA test server (https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/).

Any data submission to ENA first requires the registration of a study object.
See the associated `ENA documentation <https://ena-docs.readthedocs.io/en/latest/submit/study.html>`_ for details.

:Example:

::

    $ ena-utils submit study -a <alias> test_alias -t <title> -d <description>



