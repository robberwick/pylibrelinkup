Usage
=====

.. toctree::
   :maxdepth: 2


.. code-block:: python
   :linenos:


    # import the PyLibreLinkUp class
    from pylibrelinkup import PyLibreLinkUp

    # create a new PyLibreLinkUp client
    client = PyLibreLinkUp(email='your_username', password='your_password')

    # authenticate the client
    client.authenticate()

    # get a list of patients
    patient_list = client.get_patients()
    print(patient_list)

    # get the first patient in the list
    patient = patient_list[0]

    # get the latest data for the patient
    print(f"latest: {client.latest(patient_identifier=patient)}")

    # get the graph and logbook data for that patient
    graph_data = client.graph(patient_identifier=patient)
    print(f"graph data ({len(graph_data)} measurements):")
    for measurement in graph_data:
        print(f"{measurement.value} {measurement.timestamp} {measurement.factory_timestamp}")

    # get the logbook data for the patient
    logbook_data = client.logbook(patient_identifier=patient)
    print(f"logbook data: ({len(logbook_data)} entries)")
    for measurement in logbook_data:
        print(f"{measurement.value} {measurement.timestamp} {measurement.factory_timestamp}")


Regional redirects
------------------

Accounts are stored on a regional LibreLinkUp server. If you log in on the wrong one, ``authenticate()``
raises ``RedirectError``. Retry with a new client pointing at ``exc.api_url``:

.. code-block:: python

    from pylibrelinkup import PyLibreLinkUp, RedirectError

    client = PyLibreLinkUp(email='your_username', password='your_password')
    try:
        client.authenticate()
    except RedirectError as exc:
        client = PyLibreLinkUp(email='your_username', password='your_password', api_url=exc.api_url)
        client.authenticate()

The host is looked up in the regional map published by the LibreLinkUp API, falling back to the ``APIUrl``
enum. ``exc.region`` still holds the matching ``APIUrl`` value for backwards compatibility, but may be
``None`` for regions without an ``APIUrl`` member, so prefer ``exc.api_url``.
