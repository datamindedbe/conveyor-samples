from openaq.jobs import entrypoint


@entrypoint(name="job1")
def job1():
    pass


@entrypoint(name="job2")
def job2():
    pass


def test_jobs_in_scope_can_be_discovered():
    jobs = entrypoint.all
    assert len(jobs) == 2
