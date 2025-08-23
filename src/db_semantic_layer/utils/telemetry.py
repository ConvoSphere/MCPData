from __future__ import annotations

from ..core.config import settings

try:
	from opentelemetry import trace
	from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
	from opentelemetry.sdk.resources import Resource
	from opentelemetry.sdk.trace import TracerProvider
	from opentelemetry.sdk.trace.export import BatchSpanProcessor
	_OTEL_AVAILABLE = True
except Exception:  # pragma: no cover
	_OTEL_AVAILABLE = False


_initialized = False


def init_telemetry(service_name: str = "dbsl") -> None:
	global _initialized
	if _initialized:
		return
	if not settings.telemetry_enabled or not _OTEL_AVAILABLE:
		_initialized = True
		return
	endpoint = settings.otel_endpoint
	if not endpoint:
		_initialized = True
		return
	resource = Resource.create({"service.name": service_name})
	provider = TracerProvider(resource=resource)
	exporter = OTLPSpanExporter(endpoint=endpoint, insecure=True)
	processor = BatchSpanProcessor(exporter)
	provider.add_span_processor(processor)
	trace.set_tracer_provider(provider)
	_initialized = True