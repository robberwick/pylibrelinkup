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
from pylibrelinkup.client import LibreLinkUpClient

client = LibreLinkUpClient(username='your_username', password='your_password')
client.authenticate()
```

### Getting Patient List

You can fetch the patient list using the `get_patient_list` method:

```python
patient_list = client.get_patient_list()
print(patient_list)
```

### Getting Patient data

Retrieve patient data using the `read` method:

```python
patient = client.get_patient_list()[0]
patient_data = client.read(patient_id=patient.patient_id)
```

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
