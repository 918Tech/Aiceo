
import threading
import queue
import time
import uuid
from datetime import datetime
import traceback

class BackgroundTask:
    """Represents a task that runs in the background"""
    
    def __init__(self, name, func, args=None, kwargs=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.func = func
        self.args = args or []
        self.kwargs = kwargs or {}
        self.status = "pending"
        self.result = None
        self.error = None
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        
    def execute(self):
        """Execute the task function"""
        self.status = "running"
        self.started_at = datetime.now()
        try:
            self.result = self.func(*self.args, **self.kwargs)
            self.status = "completed"
        except Exception as e:
            self.status = "failed"
            self.error = str(e)
            self.traceback = traceback.format_exc()
        finally:
            self.completed_at = datetime.now()
        
    def get_runtime(self):
        """Get the runtime of this task in seconds"""
        if not self.started_at:
            return 0
            
        end_time = self.completed_at or datetime.now()
        return (end_time - self.started_at).total_seconds()
        
    def get_info(self):
        """Get task information as a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "created_at": str(self.created_at),
            "started_at": str(self.started_at) if self.started_at else None,
            "completed_at": str(self.completed_at) if self.completed_at else None,
            "runtime": self.get_runtime(),
            "error": self.error
        }

class TaskManager:
    """Manages background tasks and worker threads"""
    
    def __init__(self, max_workers=5):
        self.task_queue = queue.Queue()
        self.max_workers = max_workers
        self.workers = []
        self.tasks = {}  # Task ID to task mapping
        self.running = False
        self.lock = threading.RLock()
        
    def start(self):
        """Start the task manager"""
        with self.lock:
            if self.running:
                return False
                
            self.running = True
            
            # Start worker threads
            for i in range(self.max_workers):
                worker = threading.Thread(
                    target=self._worker_loop,
                    name=f"TaskWorker-{i+1}",
                    daemon=True
                )
                worker.start()
                self.workers.append(worker)
                
            return True
            
    def stop(self):
        """Stop the task manager"""
        with self.lock:
            if not self.running:
                return False
                
            self.running = False
            
            # Signal all workers to stop by adding None tasks
            for _ in range(len(self.workers)):
                self.task_queue.put(None)
                
            # Wait for workers to terminate
            for worker in self.workers:
                if worker.is_alive():
                    worker.join(timeout=1.0)
                    
            # Clear remaining tasks
            self.tasks.clear()
            
            # Clear workers list
            self.workers.clear()
            
            # Empty the queue
            while not self.task_queue.empty():
                try:
                    self.task_queue.get_nowait()
                    self.task_queue.task_done()
                except queue.Empty:
                    break
                    
            return True
            
    def _worker_loop(self):
        """Worker thread function that processes tasks"""
        while self.running:
            try:
                # Get a task from the queue with a timeout
                task = self.task_queue.get(timeout=1.0)
                
                # None is a signal to exit
                if task is None:
                    self.task_queue.task_done()
                    break
                    
                # Execute the task
                task.execute()
                
                # Mark task as done
                self.task_queue.task_done()
                
            except queue.Empty:
                # Timeout occurred, check if we should still be running
                continue
            except Exception as e:
                # Log any unexpected errors
                print(f"[TaskManager] Worker error: {str(e)}")
                if task:
                    task.status = "failed"
                    task.error = f"Worker error: {str(e)}"
                    task.completed_at = datetime.now()
                    self.task_queue.task_done()
                
    def submit_task(self, name, func, *args, **kwargs):
        """
        Submit a task to be executed in the background
        
        Args:
            name: Name of the task
            func: Function to execute
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            task_id: ID of the submitted task
        """
        with self.lock:
            if not self.running:
                self.start()
                
            task = BackgroundTask(name, func, args, kwargs)
            self.tasks[task.id] = task
            self.task_queue.put(task)
            return task.id
            
    def get_task(self, task_id):
        """Get a task by ID"""
        with self.lock:
            return self.tasks.get(task_id)
            
    def get_task_info(self, task_id):
        """Get task information by ID"""
        with self.lock:
            task = self.tasks.get(task_id)
            if task:
                return task.get_info()
            return None
            
    def get_all_tasks(self):
        """Get all tasks"""
        with self.lock:
            return list(self.tasks.values())
            
    def get_status(self):
        """Get task manager status"""
        with self.lock:
            active_workers = len([w for w in self.workers if w.is_alive()])
            pending_tasks = self.task_queue.qsize()
            total_tasks = len(self.tasks)
            
            # Count tasks by status
            task_statuses = {}
            for task in self.tasks.values():
                if task.status not in task_statuses:
                    task_statuses[task.status] = 0
                task_statuses[task.status] += 1
                
            return {
                "running": self.running,
                "active_workers": active_workers,
                "max_workers": self.max_workers,
                "pending_tasks": pending_tasks,
                "total_tasks": total_tasks,
                "task_statuses": task_statuses
            }

# Create a global instance for easy access
task_manager = TaskManager()

# Start the task manager automatically
task_manager.start()
