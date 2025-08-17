from db_semantic_layer.core.engine_manager import EngineManager

def test_engine_manager_sqlite():
	mgr = EngineManager()
	mgr.create("mem", "sqlite+pysqlite:///:memory:")
	assert "mem" in mgr.list()
	assert mgr.healthcheck("mem")