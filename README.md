# Vendia Python Tools

>This package has python utilities that are useful when interacting with [Vendia Universal Application (Uni)](https://www.vendia.net/docs/share/dev-and-use-unis) data.

[![PyPI Version][pypi-image]][pypi-url]
[![Build Status][build-image]][build-url]
[![Code Coverage][coverage-image]][coverage-url]

## Blocks

A **block** is a ledger entry which contains, in addition to its transactions, three additional pieces of metadata:

* A link to the previous entry

* A copy of the previous entry's content hash

* A content hash that includes (1) and (2)

These additional items are what make a block more than just a log entry - they ensure that the block and its history are also tamperproof, because any change to any portion of the history will cause one or more of the hashes to be invalid.

Vendia supports the following block notification types:

* Real-time block notifications: Emitted when the node commits a new block. Includes a summary of the transactions included in the block.

* Dead-letter notifications: Emitted when an asynchronous transaction cannot be committed within the retry policy. Includes the full details of the original transaction.

A new block notification is emitted when data in a node has changed.  Data could have been created, updated, or deleted.  Block reports can be sent to an outbound integration:

* HTTPS webhooks

* AWS Lambda functions

* AWS SQS queues

* Email addresses

The block report includes information about the block, including the **BlockId**, **BlockHash**, ****, but it does not include the full list of mutations that were included in the block transaction list.  Users must query the Uni to get this information.

[pypi-image]: https://img.shields.io/pypi/v/vendia-python-tools
[pypi-url]: https://pypi.org/project/vendia-python-tools/
[build-image]: https://github.com/vendia/vendia-python-tools/actions/workflows/build.yml/badge.svg
[build-url]: https://github.com/vendia/vendia-python-tools/actions/workflows/build.yml
[coverage-image]: https://codecov.io/gh/vendia/vendia-python-tools/branch/main/graph/badge.svg
[coverage-url]: https://codecov.io/gh/vendia/vendia-python-tools