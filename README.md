# pylibrelinkup

`pylibrelinkup` is a Python client for the LibreLinkUp API, which allows you to interact with the LibreLinkUp service to retrieve glucose data and other related information. This project is a Python implementation inspired by the [libre-link-up-api-client](https://github.com/DiaKEM/libre-link-up-api-client) project.

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pylibrelinkup) ![PyPI - Version](https://img.shields.io/pypi/v/pylibrelinkup) ![PyPI - License](https://img.shields.io/pypi/l/pylibrelinkup) ![Read the Docs](https://img.shields.io/readthedocs/pylibrelinkup) ![PyPI - Downloads](https://img.shields.io/pypi/dm/pylibrelinkup) 




## Installation

To install `pylibrelinkup`, you can use `pip`:

```bash
pip install pylibrelinkup
```

## Usage

### Initialization

First, you need to import the necessary modules, initialize the client, and authenticate with your LibreLinkUp credentials:

```python
from pylibrelinkup import PyLibreLinkUp

client = PyLibreLinkUp(email='your_username', password='your_password')
client.authenticate()
```

### Getting Patient List

You can fetch the list of patients using the `get_patients` method:

```python
patient_list = client.get_patients()
print(patient_list)
```

### Getting Patient data

PyLibreLinkUp provides three methods to retrieve patient data: `current`, `graph`, and `logbook`. 

- The `current` method retrieves the most recent glucose measurement reported by the LLU api for a patient.
- The `graph` method retrieves the glucose measurements for the previous 12 hours which are used to display the recent history graph in the LLU app.
- The `logbook` method retrieves the glucose event data for approximately the last two weeks.

All three methods accept a `patient_identifier` parameter in the form of a `UUID`, `str`, or `Patient` object.

**Note:** The `read` method also exists as a way to retrieve both recent and latest patient data, but it is deprecated and will be removed in a future release. Use the `graph` method for retrieving graph data and `latest` to access the most recent glucose measurement.

#### Current Glucose:

```python
latest_glucose = client.latest(patient_identifier=patient_list[0])
print(latest_glucose)
```

#### Graph Data:

```python
graph_data = client.graph(patient_identifier=patient_list[0])
print(graph_data)
```


#### Logbook Data:

```python
logbook_data = client.logbook(patient_identifier=patient_list[0])
print(logbook_data)
```

full example:

```python
from pylibrelinkup import PyLibreLinkUp

client = PyLibreLinkUp(email='your_username', password='your_password')
client.authenticate()
patient_list = client.get_patients()
print(patient_list)
patient = patient_list[0]
print(f"latest: {client.latest(patient_identifier=patient)}")
graph_data = client.graph(patient_identifier=patient)
print(f"graph data ({len(graph_data)} measurements):")
for measurement in graph_data:
    print(f"{measurement.value} {measurement.timestamp} {measurement.factory_timestamp}")
logbook_data = client.logbook(patient_identifier=patient)
print(f"logbook data: ({len(logbook_data)} entries)")
for measurement in logbook_data:
    print(f"{measurement.value} {measurement.timestamp} {measurement.factory_timestamp}")
```

For full documentation, please refer to the [API documentation](https://pylibrelinkup.readthedocs.io/en/latest/).