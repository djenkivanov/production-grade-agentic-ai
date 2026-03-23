import os

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

OTLP_ENDPOINT = os.getenv("OTLP_TRACES_ENDPOINT", "http://localhost:4318/v1/traces")

def setup_tracing(service_name: str) -> None:
    resource = Resource.create({
        "service.name": service_name,
        "service.version": "1.0.0",
        "deployment.environment": os.getenv("ENV", "dev")
    })
    
    provider = TracerProvider(resource=resource)

    span_exporter = OTLPSpanExporter(endpoint=OTLP_ENDPOINT)
    span_processor = BatchSpanProcessor(span_exporter=span_exporter)
    
    provider.add_span_processor(span_processor=span_processor)
    trace.set_tracer_provider(provider)
    

def get_tracer(name: str):
    return trace.get_tracer(name)