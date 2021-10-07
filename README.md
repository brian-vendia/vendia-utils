# vendia-utils

This package has utility modules that are useful when interacting with [Vendia Universal Application (Uni)](https://www.vendia.net/docs/share/dev-and-use-unis) data.

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

The block report includes information about the block, including the **BlockId**, and **BlockHash** but it does not include the full list of mutations that were included in the block transaction list.  Users must query the Uni to get this information.

The `vendia-utils` module makes it easier to query block data and turn it into structured data.

### Input and Output of MutationVisitor.parse_mutation() Method

#### Input

```bash
data = list(MutationVisitor.parse_mutations(['addComponentDemand(id:"017c5074-f6a3-2814-7e20-f08d6e5f47fb",input: {assembledComponentId: "123", assembledComponentName: "thing", ford6MonthDemandForecast: 35, ford6WeekDemandForecast: 30, recordDate: "2021-10-04"}){error}']))
```

#### Output

```bash
[{'operation': 'add', '__typename': 'ComponentDemand', 'arguments': {'id': '017c4c8e-5cfe-f887-9f0f-619242d23e73', 'input': {'assembledComponentId': '123', 'assembledComponentName': 'thing', 'ford6MonthDemandForecast': 17, 'ford6WeekDemandForecast': 12, 'recordDate': '2021-10-04'}}}]
```
