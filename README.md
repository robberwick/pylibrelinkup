# pylibrelinkup

`pylibrelinkup` is a Python client for the LibreLinkUp API, which allows you to interact with the LibreLinkUp service to retrieve glucose data and other related information. This project is a Python implementation inspired by the [libre-link-up-api-client](https://github.com/DiaKEM/libre-link-up-api-client) project.

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

Retrieve patient data using the `read` method:

```python
patient = patient_list[0]
patient_data = client.read(patient_identifier=patient.patient_id)
```

The `read` method accepts a `patient_identifier` parameter in the form of a `UUID`, `str`, or `Patient` object.

Get the latest glucose data:

```python
latest_glucose = patient_data.current
print(latest_glucose)
```

Get the historical glucose data:

```python
historical_glucose = patient_data.history
print(historical_glucose)
```

full example:

```python
from pylibrelinkup import PyLibreLinkUp

client = PyLibreLinkUp(email='your_username', password='your_password')
client.authenticate()
patient_list = client.get_patients()
print(patient_list)
patient = patient_list[0]
patient_data = client.read(patient_identifier=patient.patient_id)
print(f"Current glucose: {patient_data.current}")
print(f"Historical glucose: {patient_data.history}")
```