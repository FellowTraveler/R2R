import threading
from typing import Any, Callable, Optional

from core.base import OrchestrationProvider


class HatchetOrchestrationProvider(OrchestrationProvider):
    def register_workflow(self, workflow: Any) -> None:
        if self.worker:
            self.worker.register_workflow(workflow)
        else:
            raise ValueError(
                "Worker not initialized. Call get_worker() first."
            )

    def get_worker(self, name: str, max_threads: Optional[int] = None) -> Any:
        if not max_threads:
            max_threads = self.config.max_threads
        self.worker = self.orchestrator.worker(name, max_threads)
        return self.worker

    def workflow(self, *args, **kwargs) -> Callable:
        return self.orchestrator.workflow(*args, **kwargs)

    def step(self, *args, **kwargs) -> Callable:
        return self.orchestrator.step(*args, **kwargs)

    def start_worker(self):
        if not self.worker:
            raise ValueError(
                "Worker not initialized. Call get_worker() first."
            )
        worker_thread = threading.Thread(target=self.worker.start, daemon=True)
        worker_thread.start()
