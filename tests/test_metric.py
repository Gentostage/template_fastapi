from tests.factories.metrics import MetricFactory


async def test_create_metric(api_client):
    metric_data = {
        "service_name": "TestService",
        "path": "/test",
        "response_time_ms": 100,
    }
    response = await api_client.post("/metrics", json=metric_data)
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "service_name": "TestService",
        "path": "/test",
        "response_time_ms": 100,
    }


async def test_get_metrics(api_client, db):
    await MetricFactory.build_and_save(session=db, service_name="ServiceA", path="/path1", response_time_ms=100)
    await MetricFactory.build_and_save(session=db, service_name="ServiceA", path="/path1", response_time_ms=250)
    await MetricFactory.build_and_save(session=db, service_name="ServiceA", path="/path1", response_time_ms=250)

    await MetricFactory.build_and_save(session=db, service_name="ServiceB", path="/path3", response_time_ms=250)

    response = await api_client.get("/metrics/ServiceA")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["path"] == "/path1"
    assert data[0]["average"] == 200
    assert data[0]["min"] == 100
    assert data[0]["max"] == 250
