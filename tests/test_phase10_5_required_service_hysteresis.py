from __future__ import annotations

from app.startup.models import ComponentStatus
from app.startup.supervisor import ApplicationSupervisor


def make_supervisor(results):
    supervisor = object.__new__(
        ApplicationSupervisor
    )

    supervisor.snapshot = type(
        "Snapshot",
        (),
        {
            "components": {
                "analyzer": ComponentStatus(
                    "analyzer",
                    True,
                    "ready",
                ),
                "frontend": ComponentStatus(
                    "frontend",
                    True,
                    "ready",
                ),
            },
        },
    )()

    supervisor.required_service_health = (
        lambda: results.pop(0)
    )

    supervisor.save = lambda: None

    return supervisor


def test_one_failure_does_not_stop_application():
    supervisor = make_supervisor([
        {
            "analyzer": False,
            "frontend": True,
        },
    ])

    counts = {
        "analyzer": 0,
        "frontend": 0,
    }

    failed = (
        supervisor.update_required_service_health(
            counts,
        )
    )

    assert failed is None
    assert counts["analyzer"] == 1

    analyzer = (
        supervisor.snapshot.components["analyzer"]
    )

    assert analyzer.state == "checking"


def test_success_resets_failure_count():
    supervisor = make_supervisor([
        {
            "analyzer": False,
            "frontend": True,
        },
        {
            "analyzer": True,
            "frontend": True,
        },
    ])

    counts = {
        "analyzer": 0,
        "frontend": 0,
    }

    supervisor.update_required_service_health(
        counts,
    )

    failed = (
        supervisor.update_required_service_health(
            counts,
        )
    )

    assert failed is None
    assert counts["analyzer"] == 0

    analyzer = (
        supervisor.snapshot.components["analyzer"]
    )

    assert analyzer.state == "ready"


def test_three_failures_identify_analyzer():
    supervisor = make_supervisor([
        {
            "analyzer": False,
            "frontend": True,
        },
        {
            "analyzer": False,
            "frontend": True,
        },
        {
            "analyzer": False,
            "frontend": True,
        },
    ])

    counts = {
        "analyzer": 0,
        "frontend": 0,
    }

    assert (
        supervisor.update_required_service_health(
            counts,
        )
        is None
    )

    assert (
        supervisor.update_required_service_health(
            counts,
        )
        is None
    )

    assert (
        supervisor.update_required_service_health(
            counts,
        )
        == "analyzer"
    )


def test_frontend_failure_is_not_reported_as_analyzer():
    supervisor = make_supervisor([
        {
            "analyzer": True,
            "frontend": False,
        },
        {
            "analyzer": True,
            "frontend": False,
        },
        {
            "analyzer": True,
            "frontend": False,
        },
    ])

    counts = {
        "analyzer": 0,
        "frontend": 0,
    }

    supervisor.update_required_service_health(
        counts,
    )

    supervisor.update_required_service_health(
        counts,
    )

    assert (
        supervisor.update_required_service_health(
            counts,
        )
        == "frontend"
    )
