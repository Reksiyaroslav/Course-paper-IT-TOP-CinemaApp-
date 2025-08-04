async def get_service(service_type, repo_class, async_session):
    repo = repo_class(async_session)
    return service_type(repo)
