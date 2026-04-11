from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None

def init_db(database_url: str) -> None:
	global _engine, _session_factory
	_engine = create_async_engine(database_url)
	_session_factory = async_sessionmaker(bind=_engine)

def get_engine() -> AsyncEngine:
	if _engine is None:
		raise RuntimeError("Database engine is not initialized")
	return _engine

def get_session_factory() -> async_sessionmaker[AsyncSession]:
	if _session_factory is None:
		raise RuntimeError("Session factory is not initialized")
	return _session_factory

async def dispose_db() -> None:
	global _engine, _session_factory

	if _engine is not None:
		await _engine.dispose()

	_engine = None
	_session_factory = None